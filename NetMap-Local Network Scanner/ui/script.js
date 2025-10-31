let scanInterval = null;

function showAlert(message, type = 'success') {
    const alert = document.getElementById('alert');
    alert.className = `alert alert-${type} visible`;
    alert.textContent = message;
    setTimeout(() => {
        alert.classList.remove('visible');
    }, 5000);
}

async function detectNetwork() {
    try {
        showAlert('Detecting network...', 'success');
        const response = await fetch('/api/detect-network');
        const data = await response.json();

        if (data.success) {
            document.getElementById('localIp').textContent = data.local_ip;
            document.getElementById('subnet').textContent = data.subnet;
            document.getElementById('networkInfo').classList.add('visible');
            showAlert('Network detected successfully!', 'success');
        } else {
            showAlert('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error detecting network: ' + error.message, 'error');
    }
}

async function startScan() {
    try {
        const scanBtn = document.getElementById('scanBtn');
        scanBtn.disabled = true;
        scanBtn.textContent = 'Scanning...';

        const response = await fetch('/api/start-scan', { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            document.getElementById('progressContainer').classList.add('visible');
            
            scanInterval = setInterval(checkScanStatus, 1000);
        } else {
            showAlert('Error: ' + data.error, 'error');
            scanBtn.disabled = false;
            scanBtn.textContent = '🚀 Start Scan';
        }
    } catch (error) {
        showAlert('Error starting scan: ' + error.message, 'error');
        document.getElementById('scanBtn').disabled = false;
        document.getElementById('scanBtn').textContent = '🚀 Start Scan';
    }
}

async function checkScanStatus() {
    try {
        const response = await fetch('/api/scan-status');
        const data = await response.json();

        const progressFill = document.getElementById('progressFill');
        progressFill.style.width = data.progress + '%';
        document.getElementById('progressMessage').textContent = data.message + ' (' + data.progress + '%)';

        if (data.local_ip) {
            document.getElementById('localIp').textContent = data.local_ip;
            document.getElementById('subnet').textContent = data.subnet;
            document.getElementById('networkInfo').classList.add('visible');
        }

        if (!data.scanning && data.progress === 100) {
            clearInterval(scanInterval);
            document.getElementById('scanBtn').disabled = false;
            document.getElementById('scanBtn').textContent = '🚀 Start Scan';

            if (data.has_results) {
                loadResults();
            } else {
                showAlert(data.message, 'warning');
            }
        }
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

async function loadResults() {
    try {
        const response = await fetch('/api/results');
        const data = await response.json();

        if (data.success) {
            // Update statistics
            document.getElementById('statTotal').textContent = data.statistics.total_hosts;
            document.getElementById('statSSH').textContent = data.statistics.ssh_open;
            document.getElementById('statHTTP').textContent = data.statistics.http_open;
            document.getElementById('statHTTPS').textContent = data.statistics.https_open;
            document.getElementById('statistics').classList.add('visible');

            const tbody = document.getElementById('resultsBody');
            tbody.innerHTML = '';

            // Check if we have results
            if (data.results.length === 0) {
                const row = document.createElement('tr');
                row.innerHTML = `<td colspan="7" style="text-align: center; padding: 2rem; color: #888;">
                    No devices found on the network. Make sure you're running with administrator privileges.
                </td>`;
                tbody.appendChild(row);
            } else {
                // Add rows for each host
                data.results.forEach(host => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${host['IP Address']}</td>
                        <td>${host['MAC Address']}</td>
                        <td>${host['Vendor']}</td>
                        <td>${host['Hostname']}</td>
                        <td class="${host['SSH (22)'] === 'Open' ? 'status-open' : 'status-closed'}">
                            ${host['SSH (22)'] === 'Open' ? '🟢' : '🔴'} ${host['SSH (22)']}
                        </td>
                        <td class="${host['HTTP (80)'] === 'Open' ? 'status-open' : 'status-closed'}">
                            ${host['HTTP (80)'] === 'Open' ? '🟢' : '🔴'} ${host['HTTP (80)']}
                        </td>
                        <td class="${host['HTTPS (443)'] === 'Open' ? 'status-open' : 'status-closed'}">
                            ${host['HTTPS (443)'] === 'Open' ? '🟢' : '🔴'} ${host['HTTPS (443)']}
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            }

            document.getElementById('resultsContainer').classList.add('visible');
            
            if (data.results.length > 0) {
                showAlert(`Scan completed successfully! Found ${data.results.length} device(s).`, 'success');
            } else {
                showAlert('Scan completed but no devices found. Try running as administrator.', 'warning');
            }
        } else {
            showAlert('Error loading results: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error loading results: ' + error.message, 'error');
    }
}

async function exportResults() {
    try {
        const filename = document.getElementById('exportFilename').value;
        
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: filename || null })
        });

        const data = await response.json();

        if (data.success) {
            showAlert(`Results exported to: ${data.filepath}`, 'success');
            
            window.location.href = `/api/download/${data.filename}`;
        } else {
            showAlert('Error exporting: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Error exporting results: ' + error.message, 'error');
    }
}