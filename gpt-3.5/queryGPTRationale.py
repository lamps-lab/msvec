import openai, time
import pandas as pd

inFile = 'indexed_rationale_annotations.csv'
outFile = 'indexed_rationale_annotations_query_responses_075.csv'

# Insert valid API key
openai.api_key = "sk..."

requests = 0

# Adjust GPT temperature
temp = 0.75
i = 0
claimIDs = [] 
abstracts = []
abstractsNoBrackets = []
prompts = []
question = "Question: Which of the numbered sentences support the claim? Answer with only a list of numbers.\n"
responses = []

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temp, # This is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


df = pd.read_csv(inFile)

for index, row in df.iterrows():
    
    # Used to compare next id in index during iteration
    claimIDs.append(row['id'])
    
for index, row in df.iterrows():
    
    currentID = row['id']
    
    if(index <= (len(claimIDs) - 2)):
        nextID = claimIDs[index + 1]
        
    if(index == (len(claimIDs) - 1)):
        nextID = 0
    
    abstracts.append(row['published_paper_abstract'] + "\n")
    abstractsNoBrackets = ''.join(abstracts)

    i += 1
    
    if(nextID != currentID):
        prompts.append("Claim: " + str(row['claim']) + "\n" + question + abstractsNoBrackets)
        abstracts = []
        abstractsNoBrackets = []
        i = 0
        
promptsDF = pd.DataFrame(prompts, columns=['prompts'])
promptsDF = pd.concat([df, promptsDF], axis=1)

print('Done with prompt generation starting query\n')

for pos, p in enumerate(prompts):
    
    if requests>0 and requests%20 == 0:
        
        # Can make 20 calls a minute, sleep time can be lower but this worked for me
        print("\nSleeping for 70 seconds...\n")
        time.sleep(70)
        print("Continuing...currently on request " + str(requests))
        
    attempts = 0
    success = False
    
    # Kept getting ServiceUnavailableError without try block
    while attempts < 10 and not success:
    
        try:
            responses.append(get_completion(p))
            success = True
        
        except openai.error.ServiceUnavailableError as e:
            attempts += 1
            if attempts == 10:
                break
        
    # Name of column in output file
    promptsDF.at[pos, 'GPT_Response_0.75'] = responses[pos] 
    
    requests += 1
    
promptsDF.to_csv(outFile, index=False)
print('\nDone with export!')
    