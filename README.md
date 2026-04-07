# CS4310-Security_Project
An online communication platform that allows users within the filmmaking industry to securely share, update, and manage screenplays with encrypted file uploads.

## Live Demo

### Frontend
https://abbyprime.github.io/CS4310-Security_Project/

### Backend API
**Production:** https://web-production-8b8e1f.up.railway.app
**API Documentation:** https://web-production-8b8e1f.up.railway.app/docs

### Test Credentials
- Username: `testuser` | Password: `password123`
- Username: `admin` | Password: `admin123`
- Username: `demo` | Password: `demo123`

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
- **Secure File Uploads**: JWT-required file upload with 50MB size limit
- **HTTPS/TLS Encryption**: All production traffic encrypted end-to-end
- **Token Verification**: Server-side JWT validation on all protected endpoints
- **File Type Security**: Unique filename generation prevents path traversal attacks

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

### 7. File Upload Feature

The CinemaShare platform includes a secure file upload system for sharing screenplay documents and related files.

#### Using File Upload

1. **Login to Dashboard**
   - Navigate to `http://localhost:3000/dashboard.html` (local) or the production dashboard
   - Must be authenticated with valid JWT token

2. **Upload a File**
   - Click "Choose File" button
   - Select a file from your computer (max 50MB)
   - Click "Upload File"
   - Wait for success confirmation

3. **View Uploaded Files**
   - Click "View Uploaded Files" button
   - See list of all uploaded files with:
     - Filename
     - File size (in KB)
     - Upload date/time

#### Technical Details

**Security Features:**
- ✅ JWT authentication required for all file operations
- ✅ 50MB file size limit to prevent abuse
- ✅ Unique UUID-based filename generation prevents overwrites
- ✅ Files stored in isolated `uploads/` directory
- ✅ User attribution tracking (who uploaded what)

**File Storage:**
- **Local Development:** Files stored in `backend/uploads/`
- **Production (Railway):** Files stored in `/app/uploads/`
  - ⚠️ **Note:** Railway uses ephemeral storage - files are deleted on redeployment
  - For persistent storage, consider adding Railway Volumes or cloud storage (S3)

**API Endpoints:**
```bash
# Upload a file
curl -X POST https://web-production-8b8e1f.up.railway.app/api/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@screenplay.pdf"

# List uploaded files
curl -X GET https://web-production-8b8e1f.up.railway.app/api/uploads \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response Example:**
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "file_info": {
    "original_filename": "screenplay.pdf",
    "stored_filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.pdf",
    "file_size": 1048576,
    "content_type": "application/pdf",
    "uploaded_by": "testuser",
    "uploaded_at": "2026-04-06T20:30:00"
  }
}
```

#### Future Enhancements
- [ ] Database tracking of file metadata
- [ ] Persistent storage via Railway Volumes or AWS S3
- [ ] File preview and download functionality
- [ ] File sharing between production team members
- [ ] File version control and revision history

### 8. Cloud Deployment (Client-Server on Separate Machines with HTTPS)

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

**Step 5: Connect PostgreSQL to Backend Service**
1. Click on your **web service** (not the database)
2. Go to "Variables" tab
3. Click "+ New Variable"
4. Select "Add a Reference" → Choose your PostgreSQL database
5. Select `DATABASE_URL` from the dropdown
6. Railway automatically injects the database connection string

**Step 6: Add Environment Variables**
In the same Variables tab, add:
- `SECRET_KEY`: Click "Add Variable" and paste a random string
  ```bash
  # Generate a secret key (run locally):
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

**Step 7: Configure Deployment Settings**
1. The `railway.json` file in the repository configures:
   - **Builder**: Dockerfile (for custom build)
   - **Root Directory**: `backend/`
   - **Health Check**: `/health` endpoint
   - **Restart Policy**: Automatic restart on failure

2. The `backend/Dockerfile` handles:
   - Python 3.11 slim base image
   - PostgreSQL client installation
   - Dependency installation from `requirements.txt`
   - Application code copying

3. The `backend/start.sh` script:
   - Validates environment variables
   - Initializes database tables
   - Creates test users (if needed)
   - Starts uvicorn server

**Step 8: Generate Public Domain**
1. In your service, click "Settings" tab
2. Under "Networking" section:
   - Click "Generate Domain"
   - You'll get: `https://web-production-xxxxx.up.railway.app`
   - This is your public HTTPS URL!

**Step 9: Deploy & Monitor**
1. Railway automatically deploys on push to main branch
2. Watch the deployment logs in the "Deployments" tab
3. Wait for successful deployment (~3-5 minutes)
4. Look for:
   - "Database tables created successfully"
   - "Test users created"
   - "Starting FastAPI application"
   - "Uvicorn running on..."
   - Health check passing on `/health`

**Step 10: Update Frontend Configuration**
Edit `config.js` and replace with your Railway URL:
```javascript
const config = {
    API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'
        : 'https://your-app-name.up.railway.app',  // Replace with YOUR Railway URL
};
```

**Step 11: Test the Deployment**

**Test Authentication:**
1. Open `index.html` in your browser (from your local machine)
2. Login with test credentials:
   - Username: `testuser`
   - Password: `password123`
3. Check browser DevTools (F12) → Network tab
4. You should see requests going to `https://web-production-xxxxx.up.railway.app`
5. Data is now encrypted with HTTPS! 🔒

**Test File Upload:**
1. After logging in, you'll be on the dashboard
2. Click "Choose File" and select a file
3. Click "Upload File"
4. Click "View Uploaded Files" to see your upload
5. Check Network tab - file upload uses HTTPS with JWT authentication

**Test API Documentation:**
1. Visit: `https://web-production-xxxxx.up.railway.app/docs`
2. Explore interactive API documentation (Swagger UI)
3. Test endpoints directly from the browser

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

**Build fails with "pip: command not found":**
- ✅ **Fixed:** Using Dockerfile instead of Nixpacks auto-detection
- Verify `backend/Dockerfile` exists
- Check `railway.json` specifies `"builder": "DOCKERFILE"`

**Build fails with "python: command not found":**
- ✅ **Fixed:** Dockerfile explicitly installs Python 3.11
- Don't use custom start commands that bypass Dockerfile environment

**Database connection error:**
- Verify PostgreSQL database is added to project
- Check database is **connected** to web service (Variables → Add Reference)
- Look for `DATABASE_URL` in environment variables
- Railway auto-fixes `postgres://` → `postgresql://` in `database.py`

**Module import errors (e.g., "cannot import name 'verify_token'"):**
- ✅ **Fixed:** Added missing functions to `auth.py`
- Check all required functions exist in imported modules
- Verify `__init__.py` exists in `routers/` package

**"Form data requires python-multipart":**
- ✅ **Fixed:** Added `python-multipart==0.0.9` to `requirements.txt`
- File upload requires this dependency for FastAPI

**Health check fails:**
- Check `/health` endpoint returns 200 OK
- Verify uvicorn is starting (look for "Uvicorn running" in logs)
- Increase `healthcheckTimeout` in `railway.json` if needed
- Ensure database initialization completes before healthcheck starts

**Nginx appears instead of Python app:**
- ✅ **Fixed:** Using explicit Dockerfile prevents auto-detection issues
- Don't let Railway auto-detect - use explicit builder configuration

**Frontend can't connect to API:**
- Verify Railway domain is generated (Settings → Networking → Generate Domain)
- Update `config.js` with correct Railway URL
- Check CORS is enabled in `main.py` (should allow all origins for development)
- Look for CORS errors in browser console (F12)

**Files not persisting between deployments:**
- ⚠️ **Expected behavior:** Railway uses ephemeral storage
- Files in `/app/uploads/` are deleted on redeployment
- **Solution:** Use Railway Volumes or cloud storage (AWS S3)

**Deployment succeeds but app crashes immediately:**
- Check Railway Deploy Logs for Python errors
- Verify all environment variables are set correctly
- Look for database connection errors in startup
- Ensure `start.sh` has execute permissions (`chmod +x start.sh`)

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

#### Authentication
- `POST /api/login` - Authenticate user and return JWT token
- `POST /api/register` - Register new user

#### File Management (JWT Required)
- `POST /api/upload` - Upload files (requires authentication)
  - **Headers:** `Authorization: Bearer <token>`
  - **Body:** `multipart/form-data` with file
  - **Max Size:** 50MB
  - **Response:** File metadata including unique filename and upload timestamp

- `GET /api/uploads` - List all uploaded files (requires authentication)
  - **Headers:** `Authorization: Bearer <token>`
  - **Response:** Array of file metadata (filename, size, modified date)

#### Health & Monitoring
- `GET /` - API status and version information
- `GET /health` - Health check endpoint for monitoring
- `GET /docs` - Interactive API documentation (Swagger UI)

### 9. Project Structure
```
CS4310-Security_Project/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── database.py              # Database connection & configuration
│   ├── models.py                # SQLAlchemy ORM models
│   ├── schemas.py               # Pydantic request/response schemas
│   ├── auth.py                  # Authentication & JWT functions
│   ├── init_db.py               # Database initialization script
│   ├── create_test_users.py    # Test user creation script
│   ├── start.sh                 # Production startup script (Railway)
│   ├── build.sh                 # Deployment build script
│   ├── Dockerfile               # Docker container configuration
│   ├── nixpacks.toml            # Nixpacks build configuration
│   ├── .env                     # Environment variables (not in git)
│   ├── .env.example             # Example environment variables
│   ├── requirements.txt         # Python dependencies
│   ├── schema.sql               # Database schema definition
│   ├── uploads/                 # Uploaded files directory (gitignored)
│   └── routers/
│       ├── __init__.py          # Router package initialization
│       ├── login.py             # Login endpoint
│       ├── register.py          # Registration endpoint
│       └── upload.py            # File upload endpoints (NEW)
├── index.html                   # Login page
├── dashboard.html               # Dashboard page with file upload
├── dashboard.css                # Dashboard styling
├── login.css                    # Login page styling
├── config.js                    # API configuration (local/production)
├── railway.json                 # Railway deployment configuration
├── .gitignore                   # Git ignore rules
├── INDIVIDUAL_REPORT.md         # Individual contribution report
└── README.md                    # This file
```

---

## 10. Current Implementation Status

### ✅ Completed Features

- **Authentication System**
  - User registration with hashed passwords
  - JWT-based login system
  - Token-based session management
  - Secure password hashing with unique salts per user

- **Backend API**
  - FastAPI framework with automatic OpenAPI documentation
  - PostgreSQL database with SQLAlchemy ORM
  - RESTful API endpoints for auth and file management
  - CORS configuration for cross-origin requests

- **File Upload System**
  - Secure file upload with JWT authentication
  - 50MB file size limit
  - UUID-based filename generation
  - File listing endpoint
  - User attribution tracking

- **Cloud Deployment**
  - Backend deployed to Railway with HTTPS
  - PostgreSQL database hosted on Railway
  - Automatic SSL/TLS encryption
  - Health monitoring and auto-restart
  - Environment variable management

- **Security Implementations**
  - HTTPS/TLS encryption for all production traffic
  - JWT token expiration (30 minutes)
  - Server-side token validation
  - SQL injection prevention via ORM
  - Password hashing with SHA-256 + salt
  - CORS protection

### 🚧 Planned Enhancements

- **Database File Tracking**
  - Create `uploaded_files` table for metadata
  - Associate files with users and productions
  - Enable file search and filtering

- **Persistent Storage**
  - Railway Volumes integration
  - AWS S3 cloud storage option
  - File backup and recovery

- **Advanced Features**
  - File sharing between team members
  - Role-based access control for files
  - File version control
  - File preview and download functionality
  - Real-time collaboration features

- **Production Hardening**
  - Rate limiting on API endpoints
  - Enhanced error handling
  - Comprehensive logging
  - Performance monitoring
  - Automated backups

---

## 11. Important Notes

### Security Considerations

1. **Environment Variables**: Never commit `.env` files to git. Always use `.env.example` as a template.

2. **JWT Tokens**: Tokens expire after 30 minutes. Users must re-login after expiration.

3. **File Storage**: Railway uses ephemeral storage. Files are deleted on redeployment. For production, implement persistent storage.

4. **CORS**: Current configuration allows all origins (`*`) for development. In production, restrict to specific domains.

5. **Secret Keys**: Always generate strong, random secret keys for production. Never use default values.

### Development Guidelines

1. **Local Development**:
   - Always work in a virtual environment
   - Keep `requirements.txt` updated
   - Test changes locally before pushing

2. **Version Control**:
   - Use feature branches for new features
   - Write clear commit messages
   - Review changes before merging to main

3. **Testing**:
   - Test authentication flow thoroughly
   - Verify file uploads work correctly
   - Check HTTPS connections in production
   - Monitor deployment logs

4. **Documentation**:
   - Update README when adding features
   - Document API changes
   - Keep environment variable examples current

---

## 12. Support and Resources

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- Railway: https://docs.railway.app/
- PostgreSQL: https://www.postgresql.org/docs/
- SQLAlchemy: https://docs.sqlalchemy.org/

### API Testing
- Swagger UI: `/docs` endpoint
- Redoc: `/redoc` endpoint
- Manual testing: Browser DevTools (F12 → Network tab)

### Deployment
- **Railway Dashboard**: https://railway.app/dashboard
- **GitHub Repository**: https://github.com/abbyPrime/CS4310-Security_Project
- **Production API**: https://web-production-8b8e1f.up.railway.app

### Troubleshooting
1. Check deployment logs in Railway dashboard
2. Review browser console for frontend errors
3. Test API endpoints using `/docs` interface
4. Verify environment variables are set correctly
5. Consult this README's troubleshooting sections

---

## 13. Contributors

**Course**: CS4310 - Computer Security
**Institution**: Bowling Green State University
**Project**: CinemaShare - Secure Screenplay Sharing Platform

For questions or issues, please:
1. Check the troubleshooting sections in this README
2. Review deployment logs in Railway dashboard
3. Test using the `/docs` API documentation
4. Consult the `INDIVIDUAL_REPORT.md` for technical implementation details

---

**Last Updated**: April 6, 2026
**Version**: 2.0.0 (with file upload feature)
**Status**: ✅ Production Deployed
