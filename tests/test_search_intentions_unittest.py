import unittest

import openai
import pandas as pd

import config
from search_intent_to_csv import categorize_keywords

openai.api_key = config.API_KEY


class TestCategorizeKeywords(unittest.TestCase):

    # Function returns three lists of equal length
    def test_returned_lists_length(self):
        # Arrange
        # Create a sample DataFrame with keywords
        df = pd.DataFrame({'keywords': ['keyword1', 'keyword2', 'keyword3']})

        # Mock the OpenAI API response
        class MockCompletion:
            def __init__(self, text):
                self.text = text

        class MockChoices:
            def __init__(self, choices):
                self.choices = choices

        mock_response = MockChoices(
            [
                MockCompletion('keyword1 | Conversational | Discovery'),
                MockCompletion('keyword2 | Query | Consideration'),
                MockCompletion('keyword3 | Generational | Conversion'),
            ]
        )

    # Mock the OpenAI API call
    def mock_completion_create(model, prompt, max_tokens, temperature):
        return mock_response

        openai.Completion.create = mock_completion_create

        # Act
        keywords, intencion, etapa = categorize_keywords()

        # Assert
        self.assertEqual(len(keywords), len(intencion))
        self.assertEqual(len(keywords), len(etapa))

    # Function returns three lists of equal length
    def test_return_lists_length(self):
        # Arrange
        # Create a sample input file with multiple keywords
        df = pd.DataFrame({'keywords': ['keyword1', 'keyword2', 'keyword3']})
        df.to_csv('docs/keywords.csv', index=False)

        # Act
        keywords, intencion, etapa = categorize_keywords()

        # Assert
        self.assertEqual(len(keywords), len(intencion))
        self.assertEqual(len(keywords), len(etapa))

    # Function handles an empty input file
    def test_empty_input_file(self):
        # Arrange
        # Create an empty input file
        df = pd.DataFrame({'keywords': []})
        df.to_csv('docs/keywords.csv', index=False)

        # Act
        keywords, intencion, etapa = categorize_keywords()

        # Assert
        self.assertEqual(len(keywords), 0)
        self.assertEqual(len(intencion), 0)
        self.assertEqual(len(etapa), 0)
