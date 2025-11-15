// Dashboard JavaScript for Disease Outbreak Forecasting
SciChart.SciChartSurface.configure({
    wasmUrl: "https://cdn.jsdelivr.net/npm/scichart@4.0.897/_wasm/scichart2d.wasm"
});

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
        await plotForecastChart(forecastData);

        renderDataTable(forecastData); // <-- ADD THIS NEW function call

        setupExportButton();
        
        // Load and plot climate data
        await loadClimateData(disease);
        
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
async function plotForecastChart(data) {
    // Get the chart container and clear it
    const chartDiv = document.getElementById('forecastChart');
    chartDiv.innerHTML = '';

    // Create a SciChartSurface
    const { sciChartSurface, wasmContext } = await SciChart.SciChartSurface.create(chartDiv);

    // --- Styling & Theme ---
    const gridStroke = "#e2e8f0"; // slate-200
    const axisTextColor = "#64748b"; // slate-500

    // Create X and Y Axes
    sciChartSurface.xAxes.add(new SciChart.DateTimeNumericAxis(wasmContext, {
        axisTitle: "Date",
        drawMajorGridLines: true,
        majorGridLineStyle: { stroke: gridStroke },
        tickLabelStyle: { color: axisTextColor }
    }));
    sciChartSurface.yAxes.add(new SciChart.NumericAxis(wasmContext, {
        axisTitle: "Number of Cases",
        drawMajorGridLines: true,
        majorGridLineStyle: { stroke: gridStroke },
        tickLabelStyle: { color: axisTextColor }
    }));

    // --- Data Series ---
    // SciChart requires date values as numbers (timestamps)
    const historicalDates = data.historical_dates.map(d => new Date(d).getTime());
    const forecastDates = data.forecast_dates.map(d => new Date(d).getTime());

    // Create Data Series for historical and forecast data
    const historicalSeries = new SciChart.XyDataSeries(wasmContext, {
        xValues: historicalDates,
        yValues: data.historical_cases,
        dataSeriesName: "Historical Cases"
    });

    const forecastSeries = new SciChart.XyDataSeries(wasmContext, {
        xValues: forecastDates,
        yValues: data.predicted_cases,
        dataSeriesName: "Forecasted Cases"
    });

    // --- Renderable Series (The actual lines on the chart) ---
    sciChartSurface.renderableSeries.add(new SciChart.FastLineRenderableSeries(wasmContext, {
        dataSeries: historicalSeries,
        stroke: "#0ea5e9", // sky-500
        strokeThickness: 3,
        pointMarker: new SciChart.EllipsePointMarker(wasmContext, { width: 7, height: 7, fill: "#0ea5e9", stroke: "white", strokeThickness: 1 })
    }));

    sciChartSurface.renderableSeries.add(new SciChart.FastLineRenderableSeries(wasmContext, {
        dataSeries: forecastSeries,
        stroke: "#f43f5e", // rose-500
        strokeThickness: 3,
        strokeDashArray: [10, 5],
        pointMarker: new SciChart.EllipsePointMarker(wasmContext, { width: 7, height: 7, fill: "#f43f5e", stroke: "white", strokeThickness: 1 })
    }));

    // --- Interactivity and Legends ---
    sciChartSurface.chartModifiers.add(new SciChart.LegendModifier({ showCheckboxes: false }));
    sciChartSurface.chartModifiers.add(new SciChart.ZoomPanModifier());
    sciChartSurface.chartModifiers.add(new SciChart.MouseWheelZoomModifier());
    sciChartSurface.chartModifiers.add(new SciChart.RolloverModifier({ showTooltip: true }));

    // Zoom to fit the data
    sciChartSurface.zoomExtents();
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
        
        await plotClimateChart(data); // Await the async function
        
    } catch (error) {
        console.error('Error loading climate data:', error);
    }
}

// Plot climate chart
async function plotClimateChart(data) {
    const chartDiv = document.getElementById('climateChart');
    chartDiv.innerHTML = '';
    
    const { sciChartSurface, wasmContext } = await SciChart.SciChartSurface.create(chartDiv);
    const gridStroke = "#e2e8f0";

    // --- Axes (Multi-axis setup) ---
    // X-Axis (Date)
    sciChartSurface.xAxes.add(new SciChart.DateTimeNumericAxis(wasmContext, { id: "dateAxis" }));
    
    // Y-Axis 1 (Temperature) - Aligned Left
    sciChartSurface.yAxes.add(new SciChart.NumericAxis(wasmContext, {
        id: "tempAxis",
        axisTitle: "Temperature (°C)",
        axisAlignment: SciChart.EAxisAlignment.Left,
        tickLabelStyle: { color: "#f43f5e" }
    }));

    // Y-Axis 2 (Humidity) - Aligned Right
    sciChartSurface.yAxes.add(new SciChart.NumericAxis(wasmContext, {
        id: "humidityAxis",
        axisTitle: "Humidity (%)",
        axisAlignment: SciChart.EAxisAlignment.Right,
        tickLabelStyle: { color: "#16a34a" }
    }));

    // Y-Axis 3 (Rainfall) - Aligned Right
    sciChartSurface.yAxes.add(new SciChart.NumericAxis(wasmContext, {
        id: "rainfallAxis",
        axisTitle: "Rainfall (mm)",
        axisAlignment: SciChart.EAxisAlignment.Right,
        growBy: new SciChart.NumberRange(0.1, 0.1), // Add some padding
        tickLabelStyle: { color: "#3b82f6" }
    }));

    // --- Data Series ---
    const climateDates = data.dates.map(d => new Date(d).getTime());
    
    const tempSeries = new SciChart.XyDataSeries(wasmContext, { xValues: climateDates, yValues: data.temperature, dataSeriesName: "Temperature (°C)" });
    const humiditySeries = new SciChart.XyDataSeries(wasmContext, { xValues: climateDates, yValues: data.humidity, dataSeriesName: "Humidity (%)" });
    const rainfallSeries = new SciChart.XyDataSeries(wasmContext, { xValues: climateDates, yValues: data.rainfall, dataSeriesName: "Rainfall (mm)" });

    // --- Renderable Series (linking data to axes) ---
    sciChartSurface.renderableSeries.add(new SciChart.FastLineRenderableSeries(wasmContext, {
        dataSeries: tempSeries,
        yAxisId: "tempAxis",
        stroke: "#f43f5e",
        strokeThickness: 2
    }));

    sciChartSurface.renderableSeries.add(new SciChart.FastLineRenderableSeries(wasmContext, {
        dataSeries: humiditySeries,
        yAxisId: "humidityAxis",
        stroke: "#16a34a",
        strokeThickness: 2
    }));

    sciChartSurface.renderableSeries.add(new SciChart.FastColumnRenderableSeries(wasmContext, {
        dataSeries: rainfallSeries,
        yAxisId: "rainfallAxis",
        fill: "#3b82f677", // blue-500 with some transparency
        stroke: "#3b82f6"
    }));
    
    // --- Interactivity and Legends ---
    sciChartSurface.chartModifiers.add(new SciChart.LegendModifier({ showCheckboxes: false, orientation: SciChart.ELegendOrientation.Horizontal, placement: SciChart.ELegendPlacement.TopLeft }));
    sciChartSurface.chartModifiers.add(new SciChart.ZoomPanModifier());
    sciChartSurface.chartModifiers.add(new SciChart.MouseWheelZoomModifier());

    sciChartSurface.zoomExtents();
}