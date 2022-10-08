'''
Utility Functions
'''
import re
import discord

# check if a message string is a valid wordle result
def is_valid_wordle(msg: str) -> bool:

    isWordle = re.match(r"Wordle \d* [1-6X]/6\*?", msg)
    
    if isWordle:
        return True
    else:
        return False

def wordle_message_to_dict(message: discord.Message) -> dict:
    d = {}
    d["player"] = f"{message.author.name}_{message.author.discriminator}"
    d["time"] = message.created_at
    cont = message.content.split("\n")
    hdr = cont[0].split()
    d["puzzle"] = "wordle_" + hdr[1]
    d["hard_mode"] = True if hdr[2][-1] == '*' else False
    d["num_guesses"] = 0 if hdr[2][0] == 'X' else int(hdr[2][0])
    d["solved"] = False if d["num_guesses"] == -1 else True
    d["_id"]=f"{message.author.name}_{message.author.discriminator}_{d['puzzle']}"

    return d