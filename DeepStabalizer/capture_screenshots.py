"""
Screenshot Capture Tool for DeepStable Dashboard
Captures dashboard screenshots for documentation/report.

Usage:
  1. Run the dashboard: python dashboard/app.py (in another terminal)
  2. Wait ~5 seconds for it to start
  3. Run this script: python capture_screenshots.py
  4. Screenshots saved to: docs/screenshots/

Requires: selenium, webdriver-manager
Install: pip install selenium webdriver-manager
"""

import os
import sys
import time
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("Missing selenium or webdriver-manager. Install with:")
    print("  pip install selenium webdriver-manager")
    sys.exit(1)

# Create screenshots directory
SCREENSHOT_DIR = Path("docs/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def wait_for_element(driver, selector, timeout=10):
    """Wait for element to be present and visible."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, selector))
    )

def capture_dashboard():
    """Capture full dashboard screenshot."""
    print("[1/4] Capturing full dashboard...")
    driver.save_screenshot(str(SCREENSHOT_DIR / "01_dashboard_overview.png"))
    print("      ✓ Saved: 01_dashboard_overview.png")

def capture_risk_gauge():
    """Capture risk score card."""
    print("[2/4] Capturing risk score gauge...")
    try:
        risk_card = driver.find_element(By.ID, "card-risk")
        # Scroll to element
        driver.execute_script("arguments[0].scrollIntoView(true);", risk_card)
        time.sleep(0.5)
        risk_card.screenshot(str(SCREENSHOT_DIR / "02_risk_score_gauge.png"))
        print("      ✓ Saved: 02_risk_score_gauge.png")
    except Exception as e:
        print(f"      ⚠ Could not capture risk gauge: {e}")

def capture_charts():
    """Capture sensor and risk charts."""
    print("[3/4] Capturing sensor history charts...")
    try:
        # Scroll down to charts
        driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(0.5)
        driver.save_screenshot(str(SCREENSHOT_DIR / "03_charts_history.png"))
        print("      ✓ Saved: 03_charts_history.png")
    except Exception as e:
        print(f"      ⚠ Could not capture charts: {e}")

def capture_sensor_table():
    """Capture sensor readings table."""
    print("[4/4] Capturing sensor readings table...")
    try:
        driver.execute_script("window.scrollBy(0, 600);")
        time.sleep(0.5)
        driver.save_screenshot(str(SCREENSHOT_DIR / "04_sensor_table.png"))
        print("      ✓ Saved: 04_sensor_table.png")
    except Exception as e:
        print(f"      ⚠ Could not capture sensor table: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("DeepStable Dashboard Screenshot Capture")
    print("="*60 + "\n")
    
    # Check if dashboard is running
    print("Connecting to http://127.0.0.1:5000...")
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1400,1000")
        options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("http://127.0.0.1:5000")
        
        # Wait for dashboard to load
        print("Waiting for dashboard to load...")
        wait_for_element(driver, "risk-val", timeout=10)
        print("✓ Dashboard loaded successfully\n")
        
        # Give the live data a moment to populate
        time.sleep(2)
        
        # Capture screenshots
        capture_dashboard()
        time.sleep(1)
        
        capture_risk_gauge()
        time.sleep(1)
        
        capture_charts()
        time.sleep(1)
        
        capture_sensor_table()
        
        driver.quit()
        
        print("\n" + "="*60)
        print(f"✓ All screenshots saved to: {SCREENSHOT_DIR.absolute()}")
        print("="*60 + "\n")
        print("Next step: Add these images to PROJECT_REPORT.md using markdown:")
        print("""
  ![Dashboard Overview](docs/screenshots/01_dashboard_overview.png)
  ![Risk Score Gauge](docs/screenshots/02_risk_score_gauge.png)
  ![Charts History](docs/screenshots/03_charts_history.png)
  ![Sensor Table](docs/screenshots/04_sensor_table.png)
        """)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Is the dashboard running? (python dashboard/app.py)")
        print("2. Is Chrome/Chromium installed?")
        print("3. Try running: pip install selenium webdriver-manager")
        sys.exit(1)
