import unittest
from dualai.utils.text_cleaner import TextCleaner

class TestVerbatimFidelity(unittest.TestCase):
    def test_markdown_preservation(self):
        sample = """# Heading
Here is a table:
| A | B |
|---|---|
| 1 | 2 |

```python
def hello():
    return "world"
```
"""
        cleaned = TextCleaner.clean_chatgpt_response(sample)
        self.assertIn("```python", cleaned)
        self.assertIn("| A | B |", cleaned)
        self.assertTrue(TextCleaner.verify_integrity(sample, cleaned))

    def test_artifact_removal(self):
        sample = "Here is the plan. ChatGPT can make mistakes. Check important info. Copy code"
        cleaned = TextCleaner.clean_chatgpt_response(sample)
        self.assertNotIn("Copy code", cleaned)
        self.assertNotIn("ChatGPT can make mistakes", cleaned)
        self.assertIn("Here is the plan", cleaned)

if __name__ == "__main__":
    unittest.main()
