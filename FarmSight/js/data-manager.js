/* ═══════════════════════════════════════════════════════════════════
   FarmSight Data Manager - Static Data & API Integration
   ═══════════════════════════════════════════════════════════════════ */

// ═══════════════════════════════════════════════════════════════════
// STATIC MOCK DATA - Works 100% Offline
// ═══════════════════════════════════════════════════════════════════

const FARM_PROFILE = {
    farm_id: "FARM001",
    farm_name: "Green Valley Farms",
    location: {
        name: "Nashik, Maharashtra, India",
        coordinates: [20.0110, 73.7903],
        total_area_acres: 25.5,
        soil_type: "Black Cotton Soil (Regur)",
        water_source: "Drip Irrigation + Borewell"
    },
    owner: {
        name: "Rajesh Patil",
        phone: "+91-98765-43210",
        email: "rajesh@greenvalleyfarms.in"
    },
    current_season: "Rabi 2024",
    crops: [
        {
            crop_id: "CROP001",
            name: "Wheat (Triticum aestivum)",
            variety: "HD-2967",
            area_acres: 12,
            planting_date: "2023-11-15",
            expected_harvest: "2024-03-20",
            growth_stage: "Tillering",
            health_score: 85,
            coordinates: [[20.012, 73.788], [20.014, 73.788], [20.014, 73.792], [20.012, 73.792]]
        },
        {
            crop_id: "CROP002",
            name: "Chickpea (Gram)",
            variety: "JG-11",
            area_acres: 8.5,
            planting_date: "2023-10-25",
            expected_harvest: "2024-02-28",
            growth_stage: "Pod Formation",
            health_score: 72,
            coordinates: [[20.008, 73.790], [20.010, 73.790], [20.010, 73.794], [20.008, 73.794]]
        },
        {
            crop_id: "CROP003",
            name: "Onion",
            variety: "N-53",
            area_acres: 5,
            planting_date: "2023-12-01",
            expected_harvest: "2024-04-15",
            growth_stage: "Bulb Formation",
            health_score: 45,
            status: "critical",
            coordinates: [[20.010, 73.785], [20.012, 73.785], [20.012, 73.788], [20.010, 73.788]]
        }
    ]
};

const SOIL_DATA = {
    last_updated: "2024-01-15T08:30:00Z",
    zones: [
        {
            zone_id: "Z1",
            crop_id: "CROP001",
            moisture_percent: 68,
            ph_level: 7.2,
            nitrogen_mg_kg: 145,
            phosphorus_mg_kg: 22,
            potassium_mg_kg: 285,
            organic_carbon_percent: 0.8,
            temperature_c: 24,
            status: "optimal",
            recommendations: ["Maintain current irrigation schedule"]
        },
        {
            zone_id: "Z2",
            crop_id: "CROP002",
            moisture_percent: 55,
            ph_level: 7.8,
            nitrogen_mg_kg: 112,
            phosphorus_mg_kg: 18,
            potassium_mg_kg: 240,
            organic_carbon_percent: 0.6,
            temperature_c: 26,
            status: "monitor",
            recommendations: ["Increase irrigation frequency", "Monitor for water stress"]
        },
        {
            zone_id: "Z3",
            crop_id: "CROP003",
            moisture_percent: 32,
            ph_level: 8.1,
            nitrogen_mg_kg: 89,
            phosphorus_mg_kg: 45,
            potassium_mg_kg: 310,
            organic_carbon_percent: 0.4,
            temperature_c: 28,
            status: "critical",
            recommendations: ["URGENT: Irrigation required", "Check drip lines for blockage", "Soil pH high - consider sulfur treatment"]
        },
        {
            zone_id: "Z4",
            crop_id: "CROP001",
            moisture_percent: 72,
            ph_level: 6.9,
            nitrogen_mg_kg: 165,
            phosphorus_mg_kg: 28,
            potassium_mg_kg: 295,
            organic_carbon_percent: 1.1,
            temperature_c: 23,
            status: "optimal",
            recommendations: ["Excellent conditions", "Prepare for fertilizer application in 5 days"]
        }
    ]
};

const WEATHER_STATIC = {
    location: "Nashik, IN",
    generated_at: "2024-01-15T06:00:00Z",
    forecast: [
        { date: "2024-01-15", day: "Mon", temp_min: 14, temp_max: 28, humidity: 45, rainfall_mm: 0, condition: "Sunny", icon: "wi-day-sunny", wind_speed: 12, advisory: "Good weather for spraying" },
        { date: "2024-01-16", day: "Tue", temp_min: 15, temp_max: 29, humidity: 48, rainfall_mm: 0, condition: "Partly Cloudy", icon: "wi-day-cloudy", wind_speed: 14, advisory: "Continue regular irrigation" },
        { date: "2024-01-17", day: "Wed", temp_min: 16, temp_max: 30, humidity: 52, rainfall_mm: 0, condition: "Cloudy", icon: "wi-cloudy", wind_speed: 10, advisory: "Monitor soil moisture closely" },
        { date: "2024-01-18", day: "Thu", temp_min: 18, temp_max: 27, humidity: 75, rainfall_mm: 12, condition: "Rain", icon: "wi-rain", wind_speed: 18, advisory: "Pause irrigation - rainfall expected" },
        { date: "2024-01-19", day: "Fri", temp_min: 17, temp_max: 26, humidity: 80, rainfall_mm: 8, condition: "Light Rain", icon: "wi-showers", wind_speed: 15, advisory: "Avoid field work - muddy conditions" },
        { date: "2024-01-20", day: "Sat", temp_min: 15, temp_max: 28, humidity: 60, rainfall_mm: 2, condition: "Drizzle", icon: "wi-sprinkle", wind_speed: 11, advisory: "Resume irrigation tomorrow" },
        { date: "2024-01-21", day: "Sun", temp_min: 14, temp_max: 29, humidity: 50, rainfall_mm: 0, condition: "Clear", icon: "wi-day-sunny", wind_speed: 13, advisory: "Ideal conditions for harvesting chickpeas" }
    ],
    alerts: [
        { type: "warning", message: "Thunderstorm possible on Thursday", affected_zones: ["Z1", "Z2", "Z3", "Z4"] },
        { type: "info", message: "Optimal harvesting window: Jan 21-23", affected_zones: ["Z2"] }
    ]
};

const CROP_TIMELINE = {
    timelines: [
        {
            crop_id: "CROP001",
            crop_name: "Wheat",
            current_stage_index: 3,
            stages: [
                {
                    name: "Land Preparation",
                    start_date: "2023-11-01",
                    end_date: "2023-11-14",
                    duration_days: 14,
                    status: "completed",
                    activities: ["Ploughing", "Harrowing", "Fertilizer application"]
                },
                {
                    name: "Sowing",
                    start_date: "2023-11-15",
                    end_date: "2023-11-20",
                    duration_days: 6,
                    status: "completed",
                    activities: ["Seed treatment", "Line sowing", "Light irrigation"]
                },
                {
                    name: "Germination",
                    start_date: "2023-11-21",
                    end_date: "2023-12-05",
                    duration_days: 15,
                    status: "completed",
                    activities: ["First irrigation", "Weed monitoring"]
                },
                {
                    name: "Tillering",
                    start_date: "2023-12-06",
                    end_date: "2024-01-25",
                    duration_days: 51,
                    status: "current",
                    progress_percent: 65,
                    activities: ["Nitrogen top dressing", "Irrigation every 15 days", "Weed control"],
                    next_activity: "Second nitrogen split dose on Jan 20"
                },
                {
                    name: "Stem Elongation",
                    start_date: "2024-01-26",
                    end_date: "2024-02-15",
                    duration_days: 21,
                    status: "upcoming",
                    activities: ["Irrigation management", "Pest monitoring for aphids"]
                },
                {
                    name: "Heading/Flowering",
                    start_date: "2024-02-16",
                    end_date: "2024-03-05",
                    duration_days: 18,
                    status: "upcoming",
                    activities: ["Critical irrigation phase", "Disease monitoring"]
                },
                {
                    name: "Grain Filling",
                    start_date: "2024-03-06",
                    end_date: "2024-03-20",
                    duration_days: 15,
                    status: "upcoming",
                    activities: ["Final irrigation", "Nutrient management"]
                },
                {
                    name: "Harvest",
                    start_date: "2024-03-21",
                    end_date: "2024-03-25",
                    duration_days: 5,
                    status: "upcoming",
                    activities: ["Harvesting at 12% moisture", "Threshing", "Storage"]
                }
            ]
        },
        {
            crop_id: "CROP002",
            crop_name: "Chickpea",
            current_stage_index: 5,
            stages: [
                {
                    name: "Land Preparation",
                    start_date: "2023-10-10",
                    end_date: "2023-10-20",
                    duration_days: 11,
                    status: "completed",
                    activities: ["Deep ploughing", "Leveling"]
                },
                {
                    name: "Sowing",
                    start_date: "2023-10-25",
                    end_date: "2023-10-28",
                    duration_days: 4,
                    status: "completed",
                    activities: ["Seed treatment with Rhizobium", "Line sowing"]
                },
                {
                    name: "Vegetative Growth",
                    start_date: "2023-10-29",
                    end_date: "2023-12-10",
                    duration_days: 43,
                    status: "completed",
                    activities: ["Light irrigation", "Weed management"]
                },
                {
                    name: "Flowering",
                    start_date: "2023-12-11",
                    end_date: "2024-01-05",
                    duration_days: 26,
                    status: "completed",
                    activities: ["Critical irrigation", "Pest monitoring"]
                },
                {
                    name: "Pod Formation",
                    start_date: "2024-01-06",
                    end_date: "2024-02-10",
                    duration_days: 36,
                    status: "current",
                    progress_percent: 80,
                    activities: ["Irrigation management", "Pod borer control"],
                    next_activity: "Final irrigation on Feb 5"
                },
                {
                    name: "Maturity",
                    start_date: "2024-02-11",
                    end_date: "2024-02-25",
                    duration_days: 15,
                    status: "upcoming",
                    activities: ["Stop irrigation", "Monitor for maturity"]
                },
                {
                    name: "Harvest",
                    start_date: "2024-02-26",
                    end_date: "2024-02-28",
                    duration_days: 3,
                    status: "upcoming",
                    activities: ["Harvest when 80% pods turn brown", "Threshing", "Cleaning"]
                }
            ]
        }
    ]
};

const MARKET_PRICES = {
    commodities: [
        {
            crop_id: "CROP001",
            crop_name: "Wheat",
            variety: "HD-2967",
            current_price_quintal: 2150,
            price_unit: "INR/quintal",
            mandi: "Nashik APMC",
            last_updated: "2024-01-15T10:30:00Z",
            price_trend: "up",
            price_change_7d: "+3.5%",
            historical_30d: [
                { date: "2023-12-16", price: 2050 },
                { date: "2023-12-23", price: 2080 },
                { date: "2023-12-30", price: 2060 },
                { date: "2024-01-06", price: 2100 },
                { date: "2024-01-13", price: 2080 },
                { date: "2024-01-15", price: 2150 }
            ],
            msp: 2125,
            forecast: "Prices expected to rise 5-8% by harvest time due to lower production in neighboring states"
        },
        {
            crop_id: "CROP002",
            crop_name: "Chickpea",
            variety: "JG-11",
            current_price_quintal: 5850,
            price_unit: "INR/quintal",
            mandi: "Nashik APMC",
            last_updated: "2024-01-15T10:30:00Z",
            price_trend: "stable",
            price_change_7d: "-0.8%",
            historical_30d: [
                { date: "2023-12-16", price: 5800 },
                { date: "2023-12-23", price: 5820 },
                { date: "2023-12-30", price: 5850 },
                { date: "2024-01-06", price: 5900 },
                { date: "2024-01-13", price: 5880 },
                { date: "2024-01-15", price: 5850 }
            ],
            msp: 5230,
            forecast: "Stable demand expected, sell within next 10 days for optimal returns"
        }
    ]
};

// ═══════════════════════════════════════════════════════════════════
// OPENWEATHERMAP API CONFIGURATION
// ═══════════════════════════════════════════════════════════════════

// Predefined Agricultural Regions in India
const AGRICULTURAL_LOCATIONS = {
    'nashik': { name: 'Nashik, Maharashtra', lat: 20.0110, lon: 73.7903, region: 'Western India' },
    'pune': { name: 'Pune, Maharashtra', lat: 18.5204, lon: 73.8567, region: 'Western India' },
    'mumbai': { name: 'Mumbai, Maharashtra', lat: 19.0760, lon: 72.8777, region: 'Western India' },
    'delhi': { name: 'Delhi', lat: 28.7041, lon: 77.1025, region: 'Northern India' },
    'punjab': { name: 'Ludhiana, Punjab', lat: 30.9010, lon: 75.8573, region: 'Northern India' },
    'haryana': { name: 'Karnal, Haryana', lat: 29.6857, lon: 76.9905, region: 'Northern India' },
    'up': { name: 'Lucknow, UP', lat: 26.8467, lon: 80.9462, region: 'Northern India' },
    'bangalore': { name: 'Bangalore, Karnataka', lat: 12.9716, lon: 77.5946, region: 'Southern India' },
    'chennai': { name: 'Chennai, Tamil Nadu', lat: 13.0827, lon: 80.2707, region: 'Southern India' },
    'hyderabad': { name: 'Hyderabad, Telangana', lat: 17.3850, lon: 78.4867, region: 'Southern India' },
    'kerala': { name: 'Kochi, Kerala', lat: 9.9312, lon: 76.2673, region: 'Southern India' },
    'kolkata': { name: 'Kolkata, West Bengal', lat: 22.5726, lon: 88.3639, region: 'Eastern India' },
    'bhubaneswar': { name: 'Bhubaneswar, Odisha', lat: 20.2961, lon: 85.8245, region: 'Eastern India' },
    'patna': { name: 'Patna, Bihar', lat: 25.5941, lon: 85.1376, region: 'Eastern India' },
    'guwahati': { name: 'Guwahati, Assam', lat: 26.1445, lon: 91.7362, region: 'North-Eastern India' },
    'jaipur': { name: 'Jaipur, Rajasthan', lat: 26.9124, lon: 75.7873, region: 'Western India' },
    'ahmedabad': { name: 'Ahmedabad, Gujarat', lat: 23.0225, lon: 72.5714, region: 'Western India' },
    'indore': { name: 'Indore, MP', lat: 22.7196, lon: 75.8577, region: 'Central India' },
    'bhopal': { name: 'Bhopal, MP', lat: 23.2599, lon: 77.4126, region: 'Central India' }
};

const API_CONFIG = {
    // TO USE DYNAMIC WEATHER DATA:
    // 1. Get free API key from: https://openweathermap.org/api
    // 2. Replace 'YOUR_API_KEY_HERE' below with your actual key
    // 3. The app will automatically fetch live weather data
    
    WEATHER_API_KEY: 'YOUR_API_KEY_HERE',  // ⬅️ REPLACE THIS
    WEATHER_API_URL: 'https://api.openweathermap.org/data/2.5/forecast',
    FARM_LAT: 20.0110,  // Default: Nashik
    FARM_LON: 73.7903,  // Default: Nashik
    CACHE_DURATION: 30 * 60 * 1000  // 30 minutes in milliseconds
};

// ═══════════════════════════════════════════════════════════════════
// DATA MANAGER CLASS
// ═══════════════════════════════════════════════════════════════════

class DataManager {
    constructor() {
        this.farmProfile = FARM_PROFILE;
        this.soilData = SOIL_DATA;
        this.weatherData = WEATHER_STATIC;
        this.cropTimeline = CROP_TIMELINE;
        this.marketPrices = MARKET_PRICES;
        this.isOnline = navigator.onLine;
        this.useAPI = API_CONFIG.WEATHER_API_KEY !== 'YOUR_API_KEY_HERE';
        
        // Load saved location or use default
        this.currentLocation = this.loadSavedLocation() || {
            name: 'Nashik, Maharashtra',
            lat: API_CONFIG.FARM_LAT,
            lon: API_CONFIG.FARM_LON
        };
        
        // Listen for online/offline events
        window.addEventListener('online', () => this.updateOnlineStatus(true));
        window.addEventListener('offline', () => this.updateOnlineStatus(false));
        
        console.log('✓ Static data loaded successfully');
        console.log(`Connection: ${this.isOnline ? 'Online' : 'Offline'}`);
        console.log(`API Key configured: ${this.useAPI ? 'Yes' : 'No - Using static fallback'}`);
        console.log(`Current location: ${this.currentLocation.name} (${this.currentLocation.lat}, ${this.currentLocation.lon})`);
        console.log(`Current location: ${this.currentLocation.name} (${this.currentLocation.lat}, ${this.currentLocation.lon})`);
    }
    
    updateOnlineStatus(status) {
        this.isOnline = status;
        console.log(`Connection status changed: ${status ? 'Online' : 'Offline'}`);
        
        // Update UI indicator
        const statusEl = document.getElementById('connectionStatus');
        if (statusEl) {
            statusEl.className = 'connection-status' + (status ? '' : ' offline');
            statusEl.innerHTML = status 
                ? '<i class="fas fa-wifi"></i><span>Online Mode</span>'
                : '<i class="fas fa-wifi-slash"></i><span>Offline Mode</span>';
        }
    }
    
    // ═══════════════════════════════════════════════════════════════════
    // DYNAMIC WEATHER API INTEGRATION
    // ═══════════════════════════════════════════════════════════════════
    
    async fetchDynamicWeather() {
        if (!this.useAPI || !this.isOnline) {
            console.log('→ API key not configured or offline - using static weather data');
            return this.getStaticWeather();
        }
        
        // Check cache first
        const cached = this.getCachedWeather();
        if (cached) {
            console.log('→ Using cached weather data');
            return cached;
        }
        
        try {
            console.log(`→ Fetching live weather for ${this.currentLocation.name} from OpenWeatherMap API...`);
            const url = `${API_CONFIG.WEATHER_API_URL}?lat=${this.currentLocation.lat}&lon=${this.currentLocation.lon}&appid=${API_CONFIG.WEATHER_API_KEY}&units=metric`;
            
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`API Error: ${response.status} - ${response.statusText}`);
            }
            
            const data = await response.json();
            const processedData = this.processAPIWeatherData(data);
            
            // Cache the result
            this.cacheWeatherData(processedData);
            
            console.log('✓ Live weather data fetched successfully');
            return processedData;
            
        } catch (error) {
            console.warn('⚠ API fetch failed:', error.message);
            console.log('→ Falling back to static weather data');
            return this.getStaticWeather();
        }
    }
    
    processAPIWeatherData(apiData) {
        // Process OpenWeatherMap 5-day forecast data
        // API returns 3-hour interval forecasts, we need daily aggregates
        
        const dailyData = {};
        
        apiData.list.forEach(item => {
            const date = item.dt_txt.split(' ')[0];
            
            if (!dailyData[date]) {
                dailyData[date] = {
                    temps: [],
                    humidity: [],
                    rainfall: 0,
                    conditions: [],
                    wind: []
                };
            }
            
            dailyData[date].temps.push(item.main.temp);
            dailyData[date].humidity.push(item.main.humidity);
            dailyData[date].rainfall += (item.rain?.['3h'] || 0);
            dailyData[date].conditions.push(item.weather[0].main);
            dailyData[date].wind.push(item.wind.speed * 3.6); // Convert m/s to km/h
        });
        
        const forecast = Object.keys(dailyData).slice(0, 7).map((date, index) => {
            const day = dailyData[date];
            const condition = this.getMostCommonCondition(day.conditions);
            
            return {
                date: date,
                day: this.getDayName(date),
                temp_min: Math.round(Math.min(...day.temps)),
                temp_max: Math.round(Math.max(...day.temps)),
                humidity: Math.round(day.humidity.reduce((a, b) => a + b) / day.humidity.length),
                rainfall_mm: Math.round(day.rainfall),
                condition: condition,
                icon: this.getWeatherIcon(condition),
                wind_speed: Math.round(day.wind.reduce((a, b) => a + b) / day.wind.length),
                advisory: this.generateAdvisory(condition, day.rainfall)
            };
        });
        
        return {
            location: apiData.city.name + ', ' + apiData.city.country,
            generated_at: new Date().toISOString(),
            forecast: forecast,
            alerts: this.generateWeatherAlerts(forecast),
            source: 'api'
        };
    }
    
    getMostCommonCondition(conditions) {
        const counts = {};
        conditions.forEach(c => counts[c] = (counts[c] || 0) + 1);
        return Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
    }
    
    getWeatherIcon(condition) {
        const iconMap = {
            'Clear': 'wi-day-sunny',
            'Clouds': 'wi-cloudy',
            'Rain': 'wi-rain',
            'Drizzle': 'wi-sprinkle',
            'Thunderstorm': 'wi-thunderstorm',
            'Snow': 'wi-snow',
            'Mist': 'wi-fog',
            'Fog': 'wi-fog'
        };
        return iconMap[condition] || 'wi-day-cloudy';
    }
    
    generateAdvisory(condition, rainfall) {
        if (rainfall > 10) return "Pause irrigation - significant rainfall expected";
        if (rainfall > 5) return "Reduce irrigation - rainfall expected";
        if (condition === 'Clear') return "Good weather for field operations";
        if (condition === 'Rain') return "Avoid field work - rainy conditions";
        return "Continue regular farm operations";
    }
    
    generateWeatherAlerts(forecast) {
        const alerts = [];
        
        forecast.forEach((day, index) => {
            if (day.rainfall_mm > 15) {
                alerts.push({
                    type: "warning",
                    message: `Heavy rainfall expected on ${day.day} (${day.rainfall_mm}mm)`,
                    affected_zones: ["Z1", "Z2", "Z3", "Z4"]
                });
            }
            
            if (day.temp_max > 35) {
                alerts.push({
                    type: "warning",
                    message: `High temperature alert for ${day.day} (${day.temp_max}°C)`,
                    affected_zones: ["Z1", "Z2", "Z3", "Z4"]
                });
            }
        });
        
        return alerts;
    }
    
    getDayName(dateString) {
        const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const date = new Date(dateString);
        return days[date.getDay()];
    }
    
    cacheWeatherData(data) {
        const cache = {
            data: data,
            timestamp: Date.now()
        };
        try {
            localStorage.setItem('weather_cache', JSON.stringify(cache));
            console.log('✓ Weather data cached to localStorage');
        } catch (e) {
            console.warn('⚠ Failed to cache weather data:', e);
        }
    }
    
    getCachedWeather() {
        try {
            const cached = localStorage.getItem('weather_cache');
            if (!cached) return null;
            
            const { data, timestamp } = JSON.parse(cached);
            const age = Date.now() - timestamp;
            
            if (age < API_CONFIG.CACHE_DURATION) {
                const minutes = Math.round(age / 60000);
                console.log(`→ Cache age: ${minutes} minutes (valid for ${API_CONFIG.CACHE_DURATION / 60000} min)`);
                return data;
            } else {
                console.log('→ Cache expired');
                return null;
            }
        } catch (e) {
            console.warn('⚠ Failed to read cache:', e);
            return null;
        }
    }
    
    getStaticWeather() {
        return { ...WEATHER_STATIC, source: 'static' };
    }
    
    // ═══════════════════════════════════════════════════════════════════
    // DATA GETTERS
    // ═══════════════════════════════════════════════════════════════════
    
    getFarmProfile() {
        return this.farmProfile;
    }
    
    getSoilDataByZone(zoneId) {
        return this.soilData.zones.find(z => z.zone_id === zoneId);
    }
    
    getAllSoilZones() {
        return this.soilData.zones;
    }
    
    async getWeatherData() {
        return await this.fetchDynamicWeather();
    }
    
    getCropTimeline(cropId) {
        return this.cropTimeline.timelines.find(t => t.crop_id === cropId);
    }
    
    getMarketPrice(cropId) {
        return this.marketPrices.commodities.find(c => c.crop_id === cropId);
    }
    
    getAllMarketPrices() {
        return this.marketPrices.commodities;
    }
    
    getCropById(cropId) {
        return this.farmProfile.crops.find(c => c.crop_id === cropId);
    }
    
    getAllCrops() {
        return this.farmProfile.crops;
    }
    
    // ═══════════════════════════════════════════════════════════════════
    // LOCATION MANAGEMENT
    // ═══════════════════════════════════════════════════════════════════
    
    getAvailableLocations() {
        return AGRICULTURAL_LOCATIONS;
    }
    
    setLocation(locationKey) {
        const location = AGRICULTURAL_LOCATIONS[locationKey];
        if (!location) {
            console.warn('Invalid location key:', locationKey);
            return false;
        }
        
        this.currentLocation = {
            name: location.name,
            lat: location.lat,
            lon: location.lon,
            region: location.region
        };
        
        // Save to localStorage
        this.saveLocation();
        
        // Clear weather cache to force new fetch
        localStorage.removeItem('weather_cache');
        
        console.log(`✓ Location changed to: ${this.currentLocation.name}`);
        return true;
    }
    
    setCustomLocation(name, lat, lon) {
        // Validate coordinates
        if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
            console.warn('Invalid coordinates:', lat, lon);
            return false;
        }
        
        this.currentLocation = {
            name: name || `Custom (${lat}, ${lon})`,
            lat: parseFloat(lat),
            lon: parseFloat(lon),
            region: 'Custom'
        };
        
        // Save to localStorage
        this.saveLocation();
        
        // Clear weather cache
        localStorage.removeItem('weather_cache');
        
        console.log(`✓ Custom location set: ${this.currentLocation.name}`);
        return true;
    }
    
    getCurrentLocation() {
        return this.currentLocation;
    }
    
    saveLocation() {
        try {
            localStorage.setItem('farm_location', JSON.stringify(this.currentLocation));
        } catch (e) {
            console.warn('Failed to save location:', e);
        }
    }
    
    loadSavedLocation() {
        try {
            const saved = localStorage.getItem('farm_location');
            if (saved) {
                const location = JSON.parse(saved);
                console.log('→ Loaded saved location:', location.name);
                return location;
            }
        } catch (e) {
            console.warn('Failed to load saved location:', e);
        }
        return null;
    }
    
    // ═══════════════════════════════════════════════════════════════════
    // GENERATE DYNAMIC ALERTS
    // ═══════════════════════════════════════════════════════════════════
    
    generateAlerts() {
        const alerts = [];
        
        // Soil-based alerts
        this.soilData.zones.forEach(zone => {
            if (zone.status === 'critical') {
                const crop = this.getCropById(zone.crop_id);
                alerts.push({
                    type: 'critical',
                    message: `URGENT: ${zone.zone_id} (${crop.name}) requires immediate irrigation`,
                    timestamp: new Date().toISOString(),
                    zone: zone.zone_id,
                    icon: 'fa-exclamation-triangle'
                });
            }
            
            if (zone.moisture_percent < 40 && zone.status !== 'critical') {
                alerts.push({
                    type: 'warning',
                    message: `Low soil moisture in ${zone.zone_id} (${zone.moisture_percent}%)`,
                    timestamp: new Date().toISOString(),
                    zone: zone.zone_id,
                    icon: 'fa-droplet'
                });
            }
        });
        
        // Crop health alerts
        this.farmProfile.crops.forEach(crop => {
            if (crop.health_score < 50) {
                alerts.push({
                    type: 'critical',
                    message: `${crop.name} health score critically low (${crop.health_score}/100)`,
                    timestamp: new Date().toISOString(),
                    zone: 'Multiple',
                    icon: 'fa-heart-crack'
                });
            } else if (crop.health_score < 70) {
                alerts.push({
                    type: 'warning',
                    message: `Monitor ${crop.name} - health score declining (${crop.health_score}/100)`,
                    timestamp: new Date().toISOString(),
                    zone: 'Multiple',
                    icon: 'fa-heart-pulse'
                });
            }
        });
        
        // Market opportunity alerts
        this.marketPrices.commodities.forEach(market => {
            if (market.current_price_quintal > market.msp * 1.1) {
                alerts.push({
                    type: 'success',
                    message: `Excellent ${market.crop_name} prices: ₹${market.current_price_quintal}/quintal (${Math.round((market.current_price_quintal / market.msp - 1) * 100)}% above MSP)`,
                    timestamp: new Date().toISOString(),
                    zone: 'Market',
                    icon: 'fa-sack-dollar'
                });
            }
        });
        
        // Weather alerts from weather data
        if (this.weatherData.alerts) {
            this.weatherData.alerts.forEach(alert => {
                alerts.push({
                    type: alert.type,
                    message: alert.message,
                    timestamp: new Date().toISOString(),
                    zone: alert.affected_zones.join(', '),
                    icon: 'fa-cloud-bolt'
                });
            });
        }
        
        // Timeline alerts
        this.cropTimeline.timelines.forEach(timeline => {
            const currentStage = timeline.stages[timeline.current_stage_index];
            if (currentStage && currentStage.next_activity) {
                alerts.push({
                    type: 'info',
                    message: `${timeline.crop_name}: ${currentStage.next_activity}`,
                    timestamp: new Date().toISOString(),
                    zone: 'Farm Operations',
                    icon: 'fa-calendar-check'
                });
            }
        });
        
        return alerts.sort((a, b) => {
            const priority = { critical: 0, warning: 1, info: 2, success: 3 };
            return priority[a.type] - priority[b.type];
        });
    }
}

// ═══════════════════════════════════════════════════════════════════
// INITIALIZE DATA MANAGER
// ═══════════════════════════════════════════════════════════════════

const dataManager = new DataManager();
