"""Recognizes domain names using regex + validation."""
import tldextract
from analyzer import Pattern
from analyzer import PatternRecognizer

REGEX = r'\b(((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,86}[a-zA-Z0-9]))\.(([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,73}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25})))|((([a-zA-Z0-9])|([a-zA-Z0-9][a-zA-Z0-9\-]{0,162}[a-zA-Z0-9]))\.(([a-zA-Z0-9]{2,12}\.[a-zA-Z0-9]{2,12})|([a-zA-Z0-9]{2,25}))))\b'  # noqa: E501'  # noqa: E501 pylint: disable=line-too-long
CONTEXT = ["domain", "ip"]


class DomainRecognizer(PatternRecognizer):
    """Recognizes domain names using regex and validation."""

    def __init__(self):
        """Create a domain recognizer."""
        patterns = [Pattern('Domain ()', REGEX, 0.5)]
        super().__init__(supported_entity="DOMAIN_NAME", patterns=patterns,
                         context=CONTEXT)

    def validate_result(self, text, result):
        """Validate a domain name."""
        result = tldextract.extract(text)
        result.score = 1.0 if result.fqdn != '' else 0
        return result
