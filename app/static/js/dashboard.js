// Dashboard JavaScript for Disease Outbreak Forecasting

let currentDisease = null;
let currentForecastData = null;

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
}function createStatusCard(disease) {
    const card = document.createElement('div');
    // Added transition classes for smooth hover effect
    card.className = 'bg-white p-5 rounded-lg shadow-sm transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1';
    
    const isIncreasing = disease.trend === 'increasing';
    const trendColor = isIncreasing ? 'red' : 'green';
    // Using inline SVGs for icons is efficient and requires no external files.
    const trendIcon = isIncreasing 
        ? `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M12 1.5a.75.75 0 01.75.75V11.25l1.97-1.97a.75.75 0 111.06 1.06l-3.25 3.25a.75.75 0 01-1.06 0L8.22 10.34a.75.75 0 111.06-1.06l1.97 1.97V2.25A.75.75 0 0112 1.5z" clip-rule="evenodd" /></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 18.5a.75.75 0 01-.75-.75V8.75L5.28 10.72a.75.75 0 01-1.06-1.06l3.25-3.25a.75.75 0 011.06 0l3.25 3.25a.75.75 0 11-1.06 1.06L9.75 8.75v9A.75.75 0 018 18.5z" clip-rule="evenodd" /></svg>`;

    card.innerHTML = `
        <h3 class="text-md font-semibold text-slate-600">${disease.disease}</h3>
        <p class="text-3xl font-bold text-slate-900 my-1">${disease.current_cases}</p>
        <p class="text-xs text-slate-400 mb-3">cases reported on ${disease.date}</p>
        <div class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-sm font-medium bg-${trendColor}-100 text-${trendColor}-800">
            ${trendIcon}
            <span>${disease.trend}</span>
        </div>
    `;
    
    return card;
}

// Update alert banner based on current status
function updateAlertBanner(data) {
    const alertBanner = document.getElementById('alertBanner');
    
    let highestCases = 0;
    let criticalDisease = '';
    
    data.forEach(disease => {
        if (disease.current_cases > highestCases) {
            highestCases = disease.current_cases;
            criticalDisease = disease.disease;
        }
    });

    let alertConfig = {};

    if (highestCases > 100) {
        alertConfig = {
            level: 'High',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800',
            iconColor: 'text-red-400',
            icon: `<svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" /></svg>`,
            message: `<strong>High Alert:</strong> ${criticalDisease} cases are at a critical level of ${highestCases}. Monitor closely.`
        };
    } else if (highestCases > 50) {
        alertConfig = {
            level: 'Medium',
            bgColor: 'bg-yellow-100',
            textColor: 'text-yellow-800',
            iconColor: 'text-yellow-400',
            icon: `<svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8.257 3.099c.636-1.214 2.47-1.214 3.106 0l4.594 8.75c.603 1.148-.22 2.593-1.553 2.593H5.216c-1.333 0-2.156-1.445-1.553-2.593l4.594-8.75zM10 14a1 1 0 100-2 1 1 0 000 2zm-1-3a1 1 0 011-1h.008a1 1 0 011 1v1a1 1 0 01-1 1h-.008a1 1 0 01-1-1v-1z" clip-rule="evenodd" /></svg>`,
            message: `<strong>Moderate Alert:</strong> ${criticalDisease} cases have reached ${highestCases}. Stay vigilant.`
        };
    } else {
        alertConfig = {
            level: 'Low',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800',
            iconColor: 'text-green-400',
            icon: `<svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" /></svg>`,
            message: '<strong>All Clear:</strong> All diseases are currently under control. Continue routine monitoring.'
        };
    }

    alertBanner.className = `rounded-md p-4 mb-8 ${alertConfig.bgColor}`;
    alertBanner.innerHTML = `
        <div class="flex">
            <div class="flex-shrink-0 ${alertConfig.iconColor}">
                ${alertConfig.icon}
            </div>
            <div class="ml-3">
                <p class="text-sm ${alertConfig.textColor}" id="alertText">
                    ${alertConfig.message}
                </p>
            </div>
        </div>
    `;
}

function setupDiseaseButtons() {
    // The container for the buttons
    const container = document.getElementById('diseaseButtonsContainer');
    // Use event delegation for efficiency
    container.addEventListener('click', function(event) {
        // Check if a button was clicked
        const button = event.target.closest('.disease-btn');
        if (!button) return;

        // Remove active class from all buttons in the container
        container.querySelectorAll('.disease-btn').forEach(btn => btn.classList.remove('active'));
        
        // Add active class to the clicked button
        button.classList.add('active');
        
        // Load forecast for the selected disease
        const disease = button.getAttribute('data-disease');
        loadDiseaseForecasts(disease);
    });
}

// Load forecast data for a specific disease
async function loadDiseaseForecasts(disease) {
    currentDisease = disease;
    document.getElementById('selectedDisease').textContent = disease;

    // Show loading indicators for charts
    const forecastChartDiv = document.getElementById('forecastChart');
    const climateChartDiv = document.getElementById('climateChart');
    forecastChartDiv.innerHTML = `<div class="text-center text-slate-500 chart-loader"><svg class="animate-spin h-8 w-8 text-sky-600 mx-auto mb-2" ...></svg><p>Loading forecast...</p></div>`; // Use the full SVG from index.html here for brevity
    climateChartDiv.innerHTML = `<div class="text-center text-slate-500 chart-loader"><svg class="animate-spin h-8 w-8 text-sky-600 mx-auto mb-2" ...></svg><p>Loading climate data...</p></div>`;    
    try {
        // Load forecast data
        const forecastResponse = await fetch(`/api/forecast/${disease}`);
        const forecastData = await forecastResponse.json();
        
        if (forecastData.error) {
            alert(`Error: ${forecastData.error}`);
            return;
        }

        currentForecastData = forecastData;
        
        // Update alert box
        updateAlertBox(forecastData);
        
        // Update statistics
        updateStatistics(forecastData);
        
        // Plot forecast chart
        plotForecastChart(forecastData);

        renderDataTable(forecastData); // <-- ADD THIS NEW function call

        setupExportButton();
        
        // Load and plot climate data
        loadClimateData(disease);
        
    } catch (error) {
        console.error('Error loading forecast:', error);
        alert('Error loading forecast data. Please try again.');
    }
}

// ADD THIS NEW FUNCTION to render the data table
function renderDataTable(data) {
    const tableBody = document.getElementById('forecastDataTableBody');
    tableBody.innerHTML = ''; // Clear previous data

    if (!data || !data.forecast_dates || data.forecast_dates.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="3" class="text-center p-6">No forecast data available.</td></tr>`;
        return;
    }

    let previousCase = data.historical_cases[data.historical_cases.length - 1] || 0;

    data.forecast_dates.forEach((date, index) => {
        const cases = data.predicted_cases[index];
        const isIncreasing = cases > previousCase;
        const trendColor = isIncreasing ? 'text-red-500' : 'text-green-500';
        const trendIcon = isIncreasing
            ? `<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline-block" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.22 14.78a.75.75 0 001.06 0l7.22-7.22v5.69a.75.75 0 001.5 0v-7.5a.75.75 0 00-.75-.75h-7.5a.75.75 0 000 1.5h5.69l-7.22 7.22a.75.75 0 000 1.06z" clip-rule="evenodd" /></svg>`
            : `<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 inline-block" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M14.78 5.22a.75.75 0 00-1.06 0l-7.22 7.22v-5.69a.75.75 0 00-1.5 0v7.5a.75.75 0 00.75.75h7.5a.75.75 0 000-1.5h-5.69l7.22-7.22a.75.75 0 000-1.06z" clip-rule="evenodd" /></svg>`;

        const row = `
            <tr class="bg-white border-b hover:bg-slate-50">
                <td class="px-6 py-4 font-medium text-slate-900 whitespace-nowrap">${date}</td>
                <td class="px-6 py-4 text-right">${cases}</td>
                <td class="px-6 py-4 text-center ${trendColor}">
                    ${trendIcon}
                </td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
        previousCase = cases;
    });
}

// ADD THIS NEW FUNCTION to handle the export button
function setupExportButton() {
    const button = document.getElementById('exportCsvBtn');
    if (currentForecastData) {
        button.classList.remove('invisible');
        button.disabled = false;
        
        // Clone and replace to remove old event listeners
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        
        newButton.addEventListener('click', () => {
            exportDataToCSV(currentForecastData);
        });
    } else {
        button.classList.add('invisible');
        button.disabled = true;
    }
}

// ADD THIS NEW FUNCTION to generate and download the CSV
function exportDataToCSV(data) {
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Date,Predicted_Cases\n"; // Header

    data.forecast_dates.forEach((date, index) => {
        const cases = data.predicted_cases[index];
        csvContent += `${date},${cases}\n`;
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `${currentDisease}_forecast.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
    // ---> FIX: Get the container and remove loader-specific classes
    const forecastChartContainer = document.getElementById('forecastChart');
    forecastChartContainer.classList.remove('flex', 'items-center', 'justify-center');
    
    const historicalTrace = {
        x: data.historical_dates,
        y: data.historical_cases,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Historical Cases',
        line: { color: '#0ea5e9', width: 3 }, // Updated color to sky-500
        marker: { size: 6 }
    };
    
    const forecastTrace = {
        x: data.forecast_dates,
        y: data.predicted_cases,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Forecasted Cases',
        line: { color: '#f43f5e', width: 3, dash: 'dash' }, // Updated color to rose-500
        marker: { size: 8, symbol: 'diamond' }
    };
    
    const layout = {
        xaxis: { 
            title: 'Date',
            showgrid: true,
            gridcolor: '#e2e8f0' // slate-200
        },
        yaxis: { 
            title: 'Number of Cases',
            showgrid: true,
            gridcolor: '#e2e8f0' // slate-200
        },
        hovermode: 'x unified',
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: { family: 'Inter, sans-serif', size: 12, color: '#64748b' },
        title: { font: { size: 16, color: '#1e293b' }}, // slate-800
        margin: { l: 60, r: 30, t: 40, b: 60 },
        showlegend: true,
        legend: { x: 0.01, y: 0.98, bgcolor: 'rgba(255,255,255,0.6)' }
    };
    
    // The container ID is now the first argument
    Plotly.newPlot(forecastChartContainer, [historicalTrace, forecastTrace], layout, {responsive: true});
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
    // ---> FIX: Get the container and remove loader-specific classes
    const climateChartContainer = document.getElementById('climateChart');
    climateChartContainer.classList.remove('flex', 'items-center', 'justify-center');

    const temperatureTrace = {
        x: data.dates,
        y: data.temperature,
        type: 'scatter',
        mode: 'lines',
        name: 'Temperature (°C)',
        line: { color: '#f43f5e', width: 2 }, // rose-500
        yaxis: 'y'
    };
    
    const humidityTrace = {
        x: data.dates,
        y: data.humidity,
        type: 'scatter',
        mode: 'lines',
        name: 'Humidity (%)',
        line: { color: '#16a34a', width: 2 }, // green-600
        yaxis: 'y2'
    };
    
    const rainfallTrace = {
        x: data.dates,
        y: data.rainfall,
        type: 'bar',
        name: 'Rainfall (mm)',
        marker: { color: '#3b82f6' }, // blue-500
        yaxis: 'y3'
    };
    
    const layout = {
        xaxis: { 
            title: 'Date',
            domain: [0, 1]
        },
        yaxis: {
            title: 'Temp (°C)',
            titlefont: { color: '#f43f5e' },
            tickfont: { color: '#f43f5e' }
        },
        yaxis2: {
            title: 'Humidity (%)',
            titlefont: { color: '#16a34a' },
            tickfont: { color: '#16a34a' },
            overlaying: 'y',
            side: 'right'
        },
        yaxis3: {
            title: 'Rainfall (mm)',
            titlefont: { color: '#3b82f6' },
            tickfont: { color: '#3b82f6' },
            overlaying: 'y',
            side: 'right',
            anchor: 'free',
            position: 0.95,
            showgrid: false
        },
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        font: { family: 'Inter, sans-serif', size: 12, color: '#64748b' },
        title: { font: { size: 16, color: '#1e293b' }},
        margin: { l: 60, r: 120, t: 40, b: 60 }, // Increased right margin for 3rd axis
        showlegend: true,
        legend: { x: 0.01, y: 0.98, bgcolor: 'rgba(255,255,255,0.6)' }
    };
    
    // The container ID is now the first argument
    Plotly.newPlot(climateChartContainer, [temperatureTrace, humidityTrace, rainfallTrace], layout, {responsive: true});
}