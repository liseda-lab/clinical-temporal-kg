from fuzzywuzzy import fuzz
from elasticsearch import Elasticsearch
import itertools


def abreviation(word):
    """
    Produce the apropriate word abreviation
    """
    tokens = word.split()
    string = ""
    for word in tokens:
        if word != "and":
            string+= str(word[0])
    return string

def fuzzy_abrev_rank(str2match,str_options):
    """
    Given a word to match and a set of options, this function
    ranks the words from the most semilar to the least similar in therms of the string
    besides that this ranker takes in to account the abreviations and ranks them the best with
    a score of 101
    """
    str1 = str2match
    str2options = str_options
    terms = []
    for option in str2options:
        token_sort_ratio = fuzz.token_sort_ratio(str1,option)
        information = (option,token_sort_ratio)
        terms.append(information)

    terms.sort(key=lambda x:x[1],reverse=True)
    return(terms)

def elastic_single_search(term):
    term = term
    terms2match = []
    es = Elasticsearch(['http://...']) #INPUT THE RIGHT PATH TO THE ELASTIC SERVER YOU ARE USING

    body_query = {
    "from": 0, "size": 3,
    "query": {
        "dis_max": {
            "queries": [
                {"match_phrase_prefix" : {'http://www%2Ew3%2Eorg/2000/01/rdf-schema#label.value' : {"query":term}}},
                {"multi_match": {"query": term,"fuzziness": "AUTO:4,5","boost":2.0, "fields":["http://www%2Egeneontology%2Eorg/formats/oboInOwl#hasExactSynonym.value","http://www%2Ew3%2Eorg/2000/01/rdf-schema#label.value"]}}
        ]}
        }
        }

    result = es.search(index="ncit", body=body_query)

    for match in range(len(result["hits"]["hits"])):
        hits_info = result["hits"]["hits"][match]
        #link = hits_info['_source']["uri"]
        for synonym in range(len(hits_info['_source']["http://www%2Egeneontology%2Eorg/formats/oboInOwl#hasExactSynonym"])):
            synonym_all_info = hits_info['_source']["http://www%2Egeneontology%2Eorg/formats/oboInOwl#hasExactSynonym"][synonym]
            synonym_value = synonym_all_info["value"]
            terms2match.append(synonym_value)
    
    return terms2match

def elastic_multi_search(terms):
    es = Elasticsearch(['http://...']) #INPUT THE RIGHT PATH TO THE ELASTIC SERVER YOU ARE USING
    list_of_terms = terms
    final_dict = {}
    for num_query in range(0,len(list_of_terms),5000):
        list1 = list_of_terms[num_query:num_query+5000]
        semi_final_dict = {}
        queries = [{
            "from": 0, "size": 3,
            "query": {
                "dis_max": {
                    "queries": [
                        {"match_phrase_prefix" : {'http://www%2Ew3%2Eorg/2000/01/rdf-schema#label.value' : {"query":term}}},
                        {"multi_match": {"query": term,"fuzziness": "AUTO:4,5","boost":2.0, "fields":["http://www%2Egeneontology%2Eorg/formats/oboInOwl#hasExactSynonym.value","http://www%2Ew3%2Eorg/2000/01/rdf-schema#label.value"]}}
                ]}
                }
                } for term in list1]

        for i, results in enumerate(es.msearch(body=list(itertools.chain.from_iterable([{}, q] for q in queries)), index="ncit")["responses"]):
            # First, let's iterate over each hit, which will have a score for the class and a URL
            final_hit_info = []
            for match in range(len(results["hits"]["hits"])):
                hits_info = results["hits"]["hits"][match]
                hitscore = hits_info['_score']
                link = hits_info['_source']["uri"]
                synonyms = [] 

                # Having a hit from the class and to see what the class is about, let's look at the synonyms 
                for synonym in range(len(hits_info['_source']["http://www%2Egeneontology%2Eorg/formats/oboInOwl#hasExactSynonym"])):
                    synonym_all_info = hits_info['_source']["http://www%2Egeneontology%2Eorg/formats/oboInOwl#hasExactSynonym"][synonym]
                    synonym_value = synonym_all_info["value"]
                    synonyms.append(synonym_value)

                # Having the score, URL, and synonyms, let's find the term that best defines the class using string matching
                x = fuzzy_abrev_rank(list1[i],synonyms)
                # Since the class will always remain the same, we want to find the best term
                # To do this, we will allocate 25% for the class score and 75% for the string match
                # Again, this does not impact the class itself, it is merely to find the class with the best string match

                best_match_score = (hitscore*0.25)+((x[0][1])*0.75) 
                info = [link,hitscore,best_match_score,x[0][0],x[0][1]]
                final_hit_info.append(info)

            final_hit_info.sort(key=lambda x: x[2],reverse=True) #sort by string match score, from best to worst
            if list1[i] not in semi_final_dict.keys():
                semi_final_dict[list1[i]]=final_hit_info
    

        final_dict.update(semi_final_dict)
    return final_dict


if __name__ == "__main__":

    #Run this code to test the process
    #wordSet = "Processing any file this varaible should be a list of all item you whant to search"
    wordSet = []
    with open('File With All Terms','r') as file:
        for word in file.readlines():
            if word not in wordSet:
                wordSet.append(word)

    elastic_multi_search(wordSet)

