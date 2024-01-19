import streamlit as st
import pandas as pd
import praw
import torch
from transformers import DistilBertForSequenceClassification
from transformers import DistilBertTokenizer

# Load the fine-tuned DistilBERT model
model_path = 'bert-fine-tuned1-20240119T065036Z-001/bert-fine-tuned1'
loaded_model = DistilBertForSequenceClassification.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
loaded_model.to(device)

client_id = 'qTaRShbBNN4ULvpkajVFsA'
client_secret = 'ntERZmdVdabqGKC1_o2qW4Zg4TRMEg'
user_agent = 'praw_scraper_2.2'

reddit = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    user_agent=user_agent)

# Load the DistilBERT tokenizer
tokenizer_directory = 'tokenizer_directory-20240119T065027Z-001/tokenizer_directory'
tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_directory)

def get_subreddit_comments(subreddit_name, num_comments, reddit_instance):
    subreddit = reddit_instance.subreddit(subreddit_name)
    comments = []
    
    for submission in subreddit.hot(limit=num_comments):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comments.append(comment.body)
            if len(comments) == num_comments:
                return comments
    
    return comments

# Streamlit App
st.title('Reddit Toxicity Predictor')

# Input: Subreddit Name
subreddit_name = st.text_input('Enter subreddit name:', 'worldnews')

# Input: Number of Comments to Extract
num_comments = st.slider('Number of comments to extract:', 10, 1000, 100)

# Button to Trigger Prediction
if st.button('Predict Toxicity'):
    # Get subreddit comments
    comments = get_subreddit_comments(subreddit_name, num_comments, reddit)
    # Tokenize and predict toxicity for each comment
    predicted_labels = []
    toxic_probabilities = []

    for i in range(0, len(comments), 50):  # Batch size of 50
        batch_comments = comments[i:i+50]
        tokenized_inputs = tokenizer(batch_comments, truncation=True, padding=True, max_length=128, return_tensors='pt')
        input_ids = tokenized_inputs['input_ids'].to(device)
        attention_mask = tokenized_inputs['attention_mask'].to(device)

        with torch.no_grad():
            outputs = loaded_model(input_ids, attention_mask=attention_mask)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
            _, predicted_labels_batch = torch.max(probabilities, 1)

        predicted_labels.extend(predicted_labels_batch.cpu().numpy())
        toxic_probabilities.extend(probabilities[:, 1].cpu().numpy())
        print("Processing comments batch:", i, "out of", len(comments), "total comments.")

    # Create a DataFrame to display the results
    results_df = pd.DataFrame({'Comment': comments, 'Toxicity Prediction': predicted_labels, 'Toxicity Probability': toxic_probabilities})
    
    # Display the results
    st.table(results_df)
