import openai, time
import pandas as pd

# Key removed, replace with valid key
openai.api_key = "input API key here"

df = pd.read_csv('input.csv')

claimIDs = []
claims = []
abstracts = []
responses = []

requests = 0

# Adjust temperature
temp = 0.75

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temp, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

for index, row in df.iterrows():
    claimIDs.append(row['id'])
    claims.append(row['claim'])
    abstracts.append(row['published_paper_abstract'])
    
print("Done with CSV read")
    
for index, row in df.iterrows():
     
    prompt = "Claim: " + claims[index] +"\nAbstract: " + abstracts[index] + "\n Question: Is the abstract relevant to the claim? Answer with one word and a number: SUPPORT if the abstract supports the claim, CONTRADICT if the abstract contradicts the claim or NEI if the abstract does not provide enough information about the claim to decide along with a number on a scale of 0-1000 rate how relevant the abstract is to the claim.  \n Answer: "
    
    if requests>0 and requests%20 == 0:
        print("Sleeping for 70 seconds...") # Can only make 20 calls a minute, sleep time can be lower but this worked for me
        time.sleep(70)
        print("Continuing...currently on request " + str(requests))
        
    requests += 1
    
    responses.append(get_completion(prompt))
    
    df.at[index, 'GPT_Response_0.75'] = responses[index] # Name of column in output file
    
    
df.to_csv('exported3.csv')

print("Done with export")

    
    

