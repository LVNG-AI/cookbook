/**
 * Discord Bot Integration — Connect Discord to LVNG
 *
 * Lets your Discord server interact with LVNG agents,
 * workflows, and knowledge graph via slash commands.
 *
 * Setup:
 *   1. Create a Discord bot at https://discord.com/developers
 *   2. Get your LVNG API key at https://app.lvng.ai/settings/developer
 *   3. Set environment variables (see below)
 *   4. Run: node discord-bot.js
 *
 * Environment:
 *   DISCORD_TOKEN=your_discord_bot_token
 *   LVNG_API_KEY=lvng_sk_live_...
 *   LVNG_AGENT_ID=optional_default_agent_id
 */
const { Client, GatewayIntentBits, EmbedBuilder, REST, Routes, SlashCommandBuilder } = require('discord.js');
const axios = require('axios');

const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const LVNG_API_KEY = process.env.LVNG_API_KEY;
const DEFAULT_AGENT = process.env.LVNG_AGENT_ID;

const lvng = axios.create({
  baseURL: 'https://api.lvng.ai/api',
  headers: { 'x-api-key': LVNG_API_KEY, 'Content-Type': 'application/json' }
});

// ── Slash Command Definitions ────────────────────────────────────────

const commands = [
  new SlashCommandBuilder()
    .setName('ask')
    .setDescription('Ask your LVNG agent a question')
    .addStringOption(opt =>
      opt.setName('question').setDescription('Your question').setRequired(true)),

  new SlashCommandBuilder()
    .setName('research')
    .setDescription('Run a research workflow on a topic')
    .addStringOption(opt =>
      opt.setName('topic').setDescription('Research topic').setRequired(true)),

  new SlashCommandBuilder()
    .setName('knowledge')
    .setDescription('Search the knowledge graph')
    .addStringOption(opt =>
      opt.setName('query').setDescription('Search query').setRequired(true)),

  new SlashCommandBuilder()
    .setName('workflow')
    .setDescription('Execute a saved workflow')
    .addStringOption(opt =>
      opt.setName('name').setDescription('Workflow name or ID').setRequired(true))
    .addStringOption(opt =>
      opt.setName('input').setDescription('Input for the workflow').setRequired(false)),
];

// ── Command Handlers ─────────────────────────────────────────────────

async function handleAsk(interaction) {
  const question = interaction.options.getString('question');
  await interaction.deferReply();

  try {
    // Use default agent or create an ephemeral one
    let agentId = DEFAULT_AGENT;

    if (!agentId) {
      const { data } = await lvng.post('/v2/agents', {
        name: `Discord Bot — ${interaction.user.username}`,
        system_prompt: 'You are a helpful assistant responding via Discord. Keep answers concise (under 2000 chars). Use bullet points for lists. No markdown tables (Discord renders them poorly).',
        model: 'claude-sonnet-4-6',
        tools: ['web_search', 'knowledge_search']
      });
      agentId = data.data.id;
    }

    const { data } = await lvng.post(`/v2/agents/${agentId}/message`, {
      message: question
    });

    const answer = data.data.content || 'No response';

    const embed = new EmbedBuilder()
      .setColor(0x00D2FF)
      .setTitle('LVNG Agent')
      .setDescription(answer.slice(0, 4096))
      .setFooter({ text: `Asked by ${interaction.user.username}` })
      .setTimestamp();

    await interaction.editReply({ embeds: [embed] });

    // Cleanup ephemeral agent
    if (!DEFAULT_AGENT && agentId) {
      await lvng.delete(`/v2/agents/${agentId}`);
    }
  } catch (err) {
    await interaction.editReply(`Error: ${err.message}`);
  }
}

async function handleResearch(interaction) {
  const topic = interaction.options.getString('topic');
  await interaction.deferReply();

  try {
    // Search knowledge for internal context
    const { data: searchData } = await lvng.post('/knowledge/search', {
      query: topic, limit: 3
    });
    const context = (searchData.data || [])
      .map(r => `- ${r.title || 'N/A'}: ${(r.content || '').slice(0, 150)}`)
      .join('\n');

    // Create research agent
    const { data: agentData } = await lvng.post('/v2/agents', {
      name: `Research — ${topic.slice(0, 30)}`,
      system_prompt: `Research analyst. Topic: ${topic}. Be concise, data-driven. Under 1500 chars. No tables.`,
      model: 'claude-sonnet-4-6',
      tools: ['web_search']
    });
    const agentId = agentData.data.id;

    // Run research
    const { data: msgData } = await lvng.post(`/v2/agents/${agentId}/message`, {
      message: `Research: ${topic}\n\nInternal context:\n${context || 'None available'}`
    });

    const report = msgData.data.content || 'No results';

    const embed = new EmbedBuilder()
      .setColor(0x6C5CE7)
      .setTitle(`Research: ${topic}`)
      .setDescription(report.slice(0, 4096))
      .setFooter({ text: `Requested by ${interaction.user.username} | Sources: ${(searchData.data || []).length} internal + web` })
      .setTimestamp();

    await interaction.editReply({ embeds: [embed] });
    await lvng.delete(`/v2/agents/${agentId}`);
  } catch (err) {
    await interaction.editReply(`Research error: ${err.message}`);
  }
}

async function handleKnowledge(interaction) {
  const query = interaction.options.getString('query');
  await interaction.deferReply();

  try {
    const { data } = await lvng.post('/knowledge/search', {
      query, limit: 5
    });

    const results = data.data || [];

    if (results.length === 0) {
      await interaction.editReply('No knowledge entries found.');
      return;
    }

    const embed = new EmbedBuilder()
      .setColor(0x00D2FF)
      .setTitle(`Knowledge: "${query}"`)
      .setDescription(`Found ${results.length} results`)
      .setTimestamp();

    results.forEach((r, i) => {
      embed.addFields({
        name: `${i + 1}. ${r.title || 'Untitled'}`,
        value: (r.content || r.description || 'No content').slice(0, 200) +
          (r.score ? ` _(score: ${r.score})_` : ''),
        inline: false
      });
    });

    await interaction.editReply({ embeds: [embed] });
  } catch (err) {
    await interaction.editReply(`Knowledge search error: ${err.message}`);
  }
}

async function handleWorkflow(interaction) {
  const name = interaction.options.getString('name');
  const input = interaction.options.getString('input') || '';
  await interaction.deferReply();

  try {
    // Find workflow by name or use as ID
    let workflowId = name;

    if (!name.startsWith('wf_')) {
      const { data } = await lvng.get('/v2/workflows');
      const match = (data.data || []).find(w =>
        w.name.toLowerCase().includes(name.toLowerCase())
      );
      if (match) workflowId = match.id;
      else {
        await interaction.editReply(`Workflow "${name}" not found.`);
        return;
      }
    }

    // Execute
    const { data } = await lvng.post(`/v2/workflows/${workflowId}/execute`, {
      inputs: { query: input, topic: input }
    });

    const run = data.data || {};

    const embed = new EmbedBuilder()
      .setColor(0xFFA502)
      .setTitle(`Workflow: ${name}`)
      .addFields(
        { name: 'Run ID', value: run.id || 'N/A', inline: true },
        { name: 'Status', value: run.status || 'started', inline: true }
      )
      .setFooter({ text: `Triggered by ${interaction.user.username}` })
      .setTimestamp();

    if (run.result) {
      embed.setDescription(JSON.stringify(run.result).slice(0, 2000));
    }

    await interaction.editReply({ embeds: [embed] });
  } catch (err) {
    await interaction.editReply(`Workflow error: ${err.message}`);
  }
}

// ── Bot Setup ────────────────────────────────────────────────────────

const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

client.on('ready', async () => {
  console.log(`Bot ready: ${client.user.tag}`);

  // Register slash commands
  const rest = new REST().setToken(DISCORD_TOKEN);
  await rest.put(Routes.applicationCommands(client.user.id), {
    body: commands.map(c => c.toJSON())
  });
  console.log('Slash commands registered');
});

client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;

  const handlers = {
    ask: handleAsk,
    research: handleResearch,
    knowledge: handleKnowledge,
    workflow: handleWorkflow,
  };

  const handler = handlers[interaction.commandName];
  if (handler) await handler(interaction);
});

client.login(DISCORD_TOKEN);
console.log('Starting LVNG Discord bot...');
