// Fetch and display Net Worth (Assets vs Liabilities)
fetch('/net_worth')
    .then(response => response.json())
    .then(data => {
        document.getElementById('net-worth').innerText = `Net Worth: $${data.net_worth}`;
        createNetWorthChart(data.total_assets, data.total_liabilities);  // Create chart for assets vs liabilities
    });

// Fetch and display total monthly income and spending
fetch('/monthly_income_spending')
    .then(response => response.json())
    .then(data => {
        createIncomeVsSpendingChart(data.total_income, data.total_spending);  // Create chart for income vs spending
    });

// Fetch and display all assets
fetch('/assets')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#assets-table tbody');
        tableBody.innerHTML = "";  // Clear table before rendering
        data.forEach(asset => {
            const row = `<tr>
                            <td>${asset.id}</td>
                            <td>${asset.name}</td>
                            <td>${asset.value}</td>
                            <td>${asset.type}</td>
                            <td><button onclick="deleteAsset(${asset.id})">Delete</button></td>
                        </tr>`;
            tableBody.innerHTML += row;
        });
    })
    .catch((error) => console.error('Error fetching assets:', error));

// Function to send a DELETE request to the backend
function deleteAsset(assetId) {
    if (confirm('Are you sure you want to delete this asset?')) {
        fetch(`/assets/${assetId}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload();  // Reload the page to refresh the table after deletion
        })
        .catch(error => console.error('Error deleting asset:', error));
    }
}


// Fetch and display all liabilities
fetch('/liabilities')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.querySelector('#liabilities-table tbody');
        tableBody.innerHTML = "";  // Clear table before rendering
        data.forEach(liability => {
            const row = `
                <tr>
                    <td>${liability.id}</td>
                    <td>${liability.name}</td>
                    <td>${liability.value}</td>
                    <td>${liability.type}</td>
                    <td><button class="delete-liability-btn" data-id="${liability.id}">Delete</button></td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });

        // Add event listeners to each delete button
        document.querySelectorAll('.delete-liability-btn').forEach(button => {
            button.addEventListener('click', function() {
                const liabilityId = this.getAttribute('data-id');
                deleteLiability(liabilityId);
            });
        });
    })
    .catch((error) => console.error('Error fetching liabilities:', error));

// Function to delete a liability by ID
function deleteLiability(liabilityId) {
    fetch(`/liabilities/${liabilityId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();  // Reload the page to reflect the deletion
    })
    .catch((error) => console.error('Error deleting liability:', error));
}




// Function to create a pie chart for Net Worth (Assets vs Liabilities)
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

// Function to create a pie chart for Income vs Spending
function createIncomeVsSpendingChart(totalIncome, totalSpending) {
    const ctx = document.getElementById('incomeSpendingChart').getContext('2d');
    const incomeSpendingChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Income', 'Spending'],
            datasets: [{
                label: 'Income vs Spending',
                data: [totalIncome, totalSpending],
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

// Handle form submissions for adding monthly income
document.getElementById('add-income-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const incomeAmount = parseFloat(document.getElementById('income-amount').value);

    fetch('/monthly_income', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            amount: incomeAmount
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchIncomeVsSpending();  // Update the pie chart
    })
    .catch((error) => console.error('Error:', error));
});

// Handle form submissions for adding an asset
document.getElementById('add-asset-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const assetName = document.getElementById('asset-name').value;
    const assetValue = parseFloat(document.getElementById('asset-value').value);
    const assetType = document.getElementById('asset-type').value;

    fetch('/assets', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: assetName,
            value: assetValue,
            asset_type: assetType
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();  // Reload the page to refresh the data
    })
    .catch((error) => console.error('Error:', error));
});

// Handle form submissions for adding a liability
document.getElementById('add-liability-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const liabilityName = document.getElementById('liability-name').value;
    const liabilityValue = parseFloat(document.getElementById('liability-value').value);
    const liabilityType = document.getElementById('liability-type').value;

    fetch('/liabilities', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: liabilityName,
            value: liabilityValue,
            liability_type: liabilityType
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        location.reload();  // Reload the page to refresh the data
    })
    .catch((error) => console.error('Error:', error));
});


// Handle form submissions for adding monthly spending
document.getElementById('add-monthly-spending-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const spendingCategory = document.getElementById('monthly-spending-category').value;
    const spendingAmount = parseFloat(document.getElementById('monthly-spending-amount').value);

    fetch('/monthly_spending', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            category: spendingCategory,
            amount: spendingAmount
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchIncomeVsSpending();  // Update the pie chart
    })
    .catch((error) => console.error('Error:', error));
});
