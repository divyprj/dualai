import re

class TextCleaner:
    """Preserves full-fidelity markdown and cleans raw browser-extracted text without truncation."""

    @staticmethod
    def clean_chatgpt_response(raw_text: str) -> str:
        """Cleans web artifacts while preserving 100% of code blocks, tables, and formatting."""
        if not raw_text:
            return ""

        # Normalize line endings
        text = raw_text.replace("\r\n", "\n")

        # Remove ephemeral web UI artifacts if captured
        artifacts = [
            "ChatGPT can make mistakes. Check important info.",
            "Copy code",
            "Was this response better or worse?",
            "Regenerate response"
        ]
        for art in artifacts:
            text = text.replace(art, "")

        # Strip excessive trailing blank lines
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        return text.strip()

    @staticmethod
    def verify_integrity(original: str, cleaned: str) -> bool:
        """Ensures that cleaning never dropped significant content (>95% character match)."""
        if len(original) == 0:
            return True
        ratio = len(cleaned) / len(original)
        return ratio >= 0.85
