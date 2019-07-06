def flow(iterator):
    """ Start the experiment flow

    * This should be the last function in your flow

    Parameters
    ----------
    - iterator : `generator` of the last amount of data of your flow
    """

    while(True):
        next(iterator)


def makebuff(iterator, size=128):
    """ Take a generator and return a generator buffer

    Parameters
    ----------
    - iterator : `generator` of one single data
    - size: `int` buffer size

    Return
    ------
    - `Generator`: `Generator` of buffers [[n_channels] * size]
    """

    buff = []
    while(True):
        buff.append(next(iterator))

        if (len(buff) == size):
            yield(buff)
            buff = []
