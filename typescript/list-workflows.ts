import { LvngClient } from '@lvng/sdk';

const lvng = new LvngClient({ apiKey: process.env.LVNG_API_KEY! });

const { workflows } = await lvng.workflows.list();
for (const wf of workflows) {
  console.log(`${wf.name} — ${wf.status}`);
}
