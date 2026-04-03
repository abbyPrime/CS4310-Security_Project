# CS4310-Security_Project
A online communication website that will allow users within the filmmaking industry to share, update, and manage screenplays.

## Live Demo
To access the website: click on the following link: https://abbyprime.github.io/CS4310-Security_Project/

---

## Local Development Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 14 or higher
- Virtual environment (recommended)

### 1. Database Setup

#### Install PostgreSQL

**macOS (Homebrew):**
```bash
brew install postgresql@15
```

**Windows:**
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer and follow the setup wizard
3. Remember the password you set for the `postgres` user
4. Add PostgreSQL to PATH during installation (or manually add `C:\Program Files\PostgreSQL\15\bin`)

#### Start PostgreSQL

**macOS:**
```bash
brew services start postgresql@15
```

**Windows:**
PostgreSQL should start automatically after installation. If not:
- Open Services (Win + R, type `services.msc`)
- Find "postgresql-x64-15" and start it
- Or use Command Prompt as Administrator:
```cmd
net start postgresql-x64-15
```

#### Verify it's running
```bash
pg_isready
```

#### Create Database

**macOS/Linux:**
```bash
createdb cinemashare
```

**Windows (using psql):**
```cmd
psql -U postgres
CREATE DATABASE cinemashare;
\q
```

#### Verify Database

**macOS/Linux:**
```bash
psql -l | grep cinemashare
```

**Windows:**
```cmd
psql -U postgres -l
```
Look for `cinemashare` in the list.

### 2. Backend Setup

#### Install Dependencies

**macOS/Linux:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

#### Configure Environment
Edit `backend/.env` and update with your database credentials:

**macOS/Linux:**
```env
DATABASE_URL=postgresql://YOUR_USERNAME@localhost:5432/cinemashare
SECRET_KEY=your-secret-key-change-this-in-production
```
Replace `YOUR_USERNAME` with your system username (find it with `whoami` command).

**Windows:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/cinemashare
SECRET_KEY=your-secret-key-change-this-in-production
```
Replace `YOUR_PASSWORD` with the password you set during PostgreSQL installation.

#### Initialize Database Tables
```bash
python init_db.py
```

**Note:** On macOS/Linux, you might need to use `python3` instead of `python`.

#### Create Test Users
```bash
python create_test_users.py
```

This creates 3 test users:
- Username: `testuser`, Password: `password123`
- Username: `admin`, Password: `admin123`
- Username: `demo`, Password: `demo123`

#### Start Backend Server
```bash
uvicorn main:app --reload
```

Backend will run on: `http://localhost:8000`

**Note:** Make sure you're in the `backend` directory and the virtual environment is activated before running these commands.

### 3. Frontend Setup

#### Serve Frontend Files
In a new terminal, from the project root:

**macOS/Linux:**
```bash
python3 -m http.server 8080
```

**Windows:**
```cmd
python -m http.server 8080
```

**Or** simply open `index.html` directly in your browser (may have CORS issues with some browsers).

Frontend will run on: `http://localhost:8080`

### 4. Testing the Login Function

#### Test Steps:
1. Open `http://localhost:8080/index.html` in your browser
2. Enter test credentials:
   - Username: `testuser`
   - Password: `password123`
3. Click "Submit"
4. Should redirect to `dashboard.html` on success
5. Check browser console (F12) for any errors

#### View Database Users

**macOS/Linux:**
```bash
psql -d cinemashare -c "SELECT user_id, username, created_at FROM users;"
```

**Windows:**
```cmd
psql -U postgres -d cinemashare -c "SELECT user_id, username, created_at FROM users;"
```

#### View Password Hashes (for security verification)

**macOS/Linux:**
```bash
psql -d cinemashare -c "SELECT user_id, username, LEFT(password_hash, 20) as hash_preview, LEFT(salt, 20) as salt_preview FROM users;"
```

**Windows:**
```cmd
psql -U postgres -d cinemashare -c "SELECT user_id, username, LEFT(password_hash, 20) as hash_preview, LEFT(salt, 20) as salt_preview FROM users;"
```

### 5. Security Features Implemented

- **Password Hashing**: SHA-256 with unique salt per user
- **Salt Storage**: Each password has a unique random salt
- **JWT Authentication**: Stateless authentication with 30-minute expiration
- **Token Storage**: JWT stored in localStorage
- **Generic Error Messages**: Prevents username enumeration
- **CORS Configuration**: Controlled cross-origin requests

### 6. Troubleshooting

#### Backend won't start
- Check if PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in `.env` file
- Check if port 8000 is already in use

#### Login fails with connection error
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify frontend can reach backend

#### Database connection error
- **macOS/Linux:** Verify database exists: `psql -l | grep cinemashare`
- **Windows:** Verify database exists: `psql -U postgres -l`
- Check DATABASE_URL format:
  - macOS/Linux: `postgresql://username@localhost:5432/cinemashare`
  - Windows: `postgresql://postgres:password@localhost:5432/cinemashare`
- Ensure PostgreSQL is running

#### "Invalid username or password" error
- **macOS/Linux:** Verify test users exist: `psql -d cinemashare -c "SELECT * FROM users;"`
- **Windows:** Verify test users exist: `psql -U postgres -d cinemashare -c "SELECT * FROM users;"`
- Re-run `python create_test_users.py` if needed
- Check password is correct (case-sensitive)

#### Windows-specific issues
- **psql command not found:** Add PostgreSQL bin directory to PATH: `C:\Program Files\PostgreSQL\15\bin`
- **Permission denied when creating database:** Make sure you're using an Administrator command prompt or use `psql -U postgres`
- **Virtual environment activation fails:** Use `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell, then try `.venv\Scripts\Activate.ps1`

### 7. Cloud Deployment (Client-Server on Separate Machines with HTTPS)

This section explains how to deploy the backend to a cloud service with HTTPS encryption, meeting the security requirement of having client and server on separate machines with secure data transfer.

#### Why Deploy to Cloud?
- **Separate Machines**: Server runs in the cloud, client accesses from your local machine
- **HTTPS/TLS Encryption**: All data (passwords, tokens) encrypted in transit
- **Security**: Meets requirement for secure data transfer between client and server
- **Free Tier Available**: No cost for demonstration

#### Deployment Steps (Using Railway - Recommended)

**Step 1: Create Railway Account**
1. Go to https://railway.app
2. Click "Login" and sign in with GitHub
3. Authorize Railway to access your repositories

**Step 2: Push Code to GitHub**
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

**Step 3: Create New Project on Railway**
1. In Railway dashboard, click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `CS4310-Security_Project` repository
4. Railway will auto-detect it's a Python app

**Step 4: Add PostgreSQL Database**
1. In your Railway project, click "New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable
   - Connect it to your backend service

**Step 5: Configure Environment Variables**
1. Click on your web service (not the database)
2. Go to "Variables" tab
3. Add these variables:
   - `DATABASE_URL`: Should already be set automatically
   - `SECRET_KEY`: Click "Add Variable" and paste a random string
     ```bash
     # Generate a secret key (run locally):
     python -c "import secrets; print(secrets.token_hex(32))"
     ```
   - `PYTHON_VERSION`: `3.14` (if needed)

**Step 6: Configure Deployment**
Railway should auto-detect settings, but verify:
1. Click "Settings" tab
2. Check:
   - **Root Directory**: Leave empty (or set to `.`)
   - **Build Command**: Auto-detected from `railway.json`
   - **Start Command**: Auto-detected from `railway.json`
3. Under "Networking":
   - Click "Generate Domain" to get your public URL
   - You'll get something like: `https://your-app-name.up.railway.app`

**Step 7: Deploy**
1. Railway will automatically deploy on push to main
2. Watch the deployment logs
3. Wait for "Build successful" and "Deployment live" (3-5 minutes)
4. Copy your public URL

**Step 8: Update Frontend Configuration**
Edit `config.js` and replace with your Railway URL:
```javascript
const config = {
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'
        : 'https://your-app-name.up.railway.app',  // Replace with YOUR Railway URL
};
```

**Step 9: Test the Deployment**
1. Open `index.html` in your browser (from your local machine)
2. Login with test credentials:
   - Username: `testuser`
   - Password: `password123`
3. Check browser DevTools (F12) → Network tab
4. You should see requests going to `https://your-app-name.up.railway.app`
5. Data is now encrypted with HTTPS! 🔒

#### Verify Secure Connection
1. Open browser DevTools (F12)
2. Go to Network tab
3. Login and watch the `/api/login` request
4. You'll see:
   - ✅ Protocol: `https` (encrypted with TLS)
   - ✅ Status: `200 OK`
   - ✅ Server: Running on Railway cloud (separate machine)
   - ✅ Client: Your local machine

**This satisfies the requirement:**
- ✅ Client and server on separate machines (Cloud vs Local)
- ✅ Data transfers securely via HTTPS/TLS encryption
- ✅ Passwords and tokens encrypted in transit
- ✅ Different physical locations (Railway datacenter vs your laptop)

#### Troubleshooting Railway Deployment

**Build fails:**
- Check logs in Railway dashboard
- Verify `requirements.txt` is in `backend/` folder
- Make sure `init_db.py` and `create_test_users.py` exist

**Database connection error:**
- Verify PostgreSQL database is added to project
- Check `DATABASE_URL` is set in environment variables
- Database should be in same Railway project

**Frontend can't connect:**
- Verify Railway domain is generated (Settings → Networking)
- Check `config.js` has correct Railway URL
- Look for CORS errors in browser console

**App crashes on startup:**
- Check Railway logs for errors
- Verify `PORT` environment variable is used: `--port $PORT`
- Make sure all dependencies are in `requirements.txt`

---

#### Alternative: Deployment Steps (Using Render)

**Step 1: Create Render Account**
1. Go to https://render.com and sign up
2. Connect your GitHub account

**Step 2: Push Code to GitHub**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**Step 3: Create PostgreSQL Database**
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name: `cinemashare-db`
3. Database: `cinemashare`
4. User: `cinemashare_user`
5. Region: Choose closest to you
6. Plan: **Free**
7. Click "Create Database"
8. Copy the "Internal Database URL" (starts with `postgresql://`)

**Step 4: Deploy Backend**
1. In Render dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `cinemashare-api`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `bash build.sh`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: **Free**

4. Add Environment Variables (click "Advanced"):
   - `DATABASE_URL`: Paste the Internal Database URL from Step 3
   - `SECRET_KEY`: Generate a random string (e.g., `openssl rand -hex 32`)
   - `PYTHON_VERSION`: `3.14`

5. Click "Create Web Service"
6. Wait for deployment (5-10 minutes)
7. Copy your service URL (e.g., `https://cinemashare-api.onrender.com`)

**Step 5: Update Frontend Configuration**
Edit `config.js` and update the production URL:
```javascript
const config = {
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'
        : 'https://YOUR-SERVICE-NAME.onrender.com',  // Replace with your Render URL
};
```

**Step 6: Test the Deployment**
1. Open `index.html` in your browser (from your local machine)
2. Login with test credentials:
   - Username: `testuser`
   - Password: `password123`
3. Check browser console - you should see requests going to `https://your-service.onrender.com`
4. Data is now encrypted with HTTPS! 🔒

#### Verify Secure Connection
1. Open browser DevTools (F12)
2. Go to Network tab
3. Login and watch the `/api/login` request
4. You'll see:
   - ✅ Protocol: `https` (encrypted)
   - ✅ Status: `200 OK`
   - ✅ Server: Running on Render (separate machine)
   - ✅ Client: Your local machine

**This satisfies the requirement:**
- ✅ Client and server on separate machines
- ✅ Data transfers securely via HTTPS/TLS encryption
- ✅ Passwords and tokens encrypted in transit

#### Alternative: Deploy Frontend to GitHub Pages
To have the frontend also hosted separately:

1. Push code to GitHub
2. Go to repository Settings → Pages
3. Source: Deploy from main branch, root folder
4. Save
5. Access at: `https://your-username.github.io/CS4310-Security_Project/`

Now both client AND server are on separate machines with HTTPS!

### 8. API Endpoints

- `POST /api/login` - Authenticate user and return JWT token
- `POST /api/register` - Register new user

### 9. Project Structure
```
CS4310-Security_Project/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication functions
│   ├── init_db.py           # Database initialization script
│   ├── create_test_users.py # Test user creation script
│   ├── build.sh             # Deployment build script
│   ├── .env                 # Environment variables (not in git)
│   ├── .env.example         # Example environment variables
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── login.py         # Login endpoint
│       └── register.py      # Registration endpoint
├── index.html               # Login page
├── dashboard.html           # Dashboard page
├── config.js                # API configuration (local/production)
├── railway.json             # Railway deployment configuration
├── Procfile                 # Alternative deployment configuration
├── render.yaml              # Render deployment configuration (alternative)
├── .gitignore               # Git ignore rules
└── README.md                # This file
```
