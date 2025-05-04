import json
import os
import pytest
from processing.utils.uploader import upload_raw_file

TEST_FILE = "/app/output/test_raw_upload.json"
TEST_ARTICLES = [
    {
        "title": "Test Upload",
        "url": "https://example.com/raw1",
        "content": "Raw article upload test",
        "publishedAt": "2025-05-01T08:00:00Z"
    },
    {
        "title": "Another Upload",
        "url": "https://example.com/raw2",
        "content": "Second article test",
        "published": "2025-05-02T08:00:00Z"
    }
]

@pytest.fixture(scope="module")
def create_test_raw_file():
    with open(TEST_FILE, "w") as f:
        json.dump(TEST_ARTICLES, f, indent=2)
    yield
    os.remove(TEST_FILE)


def test_upload_raw_file_succeeds(create_test_raw_file):
    try:
        upload_raw_file(TEST_FILE, source="testsource")
    except Exception as e:
        pytest.fail(f"upload_raw_file failed with exception: {e}")
