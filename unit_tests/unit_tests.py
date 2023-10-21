import sys

sys.path.append('../Test Automation')

import json
import os
import unittest
from unittest import mock

from joke_machine import BASE_URL, get_joke_type, get_joke_api, get_joke, joke_machine_runner

#     get_joke()
#     joke_machine_runner()

# joke = 'No Joke Found' -> initialized but never used
# we are always returning ValueError
# if key error happens we are not logging it properly
# no one is checking for status code
# names of vars too long

mocked_obj_single = \
    {
        "error": False,
        "category": "Pun",
        "type": "single",
        "joke": "I'm reading a book about anti-gravity. It's impossible to put down!",
        "flags": {
            "nsfw": False,
            "religious": False,
            "political": False,
            "racist": False,
            "sexist": False,
            "explicit": False
        },
        "id": 126,
        "safe": True,
        "lang": "en"
    }

mocked_obj_twoparts = \
    {
        "error": False,
        "category": "Misc",
        "type": "twopart",
        "setup": "This morning I accidentally made my coffee with Red Bull instead of water.",
        "delivery": "I was already on the highway when I noticed I forgot my car at home.",
        "flags": {
            "nsfw": False,
            "religious": False,
            "political": False,
            "racist": False,
            "sexist": False,
            "explicit": False
        },
        "id": 146,
        "safe": True,
        "lang": "en"
    }


# simulate behavior of requests.models.Response object
class MockResponse:
    def __init__(self, status_code, joke_type='single', missing_fields=None, raise_on_json=False):
        if missing_fields is None:
            missing_fields = []
        self.status_code = status_code
        self.missing_fields = missing_fields
        self.raise_on_json = raise_on_json
        self.joke_type = joke_type

    def json(self):

        if self.raise_on_json:
            raise Exception('Could not return json object')

        missing_field_obj = mocked_obj_single.copy() if self.joke_type == 'single' else mocked_obj_twoparts.copy()
        for field in self.missing_fields:
            if field in missing_field_obj:
                del missing_field_obj[field]

        return missing_field_obj


# test get_joke_api()
class GetJokeApiTest(unittest.TestCase):

    @staticmethod
    def mocked_request_200(args):
        return MockResponse(200, joke_type='twopart')

    @staticmethod
    def mocked_request_exception(args):
        raise Exception('Exception occurred')

    # mock valid request/response with status code = 200
    @mock.patch('requests.get', side_effect=mocked_request_200)
    def test_get_joke_api_200(self, _):

        joke_api = get_joke_api()
        assert joke_api.status_code == 200
        assert joke_api.json() == mocked_obj_twoparts

    # mock invalid request/response, exception is raised
    @mock.patch('requests.get', side_effect=mocked_request_exception)
    def test_get_joke_api_exception(self, _):
        try:
            get_joke_api()
        except ValueError as e:
            assert e.__str__() == 'Exception occurred'
        else:
            assert False


# test get_joke_type()
class GetJokeTypeTest(unittest.TestCase):

    # test valid joke type
    @staticmethod
    def test_get_joke_type_valid():
        assert get_joke_type(MockResponse(200, joke_type='twopart')) == 'twopart'

    # test invalid joke type, json() raises exception
    @staticmethod
    def test_get_joke_type_invalid_json():
        try:
            get_joke_type(MockResponse(200, joke_type='twopart', raise_on_json=True))
        except ValueError as e:
            assert e.__str__() == 'Could not return json object'
        else:
            assert False

    # test invalid joke type, missing 'type' key from json object
    @staticmethod
    def test_get_joke_type_missing_json_field():
        try:
            get_joke_type(MockResponse(200, joke_type='twopart', missing_fields=['type']))
        except ValueError as e:
            assert type(e.args[0]) == KeyError
            assert e.args[0].__str__() == '\'type\''
        else:
            assert False


# test get_joke()
class GetJokeTest(unittest.TestCase):

    @staticmethod
    def test_get_joke_two_part():
        api_response = MockResponse(200, joke_type='twopart')
        joke_type = 'twopart'
        joke = get_joke(api_response, joke_type)
        assert joke == 'This morning I accidentally made my coffee with Red Bull instead of water.' \
                       '\nI was already on the highway when I noticed I forgot my car at home.'

    @staticmethod
    def test_get_joke_single():
        api_response = MockResponse(200, joke_type='single')
        joke_type = 'single'
        joke = get_joke(api_response, joke_type)
        assert joke == 'I\'m reading a book about anti-gravity. It\'s impossible to put down!'

    @staticmethod
    def test_get_joke_invalid_type():

        # test behavior on single response
        api_response = MockResponse(200, joke_type='single')
        joke_type = 'something'
        try:
            get_joke(api_response, joke_type)
        except ValueError as e:
            assert e.__str__() == 'Error: An invalid type was supplied'
        else:
            assert False

        # confirm same behavior with twopart response
        api_response = MockResponse(200, joke_type='twopart')
        try:
            get_joke(api_response, joke_type)
        except ValueError as e:
            assert e.__str__() == 'Error: An invalid type was supplied'
        else:
            assert False

    # test with invalid json in joke response
    @staticmethod
    def test_get_joke_invalid_json():

        api_response = MockResponse(200, joke_type='single', raise_on_json=True)
        joke_type = 'single'
        try:
            get_joke(api_response, joke_type)
        except ValueError as e:
            assert e.__str__() == 'Could not return json object'
        else:
            assert False

        api_response = MockResponse(200, joke_type='twopart', raise_on_json=True)
        joke_type = 'twopart'
        try:
            get_joke(api_response, joke_type)
        except ValueError as e:
            assert e.__str__() == 'Could not return json object'
        else:
            assert False

    @staticmethod
    def test_get_joke_invalid_json():
        # test single response with missing field
        api_response = MockResponse(200, joke_type='single', missing_fields=['joke'])
        joke_type = 'single'
        try:
            get_joke(api_response, joke_type)
        except ValueError as e:
            assert type(e.args[0]) == KeyError
            assert e.args[0].__str__() == '\'joke\''
        else:
            assert False

        # test twopart response with missing fields (setup and delivery)
        api_response = MockResponse(200, joke_type='twopart', missing_fields=['setup'])
        joke_type = 'twopart'
        try:
            get_joke(api_response, joke_type)
        except ValueError as e:
            assert type(e.args[0]) == KeyError
            assert e.args[0].__str__() == '\'setup\''
        else:
            assert False

        api_response = MockResponse(200, joke_type='twopart', missing_fields=['delivery'])
        joke_type = 'twopart'
        try:
            get_joke(api_response, joke_type)
        except ValueError as e:
            assert type(e.args[0]) == KeyError
            assert e.args[0].__str__() == '\'delivery\''
        else:
            assert False




if __name__ == '__main__':
    unittest.main()
