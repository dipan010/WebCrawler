import json
import os
import pytest
from processing.processUpload import process_articles

TEST_FILE = "/app/output/test_articles.json"
VALID_ARTICLE = {
    "title": " Valid News Article ",
    "description": "A clean test.",
    "content": "Some logistics update.",
    "author": "Alice",
    "url": "https://example.com/valid123",
    "publishedAt": "2025-05-01T12:00:00Z",
    "source": {"name": "Tester News"},
    "scraped_at": "2025-05-01T12:10:00Z"
}

INVALID_ARTICLE = {
    "title": "No URL Here",
    "description": "Missing URL will fail.",
    "content": "Content is fine",
    "author": "Bob"
}

@pytest.fixture(scope="module")
def prepare_test_articles():
    with open(TEST_FILE, "w") as f:
        json.dump([VALID_ARTICLE, INVALID_ARTICLE], f, indent=2)
    yield
    os.remove(TEST_FILE)
    if os.path.exists("/app/output/failed_testsource.json"):
        os.remove("/app/output/failed_testsource.json")

def test_process_articles_with_valid_and_invalid(prepare_test_articles):
    process_articles(TEST_FILE, source="testsource")

    failed_path = "/app/output/failed_testsource.json"
    assert os.path.exists(failed_path), "Expected failure log not found."

    with open(failed_path) as f:
        failed = json.load(f)
        assert any("url" not in article for article in failed), "Invalid article not logged properly."