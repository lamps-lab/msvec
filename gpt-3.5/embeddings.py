import openai, os, json, time
import tiktoken
#from openai.embeddings_utils import get_embedding, cosine_similarity

import numpy as np
from numpy.linalg import norm

openai.api_key = os.getenv("OPENAI_API_KEY")
#"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" soos.domi

#openai.api_key = "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" # zeus

# first embed the sentences GPT-3 embedding of text similarity
#def get_embeddings_for_claim(claim):


def get_embedding(text, model="text-embedding-ada-002"):
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

#def get_embeddings_for_abstract(abstract):

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def load_jsonl(fname, max_lines=None):
    res = []
    for i, line in enumerate(open(fname)):
        if max_lines is not None and i == max_lines:
            return res
        else:
            res.append(json.loads(line))
    return res


claims_file = load_jsonl("data/GeneralizedData.json") # 56
corpus_file = load_jsonl("data/NewCorpus.json")       # 5244

def getAbstractEmbedding(corpus_file):
	abstracts = [] # array of dictionaries
	requests = 0
	print(f"length of corpusFile: {len(corpus_file)}")
	for line in corpus_file:

		abstract = line['abstract']
		abstract_id = int(line['doc_id'])

		sentences = ""
		for sentence in abstract:
			sentences += sentence

		# OpenAI Rate Limit: 60 requests / min
		if requests > 0 and requests % 60 == 0:
			print("going to sleep for a min...z Z Z")
			print(f"{len(corpus_file) - requests} abstracts left to embed\n\n")
			time.sleep(62)
		embedding = get_embedding(sentences, "text-similarity-davinci-001")
		# text-similarity-davinci-001
		# text-similarity-curie-001
		# text-search-davinci-001
		requests += 1

		new_entry = {'docid': abstract_id, "abstract": sentences, "embedding": embedding}
		abstracts.append(new_entry)
	return abstracts


def getClaimEmbedding(claims_file):
	claims = [] # array of dictionaries
	requests = 0
	print(f"length of claimsFile: {len(claims_file)}")
	for line in claims_file:
		claimid = line['id']
		claim = line['claim']

		# OpenAI Rate Limit: 20 requests / min for Free Trial users
		if requests>0 and requests % 30 == 0: 
			print("going to sleep for a min...z Z Z")
			time.sleep(62)
			print(f"{len(claims_file) - requests} claims left")

		embedding = get_embedding(claim, "text-davinci-doc-001")
		# text-similarity-davinci-001
		# text-similarity-curie-001
		requests += 1
		print(len(embedding))
		new_entry = {'id': claimid, "claim": claim, "embedding": embedding}
		claims.append(new_entry)
	return claims



def getGroundTruth(claims_file, corpus_file):
	groundTruth = []
	claims = []
	for line in claims_file:
	    claim_id = line['id']
	    claim  = line['claim']
	    claims.append(claim)
	    evidence_label = line['evidence']
	    evidence_id = ""
	    label = ""

	    if evidence_label.keys():
	        evidence_id = int(list(evidence_label.keys())[0])
	        for ev in evidence_label.values():
	            for data in ev:
	                label = data['label']
	    #print(label, evidence_id)

	    for line in corpus_file:
	        abstract_id = int(line['doc_id'])
	        abstract = line['abstract']


	        if evidence_id == abstract_id:
	            new_entry = {'id': claim_id, 'claim': claim,"label":label ,"abstract": abstract}
	            groundTruth.append(new_entry)
	return groundTruth


# OUT -- 3 Files
#      | GroundTruth.json
#	   | ClaimEmbeddings.json
#      | AbstractEmbeddings.json

if __name__ == '__main__':
	GT = getGroundTruth(claims_file, corpus_file)
	with open("groundTruth.json", "w") as out:
		json.dump(GT, out, indent=4)

	#claims = getClaimEmbedding(claims_file)
	#with open("claimEmbeddings_Davinci.json", "w") as out:
	#	json.dump(claims, out, indent=4)

	#abstracts = getAbstractEmbedding(corpus_file)
	#with open("abstractEmbeddings_Davinci.json", "w") as out:
	#	json.dump(abstracts, out, indent=4)

