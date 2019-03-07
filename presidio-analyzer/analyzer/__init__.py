"""Initializing analyzer modul."""
import os
import sys

from .pattern import Pattern  # noqa F401
from .entity_recognizer import EntityRecognizer  # noqa F401
from .local_recognizer import LocalRecognizer  # noqa F401
from .recognizer_result import RecognizerResult  # noqa F401
from .pattern_recognizer import PatternRecognizer  # noqa F401
from .remote_recognizer import RemoteRecognizer  # noqa F401
from .recognizer_registry.recognizer_registry import RecognizerRegistry  # noqa F401 pylint: disable=line-too-long
from .analyzer_engine import AnalyzerEngine  # noqa F401

# bug #602: Fix imports issue in python
# Once done, enable pylint for __ini__.py file by editing ignore-patterns
# setting in pylintrc
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + "/analyzer")

# from analyzer.pattern import Pattern  # noqa: F401
# from analyzer.entity_recognizer import EntityRecognizer  # noqa: F401
# from analyzer.local_recognizer import LocalRecognizer  # noqa: F401
# from analyzer.recognizer_result import RecognizerResult  # noqa: F401
# from analyzer.pattern_recognizer import PatternRecognizer  # noqa: F401
# from analyzer.remote_recognizer import RemoteRecognizer  # noqa: F401
# from analyzer.recognizer_registry.recognizer_registry import RecognizerRegistry  # noqa
# from analyzer.analyzer_engine import AnalyzerEngine  # noqa
