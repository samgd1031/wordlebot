import json


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
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self) -> str:
        if self.solved:
            return f"Puzzle {self.puzzle_number} solved by {self.player} | guesses: {self.num_guesses} | hard mode: {self.hard_mode}"
        else:
            return f"Puzzle {self.puzzle_number} failed by {self.player} | hard mode: {self.hard_mode}"