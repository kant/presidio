
from analyzer.pattern import Pattern
from analyzer.pattern_recognizer import PatternRecognizer
CONTEXT = []


class CustomRecognizer(PatternRecognizer):
    """
    """

    def __init__(self, name, regex, score, entity):
        patterns = [Pattern(name, regex, score)]
        super().__init__(supported_entity=entity, patterns=patterns,
                         context=CONTEXT)
