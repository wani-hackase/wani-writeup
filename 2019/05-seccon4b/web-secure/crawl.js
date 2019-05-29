const puppeteer = require('puppeteer');
const flag = process.env.FLAG;
const browser_option = {
    executablePath: 'google-chrome-stable',
    headless: true,
    args: [
        '--no-sandbox',
        '--disable-background-networking',
        '--disable-default-apps',
        '--disable-extensions',
        '--disable-gpu',
        '--disable-sync',
        '--disable-translate',
        '--hide-scrollbars',
        '--metrics-recording-only',
        '--mute-audio',
        '--no-first-run',
        '--safebrowsing-disable-auto-update',
    ],
};
const default_cookie = {
    "domain": current_host,
    "expirationDate": 1597288045,
    "hostOnly": false,
    "httpOnly": false,
    "name": "flag",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": flag,
    "id": 1
}


/* ... */

const browser = await puppeteer.launch(browser_option);
const page = await browser.newPage();
await page.goto(current_host, {waitUntil: 'networkidle2'});
await page.setCookie(default_cookie);
await page.goto(url, {waitUntil: 'networkidle2'});
await page.waitFor(3000);
await browser.close();
