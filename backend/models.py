import uuid
import enum
from datetime import datetime, date
from sqlalchemy import (
    String, Text, Date, DateTime, Float, Integer, Enum, JSON, ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


def gen_uuid() -> str:
    return str(uuid.uuid4())


# --- Enums ---

class ArticleStatus(str, enum.Enum):
    PENDING = "PENDING"
    GENERATING = "GENERATING"
    READY = "READY"
    ERROR = "ERROR"


class RunStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class OutputStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SCORED = "SCORED"
    ERROR = "ERROR"


# --- Models ---

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=True)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[ArticleStatus] = mapped_column(
        Enum(ArticleStatus), default=ArticleStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    dataset_item: Mapped["DatasetItem | None"] = relationship(back_populates="article")


class DatasetItem(Base):
    __tablename__ = "dataset_items"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    article_id: Mapped[str] = mapped_column(ForeignKey("articles.id"), unique=True)

    ner_input: Mapped[str | None] = mapped_column(Text, nullable=True)
    ner_reference: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    summary_input: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary_reference: Mapped[str | None] = mapped_column(Text, nullable=True)

    nli_input: Mapped[str | None] = mapped_column(Text, nullable=True)
    nli_claims: Mapped[list | None] = mapped_column(JSON, nullable=True)

    coref_input: Mapped[str | None] = mapped_column(Text, nullable=True)
    coref_reference: Mapped[list | None] = mapped_column(JSON, nullable=True)

    translation_input: Mapped[str | None] = mapped_column(Text, nullable=True)
    translation_reference: Mapped[str | None] = mapped_column(Text, nullable=True)

    generated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    teacher_model: Mapped[str | None] = mapped_column(String, nullable=True)

    article: Mapped[Article] = relationship(back_populates="dataset_item")


class EvaluationRun(Base):
    __tablename__ = "evaluation_runs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    api_base_url: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.QUEUED)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    total_articles: Mapped[int] = mapped_column(Integer, default=0)
    processed_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    outputs: Mapped[list["ModelOutput"]] = relationship(back_populates="run")


class ModelOutput(Base):
    __tablename__ = "model_outputs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    run_id: Mapped[str] = mapped_column(ForeignKey("evaluation_runs.id"))
    dataset_item_id: Mapped[str] = mapped_column(ForeignKey("dataset_items.id"))
    article_id: Mapped[str] = mapped_column(ForeignKey("articles.id"))

    ner_output: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    summary_output: Mapped[str | None] = mapped_column(Text, nullable=True)
    nli_output: Mapped[list | None] = mapped_column(JSON, nullable=True)
    coref_output: Mapped[list | None] = mapped_column(JSON, nullable=True)
    translation_output: Mapped[str | None] = mapped_column(Text, nullable=True)

    ner_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    summary_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    nli_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    coref_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    translation_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    overall_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    judge_summary_rubric: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    judge_coref_rubric: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    judge_translation_rubric: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    status: Mapped[OutputStatus] = mapped_column(
        Enum(OutputStatus), default=OutputStatus.PENDING
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    run: Mapped[EvaluationRun] = relationship(back_populates="outputs")
    dataset_item: Mapped[DatasetItem] = relationship()
    article: Mapped[Article] = relationship()


class ExecutiveSummary(Base):
    __tablename__ = "executive_summaries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    run_id: Mapped[str | None] = mapped_column(
        ForeignKey("evaluation_runs.id"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LLMCallLog(Base):
    __tablename__ = "llm_call_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    model: Mapped[str] = mapped_column(String)
    prompt_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    success: Mapped[bool] = mapped_column(default=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    task_type: Mapped[str | None] = mapped_column(String, nullable=True)
