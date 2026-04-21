# 🔄 FarmSight - Dynamic Features Documentation

## Overview
FarmSight now includes **dynamic location-based weather** along with multiple real-time interactive features.

---

## 🌍 **1. DYNAMIC LOCATION SELECTION** ⭐ NEW!

### What's Dynamic:
- **19 predefined agricultural locations** across India
- **Real-time weather updates** based on selected location
- **Automatic coordinate updates** for API calls
- **Persistent location memory** (saved in localStorage)

### How It Works:
1. **Select Location** from dropdown in header
2. **Weather API automatically fetches** data for new coordinates
3. **Dashboard updates** with location-specific weather
4. **Location saved** - persists after browser refresh

### Supported Locations:

#### Western India:
- Nashik, Maharashtra (20.0110, 73.7903)
- Pune, Maharashtra (18.5204, 73.8567)
- Mumbai, Maharashtra (19.0760, 72.8777)
- Jaipur, Rajasthan (26.9124, 75.7873)
- Ahmedabad, Gujarat (23.0225, 72.5714)

#### Northern India:
- Delhi (28.7041, 77.1025)
- Ludhiana, Punjab (30.9010, 75.8573)
- Karnal, Haryana (29.6857, 76.9905)
- Lucknow, UP (26.8467, 80.9462)

#### Southern India:
- Bangalore, Karnataka (12.9716, 77.5946)
- Chennai, Tamil Nadu (13.0827, 80.2707)
- Hyderabad, Telangana (17.3850, 78.4867)
- Kochi, Kerala (9.9312, 76.2673)

#### Eastern India:
- Kolkata, West Bengal (22.5726, 88.3639)
- Bhubaneswar, Odisha (20.2961, 85.8245)
- Patna, Bihar (25.5941, 85.1376)

#### North-Eastern India:
- Guwahati, Assam (26.1445, 91.7362)

#### Central India:
- Indore, MP (22.7196, 75.8577)
- Bhopal, MP (23.2599, 77.4126)

### API Integration:
```javascript
// DataManager automatically updates API calls
const url = `${API_URL}?lat=${currentLocation.lat}&lon=${currentLocation.lon}&appid=${API_KEY}`;
```

### User Experience:
1. **Select location** → Toast notification: "Location changed to [City]"
2. **Auto-refresh** → Weather data fetched for new location
3. **Farm name updates** → "[City] Region" displayed
4. **Coordinates logged** → Check console for confirmation

---

## 🌤️ **2. DYNAMIC WEATHER DATA**

### What's Dynamic:
- ✅ **Temperature** (min/max, current)
- ✅ **Rainfall** (mm per day)
- ✅ **Humidity** (percentage)
- ✅ **Wind speed** (km/h)
- ✅ **Weather condition** (Sunny, Cloudy, Rain, etc.)
- ✅ **Weather icons** (condition-based)
- ✅ **Agricultural advisories** (generated from conditions)
- ✅ **5-day live forecast** (auto-aggregated from 3-hour data)

### Data Flow:
```
Location Change → API Fetch (lat, lon) → Process Data → Update Charts → Generate Advisories
```

### Update Frequency:
- **Manual**: Click "Refresh Data" button
- **Automatic**: Every 5 minutes (when tab active)
- **Cache**: 30 minutes (reduces API calls)
- **Offline**: Falls back to static mock data

### What Gets Updated:
- Current weather card (temp, humidity, wind, rainfall)
- 5-day live forecast chart (temperature + rainfall bars)
- Weather advisory message
- Weather-based alerts

---

## 📊 **3. REAL-TIME CHART UPDATES**

### Dynamic Charts:
#### Weather Chart:
- **Updates**: When location changes or refresh clicked
- **Data**: Temperature (red line), Rainfall (blue bars)
- **Interaction**: Hover for detailed info

#### Soil Charts:
- **Updates**: When zone selected from dropdown
- **Charts**: Moisture, pH, NPK, Health Score
- **Interaction**: Real-time gauge updates

#### Market Charts:
- **Updates**: Price trend sparklines
- **Data**: 30-day historical prices
- **Interaction**: Hover for daily prices

---

## 🗺️ **4. INTERACTIVE MAP SYNCHRONIZATION**

### What's Dynamic:
- ✅ **Bi-directional sync** (Map ↔ Soil Panel)
- ✅ **Click zone** → Updates soil charts
- ✅ **Select zone dropdown** → Highlights map
- ✅ **URL hash updates** → Shareable links (#zone=Z3)
- ✅ **Auto-scroll** → Panel scrolls into view
- ✅ **Temporary highlighting** → Selected zone pulses

### User Flow:
```
Click Map Zone → Popup Appears → "View Details" → Soil Panel Updates → Charts Refresh
```

---

## 🔢 **5. REVENUE CALCULATOR (Real-time)**

### What's Dynamic:
- ✅ **Crop selection** → Updates price & area
- ✅ **Yield input** → Instant calculation
- ✅ **Formula**: Revenue = Price × Yield × Area
- ✅ **Live updates** → No button click needed
- ✅ **Formatted output** → Indian Rupee notation

### Example:
```
Crop: Wheat
Price: ₹2,150/quintal
Area: 12 acres
Yield: 15 quintals/acre
───────────────────────
Revenue: ₹3,87,000
```

### Updates on:
- Crop dropdown change
- Yield input (debounced 500ms)
- Market price data refresh

---

## 🔔 **6. SMART ALERT GENERATION**

### What's Dynamic:
- ✅ **Auto-generated** from multiple data sources
- ✅ **Priority sorting** (Critical → Warning → Info → Success)
- ✅ **Real-time updates** (every 5 minutes)
- ✅ **Dismissible** (individual or all)
- ✅ **Timestamp tracking** (relative time)

### Alert Sources:
1. **Soil Data**: Critical moisture, pH issues
2. **Crop Health**: Low health scores
3. **Weather**: Rain, storms, extreme temps
4. **Market**: High prices above MSP
5. **Timeline**: Upcoming activities

### Dynamic Rules:
```javascript
// Example: Soil moisture alert
if (moisture_percent < 30) {
    alert = {
        type: 'critical',
        message: 'URGENT: Irrigation required',
        zone: zoneId
    }
}
```

---

## ⚡ **7. DATA REFRESH SYSTEM**

### What Happens on Refresh:

#### 1. Weather Data:
- Attempts API fetch for current location
- Falls back to cached data (< 30 min old)
- Final fallback: Static mock data

#### 2. Soil Data:
- Updates selected zone charts
- Recalculates health scores
- Regenerates recommendations

#### 3. Map:
- Updates zone colors
- Refreshes popup content
- Redraws polygons

#### 4. Alerts:
- Regenerates all alerts
- Re-sorts by priority
- Updates timestamps

#### 5. Market:
- Refreshes price trends
- Updates MSP comparisons
- Recalculates revenue

### Refresh Triggers:
- **Manual**: "Refresh Data" button
- **Location change**: Automatic refresh
- **Auto-refresh**: Every 5 minutes
- **Tab focus**: If inactive > 5 minutes
- **Keyboard**: `Ctrl/Cmd + R`

---

## 💾 **8. LOCAL STORAGE (Persistent Data)**

### What's Saved:
```javascript
localStorage:
  - farm_location: { name, lat, lon, region }
  - weather_cache: { data, timestamp }
```

### Benefits:
- ✅ **Location persists** after browser close
- ✅ **Weather cached** for 30 minutes
- ✅ **Reduces API calls** (respects rate limits)
- ✅ **Faster loading** (uses cache first)

### Storage Management:
- **Auto-cleanup**: Old cache cleared on refresh
- **Clear cache**: On location change
- **Size**: ~5-10 KB total
- **Privacy**: Client-side only

---

## 🎯 **9. USER INPUT INTERACTIONS**

### Dynamic Controls:

#### Zone Selector (Soil Panel):
```
Change → Fetch zone data → Update 4 charts → Update status badges → Show recommendations
```

#### Crop Selector (Timeline):
```
Change → Load timeline → Render stages → Show progress → Display next activity
```

#### Weather Source:
```
Auto → Tries API, falls back
API Only → Forces API attempt (no static fallback)
Static → Uses embedded data
```

#### Location Selector:
```
Change → Update coordinates → Clear cache → Fetch weather → Refresh dashboard
```

---

## 📱 **10. RESPONSIVE UPDATES**

### What Adapts:
- ✅ **Chart sizes** → Resize on window change
- ✅ **Map view** → Invalidates size on resize
- ✅ **Layout grid** → Desktop/Tablet/Mobile
- ✅ **Touch events** → Mobile-friendly
- ✅ **Dropdown widths** → Full width on mobile

### Debounced Events:
- Window resize: 250ms debounce
- Yield input: 500ms debounce
- Prevents excessive re-renders

---

## 🔍 **WHAT'S DYNAMIC VS STATIC**

### ✅ Dynamic (Changes Based on User Input/Location/Time):
1. **Weather data** → Location-based API
2. **Location selection** → 19 Indian cities
3. **Zone selection** → 4 farm zones
4. **Crop timeline** → 2 crops (Wheat, Chickpea)
5. **Revenue calculation** → User inputs
6. **Alert generation** → Data-driven rules
7. **Map interactions** → Click/hover events
8. **Chart updates** → Selection changes
9. **Status indicators** → Online/Offline
10. **Cache management** → Time-based

### ❌ Static (Embedded Mock Data):
1. **Soil data** → 4 zones (pre-defined metrics)
2. **Crop data** → 3 crops with coordinates
3. **Market prices** → Historical 30-day data
4. **Timeline stages** → Complete crop lifecycle
5. **Farm profile** → Green Valley Farms
6. **Map polygons** → Fixed coordinates
7. **NPK levels** → Per-zone values
8. **Health scores** → Calculated from static data

---

## 🚀 **HOW TO TEST DYNAMIC FEATURES**

### 1. Test Location Change:
```
1. Select "Bangalore" from location dropdown
2. Check console: "Location changed to: bangalore"
3. Click "Refresh Data"
4. Verify weather updates for Bangalore
5. Check forecast temperatures
```

### 2. Test Zone Sync:
```
1. Click Zone 3 (Onion) on map
2. Verify soil panel updates to Z3
3. Check moisture shows 32% (critical)
4. Confirm red pulsing animation
```

### 3. Test Revenue Calculator:
```
1. Select "Wheat" crop
2. Enter yield: 20 quintals/acre
3. See instant update: ₹5,16,000
4. No button click needed
```

### 4. Test Cache:
```
1. Refresh data (loads from API)
2. Wait 1 minute
3. Refresh again (loads from cache)
4. Console: "→ Using cached weather data"
```

### 5. Test Offline:
```
1. Open DevTools → Network tab
2. Set to "Offline"
3. Refresh data
4. Console: "→ Using static weather data"
```

---

## 🎯 **SUMMARY: DYNAMIC CAPABILITIES**

### Real-Time Updates:
✅ Weather fetched per location (19 cities)
✅ Charts update on user interactions
✅ Revenue calculated instantly
✅ Alerts generated automatically
✅ Map syncs with selections

### API Integration:
✅ OpenWeatherMap (location-based)
✅ 30-minute smart caching
✅ Graceful offline fallback
✅ Rate limit management

### User Interactions:
✅ Location dropdown (19 options)
✅ Zone selector (4 zones)
✅ Crop selector (2 crops)
✅ Weather source (3 modes)
✅ Revenue inputs (dynamic calc)

### Data Persistence:
✅ Location saved in localStorage
✅ Weather cached for 30 minutes
✅ Survives browser refresh
✅ Auto-cleanup on changes

---

## 📝 **USAGE INSTRUCTIONS**

### Enable Full Dynamic Features:
```javascript
// 1. Get API key: https://openweathermap.org/api
// 2. Edit: js/data-manager.js
// 3. Line 354: WEATHER_API_KEY: 'your-key-here'
// 4. Refresh browser
```

### Change Location:
```
1. Click location dropdown (header, left side)
2. Select any Indian city
3. Wait for auto-refresh
4. View location-specific weather
```

### Monitor API Calls:
```
1. Open DevTools (F12)
2. Network tab
3. Filter: "forecast"
4. Watch API requests per location
```

---

🌾 **FarmSight now features dynamic, location-aware weather monitoring!** 🌾
