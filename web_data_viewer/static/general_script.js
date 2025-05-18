function randomTest(data) {
    // data.dataInfo.forEach((dataPoint, index) => {
    //     console.log(`${index+1}: ${dataPoint}`);
    // });

    // get data arrays
    var panData = [...data.left_pan];
    var tiltData = [...data.head_tilt];
    var phoneData = [...data.phone_detected];

    const xLabels1 = [];
    for (let i = 0; i < panData.length; i++) {
        xLabels1.push(i);
    }
    if (myChart1) {
        myChart1.destroy();
    }
    myChart1 = new Chart(eyeGraph, {
        type: 'line',
        data: {
            labels: xLabels1,
            datasets: [{
                label: 'Eye Pans',
                data: panData,
                borderColor: 'rgb(255, 255, 255)',  // Bootstrap primary
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.3,  // smooth lines
                fill: true
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                    color: 'black'  // legend text
                    }
                },
            },
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: 'black'  // y-axis labels
                    },
                    grid: {
                        color: 'black'
                    }
                },
                x: {
                    ticks: {
                        color: 'black'  // x-axis labels
                    },
                    grid: {
                        color: 'black' // optional grid color
                    }
                },
            }
        }
    });

    const xLabels2 = [];
    for (let i = 0; i < tiltData.length; i++) {
        xLabels2.push(i);
    }
    if (myChart2) {
        myChart2.destroy();
    }
    myChart2 = new Chart(tiltGraph, {
        type: 'line',
        data: {
            labels: xLabels2,
            datasets: [{
                label: 'Head Tilts',
                data: tiltData,
                borderColor: 'rgb(255, 255, 255)',  // Bootstrap primary
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.3,  // smooth lines
                fill: true
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                    color: 'black'  // legend text
                    }
                },
            },
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: 'black'  // y-axis labels
                    },
                    grid: {
                        color: 'black'
                    }
                },
                x: {
                    ticks: {
                        color: 'black'  // x-axis labels
                    },
                    grid: {
                        color: 'black' // optional grid color
                    }
                },
            }
        }
    });

    const xLabels3 = [];
    for (let i = 0; i < phoneData.length; i++) {
        xLabels3.push(i);
    }
    if (myChart3) {
        myChart3.destroy();
    }
    myChart3 = new Chart(phoneGraph, {
        type: 'line',
        data: {
            labels: xLabels3,
            datasets: [{
                label: 'Phone Detected',
                data: phoneData,
                borderColor: 'rgb(255, 255, 255)',  // Bootstrap primary
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.3,  // smooth lines
                fill: true
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                    color: 'black'  // legend text
                    }
                },
            },
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: 'black'  // y-axis labels
                    },
                    grid: {
                        color: 'black'
                    }
                },
                x: {
                    ticks: {
                        color: 'black'  // x-axis labels
                    },
                    grid: {
                        color: 'black' // optional grid color
                    }
                },
            }
        }
    });

    fetch(`/get-gemini/phoneGraph`)
        .then(res => res.json())
        .then(data => {outputGemini1(data)});
    eyeVariance.innerHTML = "Deviation From Avg." + calcVariance(panData);
    fetch(`/get-gemini/eyeGraph`)
        .then(res => res.json())
        .then(data => {outputGemini2(data)});
    tiltVariance.innerHTML = "Deviation From Avg." + calcVariance(tiltData);
    fetch(`/get-gemini/tiltGraph`)
        .then(res => res.json())
        .then(data => {outputGemini3(data)});
    
}

function outputGemini1(data) {
    geminiOutput = data;
    geminiSummary1.innerHTML = `${geminiOutput.output}`;
    // console.log(`${geminiOutput.output}`);
}

function outputGemini2(data) {
    geminiOutput = data;
    geminiSummary2.innerHTML = `${geminiOutput.output}`;
    // console.log(`${geminiOutput.output}`);
}

function outputGemini3(data) {
    geminiOutput = data;
    geminiSummary3.innerHTML = `${geminiOutput.output}`;
    // console.log(`${geminiOutput.output}`);
}

function calcVariance(data) {
    const mean = (data.reduce((sum, curr) => sum + curr, 0))/data.length;
    var varianceTotal = 0;
    var variance = 0;

    for (let i=0; i<data.length; i++) {
        varianceTotal += Math.pow(data[i]-mean, 2);
    }

    variance = (varianceTotal/data.length).toFixed(2);

    return variance;
}

function getGraphs() {
    fetch('/get-data')
        .then(res => res.json())
        .then(data => (randomTest(data)));
}

var random;
var geminiOutput;
const phoneGraph = document.getElementById('phoneCheck').getContext('2d');
const geminiSummary1 = document.getElementById('geminiSummary1');
const eyeGraph = document.getElementById('eyePan').getContext('2d');
const eyeVariance = document.getElementById('eyePanVariance');
const geminiSummary2 = document.getElementById('geminiSummary2');
const tiltGraph = document.getElementById('headTilt').getContext('2d');
const tiltVariance = document.getElementById('headTiltVariance');
const geminiSummary3 = document.getElementById('geminiSummary3');
var myChart1;
var myChart2;
var myChart3;

