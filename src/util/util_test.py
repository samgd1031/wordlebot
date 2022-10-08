from util.util import is_valid_wordle


def test_valid_wordles():
    
    assert is_valid_wordle("Wordle 123 1/6*") == True
    assert is_valid_wordle("Wordle 123 2/6*") == True
    assert is_valid_wordle("Wordle 123 3/6*") == True
    assert is_valid_wordle("Wordle 123 4/6*") == True
    assert is_valid_wordle("Wordle 123 5/6*") == True
    assert is_valid_wordle("Wordle 123 6/6*") == True

    assert is_valid_wordle("Wordle 123 1/6") == True

    assert is_valid_wordle("Wordle 1 1/6*") == True
    assert is_valid_wordle("Wordle 12 1/6*") == True
    assert is_valid_wordle("Wordle 123 1/6*") == True
    assert is_valid_wordle("Wordle 1234 1/6*") == True


def test_invalid_wordles():
    assert is_valid_wordle("Wordle 123 0/6*") == False
    assert is_valid_wordle("Wordle 123 7/6*") == False
    assert is_valid_wordle("Wordle 123 7/6*") == False
    assert is_valid_wordle("wordle 123 6/6*") == False
    assert is_valid_wordle("wordle 7/6*") == False
    assert is_valid_wordle("not wordle") == False