import re
from bs4 import BeautifulSoup
from django.utils.html import escape

VALID_TAGS = {
    "a",
    "p",
    "br",
    "div",
    "pre",
    "span",
    "strong",
    "em",
    "h1",
    "h2",
    "h3",
    "article",
    "section",
}
VALID_ATTRS = {"href", "src"}
SELF_CLOSING_TAGS = {"a", "br"}


def figure_filter(figure):
    def get_figcaption(figcaption):
        return content_filter(figcaption) if figcaption else ""

    noscript = figure.find("noscript")
    if noscript is None:
        return ""
    img_src = re.search(r'et=".*"', str(noscript)).group(0).split('"')[1].split()[-2]
    return (
        f'<figure><img src="{img_src}" style="max-width: 100%" />'
        f'{get_figcaption(figure.figcaption)}</figure>'
    )


def attrs_filter(attrs):
    return "".join(
        [f'{attr}="{value}" ' for attr, value in attrs.items() if attr in VALID_ATTRS]
    )


def content_filter(tag):
    if not hasattr(tag, "contents"):
        return escape(str(tag))

    if tag.name == "figure":
        return figure_filter(tag)

    tag_content = "".join(
            [content_filter(child) for child in tag.children if tag.name in VALID_TAGS]
        )

    if tag_content:
        return (
            f"<{tag.name} {attrs_filter(tag.attrs)}>"
            + tag_content
            + f"</{tag.name}>"
        )

    return ""


def parse(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    main_content = soup.article

    return content_filter(main_content)
