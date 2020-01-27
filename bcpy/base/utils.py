import types
import json
import sys
from typing import Callable, Union, Any
from .._handlers import stop_execution, properties


props = properties.Properties()


def flow(iterator: types.GeneratorType,
         n_of_iterations: int = None,
         verbose: bool = False,
         function: Callable[[Union[list, Any]], None] = lambda x: None,
         ) -> None:
    """ Start the experiment flow

    **This should be the last function in your flow**

    Parameters
    ----------
    iterator : generator
        iterator of the last amount of data of your flow
    verbose : bool, optional
        show iterators content (default to False)
    """

    iterations = 0
    stop_execution.handle_stop_signal()
    while props.running:
        if n_of_iterations is not None and iterations >= n_of_iterations:
            break
        try:
            value = next(iterator)
        except Exception:
            break
        if verbose:
            print(value)
        function(value)
        iterations += 1
    stop_execution._interrupt_gracefully()


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


def create_window(generator: types.GeneratorType,
                  window_size: int,
                  intersection: int = None) -> types.GeneratorType:
    if not intersection:
        intersection = window_size / 2
    window = []
    is_windowing = True
    num_intersection = 0
    while props.running:
        data = next(generator)
        window.append(data)
        if window_size == len(window) and is_windowing:
            is_windowing = False
            yield window
        if window_size < len(window):
            num_intersection += 1
            window = window[1:]
        if num_intersection == intersection:
            num_intersection = 0
            yield window
