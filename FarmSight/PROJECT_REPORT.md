# FarmSight Project Report

## 1. Project Overview

FarmSight is a browser-based agricultural monitoring dashboard built with plain HTML, CSS, and vanilla JavaScript. It combines static farm data with optional live weather API integration to present weather, soil, crop timeline, market, map, and alert information in a single interface.

The project is structured as a front-end demo that can run directly in a browser. Its current value is strongest as a presentation dashboard or proof of concept for farm decision support.

## 2. Project Goal

The main goal of FarmSight is to help a user monitor farm conditions and make faster operational decisions by visualizing:

- Weather trends and advisories
- Soil health by farm zone
- Crop growth stages and upcoming activities
- Market price comparisons
- Alerts for critical conditions
- Farm zone locations on an interactive map

## 3. Technology Stack

- HTML5 for layout and page structure
- CSS3 for responsive styling and visual design
- Vanilla JavaScript for all logic and interactions
- Chart.js for charts and sparklines
- Leaflet for the interactive farm map
- OpenWeatherMap API for optional live weather data
- Google Fonts, Font Awesome, and Weather Icons for presentation and icons

## 4. Main Files and Their Roles

### Core entry points

- [index.html](index.html) - main dashboard page and script loader
- [js/app.js](js/app.js) - application startup, event handling, refresh logic
- [js/data-manager.js](js/data-manager.js) - data source, mock data, weather API, caching, location handling
- [js/chart-configs.js](js/chart-configs.js) - weather, soil, and market chart rendering
- [js/map-controller.js](js/map-controller.js) - Leaflet map, zone polygons, map sync behavior
- [js/utils.js](js/utils.js) - formatting, rendering helpers, alerts, local storage helpers
- [css/styles.css](css/styles.css) - complete UI styling and responsive layout

### Documentation and setup

- [README.md](README.md) - project description and usage guide
- [DYNAMIC_FEATURES.md](DYNAMIC_FEATURES.md) - dynamic behavior documentation
- [SETUP_GUIDE.txt](SETUP_GUIDE.txt) - quick setup and troubleshooting guide
- [API_SETUP.js](API_SETUP.js) - API configuration guide and weather integration notes

## 5. User Interface Structure

The dashboard is organized into a header and multiple panels:

1. Weather panel
2. Soil health panel
3. Farm map panel
4. Crop timeline panel
5. Market intelligence panel
6. Alerts panel

The header also contains:

- Farm name
- Location selector
- Connection status indicator
- Refresh button

## 6. Data Sources

FarmSight uses two categories of data:

### Static embedded data

The app includes mock data for:

- Farm profile
- Soil zones
- Crop timelines
- Market prices
- Base weather forecast
- Alert templates

This data is stored in [js/data-manager.js](js/data-manager.js) and allows the dashboard to work without a backend.

### Live weather data

If the OpenWeatherMap API key is configured, the app fetches live forecast data, processes 3-hour forecast records into daily summaries, and updates the weather panel and related alerts.

## 7. Functional Modules

### Weather module

The weather module can run in three modes:

- Auto mode: tries API, then falls back to cache or static data
- API mode: forces live API fetch
- Static mode: uses embedded weather data

It displays:

- Current temperature
- Humidity
- Wind speed
- Rainfall
- Weather advisory
- Forecast chart

### Soil health module

This module shows zone-wise soil data, including:

- Moisture
- pH
- NPK levels
- Health score
- Recommendations

It also renders gauge-style charts and status badges.

### Map module

The map uses Leaflet to render crop zone polygons and a farm center marker. Users can:

- Click zones to sync with soil details
- Switch between street and satellite layers
- Use URL hash links for a selected zone

### Crop timeline module

The crop timeline visualizes crop growth stages, current stage progress, and upcoming activities. It is designed to show operational planning across crop cycles.

### Market module

This section displays:

- Current crop prices
- MSP comparison
- Price trend indicators
- Mini sparkline charts
- Revenue calculation based on crop area and expected yield

### Alerts module

Alerts are generated from soil, crop health, weather, market, and timeline data. The alerts are sorted by priority and displayed with timestamps and related farm zones.

## 8. Data Flow Summary

1. The page loads [index.html](index.html)
2. The app initializes [js/data-manager.js](js/data-manager.js)
3. The dashboard fetches weather, loads static farm data, and renders charts and map layers
4. User actions such as location change, zone selection, crop selection, and refresh trigger targeted updates
5. Alerts and market values are recalculated after refresh events

## 9. Dynamic Behavior

The project includes several dynamic interactions:

- Location selector updates weather coordinates
- Refresh button updates panels and alerts
- Zone selector updates soil charts
- Crop selector updates timeline view
- Map clicks sync to the soil panel
- Revenue calculator updates live as inputs change
- Auto-refresh keeps the dashboard current during active use

## 10. Current Strengths

- Clean single-page dashboard layout
- Good visual coverage of farm monitoring use cases
- Modular code separation by responsibility
- Offline-friendly static fallback data
- Simple deployment because no build system is required
- Good presentation value because it looks complete and interactive

## 11. Current Limitations

The project is strong as a demo, but it still has important limitations:

- Only weather is truly live; most other operational data is static mock data
- It depends on CDNs for first load, so it is not fully offline at startup
- Weather API key is embedded in frontend code, so it is not secure for production use
- Soil and market data are not sourced from real external services yet
- There is no authentication or multi-user support
- There are no automated tests in the repository

## 12. Presentation Readiness

For a presentation, the project is ready to demonstrate these points:

- Live weather integration
- Interactive map and zone sync
- Soil health dashboard
- Crop progress tracking
- Market insight visualization
- Alert generation and refresh behavior

To explain it well, frame it as:

1. A front-end agricultural monitoring platform
2. A live weather plus static operational dashboard
3. A modular proof of concept that can be extended into a production system

## 13. Recommended Production Improvements

If you want to evolve this into a real operational product, the next steps should be:

- Move API calls behind a backend proxy
- Replace mock soil and market data with real data feeds
- Add authentication and user roles
- Add persistence for user preferences and farm records
- Add tests for refresh, chart rendering, and map sync
- Package external libraries locally for better offline support

## 14. Suggested Demo Script

You can present the project in this order:

1. Start with the dashboard overview
2. Show the live weather selector and refresh behavior
3. Demonstrate soil zone switching and chart updates
4. Click a map zone and show soil panel synchronization
5. Show crop timeline and explain stage tracking
6. Show market prices and revenue calculator
7. End with alerts and explain how the system prioritizes issues

## 15. Conclusion

FarmSight is a useful agricultural monitoring prototype with a strong visual interface and a clear modular structure. It is best presented as a working demo or proof of concept rather than a production farm management system, because several data sources are still simulated and the architecture is still fully client-side.

For a report or presentation, this project demonstrates the core idea of farm decision support very well and also leaves a clear roadmap for production hardening.