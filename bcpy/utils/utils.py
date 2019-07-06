def flow(iterator):
    while(True):
        next(iterator)

def makebuff(iterator, size=128):

    buff = []
    while(True):
        buff.append(next(iterator))

        if (len(buff) == size):
            yield(buff)
            buff = []
