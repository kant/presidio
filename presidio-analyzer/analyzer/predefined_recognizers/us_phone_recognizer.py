"""Recognizes US Phone number basd on regex."""
from analyzer import Pattern
from analyzer import PatternRecognizer

STRONG_REGEX = r'(\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|d{3}[-\.\s]\d{3}[-\.\s]\d{4})'  # noqa: E501 pylint: disable=line-too-long
MEDIUM_REGEX = r'\b(\d{3}[-\.\s]\d{3}[-\.\s]??\d{4})\b'
WEAK_REGEX = r'(\b\d{10}\b)'

CONTEXT = ["phone", "number", "telephone", "cell", "mobile", "call"]


class UsPhoneRecognizer(PatternRecognizer):
    """Recognizes US Phone number based on regex."""

    def __init__(self):
        """Create a Phone Number recogniser."""
        patterns = [Pattern('Phone (strong)', STRONG_REGEX, 0.7),
                    Pattern('Phone (medium)', MEDIUM_REGEX, 0.5),
                    Pattern('Phone (weak)', WEAK_REGEX, 0.05)]
        super().__init__(supported_entity="PHONE_NUMBER",
                         patterns=patterns, context=CONTEXT)

    def validate_result(self, text, result):
        """Validate US Phone number - no validation method."""
        return result
