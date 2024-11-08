import streamlit as st
import pandas as pd
import numpy as np
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")
def process_query(query, df):
    """
    Process the user's natural language query and retrieve relevant information from the dataset.

    Args:
        query (str): The user's natural language query.
        df (pandas.DataFrame): The dataset to be queried.

    Returns:
        str: The response to the user's query.
    """
    # Use spaCy to parse the user's query
    doc = nlp(query)

    # Define patterns to match common query types
    matcher = Matcher(nlp.vocab)
    pattern1 = [{"LOWER": "what"}, {"LOWER": "is"}, {"POS": "DET"}, {"POS": "NOUN"}]
    pattern2 = [{"LOWER": "show"}, {"POS": "DET"}, {"POS": "NOUN"}, {"POS": "NOUN"}]
    matcher.add("WHAT_IS", [pattern1])
    matcher.add("SHOW_ME", [pattern2])

    # Try to match the query patterns
    matches = matcher(doc)

    if matches:
        match_id, start, end = matches[0]
        match_text = doc[start:end].text.lower()

        # Handle "what is" queries
        if match_text == "what is":
            column = doc[3].text.lower()
            if column in df.columns:
                value = df[column].iloc[0]
                return f"The value for '{column}' is: {value}"
            else:
                return f"Sorry, the dataset does not contain a column named '{column}'."

        # Handle "show me" queries
        elif match_text == "show me":
            column1 = doc[2].text.lower()
            column2 = doc[3].text.lower()
            if column1 in df.columns and column2 in df.columns:
                return df[[column1, column2]].to_string(index=False)
            else:
                return f"Sorry, the dataset does not contain the columns '{column1}' and '{column2}'."

    # If no patterns match, provide a generic response
    return "I'm afraid I don't have enough information to answer that query."
def main():
    st.set_page_config(page_title="Text Automation Project")
    st.title("Text Automation Project")
    st.write("Upload a dataset and interact with it using natural language.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dataset loaded successfully!")
        st.dataframe(df)

        query = st.text_input("Enter your question about the dataset:")

        if query:
            response = process_query(query, df)
            st.write(response)
    else:
        st.write("Please upload a CSV file to get started.")