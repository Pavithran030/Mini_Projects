/**
 * ═══════════════════════════════════════════════════════════════════
 * FarmSight - OpenWeatherMap API Configuration Guide
 * ═══════════════════════════════════════════════════════════════════
 * 
 * This guide explains how to configure live weather data integration.
 * The app works 100% offline without this setup, but enabling it adds
 * real-time weather forecasting capabilities.
 */

// ═══════════════════════════════════════════════════════════════════
// STEP 1: GET YOUR FREE API KEY
// ═══════════════════════════════════════════════════════════════════

/**
 * 1. Visit: https://openweathermap.org/api
 * 2. Click "Get Started" or "Sign Up"
 * 3. Choose "Free" plan (includes 1000 API calls/day)
 * 4. Complete registration
 * 5. Check your email for verification
 * 6. Login and go to: https://home.openweathermap.org/api_keys
 * 7. Copy your default API key
 * 
 * NOTE: It may take 10-15 minutes for new keys to activate
 */

// ═══════════════════════════════════════════════════════════════════
// STEP 2: CONFIGURE THE APPLICATION
// ═══════════════════════════════════════════════════════════════════

/**
 * 1. Open: js/data-manager.js
 * 2. Find the API_CONFIG object (around line 280)
 * 3. Replace 'YOUR_API_KEY_HERE' with your actual key
 * 
 * BEFORE:
 *   const API_CONFIG = {
 *     WEATHER_API_KEY: 'YOUR_API_KEY_HERE',
 *     ...
 *   };
 * 
 * AFTER:
 *   const API_CONFIG = {
 *     WEATHER_API_KEY: 'abc123xyz789youractualkey',
 *     ...
 *   };
 * 
 * 4. Save the file
 * 5. Refresh your browser
 */

// ═══════════════════════════════════════════════════════════════════
// STEP 3: VERIFY IT'S WORKING
// ═══════════════════════════════════════════════════════════════════

/**
 * 1. Open browser DevTools (Press F12)
 * 2. Go to Console tab
 * 3. Click "Refresh Data" button in dashboard
 * 4. You should see logs like:
 * 
 *    → Fetching live weather from OpenWeatherMap API...
 *    ✓ Live weather data fetched successfully
 *    ✓ Weather data cached to localStorage
 * 
 * 5. If you see errors, check:
 *    - API key is correct (no extra spaces)
 *    - Key has been activated (wait 10-15 min after creation)
 *    - Internet connection is active
 *    - You haven't exceeded 1000 calls/day limit
 */

// ═══════════════════════════════════════════════════════════════════
// API CONFIGURATION OPTIONS
// ═══════════════════════════════════════════════════════════════════

/**
 * You can customize these settings in js/data-manager.js:
 * 
 * WEATHER_API_KEY:
 *   Your OpenWeatherMap API key
 *   Default: 'YOUR_API_KEY_HERE'
 * 
 * WEATHER_API_URL:
 *   API endpoint (don't change unless using different service)
 *   Default: 'https://api.openweathermap.org/data/2.5/forecast'
 * 
 * FARM_LAT:
 *   Your farm's latitude
 *   Default: 20.0110 (Nashik, India)
 * 
 * FARM_LON:
 *   Your farm's longitude  
 *   Default: 73.7903 (Nashik, India)
 * 
 * CACHE_DURATION:
 *   How long to cache API responses (milliseconds)
 *   Default: 30 * 60 * 1000 (30 minutes)
 *   Recommended: 30-60 minutes to avoid hitting rate limits
 */

// ═══════════════════════════════════════════════════════════════════
// EXAMPLE CONFIGURATION
// ═══════════════════════════════════════════════════════════════════

/**
 * For a farm in Pune, Maharashtra:
 * 
 * const API_CONFIG = {
 *   WEATHER_API_KEY: 'your-actual-key-here',
 *   WEATHER_API_URL: 'https://api.openweathermap.org/data/2.5/forecast',
 *   FARM_LAT: 18.5204,
 *   FARM_LON: 73.8567,
 *   CACHE_DURATION: 30 * 60 * 1000
 * };
 */

// ═══════════════════════════════════════════════════════════════════
// HOW THE FALLBACK SYSTEM WORKS
// ═══════════════════════════════════════════════════════════════════

/**
 * The app uses a smart 3-tier fallback system:
 * 
 * TIER 1: Live API Data
 *   - Attempts to fetch from OpenWeatherMap
 *   - Only if API key is configured
 *   - Only if internet is available
 *   - Respects rate limits
 * 
 * TIER 2: Cached Data
 *   - If API fails, checks localStorage
 *   - Uses cached data if < 30 minutes old
 *   - Prevents unnecessary API calls
 * 
 * TIER 3: Static Fallback
 *   - If no API key or offline
 *   - Uses embedded mock data
 *   - Guarantees app always works
 * 
 * This ensures:
 * ✓ App works 100% offline
 * ✓ No API key required for basic use
 * ✓ Live data when available
 * ✓ Graceful degradation
 */

// ═══════════════════════════════════════════════════════════════════
// RATE LIMITS & BEST PRACTICES
// ═══════════════════════════════════════════════════════════════════

/**
 * FREE PLAN LIMITS:
 * - 1000 API calls per day
 * - ~60 calls per hour (16 seconds between calls)
 * - Updates every 10 minutes
 * 
 * APP USAGE:
 * - Caches for 30 minutes by default
 * - ~48 calls per day (well within limit)
 * - Manual refresh available
 * 
 * TO OPTIMIZE:
 * 1. Increase CACHE_DURATION to 60 minutes
 * 2. Don't spam the refresh button
 * 3. Use "Static Data" mode when testing
 * 4. Monitor usage at: https://home.openweathermap.org/
 * 
 * UPGRADE OPTIONS:
 * - Startup plan: $40/month → 100,000 calls/day
 * - Developer plan: $150/month → 1,000,000 calls/day
 * - Not needed for single farm use!
 */

// ═══════════════════════════════════════════════════════════════════
// TROUBLESHOOTING
// ═══════════════════════════════════════════════════════════════════

/**
 * ERROR: "401 Unauthorized"
 * → API key is invalid or not activated yet
 * → Wait 10-15 minutes after creating key
 * → Double-check key has no extra spaces
 * 
 * ERROR: "429 Too Many Requests"  
 * → You've exceeded 1000 calls/day limit
 * → Wait 24 hours or increase CACHE_DURATION
 * → Use "Static Data" mode temporarily
 * 
 * ERROR: "Failed to fetch"
 * → Internet connection issue
 * → API endpoint is down (rare)
 * → CORS issue (shouldn't happen with OpenWeatherMap)
 * → App automatically falls back to static data
 * 
 * NO ERROR BUT USING STATIC DATA?
 * → Check: API_CONFIG.WEATHER_API_KEY !== 'YOUR_API_KEY_HERE'
 * → Check browser console for "API key not configured"
 * → Verify file was saved after editing
 * → Hard refresh browser (Ctrl+Shift+R)
 */

// ═══════════════════════════════════════════════════════════════════
// DATA FORMAT
// ═══════════════════════════════════════════════════════════════════

/**
 * OpenWeatherMap returns 40 forecast entries (5 days × 8 per day)
 * The app processes this into 7-day daily forecasts:
 * 
 * RAW API DATA:
 * {
 *   list: [
 *     { dt_txt: "2024-01-15 00:00:00", main: { temp: 20, humidity: 60 }, ... },
 *     { dt_txt: "2024-01-15 03:00:00", main: { temp: 18, humidity: 65 }, ... },
 *     ...
 *   ]
 * }
 * 
 * PROCESSED DATA:
 * {
 *   forecast: [
 *     { date: "2024-01-15", temp_min: 14, temp_max: 28, humidity: 45, ... },
 *     { date: "2024-01-16", temp_min: 15, temp_max: 29, humidity: 48, ... },
 *     ...
 *   ]
 * }
 * 
 * Processing includes:
 * - Aggregating 3-hour intervals into daily data
 * - Calculating min/max temperatures
 * - Averaging humidity readings
 * - Summing rainfall amounts
 * - Determining primary weather condition
 * - Generating agricultural advisories
 */

// ═══════════════════════════════════════════════════════════════════
// WEATHER SOURCE SELECTOR
// ═══════════════════════════════════════════════════════════════════

/**
 * The dashboard includes a dropdown to control data source:
 * 
 * AUTO MODE (Default):
 *   - Tries API if key configured
 *   - Falls back to cache/static
 *   - Best for normal use
 * 
 * API ONLY:
 *   - Forces API fetch attempt
 *   - Shows error if fails
 *   - Good for testing API key
 * 
 * STATIC DATA:
 *   - Always uses embedded mock data
 *   - Good for development/testing
 *   - Saves API calls
 * 
 * To test API integration:
 * 1. Select "API Only" mode
 * 2. Click refresh
 * 3. Check console for success/error
 * 4. Switch back to "Auto" for normal use
 */

// ═══════════════════════════════════════════════════════════════════
// SECURITY NOTES
// ═══════════════════════════════════════════════════════════════════

/**
 * ⚠️ IMPORTANT: API Key Exposure
 * 
 * Since this is a client-side app, your API key will be visible in:
 * - Browser DevTools
 * - View Source
 * - Network requests
 * 
 * THIS IS OKAY FOR:
 * ✓ Personal use
 * ✓ Internal farm dashboards
 * ✓ Free tier API keys
 * ✓ Testing and development
 * 
 * NOT RECOMMENDED FOR:
 * ✗ Public websites with high traffic
 * ✗ Paid API subscriptions
 * ✗ Shared hosting environments
 * 
 * BEST PRACTICES:
 * 1. Use domain restrictions in OpenWeatherMap dashboard
 * 2. Monitor API usage regularly
 * 3. Regenerate key if exposed publicly
 * 4. For production: Use a backend proxy
 * 
 * For production deployments with backend:
 * - Move API key to server environment variables
 * - Create proxy endpoint: /api/weather
 * - Frontend calls proxy instead of OpenWeatherMap directly
 * - Implement rate limiting on server
 */

// ═══════════════════════════════════════════════════════════════════
// ALTERNATIVE WEATHER APIS
// ═══════════════════════════════════════════════════════════════════

/**
 * While this app is configured for OpenWeatherMap, you can adapt it
 * for other weather APIs:
 * 
 * WEATHERAPI.COM:
 * - Free tier: 1M calls/month
 * - Endpoint: http://api.weatherapi.com/v1/forecast.json
 * - Similar data structure
 * 
 * TOMORROW.IO (formerly Climacell):
 * - Free tier: 500 calls/day
 * - More detailed agricultural data
 * - Higher cost for paid tiers
 * 
 * VISUAL CROSSING:
 * - Free tier: 1000 records/day
 * - Historical data available
 * - Good for analytics
 * 
 * To switch APIs:
 * 1. Get new API key
 * 2. Update API_CONFIG.WEATHER_API_URL
 * 3. Modify processAPIWeatherData() function in data-manager.js
 * 4. Map new response structure to app's format
 */

// ═══════════════════════════════════════════════════════════════════
// QUICK REFERENCE
// ═══════════════════════════════════════════════════════════════════

/**
 * FILE TO EDIT: js/data-manager.js
 * LINE TO FIND: WEATHER_API_KEY: 'YOUR_API_KEY_HERE'
 * 
 * GET API KEY: https://openweathermap.org/api
 * CHECK USAGE: https://home.openweathermap.org/
 * API DOCS: https://openweathermap.org/forecast5
 * 
 * FREE LIMIT: 1000 calls/day
 * APP USAGE: ~48 calls/day (with 30min cache)
 * CACHE TIME: 30 minutes (configurable)
 * 
 * NEED HELP? Check README.md or SETUP_GUIDE.txt
 */

// ═══════════════════════════════════════════════════════════════════

console.log('API Configuration Guide loaded. See comments above for details.');
