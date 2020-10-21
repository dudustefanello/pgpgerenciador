import re
from bs4 import BeautifulSoup

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

    noscript = figure.find('noscript')
    img_src = re.search(r'srcset=".*"', str(noscript)).group(0).split('"')[1].split()[-2]
    return f'<figure><img src="{img_src}" />{get_figcaption(figure.figcaption)}</figure>'

def attrs_filter(attrs):
    return "".join(
        [f'{attr}="{value}" ' for attr, value in attrs.items() if attr in VALID_ATTRS]
    )

def content_filter(tag):
    if not hasattr(tag, "children"):
        return tag

    if tag.name == 'figure':
        return figure_filter(tag)

    to_return = (
        f"<{tag.name} {attrs_filter(tag.attrs)}>"
        + "".join(
            [content_filter(child) for child in tag.children if tag.name in VALID_TAGS]
        )
        + f"</{tag.name}>"
    )

    return to_return


def parse(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    main_content = soup.article.div.section # .encode(formatter="html")

    return content_filter(main_content)
