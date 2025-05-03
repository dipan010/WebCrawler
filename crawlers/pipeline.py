import json
from itemadapter import ItemAdapter
from datetime import datetime
import os

class ArticlePipeline:
    def open_spider(self, spider):
        # Create output file
        self.file_path = "articles_output.json"
        self.file = open(self.file_path, 'w', encoding='utf-8')
        self.file.write('[\n')  # Start of JSON array
        self.first_item = True

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Normalize fields
        adapter['title'] = adapter.get('title', '').strip()
        adapter['author'] = adapter.get('author', '').strip() if adapter.get('author') else None
        adapter['published'] = self.normalize_date(adapter.get('published'))
        adapter['tags'] = [t.strip() for t in adapter.get('tags', [])]

        json_line = json.dumps(adapter.asdict(), ensure_ascii=False, indent=2)
        if not self.first_item:
            self.file.write(',\n')
        self.file.write(json_line)
        self.first_item = False

        return item

    def normalize_date(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str).isoformat()
        except Exception:
            return date_str
