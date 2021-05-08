def characterRemover(fugu):
    new = ''
    for alphabet in fugu:
        if ord(alphabet) >= 65 and ord(alphabet) <= 90:
            new += alphabet
        elif ord(alphabet) >= 97 and ord(alphabet) <= 122:
            new += alphabet
    return new

def listmerger(arrays):
        l = []
        for array in arrays:
            l += array
        return l