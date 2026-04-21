const { chromium } = require('playwright');
const path = require('path');

const TARGET_URL = 'file:///d:/Mini_Projects/FarmSight/index.html';
const OUTPUT_DIR = 'd:/Mini_Projects/FarmSight/report-images-2k';

async function captureLocator(page, selector, fileName) {
  const locator = page.locator(selector);
  const count = await locator.count();
  if (count === 0) {
    console.log(`Skipped ${fileName} (selector not found): ${selector}`);
    return;
  }
  await locator.first().screenshot({ path: path.join(OUTPUT_DIR, fileName) });
  console.log(`Saved: ${fileName}`);
}

(async () => {
  const browser = await chromium.launch({ headless: false, slowMo: 50 });
  const context = await browser.newContext({ viewport: { width: 2560, height: 1440 } });
  const page = await context.newPage();

  await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(3500);

  const weatherSource = page.locator('#weatherSource');
  if ((await weatherSource.count()) > 0) {
    await weatherSource.selectOption('api');
    await page.waitForTimeout(800);
  }

  await page.screenshot({
    path: path.join(OUTPUT_DIR, '01-farmsight-dashboard-architecture-2k.png'),
    fullPage: true,
  });
  console.log('Saved: 01-farmsight-dashboard-architecture-2k.png');

  await captureLocator(page, 'section.panel.weather-panel', '02-weather-panel-live-api-integration-2k.png');
  await captureLocator(page, 'section.panel.soil-panel', '03-soil-health-zone-charts-2k.png');
  await captureLocator(page, 'section.panel.map-panel', '04-interactive-farm-map-zone-polygons-2k.png');
  await captureLocator(page, 'section.panel.timeline-panel', '05-crop-timeline-growth-stages-2k.png');
  await captureLocator(page, 'section.panel.market-panel', '06-market-intelligence-revenue-calculator-2k.png');

  await page.screenshot({
    path: path.join(OUTPUT_DIR, '07-dashboard-overview-full-interface-2k.png'),
    fullPage: true,
  });
  console.log('Saved: 07-dashboard-overview-full-interface-2k.png');

  await captureLocator(page, 'section.panel.alerts-panel', '08-alerts-panel-priority-sorting-2k.png');

  await browser.close();
  console.log('All 2K report images captured.');
})().catch((error) => {
  console.error('2K screenshot capture failed:', error);
  process.exit(1);
});
