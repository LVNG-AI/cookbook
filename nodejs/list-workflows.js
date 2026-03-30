const axios = require('axios');

const api = axios.create({
  baseURL: 'https://api.lvng.ai/api',
  headers: { 'x-api-key': process.env.LVNG_API_KEY }
});

async function main() {
  const { data } = await api.get('/v2/workflows');
  for (const wf of data.data) {
    console.log(`${wf.name} — ${wf.status}`);
  }
}

main().catch(console.error);
