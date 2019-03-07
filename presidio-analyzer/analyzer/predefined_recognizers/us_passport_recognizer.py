"""Recognizes a US Passport number based on regex."""
from analyzer import Pattern
from analyzer import PatternRecognizer

# Weak pattern: all passport numbers are a weak match, e.g., 14019033
VERY_WEAK_REGEX = r'(\b[0-9]{9}\b)'

CONTEXT = [
    "us", "united", "states", "passport", "number", "passport#", "travel",
    "document"
]


class UsPassportRecognizer(PatternRecognizer):
    """Recognizes a US Passport number based on regex."""

    def __init__(self):
        """Create a US Passport number recognizer."""
        patterns = [Pattern('Passport (very weak)', VERY_WEAK_REGEX, 0.05)]
        super().__init__(supported_entity="US_PASSPORT", patterns=patterns,
                         context=CONTEXT)

    def validate_result(self, text, result):
        """Validate US Passport - no validation method."""
        return result
