"""Recognizes US Bank account numbers based on regex."""
from analyzer import Pattern
from analyzer import PatternRecognizer

# Weak pattern: all passport numbers are a weak match, e.g., 14019033
REGEX = r'\b[0-9]{8,17}\b'

CONTEXT = [
    "bank"
    # Task #603: Support keyphrases: change to "checking account"
    # as part of keyphrase change
    "checking",
    "account",
    "account#",
    "acct",
    "saving",
    "debit"
]


class UsBankRecognizer(PatternRecognizer):
    """Recognizes US bank account number based on regex."""

    def __init__(self):
        """Create a US Bank account number recogniser."""
        patterns = [Pattern('Bank Account (weak)', REGEX, 0.05)]
        super().__init__(supported_entity="US_BANK_NUMBER",
                         patterns=patterns, context=CONTEXT)

    def validate_result(self, text, result):
        """Validate US Bank Account entity - no validation method."""
        return result
