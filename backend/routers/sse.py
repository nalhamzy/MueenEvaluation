"""Server-Sent Events for real-time run progress updates."""

import asyncio
import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import EvaluationRun, ModelOutput, RunStatus, OutputStatus

router = APIRouter()


async def run_progress_stream(run_id: str):
    """Generator that yields SSE events for a run's progress."""
    while True:
        db = SessionLocal()
        try:
            run = db.query(EvaluationRun).filter(EvaluationRun.id == run_id).first()
            if not run:
                yield f"event: error\ndata: {json.dumps({'message': 'Run not found'})}\n\n"
                return

            # Progress event
            yield f"event: progress\ndata: {json.dumps({'processed': run.processed_count, 'total': run.total_articles, 'status': run.status.value if hasattr(run.status, 'value') else run.status})}\n\n"

            # Check recently scored articles
            scored = (
                db.query(ModelOutput)
                .filter(
                    ModelOutput.run_id == run_id,
                    ModelOutput.status == OutputStatus.SCORED,
                )
                .all()
            )
            for output in scored:
                yield f"event: article_scored\ndata: {json.dumps({'article_id': output.article_id, 'overall_score': output.overall_score})}\n\n"

            # Completion check
            if run.status == RunStatus.COMPLETED:
                avg_score = (
                    sum(o.overall_score or 0 for o in scored) / len(scored)
                    if scored else 0
                )
                yield f"event: run_completed\ndata: {json.dumps({'run_id': run_id, 'avg_score': round(avg_score, 2)})}\n\n"
                return

            if run.status == RunStatus.FAILED:
                yield f"event: error\ndata: {json.dumps({'message': run.error_message or 'Run failed'})}\n\n"
                return

        finally:
            db.close()

        await asyncio.sleep(3)


@router.get("/{run_id}/stream")
async def stream_run_progress(run_id: str):
    """SSE endpoint for real-time run progress."""
    return StreamingResponse(
        run_progress_stream(run_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
