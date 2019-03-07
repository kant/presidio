from analyzer import EntityRecognizer


class LocalRecognizer(EntityRecognizer):

    def __init__(self, supported_entities, supported_language, name=None,
                 version=None):
        super().__init__(supported_entities=supported_entities,
                         supported_language=supported_language, name=name,
                         version=version)

    def load(self):
        pass

    def analyze(self, text, entities):
        return None
