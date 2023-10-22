import subprocess
import sys

sys.path.append('../Test Automation')
import argparse
import unittest
from unittest import mock

from joke_machine import main
from common_fixtures import MockResponse


class ComponentTests(unittest.TestCase):

    def setUp(self):
        # reset command line args
        sys.argv = sys.argv[:1]

    @mock.patch('joke_machine.get_joke_api', side_effect=lambda: MockResponse(200))
    @mock.patch('joke_machine.print')
    def test_call_main_without_args(self, mocked_print, mocked_get_joke_api):

        main()  # no args, will default to 1 joke

        # since we are not passing any argument, the value of -n defaults to 1
        assert mocked_get_joke_api.call_count == 1
        assert mocked_print.call_count == 1

        expected_string = 'I\'m reading a book about anti-gravity. It\'s impossible to put down!'
        assert mocked_print.call_args_list[0][0][0] == expected_string

    @mock.patch('joke_machine.get_joke_api', side_effect=lambda: MockResponse(200))
    @mock.patch('joke_machine.print')
    def test_call_main_with_args(self, mocked_print, mocked_get_joke_api):

        sys.argv.append('-n 5')  # get 5 jokes
        main()

        assert mocked_get_joke_api.call_count == 5
        assert mocked_print.call_count == 5

    @mock.patch('joke_machine.get_joke_api', side_effect=lambda: MockResponse(200))
    @mock.patch('joke_machine.print')
    def test_call_main_with_negative_amount(self, mocked_print, mocked_get_joke_api):

        sys.argv.append('-n -5')  # negative value, it will not get any jokes
        main()

        assert mocked_get_joke_api.call_count == 0
        assert mocked_print.call_count == 0

    def test_call_main_with_unrecognized_args(self):

        sys.argv.append('--unknown')  # unknown argument, will result in system exit from parser.parse_args()

        try:
            main()
        except SystemExit as e:
            assert type(e) == SystemExit
            assert e.__str__() == '2'


if __name__ == '__main__':
    unittest.main()
