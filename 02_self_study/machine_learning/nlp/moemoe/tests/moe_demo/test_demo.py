"""Check routing, sparse execution and weighted combination."""

import unittest
from unittest.mock import patch

import demo


class MoEDemoTests(unittest.TestCase):
    def test_different_tokens_select_different_experts(self):
        cases = (((2.0, 0.0), 0, (4.0, 0.0)),
                 ((0.0, 2.0), 1, (0.0, 4.0)),
                 ((-2.0, -2.0), 2, (2.0, 2.0)))
        for token, expected_id, expected_output in cases:
            with self.subTest(token=token):
                output, probabilities, contributions = demo.moe_forward(token)
                self.assertEqual(contributions[0][0], expected_id)
                self.assertEqual(output, expected_output)
                self.assertAlmostEqual(sum(probabilities), 1.0)

    def test_only_selected_experts_execute(self):
        for top_k in (1, 2, 3):
            with self.subTest(top_k=top_k):
                with patch.object(demo, "expert_forward", wraps=demo.expert_forward) as expert:
                    demo.moe_forward((2.0, 0.0), top_k)
                    self.assertEqual(expert.call_count, top_k)

    def test_top_two_blends_outputs_with_normalized_weights(self):
        output, _, contributions = demo.moe_forward((1.0, 1.0), top_k=2)
        self.assertEqual([item[0] for item in contributions], [0, 1])
        self.assertEqual([item[1] for item in contributions], [0.5, 0.5])
        self.assertEqual(output, (1.5, 1.5))

    def test_bad_inputs_are_rejected(self):
        for top_k in (0, 4):
            with self.assertRaises(ValueError):
                demo.moe_forward((1.0, 1.0), top_k)
        for token in ((float("nan"), 1.0), (float("inf"), 1.0), (1.0,)):
            with self.assertRaises(ValueError):
                demo.moe_forward(token)


if __name__ == "__main__":
    unittest.main()
