var socket = io.connect('http://' + document.domain + ':' + location.port);
var cnt = 0
var firstPackage = true
var indices = []

function transpose(a)
{
  return a[0].map(function (_, c) { return a.map(function (r) { return r[c]; }); });
  // or in more modern dialect
  // return a[0].map((_, c) => a.map(r => r[c]));
}

socket.on('eeg', function (msg) {
    var graphData = []
    if (firstPackage) {
        msg.channels.forEach((channel, idx) => {
            indices.push(idx)
            graphData.push({
                y: [0],
                type: 'line',
                name: channel,
                mode: channel
            })
        })

        console.log(msg.eeg)
        console.log(indices)

        Plotly.newPlot('chart', graphData)
        firstPackage = false
        console.log(transpose(msg.eeg))
    }
    Plotly.extendTraces('chart', { y: transpose(msg.eeg)}, indices)
    cnt += msg.eeg.length;
    if (cnt > 100) {
        Plotly.relayout('chart', {
            xaxis: {
                range: [cnt - 100, cnt]
            }
        })
    }
})