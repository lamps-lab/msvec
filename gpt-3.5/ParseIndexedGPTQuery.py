import pandas as pd

inFile = 'indexed_rationale_annotations_updated_true_responses_025.csv'
outFile = 'parsed_025_results.csv'

df = pd.read_csv(inFile)
claimIDs = [] 
GPT_Response = df['GPT_Response_0.25'].tolist()
i = 0
current = 0

print(GPT_Response)

for index, row in df.iterrows():
    
    claimIDs.append(row['id']) # For referencing next claim id during iteration

for index, row in df.iterrows():
    
    currentID = row['id']
    
    if(index <= (len(claimIDs) - 2)):
        nextID = claimIDs[index + 1]
        
    if(index == (len(claimIDs) - 1)):
        nextID = 0
    
    if str(i) in GPT_Response[current]:
        df.at[index, 'GPT_Response_rationale'] = 1
        
    else:
        df.at[index, 'GPT_Response_rationale'] = 0
        
    i += 1
    
    if(nextID != currentID):
        i = 0
        current += 1
        

df.to_csv(outFile, index=False)


        

        