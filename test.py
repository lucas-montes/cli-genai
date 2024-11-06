from unittest.mock import MagicMock, patch
import unittest

from app import _questions_loop


class ModelMock:
    def __init__(self) -> None:
        self.questions = []

    def ask_question(self, question: str) -> str:
        self.questions.append(question)
        return "response"


class TestCli(unittest.TestCase):
    @patch("app._get_question")
    @patch("app._send_response")
    def test_question_loop(
        self,
        mock_send_response: MagicMock,
        mock_get_question: MagicMock,
    ):
        mock_get_question.side_effect = "first question", "stop", "second"
        expected_questions = ("first question",)
        model = ModelMock()
        result = _questions_loop(model)
        assert result == "stopped by user"
        assert mock_get_question.call_count == 2
        mock_send_response.assert_called_once_with("response")
        assert all(q == e for q, e in zip(model.questions, expected_questions))
