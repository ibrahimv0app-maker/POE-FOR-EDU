const messagesEl = document.getElementById('messages')
const historyEl = document.getElementById('history')
const messageInput = document.getElementById('message')
const sendBtn = document.getElementById('send')
const streamBtn = document.getElementById('streamSend')
const botInput = document.getElementById('bot')
const botsList = document.getElementById('botsList')
const refreshBtn = document.getElementById('refreshBots')

function appendMessage(content, cls) {
  const el = document.createElement('div')
  el.className = cls
  el.textContent = content
  messagesEl.appendChild(el)
  messagesEl.scrollTop = messagesEl.scrollHeight
}

function renderHistory(items) {
  historyEl.innerHTML = ''
  items.forEach(it => {
    const d = document.createElement('div')
    d.className = 'history-item'
    d.textContent = `${new Date(it.ts*1000).toLocaleString()} — ${it.role}: ${it.content.slice(0,80)}`
    historyEl.appendChild(d)
  })
}

async function loadHistory() {
  try {
    const res = await fetch('/history?limit=50')
    const j = await res.json()
    renderHistory(j)
  } catch (e) { console.error(e) }
}

async function refreshBots() {
  try {
    const res = await fetch('/bots')
    const j = await res.json()
    botsList.innerHTML = ''
    if (j.data && j.data.bots) {
      j.data.bots.forEach(b => {
        const o = document.createElement('option')
        o.value = b.id || b.name
        o.textContent = `${b.name || b.id} — ${b.description || ''}`
        botsList.appendChild(o)
      })
    } else {
      const o = document.createElement('option')
      o.textContent = 'No bots found'
      botsList.appendChild(o)
    }
  } catch (e) { console.error(e) }
}

async function callChat(bot, text) {
  appendMessage(text, 'user')
  appendMessage('...', 'bot')
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({bot, text})
    })
    const data = await res.json()
    const last = messagesEl.querySelector('.bot:last-child')
    if (last && last.textContent === '...') last.remove()
    if (!res.ok) { appendMessage('Error: '+JSON.stringify(data), 'bot'); return }
    appendMessage(data.reply || JSON.stringify(data.raw), 'bot')
    loadHistory()
  } catch (err) { appendMessage('Network error: '+err.message, 'bot') }
}

async function callStream(bot, text) {
  appendMessage(text, 'user')
  appendMessage('streaming...', 'bot')
  const url = `/stream?bot=${encodeURIComponent(bot)}&text=${encodeURIComponent(text)}`
  const es = new EventSource(url)
  const last = messagesEl.querySelector('.bot:last-child')
  es.addEventListener('message', (e) => {
    if (last) last.remove()
    appendMessage(e.data, 'bot')
    es.close()
    loadHistory()
  })
  es.addEventListener('error', (e) => {
    if (last) last.remove()
    appendMessage('Stream error', 'bot')
    es.close()
  })
}

sendBtn.addEventListener('click', () => {
  const text = messageInput.value.trim(); if (!text) return
  callChat(botInput.value.trim(), text)
  messageInput.value = ''
})
streamBtn.addEventListener('click', () => {
  const text = messageInput.value.trim(); if (!text) return
  callStream(botInput.value.trim(), text)
  messageInput.value = ''
})
messageInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendBtn.click() })
refreshBtn.addEventListener('click', refreshBots)

botsList.addEventListener('change', () => { botInput.value = botsList.value })

// initial
refreshBots(); loadHistory()
