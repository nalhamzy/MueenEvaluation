"""
Full Pipeline Integration Test
===============================
Tests the complete evaluation pipeline end-to-end:
  1. Verify dataset items exist (3 articles with all 4 tasks)
  2. Create an evaluation run with gpt-4o-mini
  3. Run student evaluation (4 LLM calls per article)
  4. Score deterministically (NER, NLI, Coref)
  5. Run LLM judge (Summary)
  6. Generate executive summary report
  7. Verify all scores and outputs

Run with: py -m pytest backend/tests/test_full_pipeline.py -v -s
Requires: OPENAI_API_KEY in .env, 3+ dataset items in DB
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import SessionLocal
from models import (
    Article, DatasetItem, EvaluationRun, ModelOutput,
    ExecutiveSummary, ArticleStatus, RunStatus, OutputStatus,
)
from services.student_service import run_evaluation_task
from services.judge_service import judge_run_task
from services.report_service import generate_report_task
from config import settings


def test_full_pipeline():
    """Run the complete evaluation pipeline end-to-end."""
    db = SessionLocal()
    try:
        api_key = settings.get_student_api_key()
        assert api_key, "No API key - set OPENAI_API_KEY in .env"

        # --- Step 1: Verify dataset items ---
        items = db.query(DatasetItem).filter(
            DatasetItem.generated_at.isnot(None)
        ).all()
        print(f"\n  Step 1: Found {len(items)} dataset items")
        assert len(items) >= 1, "Need at least 1 dataset item"

        for item in items:
            assert item.ner_reference is not None, f"{item.article_id}: missing NER"
            assert item.summary_reference is not None, f"{item.article_id}: missing summary"
            assert item.nli_claims is not None, f"{item.article_id}: missing NLI"
            assert item.coref_reference is not None, f"{item.article_id}: missing coref"
            coref_count = len(item.coref_reference) if isinstance(item.coref_reference, list) else 0
            print(f"    {item.article_id}: NER OK, Summary OK, "
                  f"NLI={len(item.nli_claims)} claims, Coref={coref_count} spans")

        # --- Step 2: Create evaluation run ---
        print(f"\n  Step 2: Creating evaluation run with gpt-4o-mini")
        run = EvaluationRun(
            model_name="gpt-4o-mini",
            total_articles=len(items),
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        run_id = run.id
        print(f"    Run ID: {run_id}")
        assert run.status == RunStatus.QUEUED

        # --- Step 3: Run student evaluation ---
        print(f"\n  Step 3: Running student evaluation ({len(items)} articles x 4 tasks)...")
        run_evaluation_task(run_id, api_key)

        db.refresh(run)
        print(f"    Status: {run.status}")
        print(f"    Processed: {run.processed_count}/{run.total_articles}")
        assert run.status == RunStatus.COMPLETED, f"Run failed: {run.error_message}"
        assert run.processed_count == len(items)

        # --- Step 4: Verify deterministic scores ---
        print(f"\n  Step 4: Checking deterministic scores (NER, NLI, Coref)")
        outputs = db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()
        assert len(outputs) == len(items)

        for out in outputs:
            assert out.ner_score is not None, f"{out.article_id}: missing NER score"
            assert out.nli_score is not None, f"{out.article_id}: missing NLI score"
            assert out.coref_score is not None, f"{out.article_id}: missing coref score"
            print(f"    {out.article_id}: NER={out.ner_score:.1f}, "
                  f"NLI={out.nli_score:.1f}, Coref={out.coref_score:.1f}, "
                  f"Summary={out.summary_score:.1f} (pre-judge)")

        # --- Step 5: Run LLM judge (Summary) ---
        print(f"\n  Step 5: Running LLM judge on summaries...")
        judge_run_task(run_id)

        # Reload outputs
        outputs = db.query(ModelOutput).filter(ModelOutput.run_id == run_id).all()
        for out in outputs:
            assert out.summary_score is not None, f"{out.article_id}: missing summary score"
            assert out.overall_score is not None, f"{out.article_id}: missing overall score"
            print(f"    {out.article_id}: Summary={out.summary_score:.1f} "
                  f"(judged), Overall={out.overall_score:.1f}")
            if out.judge_summary_rubric:
                r = out.judge_summary_rubric
                print(f"      Rubric: factual={r.get('factual_accuracy')}, "
                      f"coverage={r.get('coverage')}, "
                      f"inference={r.get('no_added_inference')}, "
                      f"register={r.get('register_fluency')}")

        # --- Step 6: Generate executive summary ---
        print(f"\n  Step 6: Generating executive summary report...")
        generate_report_task(run_id)

        summary = db.query(ExecutiveSummary).filter(
            ExecutiveSummary.run_id == run_id
        ).first()
        assert summary is not None, "No executive summary generated"
        assert len(summary.content) > 100, "Summary too short"
        print(f"    Report length: {len(summary.content)} chars")
        # Print first 200 chars
        print(f"    Preview: {summary.content[:200]}...")

        # --- Final summary ---
        avg_ner = sum(o.ner_score for o in outputs) / len(outputs)
        avg_nli = sum(o.nli_score for o in outputs) / len(outputs)
        avg_summary = sum(o.summary_score for o in outputs) / len(outputs)
        avg_coref = sum(o.coref_score for o in outputs) / len(outputs)
        avg_overall = sum(o.overall_score for o in outputs) / len(outputs)

        print(f"\n  === PIPELINE COMPLETE ===")
        print(f"  Model: gpt-4o-mini")
        print(f"  Articles evaluated: {len(outputs)}")
        print(f"  Average scores:")
        print(f"    NER:     {avg_ner:.2f} / 10")
        print(f"    NLI:     {avg_nli:.2f} / 10")
        print(f"    Summary: {avg_summary:.2f} / 10")
        print(f"    Coref:   {avg_coref:.2f} / 10")
        print(f"    Overall: {avg_overall:.2f} / 10")
        print(f"  Executive summary: Generated ({len(summary.content)} chars)")
        print(f"  ========================\n")

    finally:
        db.close()
