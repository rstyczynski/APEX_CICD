// Actual Chromium login and rendering against the freshly provisioned APEX/ORDS.
import fs from 'node:fs/promises';
import {chromium} from 'playwright';
const browser=await chromium.launch({headless:true});
try {
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 await page.goto('http://127.0.0.1:8080/ords/f?p=810503:1',{waitUntil:'networkidle'});
 await page.screenshot({path:'result/application-login-start.png',fullPage:true});
 console.log('OBSERVE actual blank application login before entering private inputs');
 await page.locator('#P9999_USERNAME').fill('LAB_USER');
 await page.locator('#P9999_PASSWORD').fill(process.env.APEX_ADMIN_PASSWORD);
 await page.getByRole('button',{name:/sign in|log in/i}).click();
 await page.getByText('Row 1: retained across upgrade',{exact:true}).waitFor({timeout:30000});
 await page.screenshot({path:'result/authenticated-application.png',fullPage:true});
 await fs.writeFile('result/authenticated-access.json',JSON.stringify({user:'LAB_USER',authenticated:true,preserved_row:'Row 1: retained across upgrade'}));
 console.log('PASS actual Chromium login and native retained row rendered through ORDS/APEX');
} finally {await browser.close();}
