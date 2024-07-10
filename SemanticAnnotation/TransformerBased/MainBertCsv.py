import OntologyProcessing 
import sentenceBirtRun
import csv

#Load the target labels
print('.............. Reading Target File ................')

targetFile = 'DataSetConstruction/GeneralFiles/AllDiagnostics.txt'
targetLabels = []
with open(targetFile, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        line = row[0]  # Assuming the data is in the first column
        line = line.rstrip()
        line = line.strip(',')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        targetLabels.append(line)

totalTargets = len(targetLabels)

print(totalTargets)


print('.............. Process Ontology for Candidates ................')

candidateUris,candidateLabels = OntologyProcessing.getOntologyClasses('DataSetConstruction/GeneralFiles/Ontologies/Thesaurus.owl')

print('.............. Running BERT Model ................')
bestFit = sentenceBirtRun.OntologyBert(targetLabels, candidateUris, candidateLabels)

print('.............. Writing File ................')
outfile = open('DataSetConstruction/SemanticAnnotation/TransformerBased/Outfiles/Transformer-Annotation.txt','w')

totalFound = len(bestFit)

for k,v in bestFit.items():
    line = f'{k};{v}\n'
    outfile.write(line)

outfile.close()

print(f' Got {totalFound} out of {totalTargets}')