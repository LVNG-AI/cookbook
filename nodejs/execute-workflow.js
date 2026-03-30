const axios = require('axios');

const api = axios.create({
  baseURL: 'https://api.lvng.ai/api',
  headers: { 'x-api-key': process.env.LVNG_API_KEY }
});

async function main() {
  const workflowId = process.argv[2] || 'WF_ID';
  const { data } = await api.post(`/v2/workflows/${workflowId}/execute`, {
    inputs: { topic: 'Q4 market analysis' }
  });
  console.log('Run ID:', data.data.id);
}

main().catch(console.error);
