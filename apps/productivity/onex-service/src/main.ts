import { createApp } from './app';
import { OnexService } from './lib';

const host = process.env.HOST ?? 'localhost';
const port = process.env.PORT ? Number(process.env.PORT) : 3000;

const app = createApp();

app.listen(port, host, () => {
  // Initialize service to get stats for startup message
  const onexService = new OnexService();
  const stats = onexService.getStats();
  const systemInfo = onexService.getSystemInfo();
  
  console.log(`
🚀 Onex Hacking Tools Library API
📍 Server: http://${host}:${port}
🔧 Tools Available: ${stats.toolsCount}
📂 Categories: ${stats.categoriesCount}
💻 System: ${systemInfo.system} (${systemInfo.packageManager})
🎯 API Base: http://${host}:${port}/api
  `);
});
