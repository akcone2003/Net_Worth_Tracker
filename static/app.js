// Fetch and display Net Worth
fetch('/net_worth')
    .then(response => response.json())
    .then(data => {
        document.getElementById('net-worth').innerText = `Net Worth: $${data.net_worth}`;
        createNetWorthChart(data.total_assets, data.total_liabilities);  // Create chart for assets vs liabilities
    });

// Fetch and display all assets
fetch('/assets')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#assets-table tbody');
        data.forEach(asset => {
            const row = `<tr>
                            <td>${asset.id}</td>
                            <td>${asset.name}</td>
                            <td>${asset.value}</td>
                            <td>${asset.type}</td>
                        </tr>`;
            tableBody.innerHTML += row;
        });
    });

// Fetch and display all liabilities
fetch('/liabilities')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#liabilities-table tbody');
        data.forEach(liability => {
            const row = `<tr>
                            <td>${liability.id}</td>
                            <td>${liability.name}</td>
                            <td>${liability.value}</td>
                            <td>${liability.type}</td>
                        </tr>`;
            tableBody.innerHTML += row;
        });
    });

// Fetch and display all spending
fetch('/spending')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#spending-table tbody');
        data.forEach(spend => {
            const row = `<tr>
                            <td>${spend.id}</td>
                            <td>${spend.category}</td>
                            <td>${spend.amount}</td>
                            <td>${spend.date}</td>
                        </tr>`;
            tableBody.innerHTML += row;
        });
    });

// Function to create a pie chart for assets and liabilities
function createNetWorthChart(totalAssets, totalLiabilities) {
    const ctx = document.getElementById('netWorthChart').getContext('2d');
    const netWorthChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Assets', 'Liabilities'],
            datasets: [{
                label: 'Assets vs Liabilities',
                data: [totalAssets, totalLiabilities],
                backgroundColor: ['#4CAF50', '#FF5252'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
}
