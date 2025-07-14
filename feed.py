# feed.py
import yaml
import xml.etree.ElementTree as ET

with open('feed.yaml','r') as f:
    data = yaml.safe_load(f)

rss = ET.Element('rss', {'version':'2.0'})
ch  = ET.SubElement(rss, 'channel')

# channel metadata
ET.SubElement(ch, 'title').text       = data['title']
ET.SubElement(ch, 'link').text        = data['link']
ET.SubElement(ch, 'description').text = data['description']
ET.SubElement(ch, 'language').text    = data['language']
ET.SubElement(ch, 'image').text       = data['link'] + data['image']

# each portfolio entry → <item>
for e in data['entries']:
    item = ET.SubElement(ch, 'item')
    ET.SubElement(item, 'title').text       = e['title']
    ET.SubElement(item, 'link').text        = data['link'] + e['link']
    ET.SubElement(item, 'description').text = e['description']
    ET.SubElement(item, 'pubDate').text     = e['date']

ET.ElementTree(rss).write('portfolio.xml',
                          encoding='utf-8',
                          xml_declaration=True)
