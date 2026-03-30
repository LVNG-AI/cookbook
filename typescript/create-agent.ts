import { LvngClient } from '@lvng/sdk';

const lvng = new LvngClient({ apiKey: process.env.LVNG_API_KEY! });

const agent = await lvng.agents.create({
  name: 'Research Assistant',
  systemPrompt: 'You are a helpful research assistant.',
  model: 'claude-sonnet-4-6',
  tools: ['web_search', 'knowledge_search']
});
console.log('Agent ID:', agent.id);
