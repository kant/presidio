"""Recognizes common crypto account numbers using regex + checksum."""
from hashlib import sha256
from analyzer import Pattern
from analyzer import PatternRecognizer

"""Copied from:
  http://rosettacode.org/wiki/Bitcoin/address_validation#Python
  """
REGEX = r'\b[13][a-km-zA-HJ-NP-Z0-9]{26,33}\b'
CONTEXT = ["wallet", "btc", "bitcoin", "crypto"]


class CryptoRecognizer(PatternRecognizer):
    """Recognizes common crypto account numbers using regex + checksum."""

    def __init__(self):
        """Create a crypto account recognizer."""
        patterns = [Pattern('Crypto (Medium)', REGEX, 0.5)]
        super().__init__(supported_entity="CRYPTO", patterns=patterns,
                         context=CONTEXT)

    def validate_result(self, text, result):
        """Validate a crypto account by calculating checksum (hash)."""
        # try:
        bcbytes = CryptoRecognizer.__decode_base58(text, 25)
        if bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]:
            result.score = 1.0
        return result

    @staticmethod
    def __decode_base58(bc, length):
        digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        n = 0
        for char in bc:
            n = n * 58 + digits58.index(char)
        return n.to_bytes(length, 'big')
