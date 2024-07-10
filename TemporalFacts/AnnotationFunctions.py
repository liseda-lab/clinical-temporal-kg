from tqdm import tqdm
from datetime import datetime

def IdGenerator(csv_path):
    """ In the Admissions file, the fuction will look at all the identifiers on the files,
    And open an entry on a dictionary so that information related to that identifier can be 
    Gathered.

    csv_path is the path to the folder with the MIMIC-III csv files

    Because we are looking for the hospital stay, independet of hospital section,
    The ID -> (subject, admission)
    """
    dict = {}
    with open(csv_path+"ADMISSIONS.csv", "r") as admissions_file:
        for line in tqdm(admissions_file.readlines()[1:]):
            features = line.split(',')
            subj_id = features[1]
            hadm_id = features[2]
            id = (subj_id,hadm_id)

            if id not in dict.keys():
                dict[id] = {}

    admissions_file.close()
    return dict

def IdGeneratorTimes(csv_path):
    """ In the Admissions file, the fuction will look at all the identifiers on the files,
    And open an entry on a dictionary so that information related to that identifier can be 
    Gathered. These entries are to be collected and copuled with the Admission and Discharge times
    to use furthere ahead.

    csv_path is the path to the folder with the MIMIC-III csv files

    The ID -> (subject, admission)
    Entry  -> {(subject,admission):(admission,discharge)}
    """
    dict = {}
    with open(csv_path+"ADMISSIONS.csv", "r") as admissions_file:
        for line in tqdm(admissions_file.readlines()[1:]):
            features = line.split(',')
            subj_id = features[1]
            hadm_id = features[2]

            adminTime = features[3]
            dischargeTime = features[4]

            id = (subj_id,hadm_id)
            times = (adminTime,dischargeTime)

            if id not in dict.keys():
                dict[id] = times

    admissions_file.close()
    return dict

def IdGeneratorICUTimes(csv_path):
    """ In the ICU stay file, the fuction will look at all the identifiers on the file,
    and open an entry on a dictionary so that information related to specific ICU stay is 
    gathered. These are paired with the ICU admission and discharge times. 

    Because we are looking for the ICU stay:
    The ID -> (subject, admission, icustay)
    Entry  -> {(subject,admission,icustay) : (icuadmission,icudischarge)}
    """
    overallTime = IdGeneratorTimes(csv_path)
    dict = {}
    with open(csv_path+"ICUSTAYS.csv", "r") as admissions_file:
        for line in tqdm(admissions_file.readlines()[1:]):
            features = line.split(',')
            subj_id = features[1]
            hadm_id = features[2]
            icu_id = features[3]

            adminTime = features[-3]
            dischargeTime = features[-2]

            #id = (subj_id,hadm_id,icu_id)
            id = (subj_id,hadm_id)

            if len(adminTime) < 1:
                adminTime = overallTime[id][0]

            if len(dischargeTime) < 1:
                dischargeTime = overallTime[id][1]

            times = (adminTime,dischargeTime)
            
            id = (subj_id,hadm_id,icu_id)

            if id not in dict.keys():
                dict[id] = times

    admissions_file.close()
    return dict

def calculateLenghtofStay(admin,disch):
    """ Given a time of admission and a time of dishcage formated as time series,
    Leverage time series operations to calculate the length of the stay in minutes.
    """

    # Parse the strings into datetime objects
    admission_datetime = datetime.strptime(admin, "%Y-%m-%d %H:%M:%S")
    discharge_datetime = datetime.strptime(disch, "%Y-%m-%d %H:%M:%S")

    # Calculate the length of stay
    length_of_stay = discharge_datetime - admission_datetime

    # Extract days and seconds from the timedelta object
    total_minutes = length_of_stay.total_seconds() / 60

    return total_minutes

def readInitialDiagnosis(dict,csv_path):
    """ Creates an entry to the patient's dictionary with all information regarding the
    initial diagnosis provided at the moment of admission. The data used on the dictionary
    is the data extracted from the annotation process done with the transformer based approach.

    dict     -> is the dictionary previously created containin all patient id's as keys. (IdGenerator(csv_path))
    csv_path -> is the path to the folder with the MIMIC-III csv files

    The annotaitons added to each patient ID will have the orginal label, the tranformer label and the time

    INFORMATION: The transformer file must be in the same directory as this file.
                The transformer file can be replaced with any other file, given that the proper adjustments are done.
    """

    symbols = ['/','\\','?','-']

    #Load the LLM file
    llmDict = {}
    with open("DataSetConstruction/SemanticAnnotation/TransformerBased/Outfiles/Transformer-Annotation.txt","r") as llmFile:
        for line in llmFile.readlines()[:]:
            line = line.replace('"','').split(';')
            disease = line[0].lstrip()
            uri = line[1].split(',')[-2]
            uri = uri.rstrip('').lstrip()
            llmDict[disease] = uri
    
    #Open the admissions file
    with open(csv_path+"ADMISSIONS.csv", "r") as admissionsFile:
        for line in tqdm(admissionsFile.readlines()[1:]):
            features = line.split(',')
            subj_id = features[1]
            hadm_id = features[2]
            id = (subj_id,hadm_id)

            #Process Time
            if len(features[3]) <= 2 or features[3] == ' ':
                adminTime = 'NoTime'
            else:
                adminTime = features[3]
            
            #Process the diagnosis to remove incongruencias
            diagnosis = features[-3].replace('S/P', "STATUS POST").replace('"', "").replace('%', "")
            for symbol in symbols:
                if symbol in diagnosis:
                    diagnosis = diagnosis.replace(symbol, ";")
            
            final_diagnosis = diagnosis.split(";")
            
            if len(final_diagnosis) >= 1:
                for diagnosis in final_diagnosis:
                    diagnosis = diagnosis.lstrip()
                    if len(diagnosis) > 1:
                        #Tem de ser um diagonóstico que exista no dicionário
                        if diagnosis in llmDict.keys():
                            annotation = (diagnosis,llmDict[diagnosis],adminTime)
                        
                            #Verifica se adiciona ou cria novo
                            if 'Diagnosis' not in dict[id].keys():
                                dict[id]['Diagnosis'] = [annotation]
                            else:
                                if annotation not in dict[id]['Diagnosis']:
                                    dict[id]['Diagnosis'].append(annotation)

                        else:
                            pass

    llmFile.close()
    admissionsFile.close()
    return dict

def readPrescriptions(dict, csv_path):

    """ Creates an entry to the patient's dictionary with all information regarding the
    drugs prescribed to the patient. The codes used in this fuction are the codes from the DRON
    ontology thus they need to be loaded with the DronCodes.csv file.

    dict     -> is the dictionary previously created containin all patient id's as keys. (IdGenerator(csv_path))
    csv_path -> is the path to the folder with the MIMIC-III csv files

    The annotaitons added to each patient ID will have the orginal label, ontology class URI and begging and end times
    for the prescription.

    INFORMATION: The DronCodes.csv file must be in the same directory as this file.
    """


    #Load the Recommender file in to a dictionary
    recommenderDict = {}
    with open("DataSetConstruction/GeneralFiles/DronCodes.csv","r") as recommenderFile:
        for line in recommenderFile.readlines()[:]:
            line = line.replace('"','').split(';')
            ndcCode = line[0].rstrip()
            dronUri= line[1].rstrip()
            
            recommenderDict[ndcCode] = dronUri

    with open(csv_path+"PRESCRIPTIONS.csv","r") as prescriptionsFile:
        for line in tqdm(prescriptionsFile.readlines()[1:]):
            features = line.replace('"','').split(',')
            subj_id = features[1]
            hadm_id = features[2]
            drugName = features[9]
            id = (subj_id,hadm_id)

            ndcCode = features[12]
            if ndcCode in recommenderDict.keys():
                uri = recommenderDict[ndcCode].strip('"')
            else:
                continue

            startTime = features[4]
            endTime = features[5]
            #Treat the temporal information to establish the period of validity of the annotation
            if len(startTime) <= 2 or startTime == ' ':
                startTime = 'NoTime'
            
            
            if len(endTime) <= 2 or endTime == ' ':
                endTime = 'NoTime'
            

            annotation = (drugName,uri,startTime,endTime)
            #Primeiro verifca se já exite uma prescrição
            #Esta analise é feita ao verificar quantas chaves existem, se só
            #Existir uma, significa que aida só tem diagonóstico e que criar uma nova
            if 'Prescriptions' not in dict[id].keys():
                if annotation[2] != 'empty':
                    dict[id]['Prescriptions'] = [annotation]
                else:
                    pass
            else:
                if annotation not in dict[id]['Prescriptions']:
                    if annotation[2] != 'empty':
                        dict[id]['Prescriptions'].append(annotation)
                    else:
                        pass
    
    prescriptionsFile.close()
    recommenderFile.close()
    return (dict)

def readLabEvents(dict, csv_path):

    """ Creates an entry to the patient's dictionary with all information regarding the
    laboratory procedures done to or by the patient. 

    dict     -> is the dictionary previously created containin all patient id's as keys. (IdGenerator(csv_path))
    csv_path -> is the path to the folder with the MIMIC-III csv files

    The annotaitons added to each patient ID will have the label, ontology class URI and time of the event.
    """

    itemsDict = {}
    with open(csv_path+'D_LABITEMS.csv','r') as itemsFile:
        for line in itemsFile.readlines()[1:]:
            line = line.replace('"','').split(',')
            itemId = line[1]
            item = line[2]
            loincCode = line[-1].rstrip()

            if len(loincCode) == 0:
                continue
            else:
                uri = 'http://purl.bioontology.org/ontology/LNC/'+loincCode
                itemsDict[itemId] = (item,uri)

    with open(csv_path+'LABEVENTS.csv','r') as labEventsFile:
        for line in tqdm(labEventsFile.readlines()[1:]):
            line = line.split(',')
            subj_id = line[1]
            hadm_id = line[2]
            item_id = line[3].strip('"')
            chartTime = line[4]
            id = (subj_id,hadm_id)

            if len(chartTime) <= 2 or chartTime == ' ':
                chartTime = 'NoTime'

            if item_id in itemsDict.keys():
                annotation = (itemsDict[item_id][0],itemsDict[item_id][1],chartTime)
                #This specific file has some inconsistencies
                if subj_id == '' or hadm_id == '':
                    pass
                else:
                    if 'Tests' not in dict[id].keys():
                        dict[id]['Tests'] = [annotation]
                    else:
                        if annotation not in dict[id]['Tests']:
                            dict[id]['Tests'].append(annotation)
            else:
                continue

    labEventsFile.close()
    itemsFile.close()
    return dict

def readICDProcedures(dict, csv_path):

    """ Creates an entry to the patient's dictionary with all information regarding the
    procedures done by the patient during the stay.

    dict     -> is the dictionary previously created containin all patient id's as keys. (IdGenerator(csv_path))
    csv_path -> is the path to the folder with the MIMIC-III csv files

    The annotaitons added to each patient ID will have the label, ontology class URI and time of procedure.

    """

    proceduresDict = {}
    with open(csv_path+'D_ICD_PROCEDURES.csv','r') as icdFile:
        for line in icdFile.readlines()[1:]:
            line = line.split(',')
            rawProcedure = line[1].rstrip()
            procedure = f'{rawProcedure[:3]}.{rawProcedure[3:]}'
            procedure = procedure.strip('"')

            content = line[3].rstrip()
            proceduresDict[procedure] =  content
    
    timeDict = IdGeneratorTimes(csv_path)

    with open(csv_path+'PROCEDURES_ICD.csv') as proceduresFile:
        for line in tqdm(proceduresFile.readlines()[2:]):
            line = line.split(',')
            rawProcedure = line[4].rstrip()
            procedure = f'{rawProcedure[:3]}.{rawProcedure[3:]}'
            procedure = procedure.strip('"')

            subj_id = line[1]
            hadm_id = line[2]
            id = (subj_id,hadm_id)

            dischargeTime = timeDict[id][1]

            if procedure in proceduresDict.keys():
                uri = 'http://purl.bioontology.org/ontology/ICD9CM/'+str(procedure)
                annotation = (procedure,uri, dischargeTime)
                if 'Procedures' not in dict[id].keys():
                    dict[id]['Procedures'] = [annotation]
                else:
                    dict[id]['Procedures'].append(annotation)
            
            else:
                continue

    proceduresFile.close()
    icdFile.close()        
    return dict

def readICDDiagnosis(dict,csv_path):

    """ Creates an entry to the patient's dictionary with all information regarding the
    patient's final diagnosis.

    dict     -> is the dictionary previously created containin all patient id's as keys. (IdGenerator(csv_path))
    csv_path -> is the path to the folder with the MIMIC-III csv files

    The annotaitons added to each patient ID will have the label, ontology class URI and time.

    """

    diagnosisDict = {}
    with open(csv_path+'D_ICD_DIAGNOSES.csv','r') as icdFile:
        for line in icdFile.readlines()[1:]:
            line = line.split(',')
            rawDiagnosis = line[1].rstrip()

            if 'E' in rawDiagnosis:
                diagnosis = f'{rawDiagnosis[:5]}.{rawDiagnosis[5:]}'
            else:
                diagnosis = f'{rawDiagnosis[:4]}.{rawDiagnosis[4:]}'
            
            diagnosis = diagnosis.strip('"')
            content = line[3].rstrip().strip('"')
            diagnosisDict[diagnosis] = content

    timeDict = IdGeneratorTimes(csv_path)

    with open(csv_path+'DIAGNOSES_ICD.csv','r') as diagnosisFile:
        for line in tqdm(diagnosisFile.readlines()[1:]):
            line = line.split(',')
            rawDiagnosis = line[-1].rstrip()

            if 'E' in rawDiagnosis:
                diagnosis = f'{rawDiagnosis[:5]}.{rawDiagnosis[5:]}'
            else:
                diagnosis = f'{rawDiagnosis[:4]}.{rawDiagnosis[4:]}'
            
            diagnosis = diagnosis.strip('"')

            subj_id = line[1]
            hadm_id = line[2]
            id = (subj_id,hadm_id)

            dischargeTime = timeDict[id][1]
    
            if diagnosis in diagnosisDict.keys():
                uri = 'http://purl.bioontology.org/ontology/ICD9CM/'+str(diagnosis)
                annotation = (diagnosis,uri,dischargeTime)
                if 'ICD9' not in dict[id].keys():
                    dict[id]['ICD9'] = [annotation]
                else:
                    dict[id]['ICD9'].append(annotation)

    diagnosisFile.close()
    icdFile.close()
    return dict

def RunProgram(csvPath):

    """Provided the csvPath to the MIMIC-III csv folder, this function will generate a dictionary
    with the information regarding all patients.
    """

    dict1 = IdGenerator(csvPath)
    dict1 = readInitialDiagnosis(dict1,csvPath)
    dict1 = readPrescriptions(dict1,csvPath)
    dict1 = readLabEvents(dict1,csvPath)
    dict1 = readICDProcedures(dict1,csvPath)
    dict1 = readICDDiagnosis(dict1,csvPath)

    return dict1

if __name__ == '__main__':

    print(('Please change all relevant paths to match your device folders.\
           To properly run the program please load the fuctions module and call the function RunProgram.'))
    