# Tic Tac Toe Online - Full Stack Game

A real-time multiplayer Tic Tac Toe game with user authentication, friends system, and live challenges.

## Features

- 🎮 **Real-time Multiplayer** - Play online with friends via WebSocket
- 👥 **Friends System** - Add friends and send challenges
- 🏆 **Leaderboard** - Ranked by wins
- 🎯 **Challenges** - Send and accept game challenges
- 📊 **Stats Tracking** - Wins, losses, draws
- 🔐 **Secure Auth** - Clerk integration
- 💬 **In-game Chat** - Communicate during games

## Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript (React)
- WebSocket for real-time communication

**Backend:**
- Python 3.8+
- Tornado (async web framework)
- SQLite database
- Clerk authentication

## Local Setup

### Prerequisites
- Python 3.8+
- Node.js (for frontend assets)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Safaan5559/TicTacToe-Online-Fixed.git
   cd TicTacToe-Online-Fixed
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   python server.py
   ```

4. **Access the application**
   - Open browser: `http://localhost:5000`
   - Server runs on port `5000`

## Deployment

### Option 1: Deploy on Render.com (Recommended)

1. **Create Render account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Connect your repository**
   - New → Web Service
   - Connect your GitHub repo
   - Select: `Safaan5559/TicTacToe-Online-Fixed`

3. **Configure deployment**
   - **Name:** tictactoe-online
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python server.py`
   - **Plan:** Free tier available

4. **Set environment variables** (if needed)
   - Add any required secrets in Render dashboard

5. **Deploy**
   - Click "Deploy"
   - Your app will be live at: `https://tictactoe-online.onrender.com`

---

### Option 2: Deploy on Railway.app

1. **Create Railway account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create new project**
   - New Project → Deploy from GitHub repo
   - Select: `Safaan5559/TicTacToe-Online-Fixed`

3. **Railway auto-detects** `Procfile` and deploys automatically

4. **Your app is live!**
   - Railway generates a public URL

---

### Option 3: Deploy on PythonAnywhere

1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload code**
   - Upload files or clone from GitHub

3. **Configure web app**
   - Set Python version: 3.8+
   - Configure WSGI file
   - Set virtualenv

4. **Configure static/media files**
   - Map routes for `*.js`, `*.css`, `*.html`

5. **Reload web app** → Live!

---

### Option 4: Deploy on Heroku (Paid)

> Note: Heroku free tier ended. Use Render or Railway instead.

---

## API Endpoints

### User Management
- `GET /api/user/status?userId=...` - Get user profile
- `GET /api/user/check-username?username=...` - Check username availability
- `POST /api/user/register` - Register new user
- `GET /api/users` - Get leaderboard

### Real-time Multiplayer
- `WS /api/ws` - WebSocket connection for game

### Friends
- `GET /api/friends?userId=...` - Get friends list
- `POST /api/friends/request` - Send friend request
- `POST /api/friends/respond` - Accept/decline friend request

### Challenges
- `POST /api/challenges/send` - Send game challenge
- `GET /api/challenges/incoming?userId=...` - Get incoming challenges
- `POST /api/challenges/dismiss` - Dismiss challenge

### Admin
- `POST /api/admin/setup` - Set admin user
- `GET /api/admin/verify?userId=...` - Verify admin status
- `GET /api/admin/users?userId=...` - List all users (admin only)
- `POST /api/admin/delete-user` - Delete user (admin only)
- `POST /api/admin/reset-platform` - Reset platform (admin only)

## File Structure

```
TicTacToe-Online-Fixed/
├── server.py                 # Python Tornado backend
├── index.html               # React frontend entry
├── guest.html               # Guest mode page
├── admin.html               # Admin dashboard
├── app.js                   # Frontend logic
├── app.css                  # Frontend styles
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment config
└── .gitignore              # Git ignore rules
```

## Environment Variables

Create `.env` file (not committed to git):

```
PORT=5000
DB_PATH=users.db
ADMIN_EMAIL=your@email.com
```

## Database

SQLite database includes tables:
- `users` - User profiles and stats
- `friends` - Friend relationships
- `challenges` - Game challenges
- `donate_taps` - Donation tracking

Database is auto-initialized on first run.

## Security Notes

- ✅ Use HTTPS in production
- ✅ Validate all user inputs
- ✅ Protect admin endpoints
- ✅ Rotate secrets regularly
- ✅ Never commit `.env` or `admin_config.json`

## Troubleshooting

**Port already in use:**
```bash
python server.py --port 5001
```

**Database locked:**
```bash
rm users.db
python server.py  # Reinitialize
```

**WebSocket connection fails:**
- Check browser console for errors
- Ensure server is running
- Check CORS/origin settings

## Support

Made by **Safaan** 🎮

For issues, create a GitHub Issue: [Issues](https://github.com/Safaan5559/TicTacToe-Online-Fixed/issues)

## License

MIT License - Feel free to use and modify!
