from unittest import TestCase

import pytest
import time
import logging

from analyzer import recognizers_store_pb2

from assertions import assert_result
from analyzer import AnalyzerEngine, PatternRecognizer, Pattern, \
    RecognizerResult, RecognizerRegistry
from analyzer.analyze_pb2 import AnalyzeRequest
from analyzer.predefined_recognizers import CreditCardRecognizer, \
    UsPhoneRecognizer, CustomRecognizer
from analyzer.recognizer_registry.recognizers_store_api \
    import RecognizerStoreApi  # noqa: F401


class RecognizerStoreApiMock(RecognizerStoreApi):
    def __init__(self):
        self.latest_timestamp = 0
        self.recognizers = []

    def get_latest_timestamp(self):
        return self.latest_timestamp

    def get_all_recognizers(self):
        return self.recognizers

    def add_custom_pattern_recognizer(self, new_recognizer, skip_timestamp_update=False):
        pb_recognizer = recognizers_store_pb2.PatternRecognizer()
        pb_recognizer.name = new_recognizer["name"]
        pb_recognizer.score = new_recognizer["score"]
        pb_recognizer.entity = new_recognizer["entity"]
        pb_recognizer.pattern = new_recognizer["pattern"]
        pb_recognizer.language = new_recognizer["language"]
        self.recognizers.append(pb_recognizer)

        if skip_timestamp_update:
            return

        # making sure there is a time difference (when the test run so fast two
        # sequential operations are with the same timestamp
        time.sleep(1)
        self.latest_timestamp = int(time.time())

    def remove_recognizer(self, name):
        logging.info("removing recognizer")
        for i in self.recognizers:
            if i.name == name:
                self.recognizers.remove(i)
        # making sure there is a time difference (when the test run so fast two
        # sequential operations are with the same timestamp
        time.sleep(1)
        self.latest_timestamp = int(time.time())


class MockRecognizerRegistry(RecognizerRegistry):
    def load_recognizers(self, path):
            #   TODO: Change the code to dynamic loading -
            # Task #598:  Support loading of the pre-defined recognizers
            # from the given path.
        self.recognizers.extend([CreditCardRecognizer(),
                                 UsPhoneRecognizer()])


class TestAnalyzerEngine(TestCase):

    def test_analyze_with_predefined_recognizers_return_results(self):
        recognizers_store_api_mock = RecognizerStoreApiMock()
        analyze_engine = AnalyzerEngine(
            MockRecognizerRegistry(recognizers_store_api_mock))
        text = " Credit card: 4095-2609-9393-4932,  my phone is 425 8829090"
        langauge = "en"
        entities = ["CREDIT_CARD"]
        results = analyze_engine.analyze(text, entities, langauge)

        assert len(results) == 1
        assert_result(results[0], "CREDIT_CARD", 14, 33, 1.0)

    def test_analyze_with_multiple_predefined_recognizers(self):
        analyze_engine = AnalyzerEngine(MockRecognizerRegistry())
        text = " Credit card: 4095-2609-9393-4932,  my phone is 425 8829090"
        langauge = "en"
        entities = ["CREDIT_CARD", "PHONE_NUMBER"]
        results = analyze_engine.analyze(text, entities, langauge)

        assert len(results) == 2
        assert_result(results[0], "CREDIT_CARD", 14, 33, 1.0)
        assert_result(results[1], "PHONE_NUMBER", 48, 59, 0.5)

    def test_analyze_without_entities(self):
        with pytest.raises(ValueError):
            langauge = "en"
            recognizers_store_api_mock = RecognizerStoreApiMock()
            analyze_engine = AnalyzerEngine(
                MockRecognizerRegistry(recognizers_store_api_mock))
            text = " Credit card: 4095-2609-9393-4932,  my name is  John Oliver, DateTime: September 18 " \
                   "Domain: microsoft.com"
            entities = []
            analyze_engine.analyze(text, entities, langauge)

    def test_analyze_with_empty_text(self):
        recognizers_store_api_mock = RecognizerStoreApiMock()
        analyze_engine = AnalyzerEngine(
            MockRecognizerRegistry(recognizers_store_api_mock))
        langauge = "en"
        text = ""
        entities = ["CREDIT_CARD", "PHONE_NUMBER"]
        results = analyze_engine.analyze(text, entities, langauge)
        assert len(results) == 0

    def test_analyze_with_unsupported_language(self):
        with pytest.raises(ValueError):
            langauge = "de"
            recognizers_store_api_mock = RecognizerStoreApiMock()
            analyze_engine = AnalyzerEngine(
                MockRecognizerRegistry(recognizers_store_api_mock))
            text = ""
            entities = ["CREDIT_CARD", "PHONE_NUMBER"]
            analyze_engine.analyze(text, entities, "de")

    def test_remove_duplicates(self):
        # test same result with different score will return only the highest
        arr = [RecognizerResult(start=0, end=5, score=0.1, entity_type="x"),
               RecognizerResult(start=0, end=5, score=0.5, entity_type="x")]
        results = AnalyzerEngine._AnalyzerEngine__remove_duplicates(arr)
        assert len(results) == 1
        assert results[0].score == 0.5
        # TODO: add more cases with bug:
        # bug# 597: Analyzer remove duplicates doesn't handle all cases of one result as a substring of the other

    def test_add_pattern_recognizer_from_dict(self):
        pattern_recognizer = {
            "name": "Rocket recognizer",
            "pattern": r'\W*(rocket)\W*',
            "score": 0.8,
            "entity": "ROCKET",
            "language": "en"}

        # Make sure the analyzer doesn't get this entity
        recognizers_store_api_mock = RecognizerStoreApiMock()
        analyze_engine = AnalyzerEngine(
            MockRecognizerRegistry(recognizers_store_api_mock))
        text = "rocket is my favorite transportation"
        entities = ["CREDIT_CARD", "ROCKET"]
        res = analyze_engine.analyze(text=text, entities=entities,
                                     language='en')
        assert len(res) == 0

        # Add a new recognizer for the word "rocket" (case insensitive)
        recognizers_store_api_mock.add_custom_pattern_recognizer(
            pattern_recognizer)

        # Check that the entity is recognized:
        res = analyze_engine.analyze(text=text, entities=entities,
                                     language='en')
        assert res[0].start == 0
        assert res[0].end == 7

    def test_remove_analyzer(self):
        pattern_recognizer = {
            "name": "Spaceship recognizer",
            "pattern": r'\W*(spaceship)\W*',
            "score": 0.8,
            "entity": "SPACESHIP",
            "language": "en"}
        # Make sure the analyzer doesn't get this entity
        recognizers_store_api_mock = RecognizerStoreApiMock()
        analyze_engine = AnalyzerEngine(MockRecognizerRegistry(
            recognizers_store_api_mock))
        text = "spaceship is my favorite transportation"
        entities = ["CREDIT_CARD", "SPACESHIP"]
        res = analyze_engine.analyze(text=text, entities=entities,
                                     language='en')
        assert len(res) == 0
        # Add a new recognizer for the word "rocket" (case insensitive)
        recognizers_store_api_mock.add_custom_pattern_recognizer(
            pattern_recognizer)
        # Check that the entity is recognized:
        res = analyze_engine.analyze(text=text, entities=entities,
                                     language='en')
        assert len(res) > 0
        assert res[0].start == 0
        assert res[0].end == 10

        # Remove recognizer
        recognizers_store_api_mock.remove_recognizer(
            "Spaceship recognizer")
        # Test again to see we didn't get any results
        res = analyze_engine.analyze(text=text, entities=entities,
                                     language='en')
        assert len(res) == 0

    def test_custom_cache_recognizers_logic(self):
        pattern_recognizer = {
            "name": "Rocket recognizer",
            "pattern": r'\W*(rocket)\W*',
            "score": 0.8,
            "entity": "ROCKET",
            "language": "en"}

        # Make sure the analyzer doesn't get this entity
        recognizers_store_api_mock = RecognizerStoreApiMock()
        analyze_engine = AnalyzerEngine(
            MockRecognizerRegistry(recognizers_store_api_mock))
        text = "rocket is my favorite transportation"
        entities = ["CREDIT_CARD", "ROCKET"]
        res = analyze_engine.analyze(text=text, entities=entities,
                                     language='en')
        assert len(res) == 0

        # Add a new recognizer for the word "rocket" (case insensitive)
        recognizers_store_api_mock.add_custom_pattern_recognizer(
            pattern_recognizer,
            skip_timestamp_update=True)

        # Check that the entity is recognized:
        res = analyze_engine.analyze(text=text, entities=entities,
                                     language='en')
        # Since the timestam wasn't updated the recognizers are stale from the cache
        # without the newly added one
        assert len(res) == 0
