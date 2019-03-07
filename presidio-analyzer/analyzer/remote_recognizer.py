from analyzer import EntityRecognizer


# User Sroty: #498: Adding a new external recognizer
# Once implemented, remove the pylint disable comment regarding unused **kwargs
class RemoteRecognizer(EntityRecognizer):
    """
    A configuration for a recognizer that runs on a different process
     / remote machine
    """

    def __init__(self, supported_entities, supported_language, name, version,
                 **kwargs):  # pylint: disable=unused-argument
        super().__init__(supported_entities, supported_language, name, version)

    def load(self):
        pass

    def analyze(self, text, entities):
        return None

    def analyze_text(self, text, entities):
        # add code here to connect to the side car
        pass

    def get_supported_entities(self):
        pass
