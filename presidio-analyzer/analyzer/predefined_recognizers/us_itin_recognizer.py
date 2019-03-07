"""Recognizes US ITIN (Individual Taxpayer Identification Number)."""
from analyzer import Pattern
from analyzer import PatternRecognizer

VERY_WEAK_REGEX = r'(\b(9\d{2})[- ]{1}((7[0-9]{1}|8[0-8]{1})|(9[0-2]{1})|(9[4-9]{1}))(\d{4})\b)|(\b(9\d{2})((7[0-9]{1}|8[0-8]{1})|(9[0-2]{1})|(9[4-9]{1}))[- ]{1}(\d{4})\b)'  # noqa: E501 pylint: disable=line-too-long
WEAK_REGEX = r'\b(9\d{2})((7[0-9]{1}|8[0-8]{1})|(9[0-2]{1})|(9[4-9]{1}))(\d{4})\b'  # noqa: E501 pylint: disable=line-too-long
MEDIUM_REGEX = r'\b(9\d{2})[- ]{1}((7[0-9]{1}|8[0-8]{1})|(9[0-2]{1})|(9[4-9]{1}))[- ]{1}(\d{4})\b'  # noqa: E501 pylint:disable=line-too-long

CONTEXT = [
    "individual",
    "taxpayer",
    "itin",
    "tax",
    "payer",
    "taxid",
    "tin"
]


class UsItinRecognizer(PatternRecognizer):
    """
    Recognizes US ITIN based on regex.

    ITIN stands for Individual Taxpayer Identification Number.
    """

    def __init__(self):
        """Create an ITIN recogniser."""
        patterns = [Pattern('US ITIN (very weak)', VERY_WEAK_REGEX, 0.05),
                    Pattern('US ITIN (weak)', WEAK_REGEX, 0.3),
                    Pattern('US ITIN (medium)', MEDIUM_REGEX, 0.5)]
        super().__init__(supported_entity="US_ITIN", patterns=patterns,
                         context=CONTEXT)

    def validate_result(self, text, result):
        """Validate US ITIN - nothing to validate."""
        return result
