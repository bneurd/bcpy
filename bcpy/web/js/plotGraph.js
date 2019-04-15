var socket = io.connect('http://' + document.domain + ':' + location.port);
var options;
var rawData = []
var timestamp = []
var firstPackage = true;
var MaxNumOfPoints = 200;
var chart;
var graphData = []
var numOfPoints = 17
var channelsNames;
var series;

$("#con-status").html("disconnected")
$("#con-status").addClass("text-danger")
$("#numOfPkg").html(numOfPoints)
$("#numOfPkgRange").val(numOfPoints)

$("#numOfPkgRange").on('input', function () {
    numOfPoints = $("#numOfPkgRange").val()
    $("#numOfPkg").html(numOfPoints)
})

$("#MaxOfPointsRange").val(MaxNumOfPoints)

$("#MaxOfPointsRange").on('input', function () {
    MaxNumOfPoints = $("#MaxOfPointsRange").val()
    $("#MaxOfPoints").html(MaxNumOfPoints)
})

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
        $("#channels").append(`<div id=${channel}></div>`)
        graphData.push({
            x: [time],
            y: [newValue[idx]],
            type: 'line',
            name: channel,
            mode: channel,
            line: {
                color: COLORS[idx]
            }
        })
        var layout = {
            // title: 'EEG data',
            // autosize: false,
            height: 100,
            margin: {
                l: 50,
                r: 50,
                b: 0,
                t: 0,
                pad: 2
              },
            showlegend: false
        };

        Plotly.newPlot(channel, [graphData[idx]], layout, { displayModeBar: false, staticPlot: true })
    });
}

const addData = () => {
    // console.log("teste")
    var dateToAdd = []
    var time = []
    var timeForEachPoint = []

    const size = rawData.length
    for (let i = 0; i < size; i++) {
        dateToAdd.push(rawData.shift());
        time.push(timestamp.shift());
        // cnt++;
    }

    dateToAdd = transpose(dateToAdd);
    channelsNames.forEach((channel, idx) => {
        var channelData = [dateToAdd[idx]]
        if (channelData) {
            Plotly.extendTraces(channel, { y: channelData, x: [time] }, [0])
        }
    })
    while (graphData[0].y.length > MaxNumOfPoints) {
        // for (let i = 0; i < numOfPoints; i++) {
        graphData.forEach(channel => channel.y.shift())
        // }
    }
}

socket.on('connect', () => {
    $("#con-status").html("connected")
    $("#con-status").removeClass("text-danger").addClass("text-success")
})

socket.on('disconnect', () => {
    $("#con-status").html("disconnected")
    $("#con-status").removeClass("text-success").addClass("text-danger")
})

socket.on('eeg', function (msg) {
    data = JSON.parse(msg)
    rawData = rawData.concat(data.eeg);
    timestamp = timestamp.concat(data.timestamp)

    // console.log(data.eeg.length)

    if (firstPackage) {
        channelsNames = data.channels;
        initGraph(data.channels)
        console.log(data.eeg.length)
        console.log(channelsNames)
        firstPackage = false
    }

    if (rawData.length >= numOfPoints) {
        addData(chart, rawData)
        rawData = []
    }
})