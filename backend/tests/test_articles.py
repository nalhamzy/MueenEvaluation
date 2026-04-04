"""Tests for Articles API - upload, list, get."""

import json
import io


SAMPLE_ARTICLES_JSON = [
    {
        "id": 1,
        "title": "عنوان المقال الأول",
        "body": "نص المقال الأول الكامل",
        "source": "aljazeera",
        "date_published": "2026-03-14T16:12:42Z",
    },
    {
        "id": 2,
        "title": "عنوان المقال الثاني",
        "body": "نص المقال الثاني الكامل",
        "source": "alarabiya",
        "date_published": "2026-03-15T10:00:00Z",
    },
]


SAMPLE_CSV = """article_id,title,body,source,date
ART_001,عنوان أول,نص المقال الأول,aljazeera,2026-03-14
ART_002,عنوان ثاني,نص المقال الثاني,alarabiya,2026-03-15
"""


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_upload_json(client):
    content = json.dumps(SAMPLE_ARTICLES_JSON).encode("utf-8")
    resp = client.post(
        "/api/articles/upload",
        files={"file": ("articles.json", content, "application/json")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert data["inserted"] == 2
    assert data["skipped"] == 0
    assert data["errors"] == []


def test_upload_csv(client):
    resp = client.post(
        "/api/articles/upload",
        files={"file": ("articles.csv", SAMPLE_CSV.encode("utf-8"), "text/csv")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert data["inserted"] == 2


def test_upload_deduplication(client):
    content = json.dumps(SAMPLE_ARTICLES_JSON).encode("utf-8")
    # Upload once
    client.post("/api/articles/upload", files={"file": ("a.json", content, "application/json")})
    # Upload again
    resp = client.post("/api/articles/upload", files={"file": ("a.json", content, "application/json")})
    data = resp.json()
    assert data["inserted"] == 0
    assert data["skipped"] == 2


def test_list_articles(client):
    content = json.dumps(SAMPLE_ARTICLES_JSON).encode("utf-8")
    client.post("/api/articles/upload", files={"file": ("a.json", content, "application/json")})

    resp = client.get("/api/articles")
    assert resp.status_code == 200
    articles = resp.json()
    assert len(articles) == 2
    assert articles[0]["status"] == "PENDING"


def test_get_article(client):
    content = json.dumps(SAMPLE_ARTICLES_JSON).encode("utf-8")
    client.post("/api/articles/upload", files={"file": ("a.json", content, "application/json")})

    resp = client.get("/api/articles/ART_001")
    assert resp.status_code == 200
    assert "عنوان" in resp.json()["title"]


def test_get_article_not_found(client):
    resp = client.get("/api/articles/NONEXISTENT")
    assert resp.status_code == 404


def test_upload_missing_body(client):
    bad_data = [{"id": 1, "title": "test", "body": ""}]
    content = json.dumps(bad_data).encode("utf-8")
    resp = client.post(
        "/api/articles/upload",
        files={"file": ("a.json", content, "application/json")},
    )
    data = resp.json()
    assert data["inserted"] == 0
    assert len(data["errors"]) == 1
