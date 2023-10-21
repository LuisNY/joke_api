import sys

sys.path.append('../Test Automation')

import json
import os
import unittest
from unittest import mock

from joke_machine import BASE_URL, get_joke_type, get_joke_api, get_joke, joke_machine_runner

#     get_joke()
#     joke_machine_runner()


# we are always returning ValueError
# if key error happens we are not logging it properly
# no one is checking for status code
# names of vars too long


mocked_obj = \
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
    def __init__(self, status_code):
        self.status_code = status_code

    @staticmethod
    def json():
        return mocked_obj


class MockResponseRaiseOnJson(MockResponse):

    @staticmethod
    def json():
        raise Exception('Could not return json object')


class MockResponseMissingType(MockResponse):

    @staticmethod
    def json():
        missing_field_obj = mocked_obj.copy()
        del missing_field_obj['type']
        return missing_field_obj


# test get_joke_api()
class GetJokeApiTest(unittest.TestCase):

    @staticmethod
    def mocked_request_200(args):
        return MockResponse(200)

    @staticmethod
    def mocked_request_exception(args):
        raise Exception('Exception occurred')

    # mock valid request/response with status code = 200
    @mock.patch('requests.get', side_effect=mocked_request_200)
    def test_get_joke_api_200(self, _):

        joke_api = get_joke_api()
        assert joke_api.status_code == 200
        assert joke_api.json() == mocked_obj

    # mock invalid request/response, exception is raised
    @mock.patch('requests.get', side_effect=mocked_request_exception)
    def test_get_joke_api_exception(self, _):
        try:
            get_joke_api()
        except ValueError as e:
            assert e.__str__() == 'Exception occurred'


# test get_joke_type()
class GetJokeTypeTest(unittest.TestCase):

    # test valid joke type
    @staticmethod
    def test_get_joke_type_valid():
        assert get_joke_type(MockResponse(200)) == 'twopart'

    # test invalid joke type, json() raises exception
    @staticmethod
    def test_get_joke_type_invalid_json():
        try:
            get_joke_type(MockResponseRaiseOnJson(200))
        except ValueError as e:
            assert e.__str__() == 'Could not return json object'

    # test invalid joke type, missing 'type' key from json object
    @staticmethod
    def test_get_joke_type_missing_json_field():
        try:
            get_joke_type(MockResponseMissingType(200))
        except ValueError as e:
            assert type(e.args[0]) == KeyError
            assert e.args[0].__str__() == '\'type\''


# test get_joke()
# class GetJokeTest(unittest.TestCase):



if __name__ == '__main__':
    unittest.main()
