# CS4310-Security_Project

Secure screenplay sharing platform for the filmmaking industry with encrypted file uploads and JWT authentication.

## 🔗 Live Demo

- **Frontend**: https://abbyprime.github.io/CS4310-Security_Project/
- **Backend API**: https://web-production-8b8e1f.up.railway.app
- **API Docs**: https://web-production-8b8e1f.up.railway.app/docs

### Test Credentials
- Username: `testuser` | Password: `password123`
- Username: `admin` | Password: `admin123`
- Username: `demo` | Password: `demo123`

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- PostgreSQL 14+

### Setup

```bash
# 1. Create database
createdb cinemashare

# 2. Install dependencies
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment (backend/.env)
DATABASE_URL=postgresql://username@localhost:5432/cinemashare
SECRET_KEY=your-secret-key-here

# 4. Initialize database
python init_db.py
python create_test_users.py

# 5. Run backend
uvicorn main:app --reload

# 6. Run frontend (new terminal)
python3 -m http.server 3000
```

Open `http://localhost:3000/index.html` and login with test credentials.

---

## ✨ Features

### Security
- ✅ SHA-256 password hashing with unique salts
- ✅ JWT authentication (30-min expiration)
- ✅ HTTPS/TLS encryption in production
- ✅ SQL injection prevention via SQLAlchemy ORM
- ✅ CORS protection

### File Upload
- ✅ JWT-required authentication
- ✅ 50MB file size limit
- ✅ UUID-based filename generation
- ✅ User attribution tracking
- ⚠️ **Note**: Files stored in ephemeral storage (deleted on redeploy)

### API
- ✅ FastAPI with automatic OpenAPI docs
- ✅ PostgreSQL database
- ✅ RESTful endpoints
- ✅ Health monitoring

---

## 📡 API Endpoints

### Authentication
- `POST /api/login` - Login and get JWT token
- `POST /api/register` - Register new user

### File Management (Requires JWT)
- `POST /api/upload` - Upload file (max 50MB)
- `GET /api/uploads` - List uploaded files

### Monitoring
- `GET /` - API status
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

---

## ☁️ Deployment (Railway)

### Quick Deploy

1. **Create Railway account**: https://railway.app
2. **Push to GitHub**: `git push origin main`
3. **Create project** in Railway dashboard
4. **Add PostgreSQL database** to project
5. **Connect database** to web service (Variables → Add Reference)
6. **Add environment variable**: `SECRET_KEY`
7. **Generate domain** (Settings → Networking)
8. **Update `config.js`** with your Railway URL

### Deployment Configuration

The project includes:
- `railway.json` - Railway configuration
- `backend/Dockerfile` - Container setup
- `backend/start.sh` - Startup script with DB initialization

### Common Issues

**Build fails**: Check `backend/Dockerfile` exists and `railway.json` has `"builder": "DOCKERFILE"`

**Database error**: Verify PostgreSQL is connected in Variables tab

**Health check fails**: Wait for DB initialization to complete (~2-3 min)

**Files not persisting**: Expected behavior - use Railway Volumes or S3 for persistence

---

## 📁 Project Structure

```
CS4310-Security_Project/
├── backend/
│   ├── routers/          # API endpoints (login, register, upload)
│   ├── main.py           # FastAPI app
│   ├── auth.py           # JWT & password hashing
│   ├── database.py       # PostgreSQL connection
│   ├── models.py         # Database models
│   ├── requirements.txt  # Dependencies
│   └── Dockerfile        # Container config
├── index.html            # Login page
├── dashboard.html        # Dashboard with file upload
├── config.js             # API configuration
└── railway.json          # Deployment config
```

---

## ⚠️ Important Notes

- **Environment Variables**: Never commit `.env` files
- **JWT Tokens**: Expire after 30 minutes
- **File Storage**: Railway uses ephemeral storage - files deleted on redeploy
- **CORS**: Allows all origins (`*`) for development only
- **Secret Keys**: Generate strong random keys for production

---

## 📚 Resources

- **Documentation**: [INDIVIDUAL_REPORT.md](INDIVIDUAL_REPORT.md) - Detailed technical report
- **API Testing**: Use `/docs` endpoint for interactive testing
- **Deployment Logs**: Check Railway dashboard for errors

---

**Course**: CS4310 - Computer Security | **Institution**: BGSU | **Version**: 2.0.0
