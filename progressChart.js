var ctx = document.getElementById('progressChart').getContext('2d');
var chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: {
            { dates } },
        datasets: [{
                label: 'Weight Progress',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                borderColor: 'rgba(0, 123, 255, 1)',
                data: {
                    { weights } },
                fill: true,
            },
            {
                label: 'Calories Consumed',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                borderColor: 'rgba(40, 167, 69, 1)',
                data: {
                    { calories_consumed } },
                fill: true,
            },
            {
                label: 'Calories Burned',
                backgroundColor: 'rgba(255, 193, 7, 0.1)',
                borderColor: 'rgba(255, 193, 7, 1)',
                data: {
                    { calories_burned } },
                fill: true,
            }
        ]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Your Progress Over Time'
        },
        scales: {
            xAxes: [{ display: true }],
            yAxes: [{ display: true }]
        }
    }
});