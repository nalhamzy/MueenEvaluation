"""End-to-end benchmark orchestration script.

Workflow:
  1. Sample 100 articles (20 per category, seed=42)
  2. Reset DB state for those articles
  3. Generate teacher dataset via Anthropic Batch API (50% off)
  4. For each student model:
     a. Run synchronous evaluation
     b. Run GPT-5.2 judge via OpenAI Batch API
     c. Generate executive summary report
  5. Display final cross-model comparison
  6. Save results to benchmark_results_<timestamp>.json

Usage:
    py scripts/run_benchmark.py [--per-category 20] [--seed 42]
                                [--students mistral-large-bedrock,deepseek-reasoner,qwen3.5-397b-a17b]
                                [--no-batch] [--smoke 5]
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
BACKEND_DIR = ROOT / "backend"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(ROOT / "scripts"))

# Import sample function
from sample_100 import sample_articles


# --- Configuration ---

DEFAULT_STUDENTS = [
    "mistral-large-bedrock",
    "deepseek-chat",
    "qwen3.5-397b-a17b",
]


def header(msg: str):
    print()
    print("=" * 70)
    print(f"  {msg}")
    print("=" * 70)


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


# --- Pipeline steps ---

def step_sample(per_category: int, seed: int) -> list[dict]:
    header(f"STEP 1: Sample {per_category * 5} articles (seed={seed})")
    samples = sample_articles(seed=seed, per_category=per_category)
    by_cat: dict[str, int] = {}
    for s in samples:
        cat = (s.get("category") or s.get("source") or "?").lower()
        by_cat[cat] = by_cat.get(cat, 0) + 1

    log(f"Selected {len(samples)} articles:")
    for cat, n in sorted(by_cat.items()):
        log(f"  {cat:<10} {n}")

    # Save audit trail
    out = ROOT / "selected_100.json"
    out.write_text(json.dumps(samples, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Saved: {out}")
    return samples


def step_reset_db(article_ids: list[str]):
    header(f"STEP 2: Reset DB for {len(article_ids)} selected articles")
    from database import SessionLocal
    from models import Article, DatasetItem, ArticleStatus

    db = SessionLocal()
    try:
        # Delete any existing dataset items for these articles
        deleted = db.query(DatasetItem).filter(
            DatasetItem.article_id.in_(article_ids)
        ).delete(synchronize_session=False)
        # Reset article statuses to PENDING
        updated = db.query(Article).filter(
            Article.id.in_(article_ids)
        ).update({Article.status: ArticleStatus.PENDING}, synchronize_session=False)
        db.commit()
        log(f"Deleted {deleted} stale DatasetItems, reset {updated} articles to PENDING")
    finally:
        db.close()


def step_generate_dataset(article_ids: list[str], use_batch: bool):
    header(f"STEP 3: Teacher dataset generation ({'BATCH' if use_batch else 'SYNC'})")
    if use_batch:
        from services.teacher_service import generate_dataset_batch
        log("Using Anthropic Batch API (50% off)")
        generate_dataset_batch(article_ids=article_ids, poll_interval=20)
    else:
        from services.teacher_service import generate_dataset_task
        log("Using synchronous calls (full price)")
        generate_dataset_task(article_ids=article_ids)


def step_create_run(model_id: str, article_ids: list[str]) -> str:
    """Create an evaluation run for a specific list of article IDs."""
    from database import SessionLocal
    from models import EvaluationRun, DatasetItem
    from services.model_registry import get_model_by_id, get_api_key_for_model
    from services.student_service import run_evaluation_task

    db = SessionLocal()
    try:
        registry_model = get_model_by_id(model_id)
        if not registry_model:
            raise ValueError(f"Model {model_id} not in registry")

        actual_model_id = registry_model["model_id"]
        api_key, base_url = get_api_key_for_model(model_id)
        if not base_url:
            base_url = registry_model.get("base_url")
        if not api_key:
            raise ValueError(f"No API key configured for {model_id}")

        # Count only the SELECTED articles that have dataset items
        total = db.query(DatasetItem).filter(
            DatasetItem.generated_at.isnot(None),
            DatasetItem.article_id.in_(article_ids),
        ).count()

        run = EvaluationRun(
            model_name=actual_model_id,
            api_base_url=base_url,
            total_articles=total,
        )
        db.add(run)
        db.commit()
        db.refresh(run)
        run_id = run.id
        log(f"Created run {run_id} for {model_id} ({actual_model_id}) — {total} articles")
    finally:
        db.close()

    # Run synchronously in this thread (we want to wait for it)
    log(f"Running student evaluation (this may take 5-15 min)...")
    run_evaluation_task(run_id, api_key=api_key, article_ids=article_ids)
    return run_id


def step_judge_run(run_id: str, use_batch: bool):
    if use_batch:
        from services.judge_service import judge_run_batch
        log(f"Judging run {run_id} via OpenAI Batch API (50% off)")
        judge_run_batch(run_id, poll_interval=20)
    else:
        from services.judge_service import judge_run_task
        log(f"Judging run {run_id} synchronously")
        judge_run_task(run_id)


def step_generate_report(run_id: str):
    from services.report_service import generate_report_task
    log(f"Generating executive summary for run {run_id}")
    generate_report_task(run_id)


def step_show_run_scores(run_id: str, model_label: str):
    from database import SessionLocal
    from models import ModelOutput, OutputStatus

    db = SessionLocal()
    try:
        outputs = db.query(ModelOutput).filter(
            ModelOutput.run_id == run_id,
            ModelOutput.status == OutputStatus.SCORED,
        ).all()
        if not outputs:
            log(f"No scored outputs for {model_label}")
            return None

        avg = lambda field: round(
            sum(getattr(o, field) or 0 for o in outputs) / len(outputs), 2
        )
        result = {
            "model": model_label,
            "scored": len(outputs),
            "ner": avg("ner_score"),
            "nli": avg("nli_score"),
            "summary": avg("summary_score"),
            "coref": avg("coref_score"),
            "translation": avg("translation_score"),
            "overall": avg("overall_score"),
        }
        log(f"  {model_label}: NER={result['ner']:.2f} NLI={result['nli']:.2f} "
            f"Sum={result['summary']:.2f} Coref={result['coref']:.2f} "
            f"Trans={result['translation']:.2f} Overall={result['overall']:.2f}")
        return result
    finally:
        db.close()


def step_per_category_breakdown(run_results: list[dict]):
    """For each completed run, compute per-category averages."""
    header("PER-CATEGORY BREAKDOWN")
    from database import SessionLocal
    from models import ModelOutput, Article, OutputStatus

    db = SessionLocal()
    try:
        for r in run_results:
            if not r.get("run_id"):
                continue
            outputs = (
                db.query(ModelOutput, Article)
                .join(Article, ModelOutput.article_id == Article.id)
                .filter(
                    ModelOutput.run_id == r["run_id"],
                    ModelOutput.status == OutputStatus.SCORED,
                )
                .all()
            )
            by_cat: dict[str, list] = {}
            for out, art in outputs:
                cat = (art.source or "?").lower()
                by_cat.setdefault(cat, []).append(out.overall_score or 0)

            print(f"\n  {r['model']}:")
            for cat in sorted(by_cat.keys()):
                scores = by_cat[cat]
                avg = sum(scores) / len(scores) if scores else 0
                print(f"    {cat:<10} n={len(scores):>3}  overall={avg:.2f}")
    finally:
        db.close()


# --- Main orchestration ---

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-category", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--students",
        type=str,
        default=",".join(DEFAULT_STUDENTS),
        help="Comma-separated list of student model IDs from registry",
    )
    parser.add_argument("--no-batch", action="store_true",
                        help="Disable Anthropic batch for teacher (use sync calls)")
    parser.add_argument("--judge-batch", action="store_true",
                        help="Use OpenAI batch for judge (requires gpt-4o or other batch-eligible model)")
    parser.add_argument("--smoke", type=int, default=0,
                        help="Override per-category to N for a quick smoke test")
    args = parser.parse_args()

    if args.smoke > 0:
        args.per_category = args.smoke

    use_teacher_batch = not args.no_batch
    use_judge_batch = args.judge_batch  # default OFF — gpt-5.2 doesn't support batch yet
    students = [s.strip() for s in args.students.split(",") if s.strip()]

    started_at = datetime.now()
    header("ARABIC LLM BENCHMARK — END-TO-END RUN")
    log(f"Per-category: {args.per_category} ({args.per_category * 5} total)")
    log(f"Seed: {args.seed}")
    log(f"Students: {', '.join(students)}")
    log(f"Teacher batch: {'ON' if use_teacher_batch else 'OFF'}")
    log(f"Judge batch:   {'ON' if use_judge_batch else 'OFF (sync)'}")

    # Step 1: Sample
    samples = step_sample(args.per_category, args.seed)
    article_ids = [s["id"] for s in samples]

    # Step 2: Reset DB
    step_reset_db(article_ids)

    # Step 3: Generate dataset
    t0 = time.time()
    step_generate_dataset(article_ids, use_batch=use_teacher_batch)
    log(f"Dataset generation took {int(time.time() - t0)}s")

    # Step 4: For each student
    run_results = []
    for student in students:
        header(f"STUDENT: {student}")
        try:
            t1 = time.time()
            run_id = step_create_run(student, article_ids)
            log(f"Evaluation took {int(time.time() - t1)}s")

            t2 = time.time()
            step_judge_run(run_id, use_batch=use_judge_batch)
            log(f"Judging took {int(time.time() - t2)}s")

            try:
                step_generate_report(run_id)
            except Exception as e:
                log(f"Report generation failed: {e}")

            scores = step_show_run_scores(run_id, student)
            if scores:
                scores["run_id"] = run_id
                run_results.append(scores)
        except Exception as e:
            log(f"FAILED for {student}: {e}")
            import traceback
            traceback.print_exc()

    # Step 5: Final comparison
    header("FINAL CROSS-MODEL COMPARISON")
    print()
    print(f"{'Model':<28} {'NER':>6} {'NLI':>6} {'Sum':>6} {'Coref':>6} {'Trans':>6} {'Overall':>8}")
    print("-" * 70)
    for r in run_results:
        print(f"{r['model']:<28} {r['ner']:>6.2f} {r['nli']:>6.2f} "
              f"{r['summary']:>6.2f} {r['coref']:>6.2f} "
              f"{r['translation']:>6.2f} {r['overall']:>8.2f}")

    # Step 6: Per-category breakdown
    step_per_category_breakdown(run_results)

    # Step 7: Save results
    duration = (datetime.now() - started_at).total_seconds()
    results_file = ROOT / f"benchmark_results_{started_at.strftime('%Y%m%d_%H%M%S')}.json"
    results_file.write_text(json.dumps({
        "started_at": started_at.isoformat(),
        "duration_seconds": duration,
        "per_category": args.per_category,
        "seed": args.seed,
        "students": students,
        "teacher_batch": use_teacher_batch,
        "judge_batch": use_judge_batch,
        "results": run_results,
    }, indent=2), encoding="utf-8")

    header("COMPLETE")
    log(f"Total duration: {int(duration)}s ({int(duration/60)}m)")
    log(f"Results saved: {results_file}")


if __name__ == "__main__":
    main()
