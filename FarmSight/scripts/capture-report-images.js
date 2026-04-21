const { chromium } = require('playwright');
const path = require('path');

const TARGET_URL = 'file:///d:/Mini_Projects/FarmSight/index.html';
const OUTPUT_DIR = 'd:/Mini_Projects/FarmSight/report-images';

async function captureLocator(page, selector, fileName) {
  const locator = page.locator(selector);
  const count = await locator.count();
  if (count === 0) {
    console.log(`Skipped ${fileName} (selector not found): ${selector}`);
    return;
  }
  await locator.first().screenshot({
    path: path.join(OUTPUT_DIR, fileName),
  });
  console.log(`Saved: ${fileName}`);
}

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();

  await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(3500);

  // Try to set weather source to API mode for the weather integration screenshot.
  const weatherSource = page.locator('#weatherSource');
  if ((await weatherSource.count()) > 0) {
    await weatherSource.selectOption('api');
    await page.waitForTimeout(800);
  }

  // 1) FarmSight Dashboard Architecture (uses top-level full dashboard capture)
  await page.screenshot({
    path: path.join(OUTPUT_DIR, '01-farmsight-dashboard-architecture.png'),
    fullPage: true,
  });
  console.log('Saved: 01-farmsight-dashboard-architecture.png');

  // 2) Weather Panel - Live API Integration
  await captureLocator(page, 'section.panel.weather-panel', '02-weather-panel-live-api-integration.png');

  // 3) Soil Health Zone Charts
  await captureLocator(page, 'section.panel.soil-panel', '03-soil-health-zone-charts.png');

  // 4) Interactive Farm Map with Zone Polygons
  await captureLocator(page, 'section.panel.map-panel', '04-interactive-farm-map-zone-polygons.png');

  // 5) Crop Timeline and Growth Stages
  await captureLocator(page, 'section.panel.timeline-panel', '05-crop-timeline-growth-stages.png');

  // 6) Market Intelligence and Revenue Calculator
  await captureLocator(page, 'section.panel.market-panel', '06-market-intelligence-revenue-calculator.png');

  // 7) Dashboard Overview - Full Interface
  await page.screenshot({
    path: path.join(OUTPUT_DIR, '07-dashboard-overview-full-interface.png'),
    fullPage: true,
  });
  console.log('Saved: 07-dashboard-overview-full-interface.png');

  // 8) Alerts Panel with Priority Sorting
  await captureLocator(page, 'section.panel.alerts-panel', '08-alerts-panel-priority-sorting.png');

  await browser.close();
  console.log('All requested report images captured.');
})().catch((error) => {
  console.error('Screenshot capture failed:', error);
  process.exit(1);
});
