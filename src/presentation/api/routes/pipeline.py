from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import Dict, Any
import asyncio

from src.application.services.dependency_injection import get_pipeline_orchestrator

router = APIRouter()


background_tasks = {}


@router.post("/run")
async def run_pipeline(background_tasks: BackgroundTasks):
    """Trigger the data pipeline execution"""
    orchestrator = get_pipeline_orchestrator()
    
    # Run pipeline in background
    task_id = f"pipeline_{int(asyncio.get_event_loop().time())}"
    
    async def pipeline_task():
        try:
            result = await orchestrator.run_full_pipeline()
            background_tasks[task_id] = {"status": "completed", "result": result}
        except Exception as e:
            background_tasks[task_id] = {"status": "failed", "error": str(e)}
    
    background_tasks[task_id] = {"status": "running"}
    background_tasks.add_task(pipeline_task)
    
    return {
        "message": "Pipeline execution started",
        "task_id": task_id
    }


@router.get("/status/{task_id}")
async def get_pipeline_status(task_id: str):
    """Get the status of a pipeline execution"""
    if task_id not in background_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return background_tasks[task_id]


@router.get("/runs")
async def get_pipeline_runs(limit: int = 10):
    """Get recent pipeline runs"""
    orchestrator = get_pipeline_orchestrator()
    runs = orchestrator.database.get_pipeline_runs(limit=limit)
    
    return {
        "runs": [
            {
                "id": run.id,
                "status": run.status,
                "started_at": run.started_at.isoformat(),
                "completed_at": run.completed_at.isoformat() if run.completed_at else None,
                "records_processed": run.records_processed,
                "error_message": run.error_message
            }
            for run in runs
        ]
    }