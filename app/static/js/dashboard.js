// Dashboard JavaScript for Disease Outbreak Forecasting

let currentDisease = null;

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCurrentStatus();
    setupDiseaseButtons();
    
    // Update status every 5 minutes
    setInterval(loadCurrentStatus, 300000);
});

// Load current status for all diseases
async function loadCurrentStatus() {
    try {
        const response = await fetch('/api/current_status');
        const data = await response.json();
        
        const statusGrid = document.getElementById('statusGrid');
        statusGrid.innerHTML = '';
        
        data.forEach(disease => {
            const card = createStatusCard(disease);
            statusGrid.appendChild(card);
        });
        
        updateAlertBanner(data);
        
    } catch (error) {
        console.error('Error loading current status:', error);
        document.getElementById('alertBanner').innerHTML = 
            '<span style="color: red;">Error loading data. Please refresh the page.</span>';
    }
}

// Create status card for a disease
function createStatusCard(disease) {
    const card = document.createElement('div');
    card.className = 'status-card';
    
    const trendClass = disease.trend === 'increasing' ? 'increasing' : 'decreasing';
    const trendIcon = disease.trend === 'increasing' ? '📈' : '📉';
    
    card.innerHTML = `
        <h3>${disease.disease}</h3>
        <div class="cases">${disease.current_cases}</div>
        <p style="color: #666; font-size: 0.9em;">cases reported</p>
        <p style="color: #999; font-size: 0.85em; margin-top: 5px;">${disease.date}</p>
        <span class="trend ${trendClass}">${trendIcon} ${disease.trend}</span>
    `;
    
    return card;
}

// Update alert banner based on current status
function updateAlertBanner(data) {
    const alertBanner = document.getElementById('alertBanner');
    const alertText = document.getElementById('alertText');
    
    let highestCases = 0;
    let criticalDisease = '';
    
    data.forEach(disease => {
        if (disease.current_cases > highestCases) {
            highestCases = disease.current_cases;
            criticalDisease = disease.disease;
        }
    });
    
    if (highestCases > 100) {
        alertBanner.style.background = '#ff6b6b';
        alertBanner.style.color = 'white';
        alertText.textContent = `⚠️ High Alert: ${criticalDisease} cases at ${highestCases}. Monitor closely.`;
    } else if (highestCases > 50) {
        alertBanner.style.background = '#ffc107';
        alertBanner.style.color = '#333';
        alertText.textContent = `⚡ Moderate Alert: ${criticalDisease} cases at ${highestCases}. Stay vigilant.`;
    } else {
        alertBanner.style.background = '#51cf66';
        alertBanner.style.color = 'white';
        alertText.textContent = '✅ All diseases under control. Continue monitoring.';
    }
}

// Setup disease selection buttons
function setupDiseaseButtons() {
    const buttons = document.querySelectorAll('.disease-btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            buttons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Load forecast for selected disease
            const disease = this.getAttribute('data-disease');
            loadDiseaseForecasts(disease);
        });
    });
}

// Load forecast data for a specific disease
async function loadDiseaseForecasts(disease) {
    currentDisease = disease;
    document.getElementById('selectedDisease').textContent = disease;
    
    try {
        // Load forecast data
        const forecastResponse = await fetch(`/api/forecast/${disease}`);
        const forecastData = await forecastResponse.json();
        
        if (forecastData.error) {
            alert(`Error: ${forecastData.error}`);
            return;
        }
        
        // Update alert box
        updateAlertBox(forecastData);
        
        // Update statistics
        updateStatistics(forecastData);
        
        // Plot forecast chart
        plotForecastChart(forecastData);
        
        // Load and plot climate data
        loadClimateData(disease);
        
    } catch (error) {
        console.error('Error loading forecast:', error);
        alert('Error loading forecast data. Please try again.');
    }
}

// Update alert box
function updateAlertBox(data) {
    const alertBox = document.getElementById('alertBox');
    const alertLevel = document.getElementById('alertLevel');
    const alertMessage = document.getElementById('alertMessage');
    
    alertBox.style.display = 'flex';
    
    // Remove previous alert classes
    alertBox.classList.remove('medium', 'low');
    
    // Add appropriate class
    if (data.alert_level === 'MEDIUM') {
        alertBox.classList.add('medium');
    } else if (data.alert_level === 'LOW') {
        alertBox.classList.add('low');
    }
    
    alertLevel.textContent = `${data.alert_level} RISK ALERT`;
    alertMessage.textContent = data.alert_message;
}

// Update statistics cards
function updateStatistics(data) {
    const forecastPeriod = `${data.forecast_dates[0]} to ${data.forecast_dates[data.forecast_dates.length - 1]}`;
    const peakCases = Math.max(...data.predicted_cases);
    
    document.getElementById('forecastPeriod').textContent = forecastPeriod;
    document.getElementById('peakCases').textContent = peakCases;
    document.getElementById('lastUpdated').textContent = data.last_updated;
}

// Plot forecast chart
function plotForecastChart(data) {
    const historicalTrace = {
        x: data.historical_dates,
        y: data.historical_cases,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Historical Cases',
        line: { color: '#667eea', width: 3 },
        marker: { size: 6 }
    };
    
    const forecastTrace = {
        x: data.forecast_dates,
        y: data.predicted_cases,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Forecasted Cases',
        line: { color: '#ff6b6b', width: 3, dash: 'dash' },
        marker: { size: 8, symbol: 'diamond' }
    };
    
    const layout = {
        xaxis: { 
            title: 'Date',
            showgrid: true,
            gridcolor: '#e0e0e0'
        },
        yaxis: { 
            title: 'Number of Cases',
            showgrid: true,
            gridcolor: '#e0e0e0'
        },
        hovermode: 'x unified',
        plot_bgcolor: '#f8f9fa',
        paper_bgcolor: 'white',
        font: { family: 'Segoe UI, sans-serif' },
        margin: { l: 60, r: 30, t: 30, b: 60 },
        showlegend: true,
        legend: { x: 0.02, y: 0.98 }
    };
    
    Plotly.newPlot('forecastChart', [historicalTrace, forecastTrace], layout, {responsive: true});
}

// Load and plot climate data
async function loadClimateData(disease) {
    try {
        const response = await fetch(`/api/climate_data/${disease}`);
        const data = await response.json();
        
        if (data.error) {
            console.error('Climate data error:', data.error);
            return;
        }
        
        plotClimateChart(data);
        
    } catch (error) {
        console.error('Error loading climate data:', error);
    }
}

// Plot climate chart
function plotClimateChart(data) {
    const temperatureTrace = {
        x: data.dates,
        y: data.temperature,
        type: 'scatter',
        mode: 'lines',
        name: 'Temperature (°C)',
        line: { color: '#ff6b6b', width: 2 },
        yaxis: 'y'
    };
    
    const humidityTrace = {
        x: data.dates,
        y: data.humidity,
        type: 'scatter',
        mode: 'lines',
        name: 'Humidity (%)',
        line: { color: '#51cf66', width: 2 },
        yaxis: 'y2'
    };
    
    const rainfallTrace = {
        x: data.dates,
        y: data.rainfall,
        type: 'bar',
        name: 'Rainfall (mm)',
        marker: { color: '#339af0' },
        yaxis: 'y3'
    };
    
    const layout = {
        xaxis: { 
            title: 'Date',
            domain: [0, 1]
        },
        yaxis: {
            title: 'Temperature (°C)',
            titlefont: { color: '#ff6b6b' },
            tickfont: { color: '#ff6b6b' }
        },
        yaxis2: {
            title: 'Humidity (%)',
            titlefont: { color: '#51cf66' },
            tickfont: { color: '#51cf66' },
            overlaying: 'y',
            side: 'right'
        },
        yaxis3: {
            title: 'Rainfall (mm)',
            titlefont: { color: '#339af0' },
            tickfont: { color: '#339af0' },
            overlaying: 'y',
            side: 'right',
            anchor: 'free',
            position: 0.95
        },
        plot_bgcolor: '#f8f9fa',
        paper_bgcolor: 'white',
        font: { family: 'Segoe UI, sans-serif' },
        margin: { l: 60, r: 100, t: 30, b: 60 },
        showlegend: true,
        legend: { x: 0.02, y: 0.98 }
    };
    
    Plotly.newPlot('climateChart', [temperatureTrace, humidityTrace, rainfallTrace], layout, {responsive: true});
}
