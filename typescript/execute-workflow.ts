import { LvngClient } from '@lvng/sdk';

const lvng = new LvngClient({ apiKey: process.env.LVNG_API_KEY! });

const run = await lvng.workflows.execute('WF_ID', {
  inputs: { topic: 'Q4 market analysis' }
});
console.log('Run ID:', run.id);
console.log('Status:', run.status);
