import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_pr_review import load_config, load_prompts, get_pr_number, validate_model, ai_request

class TestAIPRReview(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"test": "data"}')
    def test_load_config(self, mock_open):
        config = load_config()
        self.assertEqual(config, {"test": "data"})

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"system_role": "test role"}')
    def test_load_prompts(self, mock_open):
        prompts = load_prompts()
        self.assertEqual(prompts["system_role"], "test role")

    @patch.dict(os.environ, {"GITHUB_EVENT_PULL_REQUEST_NUMBER": "123"})
    def test_get_pr_number_from_env(self):
        pr_number = get_pr_number()
        self.assertEqual(pr_number, 123)

    @patch.dict(os.environ, {"GITHUB_REF": "refs/pull/456/merge"})
    def test_get_pr_number_from_ref(self):
        pr_number = get_pr_number()
        self.assertEqual(pr_number, 456)

    def test_validate_model_known(self):
        model = validate_model("gpt-4-turbo")
        self.assertEqual(model, "gpt-4-turbo")

    def test_validate_model_unknown(self):
        with self.assertLogs(level='WARNING') as cm:
            model = validate_model("unknown-model")
        self.assertEqual(model, "unknown-model")
        self.assertIn("WARNING:root:Model 'unknown-model' is not in the list of known models. Using anyway.", cm.output)

    @patch('openai.OpenAI')
    def test_ai_request(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Test response"

        response = ai_request("Test prompt", "gpt-4-turbo")
        self.assertEqual(response, "Test response")

if __name__ == '__main__':
    unittest.main()
