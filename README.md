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

### 7. API Endpoints

- `POST /api/login` - Authenticate user and return JWT token
- `POST /api/register` - Register new user

### 8. Project Structure
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
│   ├── .env                 # Environment variables (not in git)
│   ├── requirements.txt     # Python dependencies
│   └── routers/
│       ├── login.py         # Login endpoint
│       └── register.py      # Registration endpoint
├── index.html               # Login page
├── dashboard.html           # Dashboard page
└── README.md               # This file
```
