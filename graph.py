import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt

tree = ET.parse('coverage.xml')
root = tree.getroot()

G = nx.Graph()

    # Tek tek line'ları gezip numaraları ve onların hitlerini bulma

for class_element in root.findall('.//class'):
    class_name = class_element.get('name')
    for line_element in class_element.findall('.//lines/line'):
        line_number = line_element.get('number')
        hit_count = int(line_element.get('hits', 0))
        node_label = f"{class_name}:{line_number}"

        node_color = 'green' if hit_count >= 0 else 'red'  # Hitsler 0 ise yeşil 1 ise kırmızı
        G.add_node(node_label, color=node_color)

for class_element in root.findall('.//class'):
    class_name = class_element.get('name')
    for line_element in class_element.findall('.//lines/line'):
        line_number = line_element.get('number')
        current_node = f"{class_name}:{line_number}"

        if int(line_number) > 1:
            previous_node = f"{class_name}:{int(line_number) - 1}"
            G.add_edge(previous_node, current_node)

        for other_class_element in root.findall('.//class'):    # Diğer file'ların line'larını gezdirttim
            other_class_name = other_class_element.get('name')
            if other_class_name != class_name:
                other_line_node = f"{other_class_name}:{line_number}"
                G.add_edge(current_node, other_line_node)

pos = nx.spring_layout(G)
node_colors = [G.nodes[node].get('color', 'red') for node in G.nodes]
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=1000, node_color=node_colors, font_color="black", font_size=5, edge_color="gray")  # Node özelleriklerini tanımladım

plt.show()
