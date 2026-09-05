import requests
import gradio as gr
from IPython.core import payload

API_BASE_URL = "http://127.0.0.1:8000"

TONE_OPTIONS = [
    "발랄하게"
    "과장스럽게",
    "세련되게",
    "고급스럽게",
    "일상적으로",
    "신선하게",
    "전문성있게"
]

def normalize_item(item):
    """

    서버로부터 받은 data 1개를 dict로 뜯어주는 함수

    keys:
    상품명
    주요 내용
    톤앤 매너
    광고 문구
    생성일
    """
    user_req = item.get("user_req", {})
    server_res = item.get("server_res", {})

    return [
        user_req.get("product_name", ""),
        user_req.get("details", ""),
        user_req.get("tone_and_manner", ""),
        server_res.get("ad", ""),
        str(server_res.get("created_at", "")),
    ]

def fetch_datas():
    response = requests.get(f"{API_BASE_URL}/datas", timeout=10)
    response.raise_for_status()

    result = response.json()

    datas = result.get("datas", [])

    return [normalize_item(item) for item in datas]

def create_content(product_name, details, tone_and_manners):
    if not product_name.strip():
        raise gr.Error("상품 이름을 입력하세요")

    if not details.strip():
        raise gr.Error("상품 주요 내용을 입력하세요")

    if not tone_and_manners:
        raise gr.Error("광고 문구 톤앤매너를 하나 이상 선택하세요")

    tone_and_manners = ", ".join(tone_and_manners)

    payload = {
        "product_name": product_name,
        "details": details,
        "tone_and_manner": tone_and_manners
    }

    response = requests.post(
        f"{API_BASE_URL}/content",
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    data = result.get("data", result) if isinstance(result, dict) else result

    ad = data.get("server_res", {}).get("ad", "")
    datas = fetch_datas()

    return ad, datas

with gr.Blocks(title="AI 광고 문구 생성기") as demo:
    gr.Markdown("# AI 광고 문구 생성기")

    with gr.Row():
        with gr.Column():
            product_name = gr.Textbox(
                label="상품 이름",
                placeholder="예: AirBeat Pro 무선 이어폰",
            )

            details = gr.Textbox(
                label="상품 주요 내용",
                placeholder="상품 특징, 장점, 타깃 고객 등을 입력하세요.",
                lines=6,
            )

            tone_and_manners = gr.CheckboxGroup(
                label="광고 문구 톤앤매너",
                choices=TONE_OPTIONS,
                value=["일상적으로"],
            )

            create_button = gr.Button("광고 문구 생성", variant="primary")
        with gr.Column():
            ad_output = gr.Textbox(
                label="생성된 광고 문구",
                lines=10,
            )
    gr.Markdown("## 최근 광고 문구 목록")
    datas_output = gr.Dataframe(
        headers=["상품명", "주요 내용", "톤앤매너", "광고 문구", "생성일"],
        datatype=["str", "str", "str", "str", "str"],
        interactive=False,
        wrap=True,
    )
    refresh_button = gr.Button("목록 새로고침")
    create_button.click(
        fn=create_content,
        inputs=[product_name, details, tone_and_manners],
        outputs=[ad_output, datas_output],
    )

    refresh_button.click(
        fn=fetch_datas,
        inputs=[],
        outputs=[datas_output],
    )

    demo.load(
        fn=fetch_datas,
        inputs=[],
        outputs=[datas_output],
    )


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)