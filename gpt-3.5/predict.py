
import openai, json, time

#openai.api_key = "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"


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

		new_entry = {'id': claimid, "claim": claim}
		claims.append(new_entry)
	return claims

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

def getSimilar():
	similar = []

	with open("top100Pairs.json", "r") as in_file:
		data = json.load(in_file)

	print(len(data))
	for line in data:
		claimid = line['claimid']
		abstractid = line['abstractid']

		new_entry = {'claimid': claimid, 'abstractid':abstractid}
		similar.append(new_entry)
	return similar


#claim = "Populations of wild deer across North America have tested positive for SARS-CoV-2 antibodies."
#claimid = 2
#abstract = "The origin of severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2), the virus causing the global coronavirus disease 2019 (COVID-19) pandemic, remains a mystery. Current evidence suggests a likely spillover into humans from an animal reservoir. Understanding the host range and identifying animal species that are susceptible to SARS-CoV-2 infection may help to elucidate the origin of the virus and the mechanisms underlying cross-species transmission to humans. Here, we demonstrated that white-tailed deer (Odocoileus virginianus), an animal species in which the angiotensin-converting enzyme 2 (ACE2)—the SARS-CoV-2 receptor—shares a high degree of similarity to that of humans, are highly susceptible to infection. Intranasal inoculation of deer fawns with SARS-CoV-2 resulted in established subclinical viral infection and shedding of infectious virus in nasal secretions. Notably, infected animals transmitted the virus to noninoculated contact deer. Viral RNA was detected in multiple tissues 21 days postinoculation (p.i.). All inoculated and indirect contact animals seroconverted and developed neutralizing antibodies as early as day 7 p.i. The work provides important insights into the animal host range of SARS-CoV-2 and identifies white-tailed deer as a wild animal species susceptible to the virus"
#abstractid = 2

responses = []

claims = getClaims()
abstracts = getAbstracts()
similar = getSimilar()

requests = 0

for entry in similar:
	claimid = int(entry['claimid'])
	for c in claims:
		if claimid == int(c['id']):
			claim = c['claim']

	abstractid = int(entry['abstractid'])
	for abstract in abstracts:
		if abstractid == abstract['docid']:
			sentences = abstract['abstract']

	#if abstractid == abstracts['docid']:
	#s	sentences = abstracts['abstract']
	#print(claim)
	prompt = "Claim: " + claim +"\nAbstract: " + sentences + "\n Question: Is the abstract relevant to the claim? Answer with one word and a number: SUPPORT if the abstract supports the claim, CONTRADICT if the abstract contradicts the claim or NEI if the abstract does not provide enough information about the claim to decide along with a number on a scale of 0-1000 rate how relevant the abstract is to the claim.  \n Answer: "

	#print(prompt)
	if requests>0 and requests%20 == 0:
		print("going to sleep for a min...z Z Z")
		time.sleep(63)
		print(f"{len(similar) - requests} claims left")
	requests += 1
	completion = openai.Completion.create(engine="text-davinci-003",prompt=prompt,temperature=0.5,max_tokens=15,top_p=1,frequency_penalty=0,presence_penalty=0)
	text = completion['choices'][0]['text']
	#print(text)

	newEntry = {'claimid':claimid, "abstractid": abstractid, "completion": text}
	print(newEntry)
	responses.append(newEntry)

with open("top100Completion3.json", "w") as out:
	print("writing to file...")
	json.dump(responses, out, indent=4)

