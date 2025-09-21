from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
import os

from src.application.services.dependency_injection import get_file_storage

router = APIRouter()


@router.get("/")
async def list_reports():
    """List available reports"""
    storage = get_file_storage()
    files = storage.list_files("reports")
    
    reports = []
    for file in files:
        file_path = storage.reports_dir / file
        if file_path.exists():
            stat = file_path.stat()
            reports.append({
                "filename": file,
                "size": stat.st_size,
                "created": stat.st_ctime,
                "format": file.split('.')[-1] if '.' in file else "unknown"
            })
    
    return {"reports": reports}


@router.get("/{filename}")
async def download_report(filename: str):
    """Download a specific report"""
    storage = get_file_storage()
    file_path = storage.reports_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type='application/octet-stream'
    )


@router.delete("/{filename}")
async def delete_report(filename: str):
    """Delete a specific report"""
    storage = get_file_storage()
    file_path = storage.reports_dir / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    
    os.remove(file_path)
    
    return {"message": f"Report {filename} deleted successfully"}