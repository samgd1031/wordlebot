'''
Utility Functions
'''
import re
import discord
import pymongo
import logging
import datetime as dt
from zoneinfo import ZoneInfo


logger = logging.getLogger(__name__)

# check if a message string is a valid wordle result
def is_valid_wordle(msg: str) -> bool:
    isWordle = re.match(r"Wordle \d* [1-6X]/6\*?", msg)
    
    if isWordle:
        return True
    else:
        return False

# convert a discord message to a dictionary format for sending to MongoDB
def wordle_message_to_dict(message: discord.Message) -> dict:
    d = {}
    d["player"] = {"name":message.author.name, "discriminator":message.author.discriminator}
    d["time"] = message.created_at
    cont = message.content.split("\n")
    hdr = cont[0].split()
    d["puzzle"] = {"type": "Wordle", "number": int(hdr[1])}
    d["hard_mode"] = True if hdr[2][-1] == '*' else False
    d["num_guesses"] = 0 if hdr[2][0] == 'X' else int(hdr[2][0])
    d["solved"] = False if d["num_guesses"] == 0 else True
    d["_id"]=f"{message.author.name}_{message.author.discriminator}_{d['puzzle']['type']}_{d['puzzle']['number']}"

    return d

# given a puzzle and client connected to a database, find who did the best that day
def get_daily_winners(day: dt.datetime, collection) -> list:
    docs = collection.find({"time":{'$gte':day, '$lt':day + dt.timedelta(days=1.0)}})
    docs = list(docs)
    
    if len(docs) == 0: 
        return None, None
    # assign scores for everyone
    else:
        # sort scores and determine winners
        scores = []
        puzzle = docs[0]['puzzle']['number']
        for doc in docs:
            nguess = doc['num_guesses'] if doc['solved'] else 7
            scores.append([doc['player']['name'], nguess])
            
        # sort scores
        scores = sorted(scores, key=lambda x:x[1])
        # assign places
        nplace = 1
        score = scores[0][1]
        for ii, entry in enumerate(scores):
            if entry[1] != score:
                score = entry[1]
                nplace += 1
            scores[ii].append(nplace)
            
        # return list of lists (player, score, place), and puzzle number
        return scores, puzzle