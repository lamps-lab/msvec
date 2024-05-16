import json

"""
E1.1:Abstract relevance, i.e., the two-stage method should be able to find if a paper is relevant to the claim or not.
"""


def readFiles(file, dataToEvaluate):
	with open(file, 'r') as in_file:
		data = json.load(in_file)
	for line in data:
		claimid = line['claimid']
		abstractid = line['abstractid']
		completion = line['completion']
		new_entry = {'claimid': claimid, 'abstractid': abstractid, 'completion': completion}
		dataToEvaluate.append(new_entry)



with open("../msvec.json", 'r') as in_file:
	groundTruthdata = json.load(in_file)


dataToEvaluate = []
files = ["results/top100Completion.json", "results/top100Completion2.json", "results/top100Completion3.json"]
for file in files:
	readFiles(file, dataToEvaluate)
print(len(dataToEvaluate))

trueP = 0
falseP = 0
trueN = 0
falseN = 0

for line in dataToEvaluate:
	claimid = line['claimid']
	abstractid = line['abstractid']
	completion = line['completion']

	label = ''
	for line in groundTruthdata:
		if claimid == line['id']:
			for doc_id, evidence_list in line['evidence'].items():
				for evidence in evidence_list:
					label = evidence['label']
					break

	predictedLabel, relevance = completion.split()
	relevance = int(relevance)
	if abstractid == claimid and relevance >= 500:
		trueP += 1
	elif abstractid == claimid and relevance < 500:
		falseN += 1
	elif abstractid != claimid and relevance >= 500:
		falseP += 1
	elif abstractid != claimid and relevance < 500:
		trueN += 1
total = (trueP + trueN + falseN + falseP)
print(total)
print(f"TP: {trueP} TN: {trueN}\nFP: {falseP} FN: {falseN} \ntotal: {total}")
accuracy = (trueP+trueN)/ total
precision = (trueP)/ (trueP+falseP)
recall = (trueP)/ (trueP+falseN)
f1 = 2 * ((precision*recall)/(precision+recall))

print(f"accuracy = {format(accuracy*100, '.2f')}% \nprecision = {format(precision*100,'.2f')}%\nrecall = {format(recall*100,'.2f')}%\nf1 = {format(f1*100,'.2f')}%")
results = str({'accuracy': format(accuracy*100, '.2f'), 'precision':format(precision*100,'.2f'), 'recall': format(recall*100,'.2f'), 'f1':format(f1*100,'.2f')})

with open("E1results.json", "w") as out:
	json.dump(results, out, indent=4)

with open("AllResults.json", "w") as out:
	json.dump(dataToEvaluate, out, indent=4)
