function randomTest(data) {
    // data.dataInfo.forEach((dataPoint, index) => {
    //     console.log(`${index+1}: ${dataPoint}`);
    // });
    dataArray = [...data.left_pan];
    const dataArrayString = dataArray.join("&").replaceAll(".", "d");
    console.log(dataArrayString);
    const xLabels = [];
    for (let i = 0; i < dataArray.length; i++) {
        xLabels.push(i);
    }
    
    if (myChart) {
        myChart.destroy();
    }
    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: xLabels,
            datasets: [{
                label: 'Sales',
                data: dataArray,
                borderColor: 'rgba(0, 123, 255, 1)',  // Bootstrap primary
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                tension: 0.3,  // smooth lines
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    fetch(`/get-gemini/${dataArrayString}`)
        .then(res => res.json())
        .then(data => {outputGemini(data)});
    
}

function outputGemini(data) {
    geminiOutput = data;
    geminiSummary.innerHTML = `${geminiOutput.output}`;
    // console.log(`${geminiOutput.output}`);
}

function getGraphs() {
    fetch('/get-data')
        .then(res => res.json())
        .then(data => (randomTest(data)));
}

var random;
var dataArray;
var geminiOutput;
const ctx = document.getElementById('myLineChart').getContext('2d');
const geminiSummary = document.getElementById('geminiSummary');
var myChart;
