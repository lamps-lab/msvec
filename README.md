# The MSVEC Dataset. 
We developed a new testing dataset, namely Multi-Domain Scientific Claim Verification Evaluation Corpus (MSVEC), covering true and false evidenced scientific claims in multiple domains, designed to evaluate the robustness of SCV models. 

We evaluate GPT-3.5 and MultiVerS to assess their capabilities in the multi-domain Scientific Claim Verification (SCV) task. 

# GPT-3.5
The GPT-3.5 model (also known as the ``text-davinci-003`` model) is a cutting-edge autoregressive LLM developed by OpenAI. This model contains 175 billion parameters, making it one of the most powerful LLMs currently available. 
## Data
To make it more efficient, the abstract-labeling task was completed in two steps. In the first step, we embedded the claims and abstracts using GPT embeddings. The cosine similarity between each claim and abstract vector was then calculated. We then took the top `k = 100` cosine similarities.

## Evaluation
The two subtasks were included in a single prompt. The abstract relevance was completed by GPT-3.5 as a number on a scale of 0-1000 how relevant the abstract is to the claim. The abstract label was prompted if the abstract SUPPORT/CONTRADICT/NEI the claim which was completed by GPT-3.5.



### E1.1: Abstract relevance
This subtask only evaluated the relevance of the abstracts to the claim. The GPT model was prompted to evaluate the relevance of the abstract on a scale of 0-1000. If the abstract was correctly matched with the claim based on the ground truth, and the relevance score was equal to or above 500, it was considered to be a true positive (TP).If the abstract and claim were supposed to be a match, but the relevance score was below 500, it was considered a false negative (FN). If the abstract and claim were not a true pair, but the relevance score was equal to or greater than 500, then it was considered to be a false positive (FP). If the abstract and claim were not supposed to match and the relevance score was below 500, then it was considered to be a true negative (TN). The evaluation revealed that nearly half of the predictions were FPs, resulting in low precision and a low overall F1 score of 0.48.

### E1.2: 
In this subtask, a TP if the model predicts the relevant abstract and the correct label.
The algorithm for determining the true positive rate involved checking whether the abstract ID retrieved in E1.1 is a true pair to the claim ID in the ground truth corpus and whether the label was correct. If the abstract ID did not match the claim ID in the ground truth and "NEI" was not present in the completion, then it resulted in an FP. If the abstract ID did not match the claim ID and "NEI" was present in the completion, then it counted as TN.

# MultiVerS 
## Data
Several datasets have been proposed to train and evaluate machine learning models for SCV. Notable datasets include SciFact, HealthVer, and Covid-Fact. 
### MSVEC
The MSVEC dataset consists of 56 scientific claims obtained from Snopes.com and Politifact.com, their truthfulness labels (e.g., true, false, or mixed) are manually verified by experts on these websites. Each claim is backed by one research paper that supports or refutes the claim. The search corpus contains 5,244 papers adopted from SciFact including 56 papers above. Each paper contains metadata (title, authors, year) and abstract obtained from online digital libraries. The domains of the dataset include miscellaneous fields like Biology, Medicine, Space, Science, Geology, Political and Covid related claims.

### SciFact
SciFact contained 1,409 scientific claims verified against a corpus of 5,183 abstracts. Abstracts that support or refute each claim are annotated with rationales (abstract sentences). Different from political fake news detection datasets, such as Fever, the claims do not have much context, and understanding them usually requires more domain knowledge than news articles and social media posts.

### HealthVer
The HealthVer dataset contains 14,330 health related (claim, evidence) pairs. The claims were mainly retrieved from TREC-COVID, a test collection that captures the information needs of biomedical researchers using the scientific literature during a pandemic. Each claim was verified against abstracts from the CORD-19, a comprehensive collection of scholarly articles related to COVID-19.

### CovidFact
The Covid-Fact dataset contains 4,086 claims extracted from Reddit, and verified by evidence from CORD-19  and  sources that are not contained in CORD-19 (mostly from the Web). The list of potential abstracts is provided for each claim, a portion of claims were negated by replacing certain words in the original claims. 

## Evaluation
### E1: Abstract-labeling
The results indicate that models trained and evaluated on datasets on similar domains generally perform significantly better than MSVEC. Specifically, the model trained on SciFact achieves an F1=0.67 on Covid-fact, the model trained on HealthVer achieves an F1=0.98 on SciFact and 0.64 on Covid-fact. The model trained on Covid-fact achieves an F1=0.78 on SciFact. However, there are exceptions. Specifically, the model fine-tuned on SciFact achieved an F1=0.04 for HealthVer and the model fine-tuned on Covid-fact achieved an F1=0.33 on HealthVer. The cross-evaluation matrix indicates that the HealthVer dataset is a challenging dataset and the model trained on this dataset seems more robust than the model trained on other datasets. However, all three models achieve poor results on the MSVEC dataset, achieving F1-scores of 0.05--0.14, respectively.

### E2: Sentence-Labeling
The objective of this task is to find the sentence rationale within an abstract. The performance in Table~\ref{tab:sent} indicate a similar trend as Table~\ref{tab:abstract}. The MultiVerS fine-tuned on SciFact or Covid-fact does not generalize well on HealthVer, with an F1=0.03 and F1-0.10, respectively. However, HealthVer seems to generalize well on SciFact with an F1=0.96, and poorly on Covid-fact with an F1-0.30. The results indicate that HealthVer is a more challenging dataset and the model fine-tuned on this dataset seems to generalize better than the model trained on the other datasets. However, all three models achieve nearly zero F1 on the MSVEC dataset. 

