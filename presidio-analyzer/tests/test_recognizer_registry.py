from unittest import TestCase

import pytest

from analyzer import RecognizerRegistry, PatternRecognizer, \
    EntityRecognizer, Pattern


class TestRecognizerRegistry(TestCase):

    def get_mock_pattern_recognizer(self, lang, entity, name):
        return PatternRecognizer(supported_entity=entity,
                                 supported_language=lang, name=name,
                                 patterns=[
                                     Pattern("pat", pattern="REGEX",
                                             strength=1.0)
                                 ])

    def get_mock_custom_recognizer(self, lang, entities, name):
        return EntityRecognizer(supported_entities=entities, name=name,
                                supported_language=lang)

    def get_mock_recognizer_registry(self):
        recognizer1 = self.get_mock_pattern_recognizer("en", "PERSON", "1")
        recognizer2 = self.get_mock_pattern_recognizer("de", "PERSON", "2")
        recognizer3 = self.get_mock_pattern_recognizer("de", "ADDRESS", "3")
        recognizer4 = self.get_mock_pattern_recognizer("he", "ADDRESS", "4")
        recognizer5 = self.get_mock_custom_recognizer(
            "he", ["PERSON", "ADDRESS"], "5")
        return RecognizerRegistry([recognizer1, recognizer2,
                                   recognizer3, recognizer4,
                                   recognizer5])

    def test_get_recognizers_all(self):
        registry = self.get_mock_recognizer_registry()
        recognizers = registry.get_recognizers()
        assert len(recognizers) == 5

    def test_get_recognizers_one_language_one_entity(self):
        registry = self.get_mock_recognizer_registry()
        recognizers = registry.get_recognizers(language='de',
                                               entities=["PERSON"])
        assert len(recognizers) == 1

    def test_get_recognizers_unsupported_language(self):
        with pytest.raises(ValueError):
            registry = self.get_mock_recognizer_registry()
            registry.get_recognizers(language='brrrr', entities=["PERSON"])

    def test_get_recognizers_specific_language_and_entity(self):
        registry = self.get_mock_recognizer_registry()
        recognizers = registry.get_recognizers(language='he',
                                               entities=["PERSON"])
        assert len(recognizers) == 1

    def test_load_pattern_recognizer_from_dict(self):
        recognizer = self.get_mock_pattern_recognizer("ar", "ENTITY", "a")
        recognizer.name = "123"
        registry = self.get_mock_recognizer_registry()
        registry.add_pattern_recognizer_from_dict(recognizer.to_dict())

        recognizers = registry.get_recognizers(entities=["ENTITY"],
                                               language="ar")

        assert recognizers[0].to_dict() == recognizer.to_dict()

    def test_load_pattern_recognizer_from_defined_dict_throws_exception(self):
        recognizer1 = self.get_mock_pattern_recognizer("ar", "ENTITY", "a")
        recognizer1.name = "MyRecognizer"
        registry = self.get_mock_recognizer_registry()
        registry.add_pattern_recognizer_from_dict(recognizer1.to_dict())

        recognizer2 = self.get_mock_pattern_recognizer("em", "ENTITY3", "a")
        recognizer2.name = "MyRecognizer"
        with pytest.raises(ValueError):
            registry.add_pattern_recognizer_from_dict(recognizer2.to_dict())

    def test_remove_pattern_recognizer_not_found_exception(self):
        recognizer1 = self.get_mock_pattern_recognizer("ar", "ENTITY", "a")
        recognizer1.name = "MyRecognizer"
        registry = self.get_mock_recognizer_registry()
        registry.add_pattern_recognizer_from_dict(recognizer1.to_dict())

        with pytest.raises(ValueError):
            registry.remove_recognizer("NumeroUnoRecognizer")

    def test_remove_pattern_recognizer_removed(self):
        recognizer1 = self.get_mock_pattern_recognizer(
            "ar", "ENTITY", "MyRecognizer")
        registry = self.get_mock_recognizer_registry()
        registry.add_pattern_recognizer_from_dict(recognizer1.to_dict())

        assert len(registry.recognizers) == 6

        registry.remove_recognizer("MyRecognizer")

        assert len(registry.recognizers) == 5

        for recognizer in registry.recognizers:
            if recognizer.name == "MyRecognizer":
                assert False

        assert True
