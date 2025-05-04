import os
import json
import pytest
from crawlers.spiders.run_all_spiders import run_all_spiders

OUTPUT_DIR = "/app/output"
MERGED_FILE = os.path.join(OUTPUT_DIR, "crawlers_output.json")

@pytest.fixture(scope="module")
def cleanup_output():
    # Clean up before test run
    if os.path.exists(MERGED_FILE):
        os.remove(MERGED_FILE)
    yield
    if os.path.exists(MERGED_FILE):
        os.remove(MERGED_FILE)


def test_run_all_spiders_generates_output(cleanup_output):
    run_all_spiders(output_dir=OUTPUT_DIR)

    assert os.path.exists(MERGED_FILE), "Merged crawlers_output.json not found."

    with open(MERGED_FILE, "r") as f:
        articles = json.load(f)

    assert isinstance(articles, list), "Output is not a list."
    assert len(articles) > 0, "No articles scraped."
    assert all("url" in article for article in articles), "Missing URLs in some articles."
