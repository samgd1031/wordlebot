"""
Utility Functions
"""
import re
import discord
import logging
import datetime as dt


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
    d["channel"] = [message.channel.id]
    d["guild"] = [message.guild.id]

    return d

def print_daily_winners(entries, puzzle_num):
    if not entries:
        resp = f"No entries for Wordle {puzzle_num}"
    else:
        # sort
        entries = sorted(entries, key=lambda d: d['num_guesses'])

        # build response
        resp = f"--- Wordle {puzzle_num} ---\n"
        nplace = 1
        score = entries[0]['num_guesses']
        for e in entries:
            if e['num_guesses'] != score:
                nplace += 1
                score = e['num_guesses']
            resp += f"{nplace:2d}. {e['player']['name']:16s} - {'X' if score == 7 else score} "\
                                                                f"{':crown:' if nplace == 1 else ''}\n"
                                                            
    return resp