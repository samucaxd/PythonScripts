import os
import xml.etree.ElementTree as ET

dict_exported = './1-XMLs_Exportados'
dict_processed = './2-XMLs_Processados'
dict_finished = './3-XMLs_Finalizados'

tagsToRemove = [
   "vProd", "qTrib", "uTrip", "vUnTrib", "imposto", "vUnCom", "total", "transp", "cobr", "pag", "infAdic", "infRespTec"
]

def removeNamespaces(input, output):
    tree = ET.parse(input)
    root = tree.getroot()
    def remove_ns(element):
        if '}' in element.tag:
            element.tag = element.tag.split('}', 1)[1]

        for attrib_keys in list(element.attrib.keys()):
            if '}' in attrib_keys:
                new_key = attrib_keys.split('}', 1)[1]
                element.attrib[new_key] = element.attrib.pop(attrib_keys)

        for child in element:
            remove_ns(child)

    remove_ns(root)
    tree.write(output, encoding='utf-8', xml_declaration=True)

def removeTags(input, tagsToRemove, output):
  try:
    tree = ET.parse(input)
    root = tree.getroot()
    for tag in tagsToRemove:
        for parent in root.findall(f".//{tag}/.."):
            for element in parent.findall(tag):
                for child in element:
                   element.remove(child)
                parent.remove(element)
    return tree.write(output, encoding='utf-8', xml_declaration=True)
    
  except ET.ParseError as e:
     print(f"Erro ao tentar executar o XML: {e}")
     return None

def load_XMLs(dict_exported, dict_processed, dict_finished):
    if not os.path.exists(dict_processed) and os.path.exists(dict_finished):
        os.makedirs(dict_processed)
        os.makedirs(dict_finished)

    for filename in os.listdir(dict_exported):
        if filename.endswith('.xml'):
            input_location = os.path.join(dict_exported, filename)
            output_location = os.path.join(dict_processed, filename)

            removeNamespaces(input_location, output_location)
            os.remove(input_location)
            print(f'Arquivo {filename} processado!')
    
    for filename in os.listdir(dict_processed):
        if filename.endswith('.xml'):
            input_location = os.path.join(dict_processed, filename)
            output_location = os.path.join(dict_finished, f'Finalizado_{filename}')

            removeTags(input_location, tagsToRemove, output_location)
            os.remove(input_location)
            

load_XMLs(dict_exported, dict_processed, dict_finished)
print("XMLs finalizados com sucesso!")
     