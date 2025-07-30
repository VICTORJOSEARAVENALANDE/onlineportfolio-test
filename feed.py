# feed.py
"""Generate an RSS feed from ``feed.yaml``.

This script has no external dependencies.  If ``PyYAML`` is available it will
use it to parse the YAML file.  Otherwise a very small YAML reader is used that
understands the limited structure of ``feed.yaml``.
"""

try:  # use PyYAML when installed
    import yaml
except Exception:  # pragma: no cover - PyYAML may not be installed
    yaml = None

import re
import xml.etree.ElementTree as ET


def _load_yaml_simple(path: str) -> dict:
    """Load ``feed.yaml`` when PyYAML isn't installed."""

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    def fold(start: int, indent: int) -> tuple[str, int]:
        out = []
        while start < len(lines) and lines[start].startswith(" " * indent):
            out.append(lines[start].strip())
            start += 1
        return " ".join(out), start

    data: dict[str, str | list] = {}
    entries: list[dict[str, str]] = []
    i = 0
    # top level fields
    pattern = re.compile(r"^(\w+):\s*(.*)$")
    while i < len(lines):
        line = lines[i]
        m = pattern.match(line)
        if m:
            key, val = m.groups()
            if key == "entries":
                i += 1
                break
            if val == ">":
                val, i = fold(i + 1, 2)
            else:
                i += 1
            data[key] = val.strip('"')
            continue
        i += 1

    # parse list entries
    entry_key_re = re.compile(r"^\s*-\s*(\w+):\s*(.*)$")
    sub_key_re = re.compile(r"^\s{4}(\w+):\s*(.*)$")
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = entry_key_re.match(line)
        if m:
            entry = {}
            key, val = m.groups()
            if val == ">":
                val, i = fold(i + 1, 6)
            else:
                i += 1
            entry[key] = val
            while i < len(lines):
                sub = lines[i]
                sub_m = sub_key_re.match(sub)
                if not sub_m:
                    break
                sk, sv = sub_m.groups()
                if sv == ">":
                    sv, i = fold(i + 1, 6)
                else:
                    i += 1
                entry[sk] = sv
            entries.append(entry)
        else:
            i += 1
    data["entries"] = entries
    return data

if yaml is not None:
    with open("feed.yaml", "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
else:
    data = _load_yaml_simple("feed.yaml")

def main() -> None:
    rss = ET.Element('rss', {'version': '2.0'})
    ch = ET.SubElement(rss, 'channel')

    # channel metadata
    ET.SubElement(ch, 'title').text = data['title']
    ET.SubElement(ch, 'link').text = data['link']
    ET.SubElement(ch, 'description').text = data['description']
    ET.SubElement(ch, 'language').text = data['language']
    ET.SubElement(ch, 'image').text = data['link'] + data['image']

    # each portfolio entry → <item>
    for e in data['entries']:
        item = ET.SubElement(ch, 'item')
        ET.SubElement(item, 'title').text = e['title']
        entry_link = e.get('link') or ''
        if entry_link.startswith(('http://', 'https://')):
            link_out = entry_link
        else:
            link_out = data['link'].rstrip('/') + entry_link
        ET.SubElement(item, 'link').text = link_out
        ET.SubElement(item, 'short').text = e['short']
        ET.SubElement(item, 'long').text = e['long']
        ET.SubElement(item, 'date').text = e['date']
        ET.SubElement(item, 'category').text = e.get('category', '')

    ET.ElementTree(rss).write(
        'portfolio.xml', encoding='utf-8', xml_declaration=True
    )


if __name__ == '__main__':
    main()
