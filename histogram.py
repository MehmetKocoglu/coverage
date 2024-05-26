import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

tree = ET.parse('coverage.xml')
root = tree.getroot()

hit_data = {}

for class_element in root.findall('.//class'):
    class_name = class_element.get('name')
    hit_count = sum(int(line.get('hits', 0)) for line in class_element.findall('.//line'))
    hit_data[class_name] = hit_count

fig, ax = plt.subplots()

colors = ['green' if hits > 0 else 'red' for hits in hit_data.values()]

labels = list(hit_data.keys())

heights = list(hit_data.values())

bars = ax.bar(labels, heights, color=colors)

ax.set_ylabel('Hit Sayacı')
ax.set_xlabel('Classes')
ax.set_title('Her Class icin Hit Sayacı')

plt.show()