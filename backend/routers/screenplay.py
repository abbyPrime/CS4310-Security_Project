from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from auth import verify_token
from database import get_db
from models import UploadedFile, FileLine, LineRolePermission, Role

router = APIRouter()
security = HTTPBearer()

ROLES_CAN_UPLOAD = {"screenwriter", "director", "producer"}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload


class LinePermission(BaseModel):
    line_id: int
    roles: List[str]


class PermissionsBody(BaseModel):
    permissions: List[LinePermission]


@router.get("/roles")
def list_roles(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roles = db.query(Role.role_name).distinct().order_by(Role.role_name).all()
    return {"roles": [r.role_name for r in roles]}


@router.get("/screenplays")
def list_screenplays(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from models import User
    from sqlalchemy import distinct

    file_ids_with_lines = db.query(distinct(FileLine.file_id)).subquery()

    files = db.query(UploadedFile, User.username).join(
        User, User.user_id == UploadedFile.uploaded_by
    ).filter(
        UploadedFile.file_id.in_(file_ids_with_lines),
        UploadedFile.is_revoked == False
    ).all()

    return {
        "success": True,
        "screenplays": [
            {
                "file_id": f.UploadedFile.file_id,
                "filename": f.UploadedFile.original_filename,
                "uploaded_by": f.username,
                "uploaded_at": f.UploadedFile.uploaded_at.isoformat() if f.UploadedFile.uploaded_at else None
            }
            for f in files
        ]
    }


@router.post("/upload-screenplay")
async def upload_screenplay(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.get("role", "viewer") not in ROLES_CAN_UPLOAD:
        raise HTTPException(status_code=403, detail="Your role does not have upload permission")

    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported for screenplay upload")

    contents = await file.read()
    try:
        text = contents.decode("utf-8")
    except UnicodeDecodeError:
        text = contents.decode("latin-1")

    user_id = int(current_user.get("sub"))
    db_file = UploadedFile(
        original_filename=file.filename,
        file_data=contents,
        file_size=len(contents),
        content_type="text/plain",
        uploaded_by=user_id
    )
    db.add(db_file)
    db.flush()

    lines = text.splitlines()
    for i, line_content in enumerate(lines, 1):
        db.add(FileLine(file_id=db_file.file_id, line_number=i, content=line_content))

    db.commit()
    return {"success": True, "file_id": db_file.file_id, "line_count": len(lines)}


@router.get("/files/{file_id}/view")
def view_screenplay(
    file_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_role = current_user.get("role", "viewer")

    lines = db.query(FileLine).filter(
        FileLine.file_id == file_id
    ).order_by(FileLine.line_number).all()

    if not lines:
        raise HTTPException(status_code=404, detail="No screenplay lines found for this file")

    result = []
    for line in lines:
        allowed_roles = [p.role_name for p in line.permissions]
        visible = (
            user_role == "producer"
            or not allowed_roles
            or user_role in allowed_roles
        )
        result.append({
            "line_id": line.line_id,
            "line_number": line.line_number,
            "content": line.content if visible else "[REDACTED]",
            "visible": visible,
            "allowed_roles": allowed_roles
        })

    return {"success": True, "lines": result, "user_role": user_role}


@router.put("/files/{file_id}/permissions")
def set_permissions(
    file_id: int,
    body: PermissionsBody,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.get("role") != "producer":
        raise HTTPException(status_code=403, detail="Only producers can set permissions")

    for perm in body.permissions:
        db.query(LineRolePermission).filter(
            LineRolePermission.line_id == perm.line_id
        ).delete()
        for role_name in perm.roles:
            db.add(LineRolePermission(line_id=perm.line_id, role_name=role_name))

    db.commit()
    return {"success": True}
