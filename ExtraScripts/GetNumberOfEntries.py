from tqdm import tqdm
def numberOfPatients(*args):
    patients = []
    for arg in args:
        with open(arg,'r') as file:
            for line in tqdm(file.readlines()):
                subject = line.split(';')[0]

                if subject not in patients:
                    patients.append(subject)

    print(len(patients))


# numberOfPatients('/Users/ricardocarvalho/Documents/Thesis/ICUAnnotFinalDiagnosis.csv',\
#                '/Users/ricardocarvalho/Documents/Thesis/ICUAnnotInitialDiagnosis.csv',\
#                '/Users/ricardocarvalho/Documents/Thesis/ICUAnnotLab.csv',\
#                '/Users/ricardocarvalho/Documents/Thesis/ICUAnnotPrescriptions.csv',\
#                '/Users/ricardocarvalho/Documents/Thesis/ICUAnnotProcedures.csv')

numberOfPatients('/Users/ricardocarvalho/Documents/Thesis/DataSetConstruction/OutFiles/AnnotationsInitialDiagnosis.csv',\
                 '/Users/ricardocarvalho/Documents/Thesis/DataSetConstruction/OutFiles/AnnotationsInitialDiagnosis.csv',\
                '/Users/ricardocarvalho/Documents/Thesis/DataSetConstruction/OutFiles/AnnotationsLab.csv',\
                '/Users/ricardocarvalho/Documents/Thesis/DataSetConstruction/OutFiles/AnnotationsPrescriptions.csv',\
                '/Users/ricardocarvalho/Documents/Thesis/DataSetConstruction/OutFiles/AnnotationsProcedures.csv')