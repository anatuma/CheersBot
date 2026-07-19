# CheersBot

A Telegram bot that replies with 🥂 when your message has main-character energy — or when you literally ask for it.

Drop a deep quote, a chaotic life update, or something with genuine vibe in a group chat. Gemini decides if it deserves a toast. No vibe, no toast. `/cheers` always works if you're impatient.

## What it actually does

- Listens to regular text messages (ignores commands)
- Sends the text to **Google Gemini** with a strict TRUE/FALSE prompt
- Replies with 🥂 when the AI says the message hits
- `/cheers` — instant toast, then tries to delete your command message (permission willing)
- `/start` — wakes the bot up politely

The AI prompt is tuned for emotional weight, memes, slang, and multilingual chaos — not for "please buy milk tomorrow."

## Tech stack

- **Python 3** + **aiogram 3** (async Telegram bot)
- **Google Gemini** (`gemini-2.5-flash`) via `google-genai`
- **Flask** keep-alive server (handy on free hosting that sleeps without traffic)
- **python-dotenv** for secrets

## Project layout

| File | What lives here |
|------|-----------------|
| `handlers.py` | Telegram routes — `/start`, `/cheers`, message listener |
| `ai_service.py` | Gemini call + structured TRUE/FALSE response |
| `prompts.py` | The personality prompt (yes, it's dramatic on purpose) |
| `config.py` | Loads `BOT_TOKEN` and `GEMINI_API_KEY` from env |
| `keep_alive.py` | Tiny Flask ping so the process stays alive |

## Run it locally

1. Create a bot via [@BotFather](https://t.me/BotFather) and grab the token.
2. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   GEMINI_API_KEY=your_gemini_api_key
   ```
5. Start the bot:
   ```bash
   python main.py
   ```

The keep-alive server listens on port `8080` if your host needs something to ping.

## Try this in chat

- Send something flat: *"meeting at 3pm"* → probably silence
- Send something with energy: *"queens don't bother themselves with writing READMEs"* → 🥂
- Type `/cheers` → 🥂, no questions asked
