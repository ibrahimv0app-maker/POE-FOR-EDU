const messagesEl = document.getElementById('messages')
const messageInput = document.getElementById('message')
const sendBtn = document.getElementById('send')
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
    // remove last placeholder
    const last = messagesEl.querySelector('.bot:last-child')
    if (last && last.textContent === '...') last.remove()

    if (!res.ok) {
      appendMessage('Error: ' + (data.error || JSON.stringify(data)), 'bot')
      return
    }
    // Try to show a reply - GraphQL responses vary; inspect data.
    let reply = 'No reply field found.'
    try {
      if (data.data && data.data.sendMessage && data.data.sendMessage.text) {
        reply = data.data.sendMessage.text
      } else if (data.error) {
        reply = JSON.stringify(data.error)
      } else {
        reply = JSON.stringify(data)
      }
    } catch (e) {
      reply = String(e)
    }
    appendMessage(reply, 'bot')
  } catch (err) {
    appendMessage('Network error: ' + err.message, 'bot')
  }
}

sendBtn.addEventListener('click', () => {
  const text = messageInput.value.trim()
  if (!text) return
  callChat(botInput.value.trim(), text)
  messageInput.value = ''
})

messageInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendBtn.click() })

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
      o.textContent = 'No bots found (see server logs)'
      botsList.appendChild(o)
    }
  } catch (e) {
    console.error(e)
  }
}

refreshBtn.addEventListener('click', refreshBots)

botsList.addEventListener('change', () => { botInput.value = botsList.value })

// initial load
refreshBots()
