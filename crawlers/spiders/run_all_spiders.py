import subprocess
import os
import json

SPIDER_NAMES = [
    "gnosis",
    "thelogistics",
    "freightwaves",
    "leadiq",
    "g2",
    "marketsandmarkets"
]

OUTPUT_DIR = "/app/output"
MERGED_FILE = os.path.join(OUTPUT_DIR, "crawlers_output.json")


def run_all_spiders(output_dir: str = OUTPUT_DIR):
    all_articles = []

    for spider in SPIDER_NAMES:
        output_path = os.path.join(output_dir, f"{spider}_output.json")
        print(f"Running spider: {spider} → {output_path}")

        subprocess.run([
            "scrapy", "crawl", spider,
            "-o", output_path,
            "-t", "json"
        ], check=True)

        with open(output_path, "r") as f:
            articles = json.load(f)
            all_articles.extend(articles)

    with open(MERGED_FILE, "w") as f:
        json.dump(all_articles, f, indent=2)

    print(f"Combined output written to {MERGED_FILE}")
