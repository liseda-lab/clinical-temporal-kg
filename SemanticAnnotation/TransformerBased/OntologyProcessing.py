import xml.etree.ElementTree as ET
from tqdm import tqdm

def getOntologyClasses(inFile):
    # Load the OWL file
    tree = ET.parse(inFile)
    root = tree.getroot()
    listOfUri = []
    listOfLabels = []

    # Namespace dictionary
    ns = {'owl': 'http://www.w3.org/2002/07/owl#', 'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'}

    # Find all classes with labels
    class_elements = root.findall('.//owl:Class[rdfs:label]', ns)

    # Use tqdm to track progress
    class_elements = tqdm(class_elements, desc="Processing classes")

    # Extract class labels
    for element in class_elements:
        listOfUri.append(element.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'])
        listOfLabels.append(element.find('rdfs:label', ns).text)

    return listOfUri, listOfLabels

if __name__ == '__main__':
    x,y = getOntologyClasses('BERT/Thesaurus.owl')
    print(y)
