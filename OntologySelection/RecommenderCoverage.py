from tqdm import tqdm
import requests as rq


class TermExtractor:
    def __init__(self, file, ont):
        self.file = file
        self.ont = ont
        self.names = []

    ######## Files Processing ##########
    # The method is capable of ajustments to process all files on the MIMIC-III
    def extract_terms(self):
        with open(self.file, "r") as f:
            if self.ont == 'ndc':
                self._extract_ndc(f)
            elif self.ont in ['loinc', 'icd9']:
                self._extract_loinc_icd9(f)
            elif self.ont == 'ncit':
                self._extract_ncit(f)
        #print(self.names)
        return self.names

    #Process Drugs file
    def _extract_ndc(self, file):
        for line in file.readlines()[1:]:
            x = line.split(',')
            name = x[7].replace('"', '').upper()
            if name not in self.names:
                self.names.append(name)
    #Process items, final diagnosis and procedures files
    def _extract_loinc_icd9(self, file):
        for line in file.readlines()[1:]:
            x = line.split(',')
            name = x[2].replace('"', '').upper()
            if name not in self.names:
                self.names.append(name)
    #Process initial diagnosis files
    def _extract_ncit(self, file):
        for line in file.readlines():
            name = line.strip(',\n').rstrip().upper()
            name = name.replace('"', '')
            if name not in self.names:
                self.names.append(name)


if __name__ == '__main__':
    extractor = TermExtractor('DataSetConstruction/GeneralFiles/AllDiagnostics.txt','ncit')
    terms = extractor.extract_terms()

    ontologySet = ['NCIT', 'LOINC', 'EFO', 'SNOMEDCT', 'RXNORM', 'MEDDRA', 'MESH']
    ontologyString = ','.join(ontologySet)
    coverages = {ontology: 0 for ontology in ontologySet}

    matches = []

    for num_query in tqdm(range(0, len(terms), 100)):
        termSet = terms[num_query:num_query + 100]
        api_key = "YOUR_API_KEY"

        query = ','.join(termSet)
        query = query.replace(' ','%20')
        link = f'https://data.bioontology.org/recommender?input={query}&input_type=2&ontologies={ontologyString}&apikey={api_key}'
        
        
        try:
            request = rq.get(link)
            #print(request)
            call = request.json()
            if request.status_code == 200:
                try:
                    call = request.json()
                    print(call)  # Prints the JSON response
                    for item in range(len(call)):
                        try:
                            ontology = call[item]['ontologies'][0]['acronym']
                            for position in range(len(call[item]['coverageResult']['annotations'])):
                                term = call[item]['coverageResult']['annotations'][position]['text']
                                link = call[item]['coverageResult']['annotations'][position]['annotatedClass']['@id']

                                if ontology in coverages.keys():
                                    coverages[ontology] = coverages[ontology] + 1
                        
                        except KeyError:
                            continue

                except ValueError:
                    print("Failed to parse JSON response")
        
        except Exception as e:
                print(f"An error occurred: {e}")

    print(coverages)
