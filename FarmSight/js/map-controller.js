/* ═══════════════════════════════════════════════════════════════════
   FarmSight Map Controller - Leaflet Interactive Map
   ═══════════════════════════════════════════════════════════════════ */

let farmMap = null;
let zonePolygons = [];
let satelliteLayer = null;
let streetLayer = null;
let currentBaseLayer = 'street';

// ═══════════════════════════════════════════════════════════════════
// INITIALIZE FARM MAP
// ═══════════════════════════════════════════════════════════════════

function initializeFarmMap() {
    const farmProfile = dataManager.getFarmProfile();
    const soilZones = dataManager.getAllSoilZones();
    const crops = farmProfile.crops;
    
    const [lat, lon] = farmProfile.location.coordinates;
    
    // Create map
    farmMap = L.map('farmMap').setView([lat, lon], 15);
    
    // Street layer (default)
    streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(farmMap);
    
    // Satellite layer (optional)
    satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles © Esri',
        maxZoom: 19
    });
    
    // Create zone polygons
    crops.forEach((crop, index) => {
        const zone = soilZones[index];
        if (!zone) return;
        
        const color = getZoneColor(zone.status);
        const cropName = crop.name.split('(')[0].trim();
        
        // Create polygon
        const polygon = L.polygon(crop.coordinates, {
            color: color,
            fillColor: color,
            fillOpacity: zone.status === 'critical' ? 0.5 : 0.3,
            weight: 3,
            className: zone.status === 'critical' ? 'critical-zone-pulse' : ''
        }).addTo(farmMap);
        
        // Create popup content
        const popupContent = createZonePopup(zone, crop);
        polygon.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'zone-popup'
        });
        
        // Hover effect
        polygon.on('mouseover', function() {
            this.setStyle({
                weight: 5,
                fillOpacity: 0.6
            });
        });
        
        polygon.on('mouseout', function() {
            this.setStyle({
                weight: 3,
                fillOpacity: zone.status === 'critical' ? 0.5 : 0.3
            });
        });
        
        // Click event to sync with soil panel
        polygon.on('click', function() {
            syncSoilPanel(zone.zone_id);
            updateURLHash(zone.zone_id);
        });
        
        // Store polygon reference
        zonePolygons.push({
            zone_id: zone.zone_id,
            polygon: polygon,
            zone: zone,
            crop: crop
        });
    });
    
    // Add farm center marker
    const farmMarker = L.marker([lat, lon], {
        icon: L.divIcon({
            className: 'farm-center-marker',
            html: '<i class="fas fa-tractor" style="font-size: 24px; color: #2E7D32;"></i>',
            iconSize: [30, 30]
        })
    }).addTo(farmMap);
    
    farmMarker.bindPopup(`
        <div class="zone-popup">
            <h3>${farmProfile.farm_name}</h3>
            <p><strong>Location:</strong> ${farmProfile.location.name}</p>
            <p><strong>Total Area:</strong> ${farmProfile.location.total_area_acres} acres</p>
            <p><strong>Soil Type:</strong> ${farmProfile.location.soil_type}</p>
            <p><strong>Season:</strong> ${farmProfile.current_season}</p>
        </div>
    `);
    
    console.log('✓ Farm map initialized with', zonePolygons.length, 'zones');
    
    // Check URL hash for zone selection
    checkURLHash();
}

// ═══════════════════════════════════════════════════════════════════
// CREATE ZONE POPUP CONTENT
// ═══════════════════════════════════════════════════════════════════

function createZonePopup(zone, crop) {
    const cropName = crop.name.split('(')[0].trim();
    const statusIcon = zone.status === 'optimal' ? '✓' : 
                       zone.status === 'monitor' ? '⚠' : '⚠';
    const statusClass = zone.status;
    
    return `
        <div class="zone-popup">
            <h3>${zone.zone_id} - ${cropName}</h3>
            <div class="popup-stats">
                <div class="stat-row">
                    <span>Variety:</span>
                    <strong>${crop.variety}</strong>
                </div>
                <div class="stat-row">
                    <span>Area:</span>
                    <strong>${crop.area_acres} acres</strong>
                </div>
                <div class="stat-row">
                    <span>Growth Stage:</span>
                    <strong>${crop.growth_stage}</strong>
                </div>
                <div class="stat-row">
                    <span>Health Score:</span>
                    <strong style="color: ${getHealthColor(crop.health_score)}">
                        ${crop.health_score}/100
                    </strong>
                </div>
                <div class="stat-row">
                    <span>Soil Moisture:</span>
                    <strong style="color: ${getMoistureColor(zone.moisture_percent)}">
                        ${zone.moisture_percent}%
                    </strong>
                </div>
                <div class="stat-row">
                    <span>pH Level:</span>
                    <strong>${zone.ph_level}</strong>
                </div>
                <div class="stat-row">
                    <span>Status:</span>
                    <strong class="${statusClass}">${statusIcon} ${zone.status.toUpperCase()}</strong>
                </div>
            </div>
            <button class="view-details-btn" onclick="syncSoilPanel('${zone.zone_id}')">
                View Detailed Analysis
            </button>
        </div>
    `;
}

// ═══════════════════════════════════════════════════════════════════
// SYNC SOIL PANEL WITH MAP SELECTION
// ═══════════════════════════════════════════════════════════════════

function syncSoilPanel(zoneId) {
    const selector = document.getElementById('zoneSelector');
    if (selector) {
        selector.value = zoneId;
        // Trigger change event to update soil panel
        selector.dispatchEvent(new Event('change'));
        
        // Scroll to soil panel
        const soilPanel = document.querySelector('.soil-panel');
        if (soilPanel) {
            soilPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        
        // Highlight selected zone temporarily
        highlightZone(zoneId);
    }
}

function highlightZone(zoneId) {
    // Reset all zones
    zonePolygons.forEach(zp => {
        zp.polygon.setStyle({
            weight: 3,
            fillOpacity: zp.zone.status === 'critical' ? 0.5 : 0.3
        });
    });
    
    // Highlight selected zone
    const selectedZone = zonePolygons.find(zp => zp.zone_id === zoneId);
    if (selectedZone) {
        selectedZone.polygon.setStyle({
            weight: 5,
            fillOpacity: 0.6
        });
        
        // Pan map to zone center
        const bounds = selectedZone.polygon.getBounds();
        farmMap.fitBounds(bounds, { padding: [50, 50] });
        
        // Reset highlight after 3 seconds
        setTimeout(() => {
            selectedZone.polygon.setStyle({
                weight: 3,
                fillOpacity: selectedZone.zone.status === 'critical' ? 0.5 : 0.3
            });
        }, 3000);
    }
}

// ═══════════════════════════════════════════════════════════════════
// TOGGLE SATELLITE VIEW
// ═══════════════════════════════════════════════════════════════════

function toggleSatelliteView() {
    if (currentBaseLayer === 'street') {
        farmMap.removeLayer(streetLayer);
        farmMap.addLayer(satelliteLayer);
        currentBaseLayer = 'satellite';
        document.getElementById('toggleSatellite').innerHTML = 
            '<i class="fas fa-map"></i> Street View';
        console.log('→ Switched to satellite view');
    } else {
        farmMap.removeLayer(satelliteLayer);
        farmMap.addLayer(streetLayer);
        currentBaseLayer = 'street';
        document.getElementById('toggleSatellite').innerHTML = 
            '<i class="fas fa-satellite"></i> Satellite';
        console.log('→ Switched to street view');
    }
}

// ═══════════════════════════════════════════════════════════════════
// URL HASH MANAGEMENT (For Sharing Specific Zones)
// ═══════════════════════════════════════════════════════════════════

function updateURLHash(zoneId) {
    window.location.hash = `zone=${zoneId}`;
}

function checkURLHash() {
    const hash = window.location.hash;
    if (hash.startsWith('#zone=')) {
        const zoneId = hash.replace('#zone=', '');
        setTimeout(() => {
            syncSoilPanel(zoneId);
        }, 500);
    }
}

// Listen for hash changes
window.addEventListener('hashchange', checkURLHash);

// ═══════════════════════════════════════════════════════════════════
// UPDATE MAP ZONES (When Data Refreshes)
// ═══════════════════════════════════════════════════════════════════

function updateMapZones() {
    const soilZones = dataManager.getAllSoilZones();
    const crops = dataManager.getAllCrops();
    
    zonePolygons.forEach((zp, index) => {
        const zone = soilZones[index];
        const crop = crops[index];
        
        if (!zone || !crop) return;
        
        // Update polygon color based on new status
        const color = getZoneColor(zone.status);
        zp.polygon.setStyle({
            color: color,
            fillColor: color,
            fillOpacity: zone.status === 'critical' ? 0.5 : 0.3
        });
        
        // Update popup content
        const popupContent = createZonePopup(zone, crop);
        zp.polygon.setPopupContent(popupContent);
        
        // Update stored references
        zp.zone = zone;
        zp.crop = crop;
    });
    
    console.log('✓ Map zones updated');
}

// ═══════════════════════════════════════════════════════════════════
// HELPER FUNCTIONS
// ═══════════════════════════════════════════════════════════════════

function getZoneColor(status) {
    const colors = {
        optimal: '#4CAF50',
        monitor: '#F9A825',
        critical: '#C62828'
    };
    return colors[status] || '#78909C';
}

function getHealthColor(score) {
    if (score >= 70) return '#4CAF50';
    if (score >= 50) return '#F9A825';
    return '#C62828';
}

function getMoistureColor(percent) {
    if (percent < 30) return '#C62828';
    if (percent < 50) return '#F9A825';
    if (percent <= 80) return '#4CAF50';
    return '#0288D1';
}

// ═══════════════════════════════════════════════════════════════════
// ADD PULSING EFFECT TO CRITICAL ZONES (CSS Animation)
// ═══════════════════════════════════════════════════════════════════

// Add dynamic style for critical zone pulsing
const style = document.createElement('style');
style.innerHTML = `
    @keyframes pulse-critical {
        0%, 100% {
            stroke-opacity: 1;
        }
        50% {
            stroke-opacity: 0.5;
        }
    }
    
    .critical-zone-pulse {
        animation: pulse-critical 2s infinite;
    }
    
    .farm-center-marker {
        background: transparent;
        border: none;
    }
`;
document.head.appendChild(style);
