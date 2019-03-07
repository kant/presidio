"""Recognizes email address using regex + validation."""
import tldextract
from analyzer import Pattern
from analyzer import PatternRecognizer


REGEX = r"\b((([!#$%&'*+\-/=?^_`{|}~\w])|([!#$%&'*+\-/=?^_`{|}~\w][!#$%&'*+\-/=?^_`{|}~\.\w]{0,}[!#$%&'*+\-/=?^_`{|}~\w]))[@]\w+([-.]\w+)*\.\w+([-.]\w+)*)\b"  # noqa: E501 pylint: disable=line-too-long
CONTEXT = ["email"]


class EmailRecognizer(PatternRecognizer):
    """Recognize email addresses using regex + validation."""

    def __init__(self):
        """Create an email recogniser."""
        patterns = [Pattern('Email (Medium)', REGEX, 0.5)]
        super().__init__(supported_entity="EMAIL_ADDRESS",
                         patterns=patterns, context=CONTEXT)

    def validate_result(self, text, result):
        """Validate email addresses using rtldextract."""
        result = tldextract.extract(text)

        result.score = 1.0 if result.fqdn != '' else 0
        return result
