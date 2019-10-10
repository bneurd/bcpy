import types
import json
import sys
from .._handlers import stop_execution, properties


props = properties.Properties()


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

    stop_execution.handle_stop_signal()
    while props.running:
        if verbose:
            print(next(iterator))
            continue
        next(iterator)
    print("main process stoped")
    stop_execution.clean_all_process()


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


def buff_to_single(
        iterator: types.GeneratorType) -> types.GeneratorType:

    while(True):
        buff = next(iterator)
        for value in buff:
            yield value


def _create_data_structure(channels: list,
                           frequency: int,
                           data_type: str) -> dict:
    data_structure = {
        "channels": channels,
        "frequency": frequency,
        "data": [],
        "type": data_type,
    }
    return data_structure


def _save_file(filename: str, json_data: dict):
    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=2)


def _update_timestamp(timestamp, frequency):
    timestamp += 1
    return timestamp if timestamp < frequency else 0


def save(filename: str,
         data_gen: types.GeneratorType,
         channels: list,
         frequency: int,
         marker_gen: types.GeneratorType = iter(()),
         data_type: str = 'EEG') -> None:
    timestamp = 0
    data_structure = _create_data_structure(channels, frequency, data_type)
    while(True):
        data = next(data_gen)
        marker = next(marker_gen, None)
        data_structure["data"].append(
            {"timestamp": timestamp, "data": data.tolist(), "marker": marker})
        timestamp = _update_timestamp(timestamp, frequency)
        _save_file(filename, data_structure)
