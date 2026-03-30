import { LvngClient } from '@lvng/sdk';

const lvng = new LvngClient({ apiKey: process.env.LVNG_API_KEY! });

const response = await lvng.agents.message('AGENT_ID', {
  message: 'What are the top trends in AI for 2026?'
});
console.log(response.content);
