from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from auth import verify_token
from database import get_db
from models import UploadedFile
from datetime import datetime

router = APIRouter()
security = HTTPBearer()

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 50MB")

    user_id = int(current_user.get("sub"))

    try:
        db_file = UploadedFile(
            original_filename=file.filename,
            file_data=contents,
            file_size=len(contents),
            content_type=file.content_type,
            uploaded_by=user_id
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

    return {
        "success": True,
        "message": "File uploaded successfully",
        "file_info": {
            "file_id": db_file.file_id,
            "original_filename": db_file.original_filename,
            "file_size": db_file.file_size,
            "content_type": db_file.content_type,
            "uploaded_at": db_file.uploaded_at.isoformat() if db_file.uploaded_at else datetime.utcnow().isoformat()
        }
    }


@router.get("/uploads")
async def list_uploads(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(current_user.get("sub"))

    files = db.query(UploadedFile).filter(
        UploadedFile.uploaded_by == user_id,
        UploadedFile.is_revoked == False
    ).order_by(UploadedFile.uploaded_at.desc()).all()

    return {
        "success": True,
        "files": [
            {
                "file_id": f.file_id,
                "filename": f.original_filename,
                "size": f.file_size,
                "content_type": f.content_type,
                "uploaded_at": f.uploaded_at.isoformat() if f.uploaded_at else None
            }
            for f in files
        ],
        "total": len(files)
    }


@router.put("/files/{file_id}/revoke")
async def revoke_file(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    db_file = db.query(UploadedFile).filter(
        UploadedFile.file_id == file_id,
        UploadedFile.uploaded_by == user_id
    ).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    db_file.is_revoked = True
    db.commit()
    return {"success": True, "message": "File revoked"}


@router.get("/download/{file_id}")
async def download_file(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = int(current_user.get("sub"))

    db_file = db.query(UploadedFile).filter(
        UploadedFile.file_id == file_id,
        UploadedFile.uploaded_by == user_id,
        UploadedFile.is_revoked == False
    ).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    return Response(
        content=db_file.file_data,
        media_type=db_file.content_type or "application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{db_file.original_filename}"'}
    )
