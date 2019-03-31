from bcpy.signalacquisition import getdata
from time import sleep

p, data = getdata("LSL", board="openBCI", channels=["O1", "O2", "Oz"])

while(not p.is_receiving_data()):
    pass
print("Stream started")
data.set_marker(2)
sleep(2)
data.set_marker(1)
sleep(2)
# p.terminate()
print("data acquisition end")
print("\n\n\n")
timeStamp, eeg, markers = data.get_values()

noMarkers = 0
marker2 = 0
maeker1 = 0
for marker in markers:
    if marker == -1:
        noMarkers += 1
    elif marker == 1:
        maeker1 += 1
    elif marker == 2:
        marker2 += 1

print("-1:", noMarkers)
print("1:", maeker1)
print("2:", marker2)
