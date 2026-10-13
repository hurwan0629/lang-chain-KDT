"""다운로드 없이 CPU에서 모델의 마스크와 역전파를 확인합니다."""

import unittest

import torch
from torch import nn

from train import TinyTransformerClassifier


class TransformerTests(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(42)
        # 실제 토크나이저 대신 작은 가상 어휘로 모델 자체를 검사합니다.
        self.model = TinyTransformerClassifier(vocab_size=20, pad_token_id=0)
        self.input_ids = torch.tensor([[1, 2, 3, 0], [1, 4, 0, 0]])
        self.mask = self.input_ids.ne(0).long()

    def test_output_shape_and_finite_values(self):
        logits = self.model(self.input_ids, self.mask)
        self.assertEqual(tuple(logits.shape), (2, 2))
        self.assertTrue(torch.isfinite(logits).all().item())

    def test_masked_tokens_do_not_change_prediction(self):
        self.model.eval()
        modified = self.input_ids.clone()
        modified[self.mask == 0] = 9
        # 무시할 위치의 ID를 바꿔도 Attention과 평균의 마스크 덕분에 결과가 같습니다.
        with torch.no_grad():
            original = self.model(self.input_ids, self.mask)
            changed = self.model(modified, self.mask)
        torch.testing.assert_close(original, changed, atol=1e-6, rtol=1e-6)

    def test_backward_updates_weights(self):
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=0.003)
        before = self.model.classifier.weight.detach().clone()
        optimizer.zero_grad()
        logits = self.model(self.input_ids, self.mask)
        loss = nn.CrossEntropyLoss()(logits, torch.tensor([1, 0]))
        loss.backward()
        self.assertIsNotNone(self.model.token_embedding.weight.grad)
        self.assertTrue(torch.isfinite(self.model.token_embedding.weight.grad).all().item())
        optimizer.step()
        self.assertFalse(torch.equal(before, self.model.classifier.weight.detach()))


if __name__ == "__main__":
    unittest.main()
