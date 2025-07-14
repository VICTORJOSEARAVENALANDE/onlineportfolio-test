import yaml
import xml.etree.ElementTree as xml_tree

# Open feed.yaml doc and call it file. 
# Load the doc into variable yaml_data.
# Using yaml.safe_load function to verify that the file loads correctly 
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)
    
    # Create the RSS element
    rss_element = xml_tree.Element('rss', {'version':'2.0',
    'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content':'http://www.purl.org/rss/1.0/modules/content/'

    })
# Element creating the channel tag
channel_element = xml_tree.SubElement(rss_element, 'channel')

link_prefix = yaml_data['link']

# Inside channel tag, we create title tag, and add text reading from yaml file (in yaml_data)
xml_tree.SubElement(channel_element, 'title').text = yaml_data['title']
xml_tree.SubElement(channel_element, 'format').text = yaml_data['format']
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data['subtitle']
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data['author']
xml_tree.SubElement(channel_element, 'description').text = yaml_data['description']
xml_tree.SubElement(channel_element, 'itunes:image',{'href':link_prefix + yaml_data['image']})
xml_tree.SubElement(channel_element, 'language').text = yaml_data['language']
xml_tree.SubElement(channel_element, 'link').text = link_prefix

xml_tree.SubElement(channel_element, 'itunes:category',{'text': yaml_data['category']})

# Create a loop for every item/episode
for item in yaml_data['item']:
    # Create a contained for the item for the episodes
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data['author'] # No reason for repeating author for each episode since same author
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']
    
    # The enclosure, length in bytes for the episode, what type of element, and URL for episode:
    enclosure = xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    })

# The element we have built will be fed to the output tree so we can send it to a separate file 
output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('portfolio.xml',encoding='UTF-8', xml_declaration=True)