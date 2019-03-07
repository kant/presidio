"""Recognizes common credit card numbers using regex and checksum."""

from analyzer import Pattern
from analyzer import PatternRecognizer

REGEX = r'\b((4\d{3})|(5[0-5]\d{2})|(6\d{3})|(1\d{3})|(3\d{3}))[- ]?(\d{3,4})[- ]?(\d{3,4})[- ]?(\d{3,5})\b'  # noqa: E501 pylint: disable=line-too-long
CONTEXT = [
    "credit",
    "card",
    "visa",
    "mastercard",
    "cc ",
    # "american express" #Task #603: Support keyphrases
    "amex",
    "discover",
    "jcb",
    "diners",
    "maestro",
    "instapayment"
]


class CreditCardRecognizer(PatternRecognizer):
    """Recognizes common credit card numbers using regex + checksum."""

    def __init__(self):
        """Create a credit card recognizer."""
        patterns = [Pattern('All Credit Cards (weak)', REGEX, 0.3)]
        super().__init__(supported_entity="CREDIT_CARD", patterns=patterns,
                         context=CONTEXT)

    def validate_result(self, text, result):
        """Validate a credit card regex match by calculating checksum."""
        sanitized_text = CreditCardRecognizer.__sanitize_text(text)
        res = CreditCardRecognizer.__luhn_checksum(sanitized_text)
        if res == 0:
            result.score = 1
        else:
            result.score = 0

        return result

    @staticmethod
    def __luhn_checksum(text):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(text)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    @staticmethod
    def __sanitize_text(text):
        return text.replace('-', '').replace(' ', '')
