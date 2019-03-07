# TODO: Bug 702: RecognizerResult should be a dataclass (python 3.7.2)


class RecognizerResult:  # noqa E501 pylint: disable=too-few-public-methods

    def __init__(self, entity_type, start, end, score):
        """
        Recognizer Result represents the findings of the detected entity
        of the analyzer in the text.
        :param entity_type: the type of the entity
        :param start: the start location of the detected entity
        :param end: the end location of the detected entity
        :param score: the score of the detection
        """
        self.entity_type = entity_type
        self.start = start
        self.end = end
        self.score = score
