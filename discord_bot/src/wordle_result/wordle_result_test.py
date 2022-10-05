import json
from wordle_result import WordleResult
import datetime as dt

# test if wordle results jsonify correctly
def test_jsonification():
    msg = {"player":"xX_JohnDoe_Xx_1234", 
            "time":dt.datetime(2022,1,1,0,0,0,tzinfo=dt.timezone.utc),
            "puzzle":"wordle_123",
            "hard_mode": False,
            "num_guesses": 1,
            "solved": True,
            "_id":"xX_JohnDoe_Xx_1234_wordle_123"
    }
    wr = WordleResult(msg)
    assert(wr.to_dict() == msg)