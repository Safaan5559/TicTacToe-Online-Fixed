# Tic Tac Toe Online — portable rebuild

A Replit-independent Tic-Tac-Toe project with a static frontend and optional Tornado backend.

## What was fixed
- Removed Replit CDN/pill dependencies and mirrored HTTrack paths from the published app.
- Replaced the fragile bundled React entry with a small dependency-free frontend.
- Fixed GitHub Pages compatibility: lowercase `index.html`, root-relative assets and no server-only code required for local/AI play.
- Added a real Python/Tornado backend with SQLite, rooms, WebSocket moves, chat, friends, challenges, leaderboard and admin endpoints.
- Added Render configuration and a correct GitHub Pages Actions workflow.

## Features
- Local two-player mode
- Easy AI
- Unbeatable minimax AI
- Online rooms with five-character codes
- Real-time moves and chat
- SQLite leaderboard/stats
- Friends and challenge API
- Optional WebRTC voice can be added through the WebSocket signaling layer
- Guest mode

## GitHub Pages
GitHub Pages can host the static frontend only. Deploy `server.py` to Render/Railway/VPS for online features, then set the backend URL from the **Server** button or edit `config.js`.

## Backend
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ADMIN_KEY='choose-a-long-random-secret' python server.py
```
Open `http://localhost:5000`.

## Render
The included `render.yaml` can create the Python web service. Set a strong `ADMIN_KEY`. After deployment, copy the service URL into the site's Server setting.

## Security
The rebuilt backend intentionally does not pretend that GitHub Pages can provide authentication. User IDs are device-generated. For a production public deployment, put authentication (Clerk/OIDC or signed sessions) in front of protected user/admin operations and use a persistent database instead of Render's ephemeral filesystem.

## Files
- `index.html`, `app.css`, `app.js`, `config.js` — static frontend
- `server.py` — Tornado API/WebSocket backend
- `guest.html` — guest entry
- `admin.html` — backend admin helper
- `render.yaml`, `Procfile`, `requirements.txt` — deployment
- `.github/workflows/deploy.yml` — GitHub Pages deployment

Made by **Safaan** 🎮
