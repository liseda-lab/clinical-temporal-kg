import AnnotationFunctions as GA
from tqdm import tqdm

####################################
# Generate annotations Disctionary #
####################################

print(" -------------  Running annotations ---------------------------")

csvPath = "DataSetConstruction/MimicFiles/"
AnnotationsDict = GA.RunProgram(csvPath)

####################################
# Writing the annotations Files    #
####################################

print(" -------------  Writing Diagnosis ---------------------------")
file = open('DataSetConstruction/TemporalFacts/HospitalStayFacts/AnnotationsInitialDiagnosis.tsv','w')
for subject in tqdm(AnnotationsDict.keys()):
    if 'Diagnosis' in AnnotationsDict[subject].keys():
        annotations = [(item[1], item[2]) for item in AnnotationsDict[subject]['Diagnosis']]
        for annotation in annotations:
            if 'http' not in annotation[0]:
                annotations.remove(annotation)
        
        if len(annotations) != 0:
            for element in annotations:
                line = f'{subject[0]},{subject[1]}\t{element[0]}\t{element[1]}'
                file.write(line + '\n')

    else:
        continue
file.close()

print(" -------------  Writing Drugs ---------------------------")
file = open('DataSetConstruction/TemporalFacts/HospitalStayFacts/AnnotationsPrescriptions.tsv','w')
for subject in tqdm(AnnotationsDict.keys()):
    if 'Prescriptions' in AnnotationsDict[subject].keys():
        annotations = [(item[1], item[2], item[3]) for item in AnnotationsDict[subject]['Prescriptions']]
        for annotation in annotations:
            if 'http' not in annotation[0]: #or 'empty' in annotation[0]:
                annotations.remove(annotation)
        
        if len(annotations) != 0:
            for element in annotations:
                line = f'{subject[0]},{subject[1]}\t{element[0]}\t{element[1]}\t{element[2]}'
                file.write(line + '\n')

    else:
        continue
file.close()

print(" -------------  Writing Lab Tests ---------------------------")
file = open('DataSetConstruction/TemporalFacts/HospitalStayFacts/AnnotationsLab.tsv','w')
for subject in tqdm(AnnotationsDict.keys()):
    if 'Tests' in AnnotationsDict[subject].keys():
        annotations = [(item[1], item[2]) for item in AnnotationsDict[subject]['Tests']]
        for annotation in annotations:
            if 'http' not in annotation[0]:
                annotations.remove(annotation)
        
        if len(annotations) != 0:
            for element in annotations:
                line = f'{subject[0]},{subject[1]}\t{element[0]}\t{element[1]}'
                file.write(line + '\n')
    
    else:
        continue
file.close()

print(" -------------  Writing ICD9 Procedures ---------------------------")
file = open('DataSetConstruction/TemporalFacts/HospitalStayFacts/AnnotationsProcedures.tsv','w')
for subject in tqdm(AnnotationsDict.keys()):
    if 'Procedures' in AnnotationsDict[subject].keys():
        annotations = [(item[1], item[2]) for item in AnnotationsDict[subject]['Procedures']]
        for annotation in annotations:
            if 'http' not in annotation[0]:
                annotations.remove(annotation)
        
        if len(annotations) != 0:
            for element in annotations:
                line = f'{subject[0]},{subject[1]}\t{element[0]}\t{element[1]}'
                file.write(line + '\n')
    
    else:
        continue
file.close()

print(" -------------  Writing ICD9 Diagnosis ---------------------------")
file = open('DataSetConstruction/TemporalFacts/HospitalStayFacts/AnnotationsFinalDiagnosis.tsv','w')
for subject in tqdm(AnnotationsDict.keys()):
    if 'ICD9' in AnnotationsDict[subject].keys():
        annotations = [(item[1], item[2]) for item in AnnotationsDict[subject]['ICD9']]
        for annotation in annotations:
            if 'http' not in annotation[0]:
                annotations.remove(annotation)
        
        if len(annotations) != 0:
            for element in annotations:
                line = f'{subject[0]},{subject[1]}\t{element[0]}\t{element[1]}'
                file.write(line + '\n')
    
    else:
        continue
file.close()
