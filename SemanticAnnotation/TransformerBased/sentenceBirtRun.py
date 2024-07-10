from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import normalize
from tqdm import tqdm

def all_upper(my_list):
    return [x.upper() for x in my_list]

def displayMatchedPairs(targetLabel, matchedPairs):
    # Display the matched pairs for the current target label
    print(f"Target: {targetLabel}")
    for target_label, candidate_label, candidate_uri, similarity in matchedPairs:
        print(f"  Candidate Label: {candidate_label}, Candidate URI: {candidate_uri}, Similarity Score: {similarity}")
    print()

def OntologyTransformer(targetLabels, candidateURIS, candidateLabels):
    """
    Requires: 
    Ensures:
    """

    model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")

    # Handling the target
    target_labels = all_upper(targetLabels)
    candidate_uris = candidateURIS
    candidate_labels = all_upper(candidateLabels)

    bestFit = {}

    batch_size = 200  # Number of labels to process in each batch

    # Iterate over each target label batch
    for i in tqdm(range(0, len(target_labels), batch_size), desc="Processing targets"):

        target_label_batch = target_labels[i:i + batch_size]

        # Encode the target label and candidate labels
        target_embeddings = model.encode(target_label_batch)
        candidate_embeddings = model.encode(candidate_labels)

        ####### NORMALIZATION ########
        target_embeddings = normalize(target_embeddings)
        candidate_embeddings = normalize(candidate_embeddings)

        # Compute dot product between target and candidate embeddings
        similarities = target_embeddings.dot(candidate_embeddings.T)

        # Compute cosine similarity between target and candidate embeddings if prefered
        # similarities = cosine_similarity(target_embeddings, candidate_embeddings)

        # Set the similarity threshold
        threshold = 0.6
        # Find the matching pairs
        matched_pairs = []
        for j in range(len(target_label_batch)):
            matching_indices = [k for k, similarity in enumerate(similarities[j]) if similarity >= threshold]
            matching_pairs = [(target_labels[i + j], candidate_labels[k], candidate_uris[k], similarities[j][k])
                              for k in matching_indices]
            matched_pairs.extend(matching_pairs)

        matched_pairs.sort(key=lambda x: x[-1], reverse=True)

        for pair in matched_pairs:
            target_label = pair[0]
            if target_label not in bestFit:
                bestFit[target_label] = pair[1:]

    return bestFit


def OntologyTransformerIndividual (targetLabels, candidateURIS, candidateLabels):
    
    model = SentenceTransformer("sentence-transformers/multi-qa-mpnet-base-dot-v1")

    #Handling the tareget
    target_labels = targetLabels
    candidate_uris = candidateURIS
    candidate_labels = candidateLabels

    bestFit = {}
    
    # Iterate over each target label
    for target_label in tqdm(target_labels, desc="Processing targets"):
        # Encode the target label and candidate labels
        target_embeddings = model.encode([target_label])
        candidate_embeddings = model.encode(candidate_labels)
        
        ####### NORMALIZATION IF NEEDED ########
        target_embeddings = normalize(target_embeddings)
        candidate_embeddings = normalize(candidate_embeddings)

        # Compute dot product between target and candidate embeddings
        similarities = target_embeddings.dot(candidate_embeddings.T)

        # Compute cosine similarity between target and candidate embeddings
        #similarities = cosine_similarity(target_embeddings, candidate_embeddings)

        # Set the similarity threshold
        threshold = 0.85

        # Find the matching pairs
        matched_pairs = []
        for i, similarity in enumerate(similarities[0]):
            if similarity >= threshold:
                candidate_uri = candidate_uris[i]
                candidate_label = candidate_labels[i]
                matched_pairs.append((target_label, candidate_label, candidate_uri, similarity))

        matched_pairs.sort(key = lambda x: x[-1] ,reverse =True)
        
        #displayMatchedPairs(target_label,matched_pairs)

        if target_label not in bestFit and len(matched_pairs)>0:
            bestFit[target_label] = matched_pairs[0][1:]
    
    return bestFit
    