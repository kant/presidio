"""Recognizes US SSN (Social Security Number) number based on regex."""
from analyzer import Pattern
from analyzer import PatternRecognizer

VERY_WEAK_REGEX = r'\b(([0-9]{5})-([0-9]{4})|([0-9]{3})-([0-9]{6}))\b'
WEAK_REGEX = r'\b[0-9]{9}\b'
MEDIUM_REGEX = r'\b([0-9]{3})-([0-9]{2})-([0-9]{4})\b'

CONTEXT = [
    "social",
    "security",
    # "sec", # Task #603: Support keyphrases ("social sec")
    "ssn",
    "ssns",
    "ssn#",
    "ss#",
    "ssid"
]


class UsSsnRecognizer(PatternRecognizer):
    """Recognizes US SSN (Social Security Number) number based on regex."""

    def __init__(self):
        """Create a US SSN recogniser."""
        patterns = [Pattern('SSN (very weak)', VERY_WEAK_REGEX, 0.05),
                    Pattern('SSN (weak)', WEAK_REGEX, 0.3),
                    Pattern('SSN (medium)', MEDIUM_REGEX, 0.5)]
        super().__init__(supported_entity="US_SSN", patterns=patterns,
                         context=CONTEXT)

    def validate_result(self, text, result):
        """Validate US SSN - no validation method."""
        return result
