import { LvngClient } from '@lvng/sdk';

const lvng = new LvngClient({ apiKey: process.env.LVNG_API_KEY! });

const results = await lvng.knowledge.search({
  query: 'revenue trends Q4',
  limit: 10
});
for (const r of results) {
  console.log(`${r.title} — score: ${r.score}`);
}
