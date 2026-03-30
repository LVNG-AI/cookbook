// Stream a chat response via SSE
const response = await fetch('https://api.lvng.ai/api/v2/chat/stream', {
  method: 'POST',
  headers: {
    'x-api-key': process.env.LVNG_API_KEY!,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ message: 'Write a 3-paragraph market analysis' })
});

const reader = response.body!.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  process.stdout.write(decoder.decode(value));
}
console.log('\n--- Stream complete ---');
