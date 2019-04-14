var socket = io.connect('http://' + document.domain + ':' + location.port);
var data = []
var indices = [];
var options;
var rawData = []
var timestamp = []
var firstPackage = true;
var MaxNumOfPoints = 200;
var chart;
var graphData = []
var numOfPoints = 17
var channelsNames;
var channelData = []
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

    // channels.forEach((channel, idx) => {
    indices.push(0)
    graphData.push({
        x: [time],
        y: [newValue[0]],
        type: 'line',
        name: channels[0],
        mode: channels[0]
    })
    // });

    var layout = {
        title: 'EEG data',
        showlegend: true
    };

    Plotly.newPlot('chart', graphData, layout, { displayModeBar: false, staticPlot: true })
}

// const initGraph = (channels) => {
//     series = []
//     channels.forEach((ch, idx) => {
//         series.push(
//             {
//                 name: ch,
//                 color: COLORS[idx],
//                 data: [{ y: 0, }]
//             }
//         )
//     })
//     chart = new Rickshaw.Graph({
//         element: document.querySelector("#chart"),
//         width: 2000,
//         height: 250,
//         min: -700000,
//         max: 700000,
//         renderer: 'line',
//         series: new Rickshaw.Series.FixedDuration(series, undefined, {
//             timeInterval: 10,
//             maxDataPoints: 250,
//             timeBase: new Date().getTime() / 1000
//         })
//     });
//     chart.render();
// }

// const addData = (chart, message) => {
//     for (let i = 0; i < message.length; i++) {
//         let voltageData = {};
//         channelsNames.forEach((ch, idx) => {
//             voltageData[ch] = message[i][idx]
//         })
//         chart.series.addData(voltageData);
//     }
//     chart.render();
// }

const addData = () => {
    // console.log("teste")
    var dateToAdd = []
    var time = []
    var timeForEachPoint = []

    const size = rawData.length
    for (let i = 0; i < size; i++) {
        dateToAdd.push(rawData.shift()[0]);
        time.push(timestamp.shift());
        // cnt++;
    }


    dateToAdd = [dateToAdd];
    // console.log(dateToAdd)
    if (dateToAdd) {
        // dateToAdd.forEach((channel, idx) => {
        timeForEachPoint.push(time)
        // })
        Plotly.extendTraces('chart', { y: dateToAdd, x: timeForEachPoint }, indices)

        // console.log(graphData)
        while (graphData[0].y.length > MaxNumOfPoints) {
            // for (let i = 0; i < numOfPoints; i++) {
                graphData.forEach(channel => channel.y.shift())
            // }
        }
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