var socket = io.connect('http://' + document.domain + ':' + location.port);
var cnt = 0
var data = []
var indices = [];
var options;
var rawData = []
var timestamp = []
var firstPackage = true;
var MaxNumOfPoints = 200;
var chart;
var cnt = 0;
var max = 250;
var graphData = []
var numOfPoints = 10

function transpose(a) {
    if (a[0] && a[0].map) {
        return a[0].map(function (_, c) { return a.map(function (r) { if (r) return r[c]; }); });
    }
    // or in more modern dialect
    // return a[0].map((_, c) => a.map(r => r[c]));
}

const initGraph = (channels) => {
    var newValue = rawData.shift();
    var time = timestamp.shift();

    channels.forEach((channel, idx) => {
        indices.push(idx)
        graphData.push({
            x: [time],
            y: [newValue[idx]],
            type: 'line',
            name: channel,
            mode: channel
        })
    });

    var layout = {
        title: 'EEG data',
        showlegend: true
    };

    Plotly.newPlot('chart', graphData, layout, {displayModeBar: false, staticPlot: true})
}

const addData = () => {
    var dateToAdd = []
    var time = []
    var timeForEachPoint = []

    for (let i = 0; i < numOfPoints; i++) {
        dateToAdd.push(rawData.shift());
        time.push(timestamp.shift());
        cnt++;
    }

    // console.log(rawData.length)

    dateToAdd = transpose(dateToAdd);
    if (dateToAdd) {
        dateToAdd.forEach((channel, idx) => {
            timeForEachPoint.push(time)
        })
        Plotly.extendTraces('chart', { y: dateToAdd, x: timeForEachPoint }, indices)

        if (cnt > max) {
            for (let i = 0; i < numOfPoints; i++) {
                graphData.forEach(channel => channel.y.shift())
            }
        }
        setTimeout(addData, 20);
    } else {
        setTimeout(addData, 30);
    }
}

socket.on('eeg', function (msg) {
    rawData = rawData.concat(msg.eeg);
    timestamp = timestamp.concat(msg.timestamp)

    // console.log(rawData.length)

    if (firstPackage) {
        initGraph(msg.channels)
        console.log(msg.eeg.length)
        firstPackage = false
        addData()
    }
})