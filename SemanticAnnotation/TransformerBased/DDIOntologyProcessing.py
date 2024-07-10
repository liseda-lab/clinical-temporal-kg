import xml.etree.ElementTree as ET
from tqdm import tqdm

def getOntologyClasses(inFile):
    # Load the OWL file
    tree = ET.parse(inFile)
    root = tree.getroot()
    listOfAnnotatedURI = []
    listOfAnnotatedTarget = []

    # Namespace dictionary
    ns = {
    'owl': 'http://www.w3.org/2002/07/owl#',
    'oboInOwl': 'http://www.geneontology.org/formats/oboInOwl#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
    }

    # Find all classes with annotations
    axioms = root.findall('.//owl:Class[rdfs:label]', ns) 
    # Use tqdm to track progress
    axioms = tqdm(axioms, desc="Processing classes")

    # Extract annotations
    for axiom in axioms:
        annotated_source = axiom.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
        #annotated_source = axiom.find('owl:Class', ns).attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
        annotated_target = axiom.find('rdfs:label', ns).text
        listOfAnnotatedURI.append(annotated_source)
        listOfAnnotatedTarget.append(annotated_target)

    return listOfAnnotatedURI, listOfAnnotatedTarget

if __name__ == '__main__':

    #Test the code with the following lines.
    outfile = open('teste.txt', 'w')
    x,y = getOntologyClasses('DataSetConstruction/GeneralFiles/Ontologies/dron.owl')
    for element in range(len(x)):
        string = f'{x[element]} {y[element]}\n'
        outfile.write(string)