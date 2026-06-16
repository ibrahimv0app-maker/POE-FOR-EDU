import os
import json
import sqlite3
import time
from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse
import httpx
from dotenv import load_dotenv

load_dotenv()
POE_TOKEN = os.getenv("POE_SESSION_TOKEN")
POE_BASE = "https://poe.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

app = FastAPI(title="POE-EDU Chat — Professional Educational Chat Proxy")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
DB_PATH = os.getenv("DB_PATH", "data.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conv_id TEXT,
            role TEXT,
            bot TEXT,
            content TEXT,
            ts INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


def save_message(conv_id: str, role: str, bot: Optional[str], content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO messages (conv_id, role, bot, content, ts) VALUES (?, ?, ?, ?, ?)",
        (conv_id, role, bot, content, int(time.time())),
    )
    conn.commit()
    conn.close()


def get_history(conv_id: Optional[str] = None, limit: int = 100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if conv_id:
        c.execute(
            "SELECT id, conv_id, role, bot, content, ts FROM messages WHERE conv_id = ? ORDER BY id ASC LIMIT ?",
            (conv_id, limit),
        )
    else:
        c.execute("SELECT id, conv_id, role, bot, content, ts FROM messages ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(id=r[0], conv_id=r[1], role=r[2], bot=r[3], content=r[4], ts=r[5]) for r in rows]


def poe_headers():
    cookie = f"__Secure-next-auth.session-token={POE_TOKEN}" if POE_TOKEN else ""
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Referer": "https://poe.com/",
        "Origin": "https://poe.com",
    }


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/bots")
async def bots():
    # Simple GraphQL query to fetch bots; may need adjustments per account.
    query = "query GetBots { bots { id name description } }"
    payload = {"query": query}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(f"{POE_BASE}/api/gql_POST", headers=poe_headers(), json=payload)
            r.raise_for_status()
            return JSONResponse(r.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
async def history(conv_id: Optional[str] = None, limit: int = 200):
    return JSONResponse(get_history(conv_id, limit))


@app.post("/chat")
async def chat(payload: dict):
    bot = payload.get("bot")
    text = payload.get("text")
    conv_id = payload.get("conv_id") or str(int(time.time()))
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    # store user message
    save_message(conv_id, "user", bot, text)

    # Construct GraphQL sendMessage mutation — may require tuning for your account/bot
    graphql = (
        "mutation SendMessage($input: SendMessageInput!) { sendMessage(input: $input) { id text } }"
    )
    variables = {"input": {"bot": bot or "GPT-4", "text": text}}
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(f"{POE_BASE}/api/gql_POST", headers=poe_headers(), json={"query": graphql, "variables": variables})
            r.raise_for_status()
            j = r.json()
            # Try extract a text reply
            reply = None
            if isinstance(j, dict) and j.get("data") and j["data"].get("sendMessage"):
                reply = j["data"]["sendMessage"].get("text")

            if not reply:
                # Fallback: store raw JSON
                reply = json.dumps(j)

            save_message(conv_id, "bot", bot, reply)
            return JSONResponse({"conv_id": conv_id, "reply": reply, "raw": j})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stream")
async def stream(bot: Optional[str] = None, text: Optional[str] = None, conv_id: Optional[str] = None):
    """Server-Sent Events stream endpoint. It sends incremental data to clients.
    Note: streaming support depends on the remote API. This implementation sends one final message
    as a single SSE event; adapt this to consume chunked responses if Poe exposes them for your account.
    """
    if not text:
        return JSONResponse({"error": "No text provided"}, status_code=400)
    conv_id = conv_id or str(int(time.time()))

    async def event_generator():
        # Save user message
        save_message(conv_id, "user", bot, text)
        # Call Poe
        graphql = (
            "mutation SendMessage($input: SendMessageInput!) { sendMessage(input: $input) { id text } }"
        )
        variables = {"input": {"bot": bot or "GPT-4", "text": text}}
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                r = await client.post(f"{POE_BASE}/api/gql_POST", headers=poe_headers(), json={"query": graphql, "variables": variables})
                r.raise_for_status()
                j = r.json()
                reply = None
                if isinstance(j, dict) and j.get("data") and j["data"].get("sendMessage"):
                    reply = j["data"]["sendMessage"].get("text")
                if not reply:
                    reply = json.dumps(j)
                # Save bot reply
                save_message(conv_id, "bot", bot, reply)
                # Send as a single SSE 'message' event
                yield {"event": "message", "data": reply}
            except Exception as e:
                yield {"event": "error", "data": str(e)}

    return EventSourceResponse(event_generator())
