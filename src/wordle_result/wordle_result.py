from datetime import timezone


# class describing a single wordle result
class WordleResult():
    # initiaize from a dict (from a mongodDB request, discord messages must be converted)
    def __init__(self, d: dict):
        self.id = d["_id"]
        self.player = d['player']
        self.dt = d['time']
        if self.dt.tzinfo is None:
            self.dt = self.dt.replace(tzinfo=timezone.utc)
        self.puzzle = d['puzzle']
        self.hard_mode = d['hard_mode']
        self.num_guesses = d['num_guesses']
        self.solved = d['solved']

    # output as dict for insertion to mongoDB
    def to_dict(self):
        dc = {"_id":f"{self.player['name']}_{self.player['discriminator']}_{self.puzzle['type']}_{self.puzzle['number']}",
                "player":self.player,
                "time":self.dt,
                "puzzle":self.puzzle,
                "hard_mode":self.hard_mode,
                "num_guesses":self.num_guesses,
                "solved":self.solved}
        return dc

    def __repr__(self) -> str:
        if self.solved:
            return f"{self.puzzle['type']} {self.puzzle['number']} solved by {self.player['name']}#{self.player['discriminator']} on {self.dt.strftime('%m/%d/%Y %Z')} | guesses: {self.num_guesses} | hard mode: {self.hard_mode}"
        else:
            return f"{self.puzzle['type']} {self.puzzle['number']} failed by {self.player['name']}#{self.player['discriminator']} on {self.dt.strftime('%m/%d/%Y %Z')} | hard mode: {self.hard_mode}"