import sys

sys.path.append('../Test Automation')
import unittest
from unittest import mock
from joke_machine import get_joke_type, get_joke_api, get_joke, joke_machine_runner
from common_fixtures import MockResponse, mocked_obj_twoparts


# test get_joke_api()
class GetJokeApiTest(unittest.TestCase):

    @staticmethod
    def mocked_request_200(args):
        return MockResponse(200, joke_type='twopart')

    @staticmethod
    def mocked_request_exception(args):
        raise ValueError('Exception occurred')

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
        # test single response with missing field (joke)
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


# test joke_machine_runner()
class GetJokeMachineRunnerTest(unittest.TestCase):

    @staticmethod
    def mocked_joke_api_200():
        return MockResponse(200, joke_type='single')

    @staticmethod
    def mocked_request_exception(args):
        raise ValueError('Exception occurred')

    # test function when everything goes well
    @mock.patch('joke_machine.get_joke_api', side_effect=mocked_joke_api_200)
    @mock.patch('joke_machine.print')
    def test_joke_machine_runner_valid_n(self, mocked_print, mocked_get_joke_api):
        joke_machine_runner(3)
        assert mocked_get_joke_api.call_count == 3
        assert mocked_print.call_count == 3

        # make sure we printed the joke
        expected_string = 'I\'m reading a book about anti-gravity. It\'s impossible to put down!'
        assert mocked_print.call_args_list[0][0][0] == expected_string
        assert mocked_print.call_args_list[1][0][0] == expected_string
        assert mocked_print.call_args_list[2][0][0] == expected_string

    # test function when api call fails
    @mock.patch('requests.get', side_effect=mocked_request_exception)
    @mock.patch('joke_machine.print')
    def test_joke_machine_runner_valid_n(self, mocked_print, mocked_request):
        joke_machine_runner(3)
        assert mocked_request.call_count == 3
        assert mocked_print.call_count == 3

        # make sure we printed the error
        assert type(mocked_print.call_args_list[0][0][0]) == ValueError
        assert type(mocked_print.call_args_list[1][0][0]) == ValueError
        assert type(mocked_print.call_args_list[2][0][0]) == ValueError


if __name__ == '__main__':
    unittest.main()
