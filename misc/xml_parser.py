import xml.etree.ElementTree as ET

def parse_topics(xml_file):
    topics = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for doc in root.findall('doc'):
        title = doc.find('title').text
        title = title.replace("Wikipedia: ", "")
        topics.append(title)
    return topics

def write_topics_to_txt(topics, output_file):
    with open(output_file, 'w') as f:
        for topic in topics:
            f.write(topic + '\n')

if __name__ == "__main__":
    input_file = 'simplewiki-latest-abstract.xml'  # since deleted due to Git file size constraints
    output_file = 'topics.txt'
    
    topics = parse_topics(input_file)
    write_topics_to_txt(topics, output_file)
    print("Topics extracted and written to 'topics.txt' file.")
