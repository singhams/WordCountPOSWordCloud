import nltk

nltk.download('tokenizers','punkt','corpora','stopwords','taggers','averaged_perceptron_tagger')

import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import tempfile
import base64
import datetime
import io
import os
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Function to count the frequency of each word in a text file and identify the part of speech of each word
def word_frequency_list(file):
    with open(file, 'r') as f:
        text = f.read()
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Tokenize the text into words
        words = word_tokenize(text)
        print("Tokenized Words:", words)  # Debug print
        
        # Remove stop words
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        print("Words after removing stop words:", words)  # Debug print
        
        # Create a dictionary to store the word frequency
        word_freq = {}
        # Create a dictionary to store the part of speech of each word
        pos = {}
        
        # Tag the words with their part of speech
        tagged_words = pos_tag(words)
        print("Tagged Words:", tagged_words)  # Debug print
        
        # For each word in the text
        for word, tag in tagged_words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
            pos[word] = tag
        
        return word_freq, pos

# Streamlit app title
st.title("Word Frequency and POS Tagger")

# App description
st.write("A very simple tool for processing a text file into a word frequency list with part of speech tags. Oh, and it can also create a word cloud, because why not?")

uploaded_file = st.file_uploader("Choose a text file", type="txt")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    if st.button('Run POS Tagger and Word Counter'):
        try:
            word_freq, pos = word_frequency_list(temp_file_path)

            # Debug print to check the word frequencies and POS tags
            print("Word Frequencies:", word_freq)
            print("POS Tags:", pos)

            # Create a data frame of the results
            df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
            df['POS'] = df['Word'].map(pos)

            # Sort the DataFrame by Frequency in descending order
            df = df.sort_values(by='Frequency', ascending=False)

            st.success("POS Tagger and Word Counter ran successfully.")
            # Display the first 20 rows of the data frame
            st.dataframe(df.head(20))

            # Generate a unique filename based on the current date and time
            filename = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.csv'

            # Create a download button for the DataFrame
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download csv file</a>'
            st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")


    if st.button('Generate Word Cloud'):
        try:
            # Read the uploaded file as a single string
            with open(temp_file_path, 'r') as file:
                text = file.read()

            # Create the word cloud
            wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate(text)

            # Save the word cloud as a png file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_image_file:
                wordcloud.to_file(temp_image_file.name)
                temp_image_path = temp_image_file.name

            # Display the word cloud
            st.image(temp_image_path)
            st.success("Word cloud generated successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
