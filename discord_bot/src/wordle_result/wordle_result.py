import datetime as dt
from datetime import date


# class describing a single wordle result
class WordleResult():
    
    def __init__(self, message, header):
        self.player = message.author
        self.dt = message.created_at.isoformat()
        hdr = header.split()
        self.puzzle_number = "wordle_" + hdr[1]
        self.hard_mode = True if hdr[2][-1] == '*' else False
        self.num_guesses = -1 if hdr[2][0] == 'X' else int(hdr[2][0])
        self.solved = False if self.num_guesses == -1 else True

    # initiaize from a dict (from a mongodDB request)
    def __init__(self, d: dict):
        self.player = d['player']
        self.dt = dt.datetime.fromisoformat(d['time'])
        self.puzzle_number = d['puzzle']
        self.hard_mode = d['hard_mode']
        self.num_guesses = d['num_guesses']
        self.solved = d['solved']

    
    def to_dict(self):
        dc = {"_id":f"{self.player.name}_{self.player.discriminator}_{self.puzzle_number}",
                "player":f"{self.player.name}_{self.player.discriminator}",
                "time":self.dt,
                "puzzle":self.puzzle_number,
                "hard_mode":self.hard_mode,
                "num_guesses":self.num_guesses,
                "solved":self.solved}
        return dc

    def __repr__(self) -> str:
        if self.solved:
            return f"Puzzle {self.puzzle_number} solved by {self.player} | guesses: {self.num_guesses} | hard mode: {self.hard_mode}"
        else:
            return f"Puzzle {self.puzzle_number} failed by {self.player} | hard mode: {self.hard_mode}"