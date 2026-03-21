"""HTML and Markdown parsers"""

from html.parser import HTMLParser
from typing import Dict, List, Any
import re


class HTMLSpanParser(HTMLParser):
    """Parse HTML to extract formatting spans"""
    
    TAG_MAP = {
        'b': 'bold',
        'strong': 'bold',
        'i': 'italic',
        'em': 'italic',
        's': 'strike',
        'u': 'underline',
        'code': 'monospace',
        'spoiler': 'spoiler',
        'q': 'quote',
    }
    
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.spans: List[Dict[str, Any]] = []
        self.text_parts: List[str] = []
        self.stack: List[tuple] = []
        self.text_offset = 0
    
    def handle_starttag(self, tag: str, attrs: List[tuple]):
        if tag == 'a':
            href = None
            for attr_name, attr_value in attrs:
                if attr_name == 'href' and attr_value:
                    href = attr_value
                    break
            self.stack.append(('a', 'link', self.text_offset, href))
        elif tag in self.TAG_MAP:
            self.stack.append((tag, self.TAG_MAP[tag], self.text_offset, None))
    
    def handle_endtag(self, tag: str):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, span_type, text_start, url = self.stack.pop(i)
                self.spans.append({
                    "offset": text_start,
                    "length": self.text_offset - text_start,
                    "type": span_type,
                    "url": url
                })
                break
    
    def handle_data(self, data: str):
        self.text_parts.append(data)
        self.text_offset += len(data)
    
    def get_text(self) -> str:
        return ''.join(self.text_parts)
    
    def get_spans(self) -> List[Dict[str, Any]]:
        self.spans.sort(key=lambda s: s['offset'])
        return self.spans


def format_html(html: str) -> Dict[str, Any]:
    html = re.sub(r'\|\|(.+?)\|\|', r'<spoiler>\1</spoiler>', html, flags=re.DOTALL)

    parser = HTMLSpanParser()
    parser.feed(html)
    
    return {
        "content": parser.get_text(),
        "spans": parser.get_spans(),
    }


DELIMITERS = {
    '**': 'bold',
    '*': 'italic',
    '~~': 'strike',
    '__': 'underline',
    '`': 'monospace',
    '||': 'spoiler',
    '>': 'quote',
}


def _split_with_delimiters(s: str) -> List[str]:
    """Split text by delimiters while keeping them"""
    escaped_delimiters = [re.escape(d) for d in sorted(DELIMITERS.keys(), key=len, reverse=True)]
    link_pattern = r'\[[^\]]+\]\([^\)]*\)'
    pattern = '(' + '|'.join([r'\\.', link_pattern] + escaped_delimiters) + ')'
    return [t for t in re.split(pattern, s) if t]


def format_markdown(markdown: str) -> Dict[str, Any]:
    """
    Parse Markdown and extract formatting
    
    Supports:
    - **bold**
    - *italic*
    - ~~strike~~
    - __underline__
    - `monospace`
    - ||spoiler||
    - >quote>
    - [text](url)
    
    Example:
        >>> result = format_markdown("**Bold** and *italic* text")
        >>> print(result['content'])
        'Bold and italic text'
        >>> print(result['spans'])
        [
            {'offset': 0, 'length': 4, 'type': 'bold', 'url': None},
            {'offset': 9, 'length': 6, 'type': 'italic', 'url': None}
        ]
    """
    starts = {}
    result = ""
    spans = []
    
    for token in _split_with_delimiters(markdown):
        if token.startswith('\\') and len(token) > 1:
            # Escaped character
            result += token[1]
        elif token in starts:
            # Closing delimiter
            start = starts[token]
            del starts[token]
            spans.append({
                "offset": start,
                "length": len(result) - start,
                "type": DELIMITERS[token],
                "url": None
            })
        elif token in DELIMITERS:
            # Opening delimiter
            starts[token] = len(result)
        elif match := re.match(r'\[([^\]]+)\]\(([^\)]*)\)', token):
            # Link
            text = match.group(1)
            url = match.group(2) or text
            spans.append({
                "offset": len(result),
                "length": len(text),
                "type": "link",
                "url": url
            })
            result += text
        else:
            # Normal text
            result += token
    
    return {
        "content": result,
        "spans": spans,
    }
