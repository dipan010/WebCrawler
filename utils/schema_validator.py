from crawlers.schema import article_item_schema
from jsonschema import validate, ValidationError

def is_valid_article(article: dict) -> bool:
    try:
        validate(instance=article, schema=article_item_schema)
        return True
    except ValidationError as ve:
        print(f"Validation error: {ve.message}")
        return False