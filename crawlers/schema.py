import jsonschema

# Define the ArticleItem schema for validation
article_item_schema = {
    "type": "object",
    "properties": {
        "source"        : {"type": ["string", "null"]},
        "title"         : {"type": "string"},
        "author"        : {"type": ["string", "null"]},
        "description"   : {"type": ["string", "null"]},
        "url"           : {"type": "string", "format": "uri"},
        "published"     : {"type": ["string", "null"], "format": "date-time"},
        "content"       : {"type": ["string", "null"]},
        "tags"          : {"type": "array", "items": {"type": "string"}},
        "raw"           : {"type": ["object", "null"]},
        "scraped_at"    : {"type": "string", "format": "date-time"},
    },
    "required": ["title", "url", "scraped_at"],
}

article_item_schema
