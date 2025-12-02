// Dashboard JavaScript for Disease Outbreak Forecasting
//

// Configure SciChart to load WASM correctly
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

// --- CORE DATA LOADING ---

async function loadCurrentStatus() {
    try {
        const response = await fetch('/api/current_status');
        const data = await response.json();
        
        const statusGrid = document.getElementById('statusGrid');
        statusGrid.innerHTML = ''; // Clear skeletons
        
        data.forEach(disease => {
            const card = createStatusCard(disease);
            statusGrid.appendChild(card);
        });
        
        updateAlertBanner(data);
        
    } catch (error) {
        console.error('Error loading current status:', error);
        const banner = document.getElementById('alertBanner');
        if(banner) banner.innerHTML = '<div class="text-red-600 font-bold p-4">Error connecting to server. Please refresh.</div>';
    }
}

function createStatusCard(disease) {
    const card = document.createElement('div');
    card.className = 'bg-white p-6 rounded-xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-slate-100 transition-all duration-300 hover:shadow-lg hover:-translate-y-1';
    
    const isIncreasing = disease.trend === 'increasing';
    const trendColor = isIncreasing ? 'red' : 'emerald';
    
    const trendIcon = isIncreasing 
        ? `<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M12 1.5a.75.75 0 01.75.75V11.25l1.97-1.97a.75.75 0 111.06 1.06l-3.25 3.25a.75.75 0 01-1.06 0L8.22 10.34a.75.75 0 111.06-1.06l1.97 1.97V2.25A.75.75 0 0112 1.5z" clip-rule="evenodd" /></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 18.5a.75.75 0 01-.75-.75V8.75L5.28 10.72a.75.75 0 01-1.06-1.06l3.25-3.25a.75.75 0 011.06 0l3.25 3.25a.75.75 0 11-1.06 1.06L9.75 8.75v9A.75.75 0 018 18.5z" clip-rule="evenodd" /></svg>`;

    card.innerHTML = `
        <h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">${disease.disease}</h3>
        <div class="flex items-baseline gap-2 mb-3">
             <p class="text-3xl font-bold text-slate-900">${disease.current_cases}</p>
             <span class="text-sm text-slate-500">cases</span>
        </div>
        <div class="flex items-center justify-between">
            <div class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-${trendColor}-50 text-${trendColor}-700 border border-${trendColor}-100">
                ${trendIcon}
                <span class="capitalize">${disease.trend}</span>
            </div>
            <span class="text-xs text-slate-400">${disease.date}</span>
        </div>
    `;
    return card;
}

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
            bgColor: 'bg-red-50 border-red-100',
            textColor: 'text-red-800',
            iconColor: 'text-red-500',
            message: `<strong>High Alert:</strong> ${criticalDisease} cases are critical (${highestCases}). Monitor closely.`
        };
    } else if (highestCases > 50) {
        alertConfig = {
            level: 'Medium',
            bgColor: 'bg-amber-50 border-amber-100',
            textColor: 'text-amber-800',
            iconColor: 'text-amber-500',
            message: `<strong>Moderate Alert:</strong> ${criticalDisease} cases have reached ${highestCases}. Stay vigilant.`
        };
    } else {
        alertConfig = {
            level: 'Low',
            bgColor: 'bg-emerald-50 border-emerald-100',
            textColor: 'text-emerald-800',
            iconColor: 'text-emerald-500',
            message: '<strong>All Clear:</strong> All diseases are currently under control.'
        };
    }

    alertBanner.className = `rounded-lg p-4 mb-8 border ${alertConfig.bgColor} transition-colors duration-300`;
    alertBanner.innerHTML = `
        <div class="flex">
            <div class="flex-shrink-0 ${alertConfig.iconColor}">
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                </svg>
            </div>
            <div class="ml-3">
                <p class="text-sm ${alertConfig.textColor}">${alertConfig.message}</p>
            </div>
        </div>
    `;
}

// --- INTERACTION ---

function setupDiseaseButtons() {
    const container = document.getElementById('diseaseButtonsContainer');
    container.addEventListener('click', function(event) {
        const button = event.target.closest('.disease-btn');
        if (!button) return;

        container.querySelectorAll('.disease-btn').forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        const disease = button.getAttribute('data-disease');
        loadDiseaseForecasts(disease);
    });
}

// --- FORECAST LOADING ---

// async function loadDiseaseForecasts(disease) {
//     currentDisease = disease;
//     document.getElementById('selectedDisease').textContent = disease;

//     const forecastChartDiv = document.getElementById('forecastChart');
//     const climateChartDiv = document.getElementById('climateChart');
//     const featureContainer = document.getElementById('featureFactorsContainer');

//     const loaderHTML = (text) => `
//         <div class="text-center text-slate-500 chart-loader py-12">
//             <svg class="animate-spin h-8 w-8 text-sky-600 mx-auto mb-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
//                 <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
//                 <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
//             </svg>
//             <p>${text}</p>
//         </div>`;

//     forecastChartDiv.innerHTML = loaderHTML(`Generating ${disease} Forecast...`);
//     climateChartDiv.innerHTML = loaderHTML("Loading Climate Data...");
//     featureContainer.innerHTML = loaderHTML("Analyzing Feature Impact...");
    
//     try {
//         const forecastResponse = await fetch(`/api/forecast/${disease}`);
//         const forecastData = await forecastResponse.json();
        
//         if (forecastData.error) throw new Error(forecastData.error);

//         currentForecastData = forecastData;
        
//         updateAlertBox(forecastData);
//         updateStatistics(forecastData);
//         renderDataTable(forecastData);
//         setupExportButton();
        
//         // Use Promise.all to load all charts in parallel
//         await Promise.all([
//             plotForecastChart(forecastData),
//             loadClimateData(disease),
//             loadFeatureFactors(disease)
//         ]);
        
//     } catch (error) {
//         console.error('Error loading forecast:', error);
//         forecastChartDiv.innerHTML = `<div class="flex items-center justify-center h-full text-red-500">Error: ${error.message}</div>`;
//     }
// }
// -- WALA CLIMATE --

async function loadDiseaseForecasts(disease) {
    currentDisease = disease;
    document.getElementById('selectedDisease').textContent = disease;

    const forecastChartDiv = document.getElementById('forecastChart');
    // [MODIFIED] Check if element exists before accessing it
    const climateChartDiv = document.getElementById('climateChart'); 
    const featureContainer = document.getElementById('featureFactorsContainer');

    const loaderHTML = (text) => `...`; // (Keep your existing loader code)

    forecastChartDiv.innerHTML = loaderHTML(`Generating ${disease} Forecast...`);
    
    // [MODIFIED] Only set loader if the element exists
    if (climateChartDiv) {
        climateChartDiv.innerHTML = loaderHTML("Loading Climate Data...");
    }
    
    featureContainer.innerHTML = loaderHTML("Analyzing Feature Impact...");
    
    try {
        const forecastResponse = await fetch(`/api/forecast/${disease}`);
        const forecastData = await forecastResponse.json();
        
        if (forecastData.error) throw new Error(forecastData.error);

        currentForecastData = forecastData;
        
        updateAlertBox(forecastData);
        updateStatistics(forecastData);
        renderDataTable(forecastData);
        setupExportButton();
        
        // [MODIFIED] Remove loadClimateData from the Promise.all array
        const tasks = [
            plotForecastChart(forecastData),
            loadFeatureFactors(disease)
        ];

        // Optional: Only add climate task if the element exists
        if (climateChartDiv) {
            tasks.push(loadClimateData(disease));
        }

        await Promise.all(tasks);
        
    } catch (error) {
        console.error('Error loading forecast:', error);
        forecastChartDiv.innerHTML = `<div class="flex items-center justify-center h-full text-red-500">Error: ${error.message}</div>`;
    }
}


// --- FEATURE IMPACT LOGIC ---

async function loadFeatureFactors(disease) {
    try {
        const response = await fetch(`/api/feature_factors/${disease}`);
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);
        
        displayFeatureFactors(data);
        
    } catch (error) {
        console.error('Error loading feature factors:', error);
        document.getElementById('featureFactorsContainer').innerHTML = 
            `<div class="text-center text-red-500 py-8"><p>Could not load impact analysis.</p></div>`;
        document.getElementById('featureTabsNav').classList.add('hidden');
    }
}

function displayFeatureFactors(data) {
    const container = document.getElementById('featureFactorsContainer');
    const tabsNav = document.getElementById('featureTabsNav');
    
    container.innerHTML = '';
    
    if (!data.categories || data.categories.length === 0) {
        container.innerHTML = '<div class="text-center text-slate-500 py-8"><p>No factor data available</p></div>';
        tabsNav.classList.add('hidden');
        return;
    }
    
    tabsNav.classList.remove('hidden');
    
    const navList = document.createElement('div');
    navList.className = 'flex gap-4';
    
    data.categories.forEach((category, index) => {
        const btn = document.createElement('button');
        const isActive = index === 0;
        btn.className = `tab-btn px-4 py-2 text-sm font-medium whitespace-nowrap border-b-2 ${isActive ? 'active border-sky-600 text-sky-700' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}`;
        btn.textContent = category.name;
        btn.onclick = () => switchTab(index, btn);
        navList.appendChild(btn);
    });
    
    tabsNav.innerHTML = '';
    tabsNav.appendChild(navList);
    
    data.categories.forEach((category, index) => {
        const panel = document.createElement('div');
        panel.className = `feature-panel fade-in-up ${index === 0 ? '' : 'hidden'}`;
        panel.setAttribute('data-index', index);
        
        let html = `<div class="grid grid-cols-1 gap-4">`;
        category.features.forEach(feature => {
            const impact = feature.impact_percentage;
            let colorClass = 'bg-slate-400';
            if(impact > 50) colorClass = 'bg-red-500';
            else if(impact > 30) colorClass = 'bg-orange-500';
            else if(impact > 15) colorClass = 'bg-amber-400';
            else if(impact > 5) colorClass = 'bg-sky-400';

            html += `
                <div class="relative pt-1">
                    <div class="flex mb-2 items-center justify-between">
                        <div>
                            <span class="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-slate-600 bg-slate-100">
                                ${feature.name}
                            </span>
                        </div>
                        <div class="text-right">
                            <span class="text-xs font-semibold inline-block text-slate-600">
                                ${impact.toFixed(1)}% Impact
                            </span>
                        </div>
                    </div>
                    <div class="overflow-hidden h-2 mb-4 text-xs flex rounded bg-slate-100">
                        <div style="width:${impact}%" class="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${colorClass}"></div>
                    </div>
                </div>
            `;
        });
        html += `</div>`;
        panel.innerHTML = html;
        container.appendChild(panel);
    });
}

function switchTab(selectedIndex, clickedBtn) {
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => {
        btn.className = 'tab-btn px-4 py-2 text-sm font-medium whitespace-nowrap border-b-2 border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300';
    });
    clickedBtn.className = 'tab-btn px-4 py-2 text-sm font-medium whitespace-nowrap border-b-2 border-sky-600 text-sky-700 active';

    const panels = document.querySelectorAll('.feature-panel');
    panels.forEach((panel, index) => {
        if(index === selectedIndex) {
            panel.classList.remove('hidden');
        } else {
            panel.classList.add('hidden');
        }
    });
}

// --- CLIMATE CHART (Fixed: Light Mode & Date Formatting) ---

async function loadClimateData(disease) {
    const chartDiv = document.getElementById('climateChart');
    try {
        const response = await fetch(`/api/climate_data/${disease}`);
        if (!response.ok) throw new Error("Failed to fetch climate data");
        
        const data = await response.json();
        if (data.error) throw new Error(data.error);
        
        chartDiv.innerHTML = ''; 
        await plotClimateChart(data); 
        
    } catch (error) {
        console.error('Error loading climate data:', error);
        chartDiv.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full text-slate-400">
                <span class="text-2xl mb-2">⚠️</span>
                <p class="text-sm">Climate data unavailable</p>
                <p class="text-xs text-slate-300 mt-1">${error.message}</p>
            </div>
        `;
    }
}

async function plotClimateChart(data) {
    const chartDiv = document.getElementById('climateChart');
    
    // FIX 1: Pass the Light theme as a NEW OBJECT, not a string
    const { sciChartSurface, wasmContext } = await SciChart.SciChartSurface.create(chartDiv, {
        theme: new SciChart.SciChartJSLightTheme()
    });
    
    sciChartSurface.background = "transparent";

    // FIX 2: DateTimeNumericAxis expects SECONDS, but JS dates are MILLISECONDS
    const xAxis = new SciChart.DateTimeNumericAxis(wasmContext, { 
        id: "dateAxis",
        axisTitle: "Date",
        labelStyle: { color: "#64748b" }, // slate-500
        majorGridLineStyle: { color: "#e2e8f0" } // slate-200
    });
    sciChartSurface.xAxes.add(xAxis);
    
    sciChartSurface.yAxes.add(new SciChart.NumericAxis(wasmContext, {
        id: "tempAxis",
        axisTitle: "Temp (°C)",
        axisAlignment: SciChart.EAxisAlignment.Left,
        labelStyle: { color: "#f43f5e" }, // Rose-500
        majorGridLineStyle: { color: "#e2e8f0" }
    }));
    
    sciChartSurface.yAxes.add(new SciChart.NumericAxis(wasmContext, {
        id: "rainAxis",
        axisTitle: "Rain (mm)",
        axisAlignment: SciChart.EAxisAlignment.Right,
        labelStyle: { color: "#0ea5e9" }, // Sky-500
        majorGridLineStyle: { strokeDashArray: [2, 2], color: "#e2e8f0" }
    }));

    // Convert Milliseconds to Seconds for SciChart
    const dates = data.dates.map(d => new Date(d).getTime() / 1000);
    
    const tempSeries = new SciChart.XyDataSeries(wasmContext, { xValues: dates, yValues: data.temperature, dataSeriesName: "Temperature" });
    const rainSeries = new SciChart.XyDataSeries(wasmContext, { xValues: dates, yValues: data.rainfall, dataSeriesName: "Rainfall" });
    
    sciChartSurface.renderableSeries.add(new SciChart.FastLineRenderableSeries(wasmContext, {
        dataSeries: tempSeries,
        yAxisId: "tempAxis",
        stroke: "#f43f5e",
        strokeThickness: 2
    }));
    
    sciChartSurface.renderableSeries.add(new SciChart.FastColumnRenderableSeries(wasmContext, {
        dataSeries: rainSeries,
        yAxisId: "rainAxis",
        fill: "rgba(14, 165, 233, 0.5)",
        stroke: "#0ea5e9"
    }));
    
    // FIX 3: Add Legend
    sciChartSurface.chartModifiers.add(new SciChart.LegendModifier({ 
        showCheckboxes: false, 
        showSeriesMarkers: true, 
        placement: SciChart.ELegendPlacement.TopLeft 
    }));
    
    sciChartSurface.zoomExtents();
}


// --- FORECAST CHART (Fixed: Light Mode & Date Formatting) ---

async function plotForecastChart(data) {
    const chartDiv = document.getElementById('forecastChart');
    chartDiv.innerHTML = '';
    
    // FIX 1: Pass the Light theme as a NEW OBJECT
    const { sciChartSurface, wasmContext } = await SciChart.SciChartSurface.create(chartDiv, {
        theme: new SciChart.SciChartJSLightTheme()
    });
    
    sciChartSurface.background = "transparent";
    
    // FIX 2: Ensure correct Axis Type
    sciChartSurface.xAxes.add(new SciChart.DateTimeNumericAxis(wasmContext, { 
        drawMajorGridLines: true, 
        majorGridLineStyle: { color: "#e2e8f0" },
        labelStyle: { color: "#64748b" },
        axisTitle: "Date"
    }));
    
    sciChartSurface.yAxes.add(new SciChart.NumericAxis(wasmContext, { 
        axisTitle: "Predicted Cases",
        drawMajorGridLines: true, 
        majorGridLineStyle: { color: "#e2e8f0" },
        labelStyle: { color: "#64748b" }
    }));

    // Convert Milliseconds to Seconds
    const forecastDates = data.forecast_dates.map(d => new Date(d).getTime() / 1000);
    const historicalDates = data.historical_dates.map(d => new Date(d).getTime() / 1000);

    const histSeries = new SciChart.XyDataSeries(wasmContext, { 
        xValues: historicalDates, 
        yValues: data.historical_cases, 
        dataSeriesName: "Historical Cases" 
    });
    
    const predSeries = new SciChart.XyDataSeries(wasmContext, { 
        xValues: forecastDates, 
        yValues: data.predicted_cases, 
        dataSeriesName: "Forecast" 
    });

    sciChartSurface.renderableSeries.add(new SciChart.FastLineRenderableSeries(wasmContext, {
        dataSeries: histSeries,
        stroke: "#0ea5e9", // Sky-500
        strokeThickness: 3
    }));

    sciChartSurface.renderableSeries.add(new SciChart.FastLineRenderableSeries(wasmContext, {
        dataSeries: predSeries,
        stroke: "#f43f5e", // Rose-500
        strokeThickness: 3,
        strokeDashArray: [5, 5]
    }));
    
    // Modifiers
    sciChartSurface.chartModifiers.add(new SciChart.ZoomPanModifier());
    sciChartSurface.chartModifiers.add(new SciChart.MouseWheelZoomModifier());
    sciChartSurface.chartModifiers.add(new SciChart.RolloverModifier({ 
        showTooltip: true, 
        tooltipColor: "#ffffff", 
        tooltipTextColor: "#1e293b" 
    }));
    
    // FIX 3: Add Legend
    sciChartSurface.chartModifiers.add(new SciChart.LegendModifier({ 
        showCheckboxes: true, 
        showSeriesMarkers: true, 
        placement: SciChart.ELegendPlacement.TopLeft 
    }));
    
    sciChartSurface.zoomExtents();
}

// --- UTILITIES ---

function updateAlertBox(data) {
    const alertBox = document.getElementById('alertBox');
    
    alertBox.style.display = 'flex';
    alertBox.className = 'rounded-lg p-4 mb-6 border-l-4 shadow-sm animate-fade-in flex items-center';
    
    let colorClass = 'border-emerald-500 bg-emerald-50';
    let icon = '✅';
    
    if (data.alert_level === 'MEDIUM') {
        colorClass = 'border-amber-500 bg-amber-50';
        icon = '⚠️';
    } else if (data.alert_level === 'HIGH') {
        colorClass = 'border-red-500 bg-red-50';
        icon = '🚨';
    }
    
    alertBox.classList.add(...colorClass.split(' '));
    alertBox.innerHTML = `
        <div class="text-2xl mr-4">${icon}</div>
        <div>
            <h3 class="font-bold text-slate-800">${data.alert_level} RISK</h3>
            <p class="text-sm text-slate-600">${data.alert_message}</p>
        </div>
    `;
}

function updateStatistics(data) {
    const dates = data.forecast_dates;
    if(dates && dates.length > 0) {
        document.getElementById('forecastPeriod').textContent = `${dates[0]} to ${dates[dates.length-1]}`;
    }
    document.getElementById('peakCases').textContent = Math.max(...data.predicted_cases);
    document.getElementById('lastUpdated').textContent = data.last_updated;
}

function renderDataTable(data) {
    const tableBody = document.getElementById('forecastDataTableBody');
    tableBody.innerHTML = '';

    if (!data.forecast_dates || data.forecast_dates.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="3" class="text-center p-6 text-slate-400">No data available.</td></tr>`;
        return;
    }

    let prev = data.historical_cases[data.historical_cases.length - 1] || 0;

    data.forecast_dates.forEach((date, i) => {
        const val = data.predicted_cases[i];
        const isUp = val > prev;
        const trend = isUp 
            ? `<span class="text-red-500 flex items-center justify-center gap-1">↗ ${val}</span>` 
            : `<span class="text-emerald-500 flex items-center justify-center gap-1">↘ ${val}</span>`;

        const row = `
            <tr class="border-b border-slate-50 hover:bg-slate-50 transition-colors">
                <td class="px-6 py-4 font-medium text-slate-700">${date}</td>
                <td class="px-6 py-4 text-right text-slate-600">${val}</td>
                <td class="px-6 py-4 text-center">${trend}</td>
            </tr>
        `;
        tableBody.insertAdjacentHTML('beforeend', row);
        prev = val;
    });
}

function setupExportButton() {
    const btn = document.getElementById('exportCsvBtn');
    if (currentForecastData) {
        btn.classList.remove('invisible');
        btn.disabled = false;
        const newBtn = btn.cloneNode(true);
        btn.parentNode.replaceChild(newBtn, btn);
        newBtn.addEventListener('click', () => {
            let csv = "data:text/csv;charset=utf-8,Date,Predicted_Cases\n";
            currentForecastData.forecast_dates.forEach((d, i) => {
                csv += `${d},${currentForecastData.predicted_cases[i]}\n`;
            });
            const link = document.createElement("a");
            link.href = encodeURI(csv);
            link.download = `${currentDisease}_forecast.csv`;
            link.click();
        });
    }
}