/* ═══════════════════════════════════════════════════════════════════
   FarmSight Utility Functions - Helper Methods
   ═══════════════════════════════════════════════════════════════════ */

// ═══════════════════════════════════════════════════════════════════
// DATE & TIME UTILITIES
// ═══════════════════════════════════════════════════════════════════

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    return formatDate(dateString);
}

function getDaysUntil(targetDate) {
    const target = new Date(targetDate);
    const now = new Date();
    const diffMs = target - now;
    const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
    return diffDays;
}

// ═══════════════════════════════════════════════════════════════════
// NUMBER FORMATTING
// ═══════════════════════════════════════════════════════════════════

function formatCurrency(amount) {
    return '₹' + amount.toLocaleString('en-IN');
}

function formatNumber(num, decimals = 0) {
    return num.toLocaleString('en-IN', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

function formatPercentage(value, decimals = 1) {
    return value.toFixed(decimals) + '%';
}

// ═══════════════════════════════════════════════════════════════════
// TOAST NOTIFICATION
// ═══════════════════════════════════════════════════════════════════

function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    
    if (!toast || !toastMessage) return;
    
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}

// ═══════════════════════════════════════════════════════════════════
// LOADING OVERLAY
// ═══════════════════════════════════════════════════════════════════

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.add('show');
    }
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.classList.remove('show');
    }
}

// ═══════════════════════════════════════════════════════════════════
// TIMELINE GENERATION
// ═══════════════════════════════════════════════════════════════════

function renderTimeline(timelineData) {
    const container = document.getElementById('timelineContainer');
    if (!container || !timelineData) return;
    
    container.innerHTML = '';
    
    timelineData.stages.forEach((stage, index) => {
        const stageEl = document.createElement('div');
        stageEl.className = `timeline-stage ${stage.status}`;
        
        let iconHtml;
        if (stage.status === 'completed') {
            iconHtml = '<i class="fas fa-check"></i>';
        } else if (stage.status === 'current') {
            iconHtml = '<i class="fas fa-spinner"></i>';
        } else {
            iconHtml = '<i class="fas fa-clock"></i>';
        }
        
        let progressHtml = '';
        if (stage.status === 'current' && stage.progress_percent) {
            progressHtml = `
                <div class="stage-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${stage.progress_percent}%"></div>
                    </div>
                    <small>${stage.progress_percent}% complete</small>
                </div>
            `;
        }
        
        let nextActivityHtml = '';
        if (stage.next_activity) {
            nextActivityHtml = `
                <div class="next-activity">
                    <strong>Next:</strong> ${stage.next_activity}
                </div>
            `;
        }
        
        const daysInfo = stage.status === 'upcoming' 
            ? `<small>(Starts in ${getDaysUntil(stage.start_date)} days)</small>`
            : `<small>${stage.duration_days} days</small>`;
        
        stageEl.innerHTML = `
            <div class="stage-icon">${iconHtml}</div>
            <div class="stage-content">
                <div class="stage-header">
                    <span class="stage-name">${stage.name}</span>
                    <span class="stage-dates">${formatDate(stage.start_date)} - ${formatDate(stage.end_date)}</span>
                </div>
                <span class="stage-status">${stage.status.toUpperCase()} ${daysInfo}</span>
                ${progressHtml}
                ${nextActivityHtml}
                <div class="stage-activities">
                    ${stage.activities.map(a => `• ${a}`).join('<br>')}
                </div>
            </div>
        `;
        
        container.appendChild(stageEl);
    });
    
    console.log('✓ Timeline rendered with', timelineData.stages.length, 'stages');
}

// ═══════════════════════════════════════════════════════════════════
// ALERTS GENERATION
// ═══════════════════════════════════════════════════════════════════

function renderAlerts(alerts) {
    const container = document.getElementById('alertsContainer');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (alerts.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #757575;">
                <i class="fas fa-check-circle" style="font-size: 3rem; color: #4CAF50; margin-bottom: 16px;"></i>
                <p>No active alerts - All systems operational</p>
            </div>
        `;
        return;
    }
    
    alerts.forEach((alert, index) => {
        const alertEl = document.createElement('div');
        alertEl.className = `alert-item ${alert.type}`;
        alertEl.dataset.alertId = index;
        
        const iconMap = {
            critical: 'fa-exclamation-triangle',
            warning: 'fa-exclamation-circle',
            info: 'fa-info-circle',
            success: 'fa-check-circle'
        };
        
        const icon = alert.icon || iconMap[alert.type] || 'fa-bell';
        
        alertEl.innerHTML = `
            <i class="fas ${icon} alert-icon"></i>
            <div class="alert-content">
                <div class="alert-message">${alert.message}</div>
                <div class="alert-meta">
                    <span><i class="fas fa-clock"></i> ${getRelativeTime(alert.timestamp)}</span>
                    <span><i class="fas fa-map-marker-alt"></i> ${alert.zone}</span>
                </div>
            </div>
            <button class="dismiss-btn" onclick="dismissAlert(${index})">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        container.appendChild(alertEl);
    });
    
    console.log('✓ Rendered', alerts.length, 'alerts');
}

function dismissAlert(alertId) {
    const alertEl = document.querySelector(`[data-alert-id="${alertId}"]`);
    if (alertEl) {
        alertEl.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            alertEl.remove();
            
            // Check if no alerts remain
            const container = document.getElementById('alertsContainer');
            if (container && container.children.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 40px; color: #757575;">
                        <i class="fas fa-check-circle" style="font-size: 3rem; color: #4CAF50; margin-bottom: 16px;"></i>
                        <p>No active alerts - All systems operational</p>
                    </div>
                `;
            }
        }, 300);
    }
}

// Add fadeOut animation
if (!document.querySelector('#fadeOutStyle')) {
    const style = document.createElement('style');
    style.id = 'fadeOutStyle';
    style.innerHTML = `
        @keyframes fadeOut {
            from { opacity: 1; transform: translateX(0); }
            to { opacity: 0; transform: translateX(20px); }
        }
    `;
    document.head.appendChild(style);
}

// ═══════════════════════════════════════════════════════════════════
// MARKET PRICE CARDS UPDATE
// ═══════════════════════════════════════════════════════════════════

function updateMarketCards() {
    const prices = dataManager.getAllMarketPrices();
    
    prices.forEach(market => {
        const card = document.getElementById(`marketCard${market.crop_id}`);
        if (!card) return;
        
        // Update price trend indicator
        const trendEl = card.querySelector('.price-trend');
        if (trendEl) {
            trendEl.className = 'price-trend ' + market.price_trend;
            const trendIcon = market.price_trend === 'up' ? 'fa-arrow-up' :
                            market.price_trend === 'down' ? 'fa-arrow-down' :
                            'fa-minus';
            trendEl.innerHTML = `<i class="fas ${trendIcon}"></i> ${market.price_change_7d}`;
        }
        
        // Update current price
        const priceEl = card.querySelector('.price-value');
        if (priceEl) {
            priceEl.textContent = formatCurrency(market.current_price_quintal);
        }
        
        // Update MSP comparison bar
        const comparisonBar = card.querySelector('.current-bar');
        if (comparisonBar) {
            const percentage = (market.current_price_quintal / market.msp) * 100;
            comparisonBar.style.width = Math.min(percentage, 150) + '%';
        }
        
        // Update action badge
        const actionBadge = card.querySelector('.action-badge');
        if (actionBadge) {
            if (market.current_price_quintal > market.msp * 1.08) {
                actionBadge.className = 'action-badge sell';
                actionBadge.textContent = 'SELL NOW';
            } else if (market.price_trend === 'up') {
                actionBadge.className = 'action-badge hold';
                actionBadge.textContent = 'MONITOR';
            } else {
                actionBadge.className = 'action-badge wait';
                actionBadge.textContent = 'HOLD';
            }
        }
        
        // Update sparkline chart
        const chartId = market.crop_name.toLowerCase().replace(/\s+/g, '') + 'PriceChart';
        createPriceSparkline(chartId, market.historical_30d);
    });
    
    console.log('✓ Market cards updated');
}

// ═══════════════════════════════════════════════════════════════════
// REVENUE CALCULATOR
// ═══════════════════════════════════════════════════════════════════

function calculateRevenue() {
    const cropSelector = document.getElementById('revenueCrop');
    const yieldInput = document.getElementById('expectedYield');
    const resultEl = document.getElementById('totalRevenue');
    
    if (!cropSelector || !yieldInput || !resultEl) return;
    
    const cropId = cropSelector.value;
    const yieldPerAcre = parseFloat(yieldInput.value) || 0;
    
    const crop = dataManager.getCropById(cropId);
    const market = dataManager.getMarketPrice(cropId);
    
    if (!crop || !market) return;
    
    const totalProduction = yieldPerAcre * crop.area_acres;
    const totalRevenue = totalProduction * market.current_price_quintal;
    
    resultEl.textContent = formatCurrency(Math.round(totalRevenue));
    
    // Animate the value change
    resultEl.style.animation = 'none';
    setTimeout(() => {
        resultEl.style.animation = 'pulse 0.5s ease';
    }, 10);
}

// ═══════════════════════════════════════════════════════════════════
// LOCAL STORAGE HELPERS
// ═══════════════════════════════════════════════════════════════════

function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (e) {
        console.warn('Failed to save to localStorage:', e);
        return false;
    }
}

function getFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.warn('Failed to read from localStorage:', e);
        return null;
    }
}

function clearLocalStorage(key) {
    try {
        if (key) {
            localStorage.removeItem(key);
        } else {
            localStorage.clear();
        }
        return true;
    } catch (e) {
        console.warn('Failed to clear localStorage:', e);
        return false;
    }
}

// ═══════════════════════════════════════════════════════════════════
// ERROR HANDLER
// ═══════════════════════════════════════════════════════════════════

function handleError(error, userMessage = 'An error occurred') {
    console.error('Error:', error);
    showToast(userMessage + ' - Using cached/offline data', 4000);
}

// ═══════════════════════════════════════════════════════════════════
// SKELETON LOADER
// ═══════════════════════════════════════════════════════════════════

function showSkeleton(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.classList.add('skeleton-loading');
}

function hideSkeleton(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.classList.remove('skeleton-loading');
}

// Add skeleton styles dynamically
if (!document.querySelector('#skeletonStyle')) {
    const style = document.createElement('style');
    style.id = 'skeletonStyle';
    style.innerHTML = `
        .skeleton-loading {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: skeleton-loading 1.5s infinite;
            pointer-events: none;
        }
        
        @keyframes skeleton-loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
    `;
    document.head.appendChild(style);
}

// ═══════════════════════════════════════════════════════════════════
// DEBOUNCE UTILITY
// ═══════════════════════════════════════════════════════════════════

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ═══════════════════════════════════════════════════════════════════
// EXPORT FUNCTIONS FOR GLOBAL ACCESS
// ═══════════════════════════════════════════════════════════════════

window.dismissAlert = dismissAlert;
window.calculateRevenue = calculateRevenue;
