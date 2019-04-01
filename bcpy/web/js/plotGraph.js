var socket = io.connect('http://' + document.domain + ':' + location.port);
var cnt = 0
var firstPackage = true
var indices = []

function transpose(a) {
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
                x: msg.timestamp,
                y: transpose(msg.eeg)[idx],
                type: 'line',
                name: channel,
                mode: channel
            })
        })

        Plotly.newPlot('chart', graphData)
        firstPackage = false
    }

    timestamp = []
    eegData = transpose(msg.eeg);
    msg.channels.forEach((channel, idx) => {
        timestamp.push(msg.timestamp)
    })

    Plotly.extendTraces('chart', { y: eegData, x: timestamp }, indices)
    cnt = msg.timestamp[msg.timestamp.length - 1];
    if (cnt > 100) {
        Plotly.relayout('chart', {
            xaxis: {
                range: [cnt - 100, cnt]
            }
        })
    }
})