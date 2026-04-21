/* ═══════════════════════════════════════════════════════════════════
   FarmSight Main Application - Initialization & Event Handlers
   ═══════════════════════════════════════════════════════════════════ */

console.log('%c🌾 FarmSight Agricultural Dashboard', 'font-size: 24px; color: #2E7D32; font-weight: bold;');
console.log('%cInitializing...', 'font-size: 14px; color: #757575;');

// ═══════════════════════════════════════════════════════════════════
// APPLICATION STATE
// ═══════════════════════════════════════════════════════════════════

const appState = {
    currentZone: 'Z1',
    currentCrop: 'CROP001',
    weatherSource: 'auto',
    lastRefresh: null,
    isRefreshing: false
};

// ═══════════════════════════════════════════════════════════════════
// INITIALIZE APPLICATION
// ═══════════════════════════════════════════════════════════════════

async function initializeApp() {
    try {
        console.log('→ Starting application initialization');
        
        // Update farm name in header
        const farmProfile = dataManager.getFarmProfile();
        document.getElementById('farmName').textContent = farmProfile.farm_name;
        
        // Load initial data
        await loadAllData();
        
        // Initialize event listeners
        initializeEventListeners();
        
        // Set initial state
        appState.lastRefresh = new Date();
        
        console.log('✓ Application initialized successfully');
        console.log('═'.repeat(60));
        
        showToast('Dashboard loaded - Ready to use', 2000);
        
    } catch (error) {
        handleError(error, 'Initialization failed');
    }
}

// ═══════════════════════════════════════════════════════════════════
// LOAD ALL DATA
// ═══════════════════════════════════════════════════════════════════

async function loadAllData() {
    console.log('→ Loading dashboard data...');
    
    showLoading();
    
    try {
        // Load weather data (async - may use API or static)
        const weatherData = await dataManager.getWeatherData();
        updateWeatherPanel(weatherData);
        
        // Load soil data for initial zone
        updateSoilPanel(appState.currentZone);
        
        // Initialize farm map
        initializeFarmMap();
        
        // Load crop timeline
        updateTimelinePanel(appState.currentCrop);
        
        // Load market prices
        updateMarketPanel();
        
        // Load alerts
        updateAlertsPanel();
        
        hideLoading();
        
    } catch (error) {
        hideLoading();
        throw error;
    }
}

// ═══════════════════════════════════════════════════════════════════
// UPDATE WEATHER PANEL
// ═══════════════════════════════════════════════════════════════════

function updateWeatherPanel(weatherData) {
    console.log(`→ Updating weather panel (source: ${weatherData.source || 'static'})`);
    
    // Update current weather display
    updateCurrentWeather(weatherData);
    
    // Create weather chart
    createWeatherChart(weatherData);
    
    // Store in app state
    appState.weatherData = weatherData;
}

// ═══════════════════════════════════════════════════════════════════
// UPDATE SOIL PANEL
// ═══════════════════════════════════════════════════════════════════

function updateSoilPanel(zoneId) {
    console.log(`→ Updating soil panel for zone: ${zoneId}`);
    
    const zoneData = dataManager.getSoilDataByZone(zoneId);
    if (!zoneData) {
        console.warn('Zone data not found:', zoneId);
        return;
    }
    
    // Update all soil charts
    updateSoilCharts(zoneData);
    
    // Store current zone
    appState.currentZone = zoneId;
}

// ═══════════════════════════════════════════════════════════════════
// UPDATE TIMELINE PANEL
// ═══════════════════════════════════════════════════════════════════

function updateTimelinePanel(cropId) {
    console.log(`→ Updating timeline for crop: ${cropId}`);
    
    const timeline = dataManager.getCropTimeline(cropId);
    if (!timeline) {
        console.warn('Timeline not found for crop:', cropId);
        return;
    }
    
    renderTimeline(timeline);
    
    // Store current crop
    appState.currentCrop = cropId;
}

// ═══════════════════════════════════════════════════════════════════
// UPDATE MARKET PANEL
// ═══════════════════════════════════════════════════════════════════

function updateMarketPanel() {
    console.log('→ Updating market panel');
    
    updateMarketCards();
    
    // Initialize revenue calculator
    calculateRevenue();
}

// ═══════════════════════════════════════════════════════════════════
// UPDATE ALERTS PANEL
// ═══════════════════════════════════════════════════════════════════

function updateAlertsPanel() {
    console.log('→ Updating alerts panel');
    
    const alerts = dataManager.generateAlerts();
    renderAlerts(alerts);
}

// ═══════════════════════════════════════════════════════════════════
// EVENT LISTENERS
// ═══════════════════════════════════════════════════════════════════

function initializeEventListeners() {
    console.log('→ Setting up event listeners');
    
    // Location selector
    const locationSelector = document.getElementById('locationSelector');
    if (locationSelector) {
        // Set initial value from saved location
        const currentLoc = dataManager.getCurrentLocation();
        const locKey = Object.keys(dataManager.getAvailableLocations()).find(key => {
            const loc = dataManager.getAvailableLocations()[key];
            return loc.lat === currentLoc.lat && loc.lon === currentLoc.lon;
        });
        if (locKey) {
            locationSelector.value = locKey;
        }
        
        locationSelector.addEventListener('change', async (e) => {
            const locationKey = e.target.value;
            console.log('→ Location changed to:', locationKey);
            
            // Update location in data manager
            if (dataManager.setLocation(locationKey)) {
                const newLocation = dataManager.getCurrentLocation();
                showToast(`Location changed to ${newLocation.name}`, 2000);
                
                // Update farm name display
                document.getElementById('farmName').textContent = `${newLocation.name} Region`;

                // Recenter map to selected location for a consistent live demo experience
                if (typeof updateMapLocation === 'function') {
                    updateMapLocation(newLocation.lat, newLocation.lon, newLocation.name);
                }
                
                // Trigger weather refresh
                await handleRefreshData();
            }
        });
    }
    
    // Refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', handleRefreshData);
    }
    
    // Zone selector
    const zoneSelector = document.getElementById('zoneSelector');
    if (zoneSelector) {
        zoneSelector.addEventListener('change', (e) => {
            updateSoilPanel(e.target.value);
            // Update map highlight
            if (typeof highlightZone === 'function') {
                highlightZone(e.target.value);
            }
        });
    }
    
    // Crop selector (timeline)
    const cropSelector = document.getElementById('cropSelector');
    if (cropSelector) {
        cropSelector.addEventListener('change', (e) => {
            updateTimelinePanel(e.target.value);
        });
    }
    
    // Weather source selector
    const weatherSource = document.getElementById('weatherSource');
    if (weatherSource) {
        weatherSource.addEventListener('change', (e) => {
            appState.weatherSource = e.target.value;
            console.log('Weather source changed to:', e.target.value);
        });
    }
    
    // Satellite toggle button
    const toggleSatellite = document.getElementById('toggleSatellite');
    if (toggleSatellite) {
        toggleSatellite.addEventListener('click', () => {
            if (typeof toggleSatelliteView === 'function') {
                toggleSatelliteView();
            }
        });
    }
    
    // Clear alerts button
    const clearAlerts = document.getElementById('clearAlerts');
    if (clearAlerts) {
        clearAlerts.addEventListener('click', () => {
            const container = document.getElementById('alertsContainer');
            if (container) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 40px; color: #757575;">
                        <i class="fas fa-check-circle" style="font-size: 3rem; color: #4CAF50; margin-bottom: 16px;"></i>
                        <p>All alerts cleared</p>
                    </div>
                `;
                showToast('All alerts cleared', 2000);
            }
        });
    }
    
    // Revenue calculator inputs
    const revenueCrop = document.getElementById('revenueCrop');
    const expectedYield = document.getElementById('expectedYield');
    
    if (revenueCrop) {
        revenueCrop.addEventListener('change', calculateRevenue);
    }
    
    if (expectedYield) {
        expectedYield.addEventListener('input', debounce(calculateRevenue, 500));
    }
    
    // Auto-refresh every 5 minutes (for alerts and dynamic data)
    setInterval(() => {
        if (!appState.isRefreshing) {
            console.log('→ Auto-refresh triggered');
            handleRefreshData();
        }
    }, 5 * 60 * 1000); // 5 minutes
    
    console.log('✓ Event listeners initialized');
}

// ═══════════════════════════════════════════════════════════════════
// REFRESH DATA HANDLER
// ═══════════════════════════════════════════════════════════════════

async function handleRefreshData() {
    if (appState.isRefreshing) {
        console.log('⚠ Refresh already in progress');
        return;
    }
    
    appState.isRefreshing = true;
    
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.classList.add('loading');
        refreshBtn.disabled = true;
    }
    
    console.log('═'.repeat(60));
    console.log('🔄 REFRESH DATA REQUESTED');
    console.log('═'.repeat(60));
    
    showLoading();
    
    try {
        // Determine weather source based on selector
        let weatherData;
        const sourceMode = appState.weatherSource;
        
        if (sourceMode === 'static') {
            console.log('→ Using static weather data (forced)');
            weatherData = dataManager.getStaticWeather();
        } else if (sourceMode === 'api') {
            console.log('→ Attempting strict API fetch (no static fallback)');
            weatherData = await dataManager.fetchDynamicWeatherStrict();
        } else {
            // Auto mode - try API, fallback to static
            console.log('→ Auto mode - attempting API with fallback');
            weatherData = await dataManager.fetchDynamicWeather();
        }
        
        // Update weather panel
        updateWeatherPanel(weatherData);
        
        // Refresh current zone data
        updateSoilPanel(appState.currentZone);
        
        // Update map zones
        if (typeof updateMapZones === 'function') {
            updateMapZones();
        }
        
        // Refresh alerts
        updateAlertsPanel();
        
        // Update market data
        updateMarketPanel();
        
        appState.lastRefresh = new Date();
        
        hideLoading();
        
        const source = weatherData.source === 'api' ? 'live API data' : 'static data';
        showToast(`✓ Data refreshed using ${source}`, 3000);
        
        console.log('✓ Refresh completed successfully');
        console.log('═'.repeat(60));
        
    } catch (error) {
        hideLoading();
        const sourceMode = appState.weatherSource;
        if (sourceMode === 'api') {
            showToast(`API-only refresh failed: ${error.message}`, 4500);
            console.error('API-only refresh failed:', error);
        } else {
            handleError(error, 'Refresh failed');
        }
    } finally {
        appState.isRefreshing = false;
        
        if (refreshBtn) {
            refreshBtn.classList.remove('loading');
            refreshBtn.disabled = false;
        }
    }
}

// ═══════════════════════════════════════════════════════════════════
// KEYBOARD SHORTCUTS
// ═══════════════════════════════════════════════════════════════════

document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + R: Refresh data
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        handleRefreshData();
    }
    
    // Ctrl/Cmd + M: Toggle map view
    if ((e.ctrlKey || e.metaKey) && e.key === 'm') {
        e.preventDefault();
        if (typeof toggleSatelliteView === 'function') {
            toggleSatelliteView();
        }
    }
});

// ═══════════════════════════════════════════════════════════════════
// RESPONSIVE HANDLERS
// ═══════════════════════════════════════════════════════════════════

window.addEventListener('resize', debounce(() => {
    // Resize charts on window resize
    if (weatherChart) weatherChart.resize();
    if (moistureChart) moistureChart.resize();
    if (phChart) phChart.resize();
    if (healthChart) healthChart.resize();
    
    // Invalidate map size
    if (farmMap) {
        farmMap.invalidateSize();
    }
}, 250));

// ═══════════════════════════════════════════════════════════════════
// VISIBILITY CHANGE HANDLER (Tab focus)
// ═══════════════════════════════════════════════════════════════════

document.addEventListener('visibilitychange', () => {
    if (!document.hidden && appState.lastRefresh) {
        const timeSinceRefresh = Date.now() - appState.lastRefresh.getTime();
        const fiveMinutes = 5 * 60 * 1000;
        
        // Auto-refresh if tab was hidden for more than 5 minutes
        if (timeSinceRefresh > fiveMinutes) {
            console.log('→ Tab refocused after 5+ minutes - auto-refreshing');
            handleRefreshData();
        }
    }
});

// ═══════════════════════════════════════════════════════════════════
// ERROR LOGGING
// ═══════════════════════════════════════════════════════════════════

window.addEventListener('error', (e) => {
    console.error('Global error:', e.error);
    // Don't show toast for every error to avoid spam
});

window.addEventListener('unhandledrejection', (e) => {
    console.error('Unhandled promise rejection:', e.reason);
});

// ═══════════════════════════════════════════════════════════════════
// PRINT SUPPORT
// ═══════════════════════════════════════════════════════════════════

window.addEventListener('beforeprint', () => {
    console.log('→ Preparing for print...');
    // Could add print-specific optimizations here
});

// ═══════════════════════════════════════════════════════════════════
// SERVICE WORKER REGISTRATION (Future Enhancement)
// ═══════════════════════════════════════════════════════════════════

// Uncomment to add offline support with service worker
// if ('serviceWorker' in navigator) {
//     navigator.serviceWorker.register('/sw.js')
//         .then(() => console.log('✓ Service Worker registered'))
//         .catch(err => console.warn('Service Worker registration failed:', err));
// }

// ═══════════════════════════════════════════════════════════════════
// START APPLICATION WHEN DOM IS READY
// ═══════════════════════════════════════════════════════════════════

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApp);
} else {
    initializeApp();
}

// ═══════════════════════════════════════════════════════════════════
// CONSOLE INSTRUCTIONS
// ═══════════════════════════════════════════════════════════════════

setTimeout(() => {
    console.log('%c═══════════════════════════════════════════════════════', 'color: #2E7D32;');
    console.log('%c📝 DEVELOPER NOTES', 'font-size: 16px; font-weight: bold; color: #2E7D32;');
    console.log('%c═══════════════════════════════════════════════════════', 'color: #2E7D32;');
    console.log('');
    console.log('%cTO ENABLE LIVE WEATHER DATA:', 'font-weight: bold; color: #0288D1;');
    console.log('1. Get free API key: https://openweathermap.org/api');
    console.log('2. Open: js/data-manager.js');
    console.log("3. Replace 'YOUR_API_KEY_HERE' with your actual key");
    console.log('4. Refresh the page');
    console.log('');
    console.log('%cKEYBOARD SHORTCUTS:', 'font-weight: bold; color: #F9A825;');
    console.log('• Ctrl/Cmd + R: Refresh data');
    console.log('• Ctrl/Cmd + M: Toggle map view');
    console.log('');
    console.log('%cDEBUGGING:', 'font-weight: bold; color: #C62828;');
    console.log('• Check network tab for API calls');
    console.log('• All data operations are logged to console');
    console.log('• LocalStorage key: "weather_cache"');
    console.log('');
    console.log('%c═══════════════════════════════════════════════════════', 'color: #2E7D32;');
}, 1000);
