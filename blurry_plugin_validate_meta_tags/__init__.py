from pathlib import Path
from blurry.types import TemplateContext
from selectolax.parser import HTMLParser
from rich import print

# Research:
# https://developers.google.com/search/docs/appearance/title-link
# https://www.semrush.com/blog/title-tag/
TITLE_LENGTH_MAX = 60
TITLE_LENGTH_MIN = 20

# Research:
# https://developers.google.com/search/docs/appearance/snippet#meta-descriptions
# https://www.semrush.com/blog/meta-description/
DESCRIPTION_LENGTH_MAX = 160
DESCRIPTION_LENGTH_WARN = 105
DESCRIPTION_LENGTH_MIN = 75


def validate_title_tag(parser: HTMLParser, filepath: Path):
    title_tag = parser.css_first("title")
    if not title_tag:
        return f"{filepath}: Title tag missing"

    title = title_tag.text()

    if not title:
        return f"{filepath}: Title content missing"

    title_length = len(title)

    if title_length < TITLE_LENGTH_MIN:
        return f"{filepath}: Title too short ({title_length}); should be {TITLE_LENGTH_MIN}-{TITLE_LENGTH_MAX} characters"
    elif title_length > TITLE_LENGTH_MAX:
        return f"{filepath}: Title too long ({title_length}); should be {TITLE_LENGTH_MIN}-{TITLE_LENGTH_MAX} characters"


def validate_description_tag(parser: HTMLParser, filepath: Path):
    description_tag = parser.css_first("meta[name='description']")
    if not description_tag:
        return f"{filepath}: Meta description tag missing"

    description = description_tag.attrs.get("content")

    if not description:
        return f"{filepath}: Meta description content missing"

    description_length = len(description)

    if description_length < DESCRIPTION_LENGTH_MIN:
        return f"{filepath}: Meta description too short ({description_length}); should be {DESCRIPTION_LENGTH_MIN}-{DESCRIPTION_LENGTH_MAX} characters"
    elif description_length > DESCRIPTION_LENGTH_MAX:
        return f"{filepath}: Meta description too long ({description_length}); should be {DESCRIPTION_LENGTH_MIN}-{DESCRIPTION_LENGTH_MAX} characters"
    elif description_length > DESCRIPTION_LENGTH_WARN:
        return f"{filepath}: Meta description quite long ({description_length}) and may be truncated on smaller devices"


def validate_meta_tags(html: str, context: TemplateContext, release: bool):
    parser = HTMLParser(html)
    filepath = context.get("filepath")

    if not filepath:
        return

    if title_validation_message := validate_title_tag(parser, filepath):
        print(title_validation_message)

    if description_validation_message := validate_description_tag(parser, filepath):
        print(description_validation_message)

    return html
