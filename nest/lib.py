

def ascii_char(char):
    """Returns the input character if it is an ASCII character, otherwise empty string.
    """
    if ord(char) > 127: 
        return ''
    else: 
        return char