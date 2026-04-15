from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./data/benchmark.db"

    # Teacher LLM (Claude Opus for dataset generation)
    TEACHER_MODEL: str = "claude-opus-4-6"
    TEACHER_API_KEY: str = ""

    # Student LLMs
    STUDENT_MODELS: str = "gpt-4o-mini"
    STUDENT_API_KEY: str = ""

    # Judge LLM (GPT-5.2)
    JUDGE_MODEL: str = "gpt-5.2"
    JUDGE_API_KEY: str = ""

    # OpenAI
    OPENAI_BASE_URL: Optional[str] = None
    OPENAI_API_KEY: str = ""

    # Claude / Anthropic
    CLAUDE_API_KEY: str = ""
    CLAUDE_MODEL_LIGHT: str = "claude-haiku-4-5-20251001"

    # Qwen / Dashscope
    QWEN: str = ""

    # AWS Bedrock (Mistral, Llama)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"

    # Optional providers
    MISTRAL_API_KEY: str = ""
    TOGETHER_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    FIREWORKS_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""

    model_config = {
        "env_file": os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"),
        "extra": "ignore",
    }

    def get_teacher_api_key(self) -> str:
        """Teacher uses Claude → return Claude API key."""
        if self.TEACHER_API_KEY:
            return self.TEACHER_API_KEY
        if "claude" in self.TEACHER_MODEL.lower():
            return self.CLAUDE_API_KEY
        return self.OPENAI_API_KEY

    def get_student_api_key(self) -> str:
        return self.STUDENT_API_KEY or self.OPENAI_API_KEY

    def get_judge_api_key(self) -> str:
        """Judge uses GPT → return OpenAI API key."""
        if self.JUDGE_API_KEY:
            return self.JUDGE_API_KEY
        if "claude" in self.JUDGE_MODEL.lower():
            return self.CLAUDE_API_KEY
        return self.OPENAI_API_KEY


settings = Settings()
