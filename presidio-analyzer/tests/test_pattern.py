from unittest import TestCase

from analyzer import Pattern

my_pattern = Pattern(name="my pattern", strength=0.9, pattern="[pat]")
my_pattern_dict = {"name": "my pattern", "pattern": "[pat]", "strength": 0.9}


class TestPattern(TestCase):

    def test_to_dict(self):
        expected = {"name": "my pattern", "regex": "[re]", "score": 0.9}
        pat = Pattern(name="my pattern", score=0.9, regex="[re]")
        actual = pat.to_dict()

        assert expected == actual

    def test_from_dict(self):
        expected = {"name": "my pattern", "regex": "[re]", "score": 0.9}
        pat = Pattern.from_dict(expected)
        actual = pat.to_dict()

        assert expected.name == actual.name
        assert expected.score == actual.score
        assert expected.pattern == actual.pattern

       # assert expected == actual
