import xml.etree.ElementTree as ET

tree = ET.parse('assets/map/flutter_runnergame_map_A.tmx')
root = tree.getroot()
print("Tilesets:")
for ts in root.findall('tileset'):
    print(f"  firstgid={ts.attrib.get('firstgid')}, source={ts.attrib.get('source')}")

print("\nLayers & Groups:")
for child in root:
    if child.tag in ('layer', 'group', 'objectgroup'):
        p_x = child.attrib.get('parallaxx', '1')
        p_y = child.attrib.get('parallaxy', '1')
        print(f"{child.tag}: name='{child.attrib.get('name')}', px={p_x}, py={p_y}")
        for sub in child:
            if sub.tag in ('layer', 'group', 'objectgroup'):
                sp_x = sub.attrib.get('parallaxx', p_x)
                sp_y = sub.attrib.get('parallaxy', p_y)
                print(f"    {sub.tag}: name='{sub.attrib.get('name')}', px={sp_x}, py={sp_y}")
