from xml.dom import minidom
from rdflib import Graph, OWL, URIRef


class OntologyLinkExtractor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.count = 0

    def updateCount(self):
        self.count += 1

    def parse_and_extract(self):
        parsed = minidom.parse(self.input_file)
        models = parsed.getElementsByTagName('Cell')
        
        with open(self.output_file,'w') as outfile:
            for cell in models:
                # Extract entity1, entity2, and relation from each Cell
                entity1 = cell.getElementsByTagName('entity1')[0].getAttribute('rdf:resource')
                entity2 = cell.getElementsByTagName('entity2')[0].getAttribute('rdf:resource')
                relation = cell.getElementsByTagName('relation')[0].firstChild.data

                if relation == '=':
                    outfile.write(f'{entity1}\towl:equivalentClass\t{entity2}\n')
                    self.updateCount()

    
    def parse_turtle(self):
        parsed = minidom.parse(self.input_file)
        models = parsed.getElementsByTagName('Cell')
        
        graph = Graph()
        with open(self.output_file,'w') as outfile:
            for cell in models:
                # Extract entity1, entity2, and relation from each Cell
                entity1 = cell.getElementsByTagName('entity1')[0].getAttribute('rdf:resource')
                entity2 = cell.getElementsByTagName('entity2')[0].getAttribute('rdf:resource')
                relation = cell.getElementsByTagName('relation')[0].firstChild.data

                if relation == '=':
                    graph.add((URIRef(entity1), OWL.equivalentClass, URIRef(entity2)))
                    

        graph.serialize(self.output_file, format='turtle')


                
        

if __name__ == '__main__':

    #Ncit to Dron
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/ncit-dron-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/ncit-dron-triples.tsv').parse_and_extract()
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/ncit-dron-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/ncit-dron-triples.ttl').parse_turtle()
    #Ncit to Loinc 
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/ncit-loinc-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/ncit-loinc-triples.tsv').parse_and_extract()
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/ncit-loinc-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/ncit-loinc-triples.ttl').parse_turtle()
    #Ncit to Icd9cm
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/ncit-icd9cm-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/ncit-icd9cm-triples.tsv').parse_and_extract()
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/ncit-icd9cm-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/ncit-icd9cm-triples.ttl').parse_turtle()
    #Icd9cm to Loinc 
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/icd9cm-loinc-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/icd9cm-loinc-triples.tsv').parse_and_extract()
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/icd9cm-loinc-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/icd9cm-loinc-triples.ttl').parse_turtle()
    #Icd9cm to dron 
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/icd9cm-dron-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/icd9cm-dron-triples.tsv').parse_and_extract()
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/icd9cm-dron-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/icd9cm-dron-triples.ttl').parse_turtle()
    #loinc to dron 
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/loinc-dron-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/loinc-dron-triples.tsv').parse_and_extract()
    OntologyLinkExtractor('DataSetConstruction/OntologyAlignment/AlignmentFiles/loinc-dron-alignment.rdf',\
                        'DataSetConstruction/OntologyAlignment/TriplesFiles/loinc-dron-triples.ttl').parse_turtle()
    
   