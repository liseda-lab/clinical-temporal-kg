from rdflib import Graph
file = '/Users/ricardocarvalho/Desktop/ICD9CM.ttl'
g = Graph()
g.parse(file, format="turtle")

g.serialize(destination='ICD9CM.rdf', format='xml')