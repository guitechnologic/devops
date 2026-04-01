const express = require('express');
const client = require('prom-client');

const app = express();
const register = new client.Registry();

client.collectDefaultMetrics({ register });

const httpRequests = new client.Counter({
  name: 'demo_http_requests_total',
  help: 'Total HTTP Requests',
});

register.registerMetric(httpRequests);

app.get('/', (req, res) => {
  httpRequests.inc();

  // Simula carga CPU
  const end = Date.now() + Math.random() * 200;
  while (Date.now() < end) {}

  console.log(`Request recebida em ${new Date().toISOString()}`);
  res.send('Demo App Running 🚀');
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});