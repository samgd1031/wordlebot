'''
Utility Functions
'''
import re

# check if a message string is a valid wordle result
def is_valid_wordle(msg: str) -> bool:

    isWordle = re.match(r"Wordle \d* [1-6X]/6\*?", msg)
    
    if isWordle:
        return True
    else:
        return False