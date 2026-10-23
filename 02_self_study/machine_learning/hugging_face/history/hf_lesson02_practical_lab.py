"""Hugging Face 2강 보충 실습: 정규화, safetensors, Hub 리비전, 모델 구조 확인.

기본 실행은 네트워크와 모델 가중치 다운로드가 필요하지 않습니다.
옵션:
    --hub    Hub 메타데이터/설정/Tokenizer를 조회합니다 (네트워크 필요).
    --model  모델 가중치를 로딩해 모듈, 파라미터, 출력 Shape를 확인합니다 (시간/메모리 필요).
"""
from __future__ import annotations

import argparse
import inspect
import json
import tempfile
from pathlib import Path

import torch
from safetensors import safe_open
from safetensors.torch import save_file

MODEL_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"


def norm_lab() -> None:
    print("\n=== 1. LayerNorm vs RMSNorm ===")
    x = torch.tensor([[[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]])
    ln = torch.nn.LayerNorm(3, elementwise_affine=False)
    rms = torch.nn.RMSNorm(3, elementwise_affine=False)
    print("input shape", tuple(x.shape))
    print("LayerNorm", ln(x).tolist())
    print("RMSNorm  ", rms(x).tolist())
    print("mean(-1, keepdim=True).shape", tuple(x.mean(-1, keepdim=True).shape))
    assert ln(x).shape == rms(x).shape == x.shape
    assert torch.allclose(ln(x).mean(dim=-1), torch.zeros(1, 2), atol=1e-5)


def safe_tensor_lab() -> None:
    print("\n=== 2. safetensors: 테스트용 가중치 저장/조회 ===")
    state = {
        "linear.weight": torch.arange(12, dtype=torch.float32).reshape(3, 4),
        "linear.bias": torch.zeros(3),
    }
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "toy.safetensors"
        save_file(state, str(path))
        with safe_open(str(path), framework="pt", device="cpu") as f:
            keys = list(f.keys())
            print("keys:", keys)
            for key in keys:
                value = f.get_tensor(key)
                print(key, "shape:", tuple(value.shape), "dtype:", value.dtype)
                assert torch.equal(value, state[key])
        print("round-trip: OK")


def hub_lab(with_model: bool) -> None:
    from huggingface_hub import HfApi, hf_hub_download
    from transformers import AutoConfig, AutoTokenizer

    print("\n=== 3. Hub: 저장소, revision, 파일 조회 ===")
    api = HfApi()

    info = api.model_info(repo_id=MODEL_ID, revision="main")
    revision = info.sha
    if not revision:
        raise RuntimeError("Hub metadata에서 commit SHA를 가져오지 못했습니다.")
    files = api.list_repo_files(repo_id=MODEL_ID, revision=revision)

    print("repo_id:", info.id)
    print("revision SHA:", revision)
    print("files (first 20):", files[:20])

    path = hf_hub_download(MODEL_ID, "config.json", revision=revision)

    config_dict = json.loads(Path(path).read_text(encoding="utf-8"))
    print("config file path:", path)
    print("raw config type:", type(config_dict).__name__)

    config = AutoConfig.from_pretrained(MODEL_ID, revision=revision)
    print("Config class:", type(config).__name__)
    print("architecture:", config.architectures)
    print("model_type:", config.model_type)
    print("hidden_size:", getattr(config, "hidden_size", "n/a"))
    print("vocab_size:", getattr(config, "vocab_size", "n/a"))

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=revision)
    encoded = tokenizer("Hello world", return_tensors="pt")
    print("Tokenizer class:", type(tokenizer).__name__)
    print("BatchEncoding type:", type(encoded).__name__)
    print("input_ids:", tuple(encoded["input_ids"].shape))

    manifest = {
        "repo_id": MODEL_ID,
        "revision": revision,
        "model_type": config.model_type,
        "torch_version": torch.__version__,
    }
    try:
        import transformers
        import huggingface_hub
        manifest["transformers_version"] = transformers.__version__
        manifest["huggingface_hub_version"] = huggingface_hub.__version__
    except Exception:
        pass
    Path("hf_lab_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("saved: hf_lab_manifest.json")

    if with_model:
        model_lab(revision, tokenizer)


def model_lab(revision: str, tokenizer: object) -> None:
    from transformers import AutoModelForCausalLM

    print("\n=== 4. Model: 실제 클래스, Module, Parameter, Logits ===")
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=revision)
    model.eval()
    print("model class:", type(model).__name__)
    print("MRO:", [cls.__name__ for cls in type(model).__mro__[:5]])
    print("forward signature:", inspect.signature(model.forward))
    print("first modules:")
    for name, module in list(model.named_modules())[:15]:
        print(" ", name or "<root>", type(module).__name__)
    print("first parameters:")
    for name, param in list(model.named_parameters())[:12]:
        print(" ", name, tuple(param.shape), param.dtype)
    if hasattr(model, "model") and hasattr(model.model, "layers"):
        attn = model.model.layers[0].self_attn
        for name in ("q_proj", "k_proj", "v_proj"):
            layer = getattr(attn, name)
            print(name, "weight:", tuple(layer.weight.shape))

    inputs = tokenizer("Hello world", return_tensors="pt")
    with torch.inference_mode():
        output = model(**inputs, use_cache=False, return_dict=True)
    print("logits shape:", tuple(output.logits.shape))
    predicted_id = output.logits[:, -1, :].argmax(dim=-1)
    print("next token IDs:", predicted_id.tolist())
    print("decoded:", tokenizer.batch_decode(predicted_id))
    assert output.logits.shape[:2] == inputs["input_ids"].shape
    assert output.logits.shape[-1] == model.config.vocab_size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub", action="store_true", help="Hub metadata/config/tokenizer 실습")
    parser.add_argument("--model", action="store_true", help="모델 가중치까지 로딩 (--hub 자동 포함)")
    args = parser.parse_args()

    norm_lab()
    safe_tensor_lab()
    if args.hub or args.model:
        hub_lab(with_model=args.model)
    else:
        print("\nHub 실습은 --hub, 모델 구조 실습은 --model 옵션으로 실행하세요.")


if __name__ == "__main__":
    main()
