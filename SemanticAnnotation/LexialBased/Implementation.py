import ES_functions as Esf
import matplotlib.pyplot as plt
#from sklearn import preprocessing
import numpy as np
import csv


in_file = open('DataSetConstruction/GeneralFiles/AllDiagnostics.txt','r')
list_of_terms = []
for line in in_file.readlines():
    list_of_terms.append(line.strip(',\n'))

content = Esf.elastic_msearch(list_of_terms)
empty = 0
write_list = [["TERM","URI","HIT SCORE","PONDERATED SCORE","TERM MATCHED","TERM SIMILARITY"]]
sim_scores = []
hit_scores = []
for i in content.keys():
    if len(content[i]) == 0:
        empty += 1
    else:
        max_sim_score = content[i][0][4]
        hit_score = content[i][0][1]
        info_list = [i,content[i][0][0],content[i][0][1],content[i][0][2],content[i][0][3],content[i][0][4]]
        sim_scores.append(max_sim_score)
        hit_scores.append(hit_score)
        write_list.append(info_list)

#Output com a informação
with open('DataSetConstruction/SemanticAnnotation/LexialBased/Outfiles/Elastic_results.csv', 'w', newline='') as file:
    writer = csv.writer(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=';')
    writer.writerows(write_list)

#Histogramas
fig1 = plt.figure()
plt.hist(hit_scores, density=True, bins=10)
plt.ylabel('Probability')
plt.xlabel('Hit_scores')
plt.savefig('Hit_score.png')

fig2 = plt.figure()
plt.hist(sim_scores, density=True, bins=10)
plt.ylabel('Probability')
plt.xlabel('Similarity_scores')
plt.savefig('Similarity_score.png')

fig3 = plt.figure()
y = np.sin(hit_scores)
plt.scatter(hit_scores, y)
plt.xlabel('Hit_score')
plt.ylabel('Sin(Hit_score)')
plt.savefig('Scater_hit_score.png')

#Análise estatistica
print('Mean Hit Scores = '+ str(sum(hit_scores)/len(hit_scores)))
print('Mean Similarity scores = '+ str(sum(sim_scores)/len(sim_scores)))
print('Undetected Terms = ' + str(empty))
print('Multi Search Reach = '+(str(100-(empty*100/len(list_of_terms))))+'%')
