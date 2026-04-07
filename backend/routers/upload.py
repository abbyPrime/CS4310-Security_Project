from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import verify_token
import os
import uuid
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

# Upload directory configuration
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return user info"""
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a file to the server

    - **file**: The file to upload
    - Requires authentication (Bearer token)
    """
    try:
        # Read file content
        contents = await file.read()

        # Check file size
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {MAX_FILE_SIZE / 1024 / 1024} MB"
            )

        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Save file
        with open(file_path, "wb") as f:
            f.write(contents)

        # Return file info
        return {
            "success": True,
            "message": "File uploaded successfully",
            "file_info": {
                "original_filename": file.filename,
                "stored_filename": unique_filename,
                "file_size": len(contents),
                "content_type": file.content_type,
                "uploaded_by": current_user.get("sub"),
                "uploaded_at": datetime.utcnow().isoformat()
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")


@router.get("/uploads")
async def list_uploads(current_user: dict = Depends(get_current_user)):
    """
    List all uploaded files

    - Requires authentication (Bearer token)
    """
    try:
        files = []
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                file_stat = os.stat(file_path)
                files.append({
                    "filename": filename,
                    "size": file_stat.st_size,
                    "modified": datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                })

        return {
            "success": True,
            "files": files,
            "total": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")
