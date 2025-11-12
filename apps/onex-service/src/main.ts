import { createApp, getOnexServiceInfo } from './app/app';

const host = process.env.HOST ?? 'localhost';
const port = process.env.PORT ? Number(process.env.PORT) : 3000;

const app = createApp();

app.listen(port, host, () => {
  const serviceInfo = getOnexServiceInfo();
  
  console.log(`
🚀 Onex Hacking Tools Library API
📍 Server: http://${host}:${port}
🔧 Tools Available: ${serviceInfo.toolsCount}
📂 Categories: ${serviceInfo.categoriesCount}
💻 System: ${serviceInfo.system} (${serviceInfo.packageManager})
  `);
});
