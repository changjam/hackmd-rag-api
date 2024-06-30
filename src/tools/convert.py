import xml.etree.ElementTree as ET




def convert_list_to_xml(data_list: list, root_name: str = "News_List", sub_element_name: str = "News") -> str:
    root = ET.Element(root_name)
    for item in data_list:
        product = ET.SubElement(root, sub_element_name)
        for key, value in item.items():
            if isinstance(value, list):
                sub_entry = ET.SubElement(product, key)
                for sub_value in value:
                    sub_sub_entry = ET.SubElement(sub_entry, "item")
                    sub_sub_entry.text = sub_value
            else:
                sub_entry = ET.SubElement(product, key)
                sub_entry.text = value

    xml_string = ET.tostring(root, encoding='utf-8', method='xml').decode()
    xml_string = xml_string.replace("><", ">\n<")
    return xml_string


def convert_dict_to_xml(data: dict, root_name: str = "News") -> str:
    root = ET.Element(root_name)
    for key, value in data.items():
        if isinstance(value, list):
            sub_entry = ET.SubElement(root, key)
            for sub_value in value:
                sub_sub_entry = ET.SubElement(sub_entry, "item")
                sub_sub_entry.text = sub_value
        else:
            sub_entry = ET.SubElement(root, key)
            sub_entry.text = value

    xml_string = ET.tostring(root, encoding='utf-8', method='xml').decode()
    xml_string = xml_string.replace("><", ">\n<")
    return xml_string