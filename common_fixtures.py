# sample response for a single joke
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

# sample response for a twopart joke
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
