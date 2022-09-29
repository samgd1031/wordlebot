import json
from wordle_result import WordleResult
import datetime as dt

# mocks a discord message class
class MessageMock():
    def __init__(self, author, created, header):
        self.author = author
        self.created_at = created
        self.header = header

# test if wordle results jsonify correctly
def test_jsonification():
    msg = MessageMock("xX_JohnDoe_Xx", dt.datetime(2022,1,1,0,0,0), "Wordle 123 1/6")
    wr = WordleResult(msg, msg.header)
    dc = {"player":"xX_JohnDoe_Xx",
        "dt":"2022-01-01T00:00:00",
        "puzzle_number":"wordle_123",
        "hard_mode":False,
        "num_guesses":1,
        "solved":True}
    assert(wr.toJSON() == json.dumps(dc))