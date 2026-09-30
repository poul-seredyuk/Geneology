// Друкує report.html у Posich_film_dopovid.pdf через Chromium.
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'report.html'), { waitUntil: 'networkidle' });
  await page.pdf({
    path: path.join(__dirname, 'Posich_film_dopovid.pdf'),
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:7pt;color:#777;width:100%;padding:0 18mm;display:flex;justify-content:space-between">' +
      '<span>Посіч: депортована, але не знищена — доповідь за переглядом фільму</span>' +
      '<span>с. <span class="pageNumber"></span></span></div>',
    margin: { top: '16mm', bottom: '18mm', left: '18mm', right: '18mm' },
  });
  await browser.close();
})();
