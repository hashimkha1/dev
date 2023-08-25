# custom_tags.py
from django import template
import json

register = template.Library()

@register.filter
def format_dynamic_fields(value):
    try:
        dynamic_fields = json.loads(value)
        formatted_fields = []
        for field_name, field_value in dynamic_fields.items():
            formatted_field = f"<strong>{field_name}:</strong> {field_value}"
            formatted_fields.append(formatted_field)
        return "<br>".join(formatted_fields)
    except (json.JSONDecodeError, AttributeError):
        return ""
