import os, json
import tiktoken
#from openai.embeddings_utils import get_embedding, cosine_similarity

import numpy as np
from numpy.linalg import norm



# first embed the sentences GPT-3 embedding of text similarity
#def get_embeddings_for_claim(claim):


#def get_embeddings_for_abstract(abstract):

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


# calculate cosine similarity
def cosine_similarity(claim_vector, abstract_vector):
    similarity = np.dot(claim_vector, abstract_vector) / (norm(claim_vector) * norm(abstract_vector))
    return similarity

def get_top_k_similar_pairs(claims, abstracts, k=100):
    similarities = []
    for claim in claims:
        claimid = claim['id']
        claimembedding = claim['embedding']
        for abstract in abstracts:
            abstractid = abstract['docid']
            abstractembedding = abstract['embedding']

            similarity = cosine_similarity(claimembedding, abstractembedding)
            new_entry = {'claimid': claimid, "abstractid": abstractid, "similarity": similarity}
            similarities.append(new_entry)
    sorted_similarities = sorted(similarities, key=lambda x: x['similarity'], reverse=True)

    return sorted_similarities[:k]


def load_jsonl(fname, max_lines=None):
    res = []
    for i, line in enumerate(open(fname)):
        if max_lines is not None and i == max_lines:
            return res
        else:
            res.append(json.loads(line))
    return res


def getAbstracts():
	abstracts = [] # array of dictionaries

	with open("abstractEmbeddings.json", 'r') as file:
		data = json.load(file)

	print(len(data))
	for line in data:
		abstract = line['abstract']
		abstractid = int(line['docid'])
		embedding = line['embedding']
		sentences = ""
		for sentence in abstract:
			sentences += sentence

		new_entry = {'docid': abstractid, "abstract": sentences, "embedding": embedding}
		abstracts.append(new_entry)
	return abstracts


def getClaims():
	claims = [] # array of dictionaries
	#{'id': claimid, "claim": claim, "embedding": embedding}

	with open('claimEmbeddings.json', 'r') as file:
		data = json.load(file)

	print(len(data))
	for line in data:
		claimid = str(line['id'])
		claim = line['claim']
		embedding = line['embedding']

		new_entry = {'id': claimid, "claim": claim, "embedding": embedding}
		claims.append(new_entry)
	return claims


#GT: new_entry =# {'id': claim_id, 'claim': claim,"label":label ,"abstract": abstract}



# Step 2:

# query the 100 prompts against GPT-3 and compare the results


# OUT 
if __name__ == '__main__':
	claims = getClaims()
	abstracts = getAbstracts()

	topk = get_top_k_similar_pairs(claims, abstracts)
	for k in topk:
		print(k)

	with open("top100Pairs.json", "w") as out:
		json.dump(topk, out)
