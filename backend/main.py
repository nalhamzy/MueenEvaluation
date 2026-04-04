import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import articles, dataset, runs, outputs, scoring, reports, config, sse

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Arabic LLM Benchmark Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router, prefix="/api/articles", tags=["Articles"])
app.include_router(dataset.router, prefix="/api/dataset", tags=["Dataset"])
app.include_router(runs.router, prefix="/api/runs", tags=["Runs"])
app.include_router(outputs.router, prefix="/api/outputs", tags=["Outputs"])
app.include_router(scoring.router, prefix="/api/scoring", tags=["Scoring"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(config.router, prefix="/api/config", tags=["Config"])
app.include_router(sse.router, prefix="/api/runs", tags=["SSE"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
