from bcpy.acquisition import getdata
from bcpy.realtimevisualization import realtimevisualization
from bcpy.utils import makebuff, flow, save, buff_to_single
from bcpy.processing import bandfilter

options = {
    "channels": ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2"],
    "fs": 256
}

data = getdata("FileBuffer", filename="data.json")
buff = makebuff(data, 256)
filter_buff = bandfilter(buff, lo=8, hi=50)
filter_buff = bandfilter(filter_buff, lo=8, hi=50)
buffvis = realtimevisualization(
    "WebPage", filter_buff, options)

# save('data.json', buff_to_single(buffvis), options["channels"], options["fs"])
flow(buffvis, verbose=True)
