import csv
import requests as rq
from tqdm import tqdm
import difflib

def annotator_request(ndc_code):
    triage = []
    false = []
    final = []
    api_key = "YOUR NCBO API KEY"

    for num_query in tqdm(range(0,len(ndc_code),200)):
        
        drugs = ndc_code[num_query:num_query+200]

        query = ','.join(drugs)
        link = 'http://data.bioontology.org/annotator?text='+query+'&input_type=2&ontologies=DRON&exact_match=true&apikey=' + api_key
        res = rq.get(link)
        x = res.json()

        notMatched = []
        #Tentar entender quais não estão a dar match para perceber o porque?
        for i in range(len(x)):
            
            if len(x[i])>1:
                uri = x[i]['annotatedClass']['@id']
            else:
                uri = 'no match'

            info = (x[i]['annotations'][0]['text'],uri)
            codes = x[i]['annotations'][0]['text']
            final.append(info)
            triage.append(codes)

        for classe in drugs:
            if classe.strip('"') not in triage and classe.strip('"') not in false:
                false.append(classe)
                
        #print(str(num_query)+' out of '+str(len(ndc_code)))
    
    return final, false

def annotator_single(pairs):
    final = []
    no_match = []
    api_key = "YOUR NCBO API KEY"
    
    for pair in tqdm(pairs):
        print(pair)
        code = pair[0].strip('"')
        term = pair[1]
        link = 'http://data.bioontology.org/annotator?text='+term+'&input_type=2&ontologies=DRON&exact_match=true&apikey=' + api_key
        res = rq.get(link)
        fetch = res.json()
        possible = []

        for i in range(len(fetch)):
            try:
                uri = fetch[i]['annotatedClass']['@id']
                info = fetch[i]['annotations'][0]['text']
                seq = difflib.SequenceMatcher(None, info, term)
                similarity = seq.ratio()
                if similarity>0.70:
                    match = (similarity,info,code,uri)
                    possible.append(match)
                else:
                    continue

            except KeyError:
                continue
        
        possible = sorted(possible,key=lambda x: x[0], reverse=True)
        if len(possible) > 0:
            pair = (possible[0][2],possible[0][-1])

            if pair not in final:
                final.append(pair)    
                print(f'found a match for:{pair}')    
        
        else:
            continue

    
    return final
######################################
############# PROGRAMA ###############
######################################

#path to the csv files
csv_path = "DataSetConstruction/MimicFiles/"
prescriptions_file = open(f'{csv_path}PRESCRIPTIONS.csv',"r")
ndc_codes = []
concepts = {}
total = 0

for line in prescriptions_file.readlines()[1:]:
    x = line.split(',')
    name = x[7]
    name = name.replace('"','')
    name = name.upper()

    ndc_code = x[12]
    ndc_code = ndc_code.replace('"','')

    if len(ndc_code) > 0:
        total += 1
    if ndc_code not in  concepts.keys():
        concepts[ndc_code] = name

prescriptions_file.close()

mapped, missing = annotator_request(list(concepts.keys()))

pairs = []
for code in missing:
    term = concepts[code]
    pair = (code, term)
    pairs.append(pair)

remaining = annotator_single(pairs)

with open('DronCodes.csv','w', newline='') as file:
   writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
   writer.writerows(mapped)
   writer.writerows(remaining)