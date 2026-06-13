# 🚀 Ultimate Guide: Create Your Own AI Chatbot Website Using Poe.com Reverse Engineering (Educational Purpose)

---

## 📌 **Disclaimer**

> **⚠️ Educational Purpose Only**  
> This guide is intended **solely for educational purposes** to understand how APIs work, reverse engineering, and building AI chatbots. **Do not use this for illegal activities, abuse, or violating terms of service.**  
> **Respect Poe.com's terms and conditions.**

---

## 🌍 **Introduction**

This repository provides a **step-by-step guide** to create your own **AI chatbot website** using **Poe.com's reverse-engineered API**. You will learn how to:

- **Reverse engineer Poe.com’s API** to access **GPT-4, Claude-3, Llama-3, Mistral, and other models** (including paid ones).
- **Extract authentication tokens** and understand API endpoints.
- **Build a full-stack AI chatbot website** using **Python, FastAPI, and JavaScript**.
- **Deploy your chatbot** for free using **Railway, Fly.io, or Vercel**.
- **Automate requests** using **cURL, Python scripts, and WebSockets**.
- **Bypass rate limits** and **maintain persistent chats**.

---

## 🛠️ **Prerequisites**

Before starting, ensure you have the following:

- **Basic knowledge of Python and JavaScript.**
- **A code editor** (VS Code, Sublime Text, etc.).
- **A browser** (Chrome or Firefox for DevTools).
- **Python 3.10+** installed.
- **Node.js** (for frontend, optional).
- **Git** (for version control).

---

## 📋 **Table of Contents**

1. [🔍 Step 1: Understand Poe.com’s API](#-step-1-understand-poecoms-api)
2. [🕵️ Step 2: Extract Authentication Token](#-step-2-extract-authentication-token)
3. [📡 Step 3: Identify Key API Endpoints](#-step-3-identify-key-api-endpoints)
4. [💻 Step 4: Test API with cURL](#-step-4-test-api-with-curl)
5. [🐍 Step 5: Automate with Python](#-step-5-automate-with-python)
6. [🌐 Step 6: Build a FastAPI Backend](#-step-6-build-a-fastapi-backend)
7. [🎨 Step 7: Create a Frontend (HTML/CSS/JS)](#-step-7-create-a-frontend-htmlcssjs)
8. [🚀 Step 8: Deploy Your Chatbot](#-step-8-deploy-your-chatbot)
9. [🔄 Step 9: Bypass Rate Limits](#-step-9-bypass-rate-limits)
10. [🔗 Step 10: Add All Poe Models](#-step-10-add-all-poe-models)
11. [📜 Step 11: Legal and Ethical Considerations](#-step-11-legal-and-ethical-considerations)

---

## 🔍 **Step 1: Understand Poe.com’s API**

Poe.com is a **frontend** for multiple AI models (GPT-4, Claude, Llama, etc.). It **does not officially provide an API**, but its **web app communicates with a backend API** that we can reverse engineer.

### **How Poe.com Works**

1. **User sends a message** → Poe.com’s frontend sends a request to its backend API.
2. **Backend processes the request** → Forwards it to the respective AI model (GPT-4, Claude, etc.).
3. **AI model responds** → Poe.com’s backend sends the response back to the frontend.

### **Our Goal**

- **Intercept these API calls** using browser DevTools.
- **Mimic the requests** in our own scripts.
- **Build a custom frontend** to interact with Poe.com’s API.

---

## 🕵️ **Step 2: Extract Authentication Token**

Poe.com uses **JWT (JSON Web Token)** for authentication. **Without this token, you cannot access the API.**

### **Steps to Extract Token**

#### **Method 1: From Cookies (Easiest)**

1. Open **Poe.com** in Chrome/Firefox and **log in** (use a burner account if needed).
2. Open **DevTools** (`F12` or `Ctrl+Shift+I`).
3. Go to the **Application** tab → **Cookies** (or **Storage** → **Cookies**).
4. Look for:
  - `next-auth.session-token`
  - `__Secure-next-auth.session-token`
5. **Copy the value** of the token. **This is your golden ticket!**

#### **Method 2: From Authorization Header**

1. Open **DevTools** → **Network tab**.
2. **Filter by `XHR**` (see [XHR Filter Guide](#xhr-filter-kaise-lagana)).
3. Send a message in Poe.com (e.g., "Hello").
4. Find a request to `**/api/gql_POST**` or `**/api/receive_POST**`.
5. Click on the request → **Headers** tab.
6. Look for the `**Authorization**` header:
  ```http
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```
7. **Copy the token** after `Bearer` .

> **⚠️ Note:** The token **expires after some time**. If it stops working, **extract a new one**.

---

## 📡 **Step 3: Identify Key API Endpoints**

Poe.com uses **two main endpoints** for its API:


| Endpoint                           | Purpose                                             | HTTP Method |
| ---------------------------------- | --------------------------------------------------- | ----------- |
| `https://poe.com/api/gql_POST`     | **GraphQL queries** (e.g., list bots, chat history) | POST        |
| `https://poe.com/api/receive_POST` | **Send/receive messages** (real-time chat)          | POST        |


### **How to Find Endpoints**

1. Open **DevTools** → **Network tab** → **Filter by `XHR**`.
2. Send a message in Poe.com.
3. Look for requests to:
  - `/api/gql_POST`
  - `/api/receive_POST`
4. **Right-click** → **Copy** → **Copy as cURL** (for testing).

---

## 💻 **Step 4: Test API with cURL**

Before writing code, **test the API manually** using **cURL**.

### **Example 1: List All Available Bots**

```bash
curl 'https://poe.com/api/gql_POST' \
  -H 'Authorization: Bearer YOUR_TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
  -H 'Referer: https://poe.com/' \
  --data-raw '{
    "query": "query GetBots { bots { id name description } }",
    "variables": {}
  }'
```

**Expected Response:**

```json
{
  "data": {
    "bots": [
      {"id": "GPT-4", "name": "GPT-4", "description": "OpenAI's best model"},
      {"id": "Claude-3", "name": "Claude 3", "description": "Anthropic's latest"},
      {"id": "Llama-3", "name": "Llama 3", "description": "Meta's open model"}
    ]
  }
}
```

### **Example 2: Send a Message to GPT-4**

```bash
curl 'https://poe.com/api/receive_POST' \
  -H 'Authorization: Bearer YOUR_TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' \
  -H 'Referer: https://poe.com/' \
  --data-raw '{
    "query": "mutation SendMessage($input: SendMessageInput!) { sendMessage(input: $input) { id text chatId contextId } }",
    "variables": {
      "input": {
        "botId": "GPT-4",
        "message": "Hello, Poe.com!",
        "chatId": null,
        "contextId": null
      }
    }
  }'
```

**Expected Response:**

```json
{
  "data": {
    "sendMessage": {
      "id": "12345",
      "text": "Hello! How can I assist you today?",
      "chatId": "abc123",
      "contextId": "xyz456"
    }
  }
}
```

---

## 🐍 **Step 5: Automate with Python**

Now, let’s **automate the API calls** using Python.

### **Install Required Libraries**

```bash
pip install requests httpx
```

### **Python Script: List All Bots**

```python
import requests

# Replace with your token
AUTH_TOKEN = "YOUR_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://poe.com/",
}

def get_bots():
    url = "https://poe.com/api/gql_POST"
    payload = {
        "query": "query GetBots { bots { id name description } }",
        "variables": {}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Test
bots = get_bots()
print(bots)
```

### **Python Script: Send a Message**

```python
import requests

def send_message(message, bot_id="GPT-4", chat_id=None, context_id=None):
    url = "https://poe.com/api/receive_POST"
    payload = {
        "query": """
        mutation SendMessage($input: SendMessageInput!) {
          sendMessage(input: $input) {
            id
            text
            chatId
            contextId
          }
        }
        """,
        "variables": {
            "input": {
                "botId": bot_id,
                "message": message,
                "chatId": chat_id,
                "contextId": context_id
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Test
response = send_message("Hello, Poe.com!")
print(response)
```

### **Python Script: Streaming Responses (Real-Time)**

```python
import httpx
import asyncio

async def stream_message(message, bot_id="GPT-4"):
    url = "https://poe.com/api/receive_POST"
    payload = {
        "query": """
        mutation SendMessage($input: SendMessageInput!) {
          sendMessage(input: $input) {
            id
            text
            chatId
            contextId
          }
        }
        """,
        "variables": {
            "input": {
                "botId": bot_id,
                "message": message,
                "chatId": None,
                "contextId": None
            }
        }
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        async for line in response.aiter_lines():
            if line:
                print(line)

# Run
asyncio.run(stream_message("Hello, streaming world!"))
```

---

## 🌐 **Step 6: Build a FastAPI Backend**

Now, let’s **build a backend API** using **FastAPI** to handle requests from our frontend.

### **Install FastAPI**

```bash
pip install fastapi uvicorn
```

### **FastAPI Code (`main.py`)**

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Enable CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replace with your token
AUTH_TOKEN = "YOUR_TOKEN_HERE"

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://poe.com/",
}

# Endpoint to list all bots
@app.get("/bots")
async def list_bots():
    url = "https://poe.com/api/gql_POST"
    payload = {
        "query": "query GetBots { bots { id name description } }",
        "variables": {}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Endpoint to send a message
@app.post("/chat")
async def send_chat_message(request: Request):
    data = await request.json()
    message = data.get("message")
    bot_id = data.get("botId", "GPT-4")
    chat_id = data.get("chatId")
    context_id = data.get("contextId")

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    url = "https://poe.com/api/receive_POST"
    payload = {
        "query": """
        mutation SendMessage($input: SendMessageInput!) {
          sendMessage(input: $input) {
            id
            text
            chatId
            contextId
          }
        }
        """,
        "variables": {
            "input": {
                "botId": bot_id,
                "message": message,
                "chatId": chat_id,
                "contextId": context_id
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### **Test the FastAPI Backend**

1. Run the server:
  ```bash
   python main.py
  ```
2. Open **Postman** or **cURL** to test:
  - **List Bots:**
  - **Send Message:**
    ```bash
    curl -X POST http://localhost:8000/chat \
      -H "Content-Type: application/json" \
      -d '{"message": "Hello, FastAPI!", "botId": "GPT-4"}'
    ```

---

## 🎨 **Step 7: Create a Frontend (HTML/CSS/JS)**

Now, let’s **build a simple frontend** to interact with our FastAPI backend.

### **Folder Structure**

```
poe-chatbot/
├── backend/
│   └── main.py (FastAPI)
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

### **1. `index.html**`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poe.com AI Chatbot</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>🤖 Poe.com AI Chatbot</h1>
        
        <div class="bot-selector">
            <label for="bot">Select AI Model:</label>
            <select id="bot">
                <option value="GPT-4">GPT-4</option>
                <option value="Claude-3">Claude-3</option>
                <option value="Llama-3">Llama-3</option>
                <option value="Mistral">Mistral</option>
            </select>
        </div>

        <div class="chat-container">
            <div id="chat" class="chat-box"></div>
            <div class="input-box">
                <input type="text" id="message" placeholder="Type your message..." autocomplete="off">
                <button id="send">Send</button>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
```

### **2. `style.css**`

```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

.container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    width: 90%;
    max-width: 800px;
    padding: 20px;
}

h1 {
    text-align: center;
    color: #333;
}

.bot-selector {
    margin-bottom: 20px;
}

.bot-selector select {
    width: 100%;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ddd;
    font-size: 16px;
}

.chat-container {
    display: flex;
    flex-direction: column;
    height: 70vh;
}

.chat-box {
    flex: 1;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 15px;
    margin-bottom: 10px;
    background-color: #f9f9f9;
}

.chat-box .message {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
    max-width: 80%;
}

.chat-box .user {
    background-color: #e3f2fd;
    margin-left: auto;
    text-align: right;
}

.chat-box .bot {
    background-color: #f1f1f1;
    margin-right: auto;
}

.input-box {
    display: flex;
    gap: 10px;
}

.input-box input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

.input-box button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

.input-box button:hover {
    background-color: #45a049;
}
```

### **3. `script.js**`

```javascript
const chatBox = document.getElementById('chat');
const messageInput = document.getElementById('message');
const sendButton = document.getElementById('send');
const botSelect = document.getElementById('bot');

// API endpoint (replace with your FastAPI backend URL)
const API_URL = 'http://localhost:8000/chat';

// Add a message to the chat box
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user' : 'bot');
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send a message to the backend
async function sendMessage() {
    const message = messageInput.value.trim();
    const botId = botSelect.value;

    if (!message) return;

    addMessage(message, true);
    messageInput.value = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                botId: botId
            })
        });

        const data = await response.json();
        
        if (data.data && data.data.sendMessage) {
            const botReply = data.data.sendMessage.text;
            addMessage(botReply, false);
        } else {
            addMessage("Error: No response from AI.", false);
        }
    } catch (error) {
        addMessage("Error: Could not connect to AI.", false);
        console.error(error);
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Initial message
addMessage("Hello! I'm your AI assistant. Ask me anything!", false);
```

---

## 🚀 **Step 8: Deploy Your Chatbot**

Now, let’s **deploy your chatbot** so anyone can use it.

### **Option 1: Deploy Backend on Railway**

1. **Sign up** on [Railway](https://railway.app/).
2. **Create a new project** and connect your GitHub repository.
3. **Add environment variables** (e.g., `AUTH_TOKEN`).
4. **Deploy!**

### **Option 2: Deploy Backend on Fly.io**

1. **Install Fly.io CLI**:
  ```bash
   curl -L https://fly.io/install.sh | sh
  ```
2. **Login to Fly.io**:
  ```bash
   fly auth login
  ```
3. **Deploy your FastAPI app**:
  ```bash
   fly launch
  ```
4. **Set environment variables**:
  ```bash
   fly secrets set AUTH_TOKEN=YOUR_TOKEN_HERE
  ```

### **Option 3: Deploy Frontend on Vercel/Netlify**

1. **Sign up** on [Vercel](https://vercel.com/) or [Netlify](https://www.netlify.com/).
2. **Upload your `frontend` folder** (HTML/CSS/JS).
3. **Deploy!**

### **Update Frontend API URL**

After deploying the backend, **update the `API_URL` in `script.js**` to point to your deployed backend:

```javascript
const API_URL = 'https://your-backend-url.railway.app/chat';
```

---

## 🔄 **Step 9: Bypass Rate Limits**

Poe.com **rate-limits** requests. Here’s how to **avoid getting blocked**:

### **1. Rotate User-Agents**

```python
import random

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": random.choice(user_agents),
    "Referer": "https://poe.com/",
}
```

### **2. Use Proxies**

```python
proxies = {
    "http": "http://123.45.67.89:8080",
    "https": "http://123.45.67.89:8080",
}

response = requests.post(url, headers=headers, json=payload, proxies=proxies)
```

**Free Proxies:**

- [FreeProxyList](https://free-proxy-list.net/)
- [HideMy.name](https://hidemy.name/en/proxy-list/)

### **3. Rotate Tokens**

- Create **multiple Poe.com accounts** (use [temp-mail.org](https://temp-mail.org/) for emails).
- Extract tokens from each and **rotate them** in your script.

### **4. Slow Down Requests**

```python
import time
time.sleep(2)  # Wait 2 seconds between requests
```

---

## 🔗 **Step 10: Add All Poe Models**

Poe.com supports **many models**, including:

- **GPT-4** (OpenAI)
- **Claude-3** (Anthropic)
- **Llama-3** (Meta)
- **Mistral** (Mistral AI)
- **Gemini** (Google)
- **And many more!**

### **How to Find All Models**

Use the `**/bots` endpoint** to list all available models:

```python
def get_bots():
    url = "https://poe.com/api/gql_POST"
    payload = {
        "query": "query GetBots { bots { id name description } }",
        "variables": {}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

bots = get_bots()
print(bots)
```

### **Update Frontend Dropdown**

Dynamically load all models in the frontend:

```javascript
// Fetch and populate bot list
async function loadBots() {
    const response = await fetch('http://localhost:8000/bots');
    const data = await response.json();
    const botSelect = document.getElementById('bot');
    
    botSelect.innerHTML = ''; // Clear existing options
    
    data.data.bots.forEach(bot => {
        const option = document.createElement('option');
        option.value = bot.id;
        option.textContent = bot.name;
        botSelect.appendChild(option);
    });
}

// Call on page load
loadBots();
```

---

## 📜 **Step 11: Legal and Ethical Considerations**

> **⚠️ Important:**
>
> - **This guide is for educational purposes only.**
> - **Do not use this to abuse Poe.com’s services.**
> - **Respect Poe.com’s [Terms of Service](https://poe.com/terms).**
> - **Reverse engineering may violate Poe.com’s policies.**
> - **Use at your own risk.**

---

## 🎉 **Conclusion**

You’ve now learned how to:  
✅ **Reverse engineer Poe.com’s API** to access **GPT-4, Claude-3, Llama-3, and more**.  
✅ **Extract authentication tokens** and understand API endpoints.  
✅ **Build a full-stack AI chatbot website** using **FastAPI and JavaScript**.  
✅ **Deploy your chatbot** for free.  
✅ **Bypass rate limits** and **maintain persistent chats**. 

---

## 📚 **Further Improvements**

- **Add more models** (e.g., DALL·E, MidJourney via Poe.com).
- **Implement user accounts** (e.g., Firebase Auth).
- **Add a database** (e.g., SQLite, PostgreSQL) to save chat history.
- **Improve the UI** with frameworks like **React or Vue.js**.
- **Add voice input/output** using Web Speech API.

---

## 🌟 **Contributing**

If you’d like to contribute to this project:

1. **Fork the repository.**
2. **Create a new branch.**
3. **Make your changes.**
4. **Submit a pull request.**

---

## 📜 **License**

This project is **open-source** and available under the **[MIT License](LICENSE)**.

---

## 🙏 **Acknowledgments**

- **Poe.com** for providing access to amazing AI models.
- **FastAPI** for making backend development easy.
- **All open-source contributors** who make tools like this possible.

---

## 📞 **Contact**

For questions or feedback, open an **issue** in the repository.

---

**🚀 Happy Coding! Build something amazing!**
