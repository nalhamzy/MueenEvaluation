from pydantic import BaseModel, field_serializer
from typing import Optional, Any
from datetime import datetime, date


# --- Article schemas ---

class ArticleOut(BaseModel):
    id: str
    title: str
    body: str
    source: Optional[str] = None
    date: Any = None
    status: str
    created_at: Any = None

    model_config = {"from_attributes": True}


class ArticleUploadResponse(BaseModel):
    total: int
    inserted: int
    skipped: int
    errors: list[str]


# --- Dataset schemas ---

class DatasetItemOut(BaseModel):
    id: str
    article_id: str
    ner_input: Optional[str] = None
    ner_reference: Optional[dict] = None
    summary_input: Optional[str] = None
    summary_reference: Optional[str] = None
    nli_input: Optional[str] = None
    nli_claims: Optional[list] = None
    coref_input: Optional[str] = None
    coref_reference: Optional[list] = None
    translation_input: Optional[str] = None
    translation_reference: Optional[str] = None
    generated_at: Optional[datetime] = None
    teacher_model: Optional[str] = None

    model_config = {"from_attributes": True}


class DatasetStatsOut(BaseModel):
    total_items: int
    completed: int
    pending: int


# --- Run schemas ---

class RunCreate(BaseModel):
    model_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    limit: Optional[int] = None  # max articles to evaluate (None = all)


class RunOut(BaseModel):
    id: str
    model_name: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_articles: int
    processed_count: int
    error_message: Optional[str] = None

    model_config = {"from_attributes": True}


# --- Output schemas ---

class ModelOutputOut(BaseModel):
    id: str
    run_id: str
    dataset_item_id: str
    article_id: str
    ner_output: Optional[dict] = None
    summary_output: Optional[str] = None
    nli_output: Optional[list] = None
    coref_output: Optional[list] = None
    translation_output: Optional[str] = None
    ner_score: Optional[float] = None
    summary_score: Optional[float] = None
    nli_score: Optional[float] = None
    coref_score: Optional[float] = None
    translation_score: Optional[float] = None
    overall_score: Optional[float] = None
    judge_summary_rubric: Optional[dict] = None
    judge_coref_rubric: Optional[dict] = None
    judge_translation_rubric: Optional[dict] = None
    status: str
    error_message: Optional[str] = None
    processed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# --- Scoring schemas ---

class ManualScoreRequest(BaseModel):
    article_id: str
    task: str  # ner | summary | nli | coref | translation
    model_output: str  # raw string or JSON string


class ScoreBreakdown(BaseModel):
    task: str
    score: float
    details: Optional[dict] = None


# --- Config schemas ---

class ConfigOut(BaseModel):
    teacher_model: str
    judge_model: str
    student_models: str
    openai_base_url: Optional[str] = None
    teacher_api_key: str  # masked
    student_api_key: str  # masked
    judge_api_key: str  # masked


class ConfigUpdate(BaseModel):
    teacher_model: Optional[str] = None
    judge_model: Optional[str] = None
    student_models: Optional[str] = None
    openai_base_url: Optional[str] = None
    teacher_api_key: Optional[str] = None
    student_api_key: Optional[str] = None
    judge_api_key: Optional[str] = None
