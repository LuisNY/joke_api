import requests
import argparse

BASE_URL = 'https://v2.jokeapi.dev/joke/Any?safe-mode'

class ConnectionToJokeAPI:
    def __init__(self):
        self.joke_api = requests.get(BASE_URL)

def argument_parser():
    '''
    argument_parser() is a helper function to parse input arguments from the CLI

    :param: none

    :return args: The parsed CLI args
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number_of_jokes", type=int, default=1, help="The number of jokes you want to generate")
    args = parser.parse_args()

    return args

def error_handler(exception):
    '''
    error_handler() is a helper function to raise a ValueError when a stage fails

    :param: none

    :return: none
    '''

    raise ValueError(exception)

def get_joke_api():
    '''
    get_joke_api() is a helepr function to get the joke website api defined by the base url

    :param: none

    :return joke_api: The api to the joke generator
    '''

    try:
        joke_api = ConnectionToJokeAPI().joke_api
        return joke_api

    except Exception as arg:
        error_handler(arg)


def get_joke_type(joke_api):
    '''
    get_joke_type() is a helper function to get the joke type from the joke api

    :param joke_api: The api for the joke generator

    :return joke_type: The type of joke, it can be "single" or "twopart" 
    '''

    try:
        joke_type = joke_api.json()['type']
        return joke_type

    except Exception as arg:
        error_handler(arg)   

def get_joke(joke_api, joke_type):
    '''
    get_joke() is a helper fucntion to get the joke with a specified joke type from the joke api

    :param joke_api: The api for the joke generator
    :param joke_type: The joke type to pass to the joke generator

    :return joke: The joke generated 
    '''

    try:
        joke = 'No Joke Found'

        if joke_type == "single":
            joke = f"{joke_api.json()['joke']}"
        elif joke_type == "twopart":
            joke = f"{joke_api.json()['setup']}\n{joke_api.json()['delivery']}"
        else: 
            error_handler("Error: An invalid type was supplied")
        return joke
        
    except Exception as arg:
        error_handler(arg)

def joke_machine_runner(number_of_jokes_to_generate):
    '''
    joke_machine_runner() runs the joke machine

    :param number_of_jokes_to_generate: The number of jokes we want to generate from the machine

    :return none:
    '''

    for i in range(number_of_jokes_to_generate):
        try:
            joke_api = get_joke_api()
            joke_type = get_joke_type(joke_api)
            joke = get_joke(joke_api, joke_type)
            print(joke)

        except ValueError as arg:
            print(arg)

def main():
    args = argument_parser()
    joke_machine_runner(args.number_of_jokes)

if __name__ == '__main__':
    main()

#
#
# {
#   "error": false,
#   "category": "Pun",
#   "type": "single",
#   "joke": "I'm reading a book about anti-gravity. It's impossible to put down!",
#   "flags": {
#     "nsfw": false,
#     "religious": false,
#     "political": false,
#     "racist": false,
#     "sexist": false,
#     "explicit": false
#   },
#   "id": 126,
#   "safe": true,
#   "lang": "en"
# }
#
# {
#   "error": false,
#   "category": "Misc",
#   "type": "twopart",
#   "setup": "This morning I accidentally made my coffee with Red Bull instead of water.",
#   "delivery": "I was already on the highway when I noticed I forgot my car at home.",
#   "flags": {
#     "nsfw": false,
#     "religious": false,
#     "political": false,
#     "racist": false,
#     "sexist": false,
#     "explicit": false
#   },
#   "id": 146,
#   "safe": true,
#   "lang": "en"
# }