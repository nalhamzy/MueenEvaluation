from fastapi import APIRouter
from config import settings
from schemas import ConfigOut, ConfigUpdate
from services.model_registry import get_model_registry, get_model_by_id, get_api_key_for_model

router = APIRouter()


def _mask(key: str) -> str:
    if not key:
        return ""
    return key[:8] + "..." + key[-4:] if len(key) > 12 else "****"


@router.get("", response_model=ConfigOut)
def get_config():
    return ConfigOut(
        teacher_model=settings.TEACHER_MODEL,
        judge_model=settings.JUDGE_MODEL,
        student_models=settings.STUDENT_MODELS,
        openai_base_url=settings.OPENAI_BASE_URL,
        teacher_api_key=_mask(settings.get_teacher_api_key()),
        student_api_key=_mask(settings.get_student_api_key()),
        judge_api_key=_mask(settings.get_judge_api_key()),
    )


@router.put("")
def update_config(req: ConfigUpdate):
    if req.teacher_model:
        settings.TEACHER_MODEL = req.teacher_model
    if req.judge_model:
        settings.JUDGE_MODEL = req.judge_model
    if req.student_models:
        settings.STUDENT_MODELS = req.student_models
    if req.openai_base_url is not None:
        settings.OPENAI_BASE_URL = req.openai_base_url
    if req.teacher_api_key:
        settings.TEACHER_API_KEY = req.teacher_api_key
    if req.student_api_key:
        settings.STUDENT_API_KEY = req.student_api_key
    if req.judge_api_key:
        settings.JUDGE_API_KEY = req.judge_api_key
    return {"message": "Config updated"}


@router.get("/models")
def list_models():
    """List all available models from the registry with API key status."""
    models = get_model_registry()
    result = []
    for m in models:
        api_key, _ = get_api_key_for_model(m["id"])
        result.append({
            "id": m["id"],
            "display_name": m["display_name"],
            "model_id": m["model_id"],
            "provider": m["provider"],
            "provider_name": m["provider_name"],
            "category": m["category"],
            "base_url": m["base_url"],
            "has_api_key": bool(api_key),
        })
    return {"models": result}


@router.post("/models/{model_id}/test")
def test_model(model_id: str):
    """Quick connectivity test for a model."""
    model = get_model_by_id(model_id)
    if not model:
        return {"status": "error", "message": f"Model {model_id} not found in registry"}

    api_key, base_url = get_api_key_for_model(model_id)
    if not api_key:
        return {"status": "no_key", "message": f"No API key configured for {model['env_key']}"}

    try:
        from services.llm_client import call_llm
        resp = call_llm(
            api_key=api_key,
            model=model["model_id"],
            system_prompt="Return valid JSON only.",
            user_prompt='Return: {"status": "ok"}',
            base_url=base_url,
            json_mode=True,
        )
        return {"status": "ok", "message": f"Connected to {model['display_name']}", "response": resp[:100]}
    except Exception as e:
        return {"status": "error", "message": str(e)[:200]}
