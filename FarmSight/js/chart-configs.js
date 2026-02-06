/* ═══════════════════════════════════════════════════════════════════
   FarmSight Chart Configurations - All Visualizations
   ═══════════════════════════════════════════════════════════════════ */

// ═══════════════════════════════════════════════════════════════════
// CHART COLOR SCHEMES
// ═══════════════════════════════════════════════════════════════════

const CHART_COLORS = {
    primary: '#2E7D32',
    light: '#4CAF50',
    dark: '#1B5E20',
    warning: '#F9A825',
    danger: '#C62828',
    info: '#0288D1',
    gray: '#78909C',
    
    // Soil moisture zones
    moistureCritical: '#C62828',
    moistureLow: '#F9A825',
    moistureOptimal: '#4CAF50',
    moistureHigh: '#0288D1',
    
    // pH zones
    phAcidic: '#FF6F00',
    phOptimal: '#4CAF50',
    phAlkaline: '#7B1FA2',
    
    // Temperature
    tempCool: '#0288D1',
    tempWarm: '#F9A825',
    tempHot: '#C62828'
};

// ═══════════════════════════════════════════════════════════════════
// WEATHER CHART (Dual-Axis: Temperature + Rainfall)
// ═══════════════════════════════════════════════════════════════════

let weatherChart = null;

function createWeatherChart(weatherData) {
    const ctx = document.getElementById('weatherChart');
    if (!ctx) return;
    
    // Destroy existing chart
    if (weatherChart) {
        weatherChart.destroy();
    }
    
    const forecast = weatherData.forecast;
    
    weatherChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: forecast.map(d => d.day),
            datasets: [
                {
                    label: 'Max Temp (°C)',
                    data: forecast.map(d => d.temp_max),
                    borderColor: '#E53935',
                    backgroundColor: 'rgba(229, 57, 53, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: '#E53935',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                },
                {
                    label: 'Min Temp (°C)',
                    data: forecast.map(d => d.temp_min),
                    borderColor: '#1E88E5',
                    backgroundColor: 'rgba(30, 136, 229, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    yAxisID: 'y',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    pointBackgroundColor: '#1E88E5',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                },
                {
                    label: 'Rainfall (mm)',
                    data: forecast.map(d => d.rainfall_mm),
                    type: 'bar',
                    backgroundColor: 'rgba(2, 136, 209, 0.6)',
                    borderColor: '#0288D1',
                    borderWidth: 2,
                    yAxisID: 'y1',
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: {
                            size: 12,
                            family: 'Nunito'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        title: function(context) {
                            const index = context[0].dataIndex;
                            return forecast[index].date + ' (' + forecast[index].day + ')';
                        },
                        afterBody: function(context) {
                            const index = context[0].dataIndex;
                            return [
                                '',
                                'Condition: ' + forecast[index].condition,
                                'Humidity: ' + forecast[index].humidity + '%',
                                'Wind: ' + forecast[index].wind_speed + ' km/h'
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Temperature (°C)',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y1: {
                    type: 'linear',
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Rainfall (mm)',
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        drawOnChartArea: false
                    },
                    beginAtZero: true
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
    
    console.log('✓ Weather chart created');
}

// ═══════════════════════════════════════════════════════════════════
// SOIL HEALTH CHARTS (Donut/Gauge Charts)
// ═══════════════════════════════════════════════════════════════════

let moistureChart = null;
let phChart = null;
let healthChart = null;

function createMoistureChart(value) {
    const ctx = document.getElementById('moistureChart');
    if (!ctx) return;
    
    if (moistureChart) moistureChart.destroy();
    
    const color = value < 30 ? CHART_COLORS.moistureCritical :
                  value < 50 ? CHART_COLORS.moistureLow :
                  value < 80 ? CHART_COLORS.moistureOptimal :
                  CHART_COLORS.moistureHigh;
    
    moistureChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, 100 - value],
                backgroundColor: [color, '#F5F5F5'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

function createPhChart(value) {
    const ctx = document.getElementById('phChart');
    if (!ctx) return;
    
    if (phChart) phChart.destroy();
    
    // pH color coding
    const color = value < 6.5 ? CHART_COLORS.phAcidic :
                  value <= 7.5 ? CHART_COLORS.phOptimal :
                  CHART_COLORS.phAlkaline;
    
    // Normalize to 0-100 scale (pH 0-14 -> 0-100)
    const normalizedValue = (value / 14) * 100;
    
    phChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [normalizedValue, 100 - normalizedValue],
                backgroundColor: [color, '#F5F5F5'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

function createHealthChart(value) {
    const ctx = document.getElementById('healthChart');
    if (!ctx) return;
    
    if (healthChart) healthChart.destroy();
    
    const color = value < 50 ? CHART_COLORS.danger :
                  value < 70 ? CHART_COLORS.warning :
                  CHART_COLORS.primary;
    
    healthChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, 100 - value],
                backgroundColor: [color, '#F5F5F5'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

// ═══════════════════════════════════════════════════════════════════
// NPK BAR CHART UPDATER
// ═══════════════════════════════════════════════════════════════════

function updateNPKBars(nitrogen, phosphorus, potassium) {
    // Update values
    document.getElementById('nValue').textContent = nitrogen;
    document.getElementById('pValue').textContent = phosphorus;
    document.getElementById('kValue').textContent = potassium;
    
    // Update bar widths (assuming max values: N=200, P=50, K=400)
    const nPercent = Math.min((nitrogen / 200) * 100, 100);
    const pPercent = Math.min((phosphorus / 50) * 100, 100);
    const kPercent = Math.min((potassium / 400) * 100, 100);
    
    document.getElementById('nBar').style.width = nPercent + '%';
    document.getElementById('pBar').style.width = pPercent + '%';
    document.getElementById('kBar').style.width = kPercent + '%';
}

// ═══════════════════════════════════════════════════════════════════
// MARKET PRICE SPARKLINE CHARTS
// ═══════════════════════════════════════════════════════════════════

let wheatPriceChart = null;
let chickpeaPriceChart = null;

function createPriceSparkline(canvasId, priceData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Destroy existing chart
    if (canvasId === 'wheatPriceChart' && wheatPriceChart) {
        wheatPriceChart.destroy();
    }
    if (canvasId === 'chickpeaPriceChart' && chickpeaPriceChart) {
        chickpeaPriceChart.destroy();
    }
    
    const prices = priceData.map(d => d.price);
    const labels = priceData.map(d => formatDate(d.date));
    
    // Determine trend color
    const firstPrice = prices[0];
    const lastPrice = prices[prices.length - 1];
    const color = lastPrice > firstPrice ? CHART_COLORS.primary : CHART_COLORS.danger;
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: prices,
                borderColor: color,
                backgroundColor: `${color}33`,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 4,
                pointBackgroundColor: color,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 8,
                    titleFont: {
                        size: 11
                    },
                    bodyFont: {
                        size: 12,
                        weight: 'bold'
                    },
                    callbacks: {
                        label: function(context) {
                            return '₹' + context.parsed.y.toLocaleString('en-IN');
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: false
                },
                y: {
                    display: false
                }
            }
        }
    });
    
    if (canvasId === 'wheatPriceChart') {
        wheatPriceChart = chart;
    } else if (canvasId === 'chickpeaPriceChart') {
        chickpeaPriceChart = chart;
    }
}

// ═══════════════════════════════════════════════════════════════════
// UPDATE ALL SOIL CHARTS
// ═══════════════════════════════════════════════════════════════════

function updateSoilCharts(zoneData) {
    // Update moisture chart
    createMoistureChart(zoneData.moisture_percent);
    document.getElementById('moistureValue').textContent = zoneData.moisture_percent;
    
    // Update pH chart
    createPhChart(zoneData.ph_level);
    document.getElementById('phValue').textContent = zoneData.ph_level.toFixed(1);
    
    // Update NPK bars
    updateNPKBars(zoneData.nitrogen_mg_kg, zoneData.phosphorus_mg_kg, zoneData.potassium_mg_kg);
    
    // Calculate overall health score
    let healthScore = 0;
    
    // Moisture contribution (30%)
    if (zoneData.moisture_percent >= 50 && zoneData.moisture_percent <= 80) {
        healthScore += 30;
    } else if (zoneData.moisture_percent >= 40 || zoneData.moisture_percent <= 85) {
        healthScore += 20;
    } else {
        healthScore += 10;
    }
    
    // pH contribution (25%)
    if (zoneData.ph_level >= 6.5 && zoneData.ph_level <= 7.5) {
        healthScore += 25;
    } else if (zoneData.ph_level >= 6.0 && zoneData.ph_level <= 8.0) {
        healthScore += 15;
    } else {
        healthScore += 5;
    }
    
    // NPK contribution (45%)
    const nScore = Math.min((zoneData.nitrogen_mg_kg / 150) * 15, 15);
    const pScore = Math.min((zoneData.phosphorus_mg_kg / 25) * 15, 15);
    const kScore = Math.min((zoneData.potassium_mg_kg / 300) * 15, 15);
    healthScore += nScore + pScore + kScore;
    
    healthScore = Math.round(healthScore);
    
    // Update health chart
    createHealthChart(healthScore);
    document.getElementById('healthValue').textContent = healthScore;
    
    // Update status badges
    updateStatusBadge('moistureStatus', zoneData.moisture_percent, 'moisture');
    updateStatusBadge('phStatus', zoneData.ph_level, 'ph');
    updateStatusBadge('healthStatus', healthScore, 'health');
    
    // Update recommendations
    const recList = document.getElementById('recommendationsList');
    if (recList) {
        recList.innerHTML = zoneData.recommendations.map(rec => `<li>${rec}</li>`).join('');
    }
    
    console.log(`✓ Soil charts updated for zone (Health: ${healthScore}%)`);
}

function updateStatusBadge(elementId, value, type) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let status, text;
    
    if (type === 'moisture') {
        if (value < 30) {
            status = 'critical';
            text = 'Critical - Irrigate';
        } else if (value < 50) {
            status = 'monitor';
            text = 'Monitor';
        } else if (value <= 80) {
            status = 'optimal';
            text = 'Optimal';
        } else {
            status = 'monitor';
            text = 'High';
        }
    } else if (type === 'ph') {
        if (value >= 6.5 && value <= 7.5) {
            status = 'optimal';
            text = 'Optimal';
        } else if (value >= 6.0 && value <= 8.0) {
            status = 'monitor';
            text = 'Monitor';
        } else {
            status = 'critical';
            text = 'Action Needed';
        }
    } else if (type === 'health') {
        if (value >= 70) {
            status = 'optimal';
            text = 'Excellent';
        } else if (value >= 50) {
            status = 'monitor';
            text = 'Good';
        } else {
            status = 'critical';
            text = 'Poor';
        }
    }
    
    element.className = 'metric-status ' + status;
    element.textContent = text;
}

// ═══════════════════════════════════════════════════════════════════
// CURRENT WEATHER UPDATE
// ═══════════════════════════════════════════════════════════════════

function updateCurrentWeather(weatherData) {
    const today = weatherData.forecast[0];
    
    // Update current weather display
    document.getElementById('currentTemp').textContent = today.temp_max;
    document.getElementById('currentHumidity').textContent = today.humidity;
    document.getElementById('currentWind').textContent = today.wind_speed;
    document.getElementById('currentRainfall').textContent = today.rainfall_mm;
    
    // Update weather icon
    const iconEl = document.getElementById('currentIcon');
    if (iconEl) {
        iconEl.className = `wi ${today.icon} current-weather-icon`;
    }
    
    // Update advisory
    const advisoryEl = document.getElementById('weatherAdvisory');
    if (advisoryEl) {
        advisoryEl.innerHTML = `
            <i class="fas fa-lightbulb"></i>
            <span>${today.advisory}</span>
        `;
    }
    
    console.log('✓ Current weather updated');
}

// ═══════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════

function formatDate(dateString) {
    const date = new Date(dateString);
    const month = date.toLocaleString('en-US', { month: 'short' });
    const day = date.getDate();
    return `${month} ${day}`;
}
