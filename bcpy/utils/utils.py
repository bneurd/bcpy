import types


def flow(iterator: types.GeneratorType, verbose: bool = False) -> None:
    """ Start the experiment flow

    **This should be the last function in your flow**

    Parameters
    ----------
    iterator : generator
        iterator of the last amount of data of your flow
    verbose : bool, optional
        show iterators content (default to False)
    """

    while(True):
        if verbose:
            print(next(iterator))
            continue
        next(iterator)


def makebuff(
        iterator: types.GeneratorType, size: int = 128) -> types.GeneratorType:
    """ Take a generator and return a generator buffer

    Parameters
    ----------
    iterator : `generator` of one single data
    size: `int` buffer size

    Yield
    ------
    buffer: :obj:`list` with len = size of :obj:`list` with size = n_channels
    """

    buff = []
    while(True):
        buff.append(next(iterator))

        if (len(buff) == size):
            yield(buff)
            buff = []
