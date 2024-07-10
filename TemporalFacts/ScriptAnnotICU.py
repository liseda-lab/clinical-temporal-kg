import AnnotationFunctions as GA
from tqdm import tqdm

####################################
# Generate annotations Disctionary #
####################################

print(" -------------  Running annotations ---------------------------")

csvPath = "DataSetConstruction/MimicFiles/"

AnnotationsDict = GA.RunProgram(csvPath)
ICUTimesDict = GA.IdGeneratorICUTimes(csvPath)

####################################
# Writing the annotations Files    #
####################################


print(" -------------  Writing Diagnosis ---------------------------")
#If the annotations happened prior to the release they are kept and ajusted to have a temporal label that matches the beggining of the ICU stay

file = open('DataSetConstruction/TemporalFacts/IcuStayFacts/ICUAnnotInitialDiagnosis.tsv','w')
for subject in tqdm(AnnotationsDict.keys()):
    matching_keys = [key for key in ICUTimesDict.keys() if subject == (key[0], key[1])]
    
    #Got trow each ICU Stay
    for key in matching_keys:
        ICUadmission = ICUTimesDict[key][0]
        ICUdischarge = ICUTimesDict[key][1]
        if 'Diagnosis' in AnnotationsDict[subject].keys():
            annotations = [(item[1], item[2]) for item in AnnotationsDict[subject]['Diagnosis']] #Annotation,
            for annotation in annotations:
                if 'http' not in annotation[0]:
                    annotations.remove(annotation)
            
            if len(annotations) != 0:
                for annotation in annotations:
                    if annotation[1] <= ICUdischarge:
                        line = f'{key[0]},{key[1]},{key[2]}\t{annotation[0]}\t{ICUadmission}'
                        file.write(line + '\n')
                        
        else:
            continue


file.close()

print(" -------------  Writing Drugs ---------------------------")
file = open('DataSetConstruction/TemporalFacts/IcuStayFacts/ICUAnnotPrescriptions.tsv','w')
for subject in tqdm(AnnotationsDict.keys()):
    matching_keys = [key for key in ICUTimesDict.keys() if subject == (key[0], key[1])]

    #Go trow each ICU Stay
    for key in matching_keys:
        ICUadmission = ICUTimesDict[key][0]
        ICUdischarge = ICUTimesDict[key][1]
        print(f'{ICUadmission} -------- {ICUdischarge}')

        if 'Prescriptions' in AnnotationsDict[subject].keys():
            annotations = [(item[1], item[2], item[3]) for item in AnnotationsDict[subject]['Prescriptions']]
            for annotation in annotations:
                if 'http' not in annotation[0] or 'empty' in annotation[0]:
                    annotations.remove(annotation)
            
            if len(annotations) != 0:
                for annotation in annotations:
                    #Only count annotation that are valid in the intervale of the stay. 
                    #Those that begin after are exluded.
                    if not (annotation[1] > ICUdischarge): 
                        line = f'{key[0]},{key[1]},{key[2]}\t{annotation[0]}\t{annotation[1]}\t{annotation[2]}'
                        file.write(line + '\n')
                        print(line)
        else:
            continue

file.close()

print(" -------------  Writing Lab Tests ---------------------------")
file = open('DataSetConstruction/TemporalFacts/IcuStayFacts/ICUAnnotLab.tsv','w')

for subject in tqdm(AnnotationsDict.keys()):
    matching_keys = [key for key in ICUTimesDict.keys() if subject == (key[0], key[1])]

    #Go trow each ICU Stay
    for key in matching_keys:
        ICUadmission = ICUTimesDict[key][0]
        ICUdischarge = ICUTimesDict[key][1]
        print(f'{ICUadmission} -------- {ICUdischarge}')

        if 'Tests' in AnnotationsDict[subject].keys():
            annotations = [(item[1], item[2]) for item in AnnotationsDict[subject]['Tests']]
            for annotation in annotations:
                if 'http' not in annotation[0]:
                    annotations.remove(annotation)
            
            if len(annotations) != 0:
                for annotation in annotations:
                    #If it procedes or is within the ICU
                    if annotation[1] <= ICUdischarge:
                        line = f'{key[0]},{key[1]},{key[2]}\t{annotation[0]}\t{annotation[1]}'
                        file.write(line + '\n')
        
        else:
            continue
file.close()


print(" -------------  Writing ICD9 Procedures ---------------------------")
file = open('DataSetConstruction/TemporalFacts/IcuStayFacts/ICUAnnotProcedures.tsv','w')

for subject in tqdm(AnnotationsDict.keys()):
    matching_keys = [key for key in ICUTimesDict.keys() if subject == (key[0], key[1])]

    #Go trow each ICU Stay
    for key in matching_keys:
        ICUadmission = ICUTimesDict[key][0]
        ICUdischarge = ICUTimesDict[key][1]

        if 'Procedures' in AnnotationsDict[subject].keys():
            annotations = [(item[1], item[2]) for item in AnnotationsDict[subject]['Procedures']]
            for annotation in annotations:
                if 'http' not in annotation[0]:
                    annotations.remove(annotation)

            if len(annotations) != 0:
                for annotation in annotations:
                    #If it procedes or is within the ICU
                    if annotation[1] <= ICUdischarge:
                        line = f'{key[0]},{key[1]},{key[2]}\t{annotation[0]}\t{annotation[1]}'
                        file.write(line + '\n')
        else:
            continue
file.close()


print(" -------------  Writing ICD9 Diagnosis ---------------------------")
file = open('DataSetConstruction/TemporalFacts/IcuStayFacts/ICUAnnotFinalDiagnosis.tsv','w')

for subject in tqdm(AnnotationsDict.keys()):
    matching_keys = [key for key in ICUTimesDict.keys() if subject == (key[0], key[1])]

    #Go trow each ICU Stay
    for key in matching_keys:
        ICUadmission = ICUTimesDict[key][0]
        ICUdischarge = ICUTimesDict[key][1]

        if 'ICD9' in AnnotationsDict[subject].keys():
            annotations = [(item[1], item[2]) for item in AnnotationsDict[subject]['ICD9']]
            for annotation in annotations:
                if 'http' not in annotation[0]:
                    annotations.remove(annotation)

            if len(annotations) != 0:
                for annotation in annotations:
                    #If it procedes or is within the ICU
                    if annotation[1] <= ICUdischarge:
                        line = f'{key[0]},{key[1]},{key[2]}\t{annotation[0]}\t{annotation[1]}'
                        file.write(line + '\n')
        else:
            continue
file.close()