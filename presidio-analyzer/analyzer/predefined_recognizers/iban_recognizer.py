"""Recognizes IBAN code using regex + checksum."""
import string
from analyzer import Pattern
from analyzer import PatternRecognizer


REGEX = u'[a-zA-Z]{2}[0-9]{2}[a-zA-Z0-9]{4}[0-9]{7}([a-zA-Z0-9]?){0,16}'
CONTEXT = ["iban"]
LETTERS = {
    ord(d): str(i)
    for i, d in enumerate(string.digits + string.ascii_uppercase)
}


class IbanRecognizer(PatternRecognizer):
    """Recognizes IBAN code using regex and checksum.

    First, a generic regex is used to identify IBAN candidates.
    Once found, a check-sum validation is ran. If the checksum is valid,
    the candidate is matched with a country-specific IBAN format.
    """

    def __init__(self):
        """Crate an IBAN code recogniser."""
        patterns = [Pattern('Iban (Medium)', REGEX, 0.5)]
        super().__init__(supported_entity="IBAN_CODE", patterns=patterns,
                         context=CONTEXT)

    def validate_result(self, text, result):
        """Validate an IBAN code using checksum."""
        is_valid_iban = IbanRecognizer.__generate_iban_check_digits(
            text) == text[2:4] and IbanRecognizer.__valid_iban(text)

        result.score = 1.0 if is_valid_iban else 0
        return result

    @staticmethod
    def __number_iban(iban):
        return (iban[4:] + iban[:4]).translate(LETTERS)

    @staticmethod
    def __generate_iban_check_digits(iban):
        number_iban = IbanRecognizer.__number_iban(iban[:2] + '00' + iban[4:])
        return '{:0>2}'.format(98 - (int(number_iban) % 97))

    @staticmethod
    def __valid_iban(iban):
        return int(IbanRecognizer.__number_iban(iban)) % 97 == 1
