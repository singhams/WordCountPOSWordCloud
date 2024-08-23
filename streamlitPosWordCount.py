import nltk

def download_nltk_packages():
    nltk_packages = [
        ('tokenizers', 'punkt'),
        ('corpora', 'stopwords'),
        ('taggers', 'averaged_perceptron_tagger'),
    ]

    for package in nltk_packages:
        try:
            nltk.data.find(f'{package[0]}/{package[1]}')
        except LookupError:
            nltk.download(package[1])

download_nltk_packages()

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
from nltk.tokenize.punkt import PunktTokenizer
from nltk.tag.perceptron import PerceptronTagger

# Function to count the frequency of each word in a text file and identify the part of speech of each word
def word_frequency_list(file):
    with open(file, 'r') as f:
        text = f.read()
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        tokenizer = PunktTokenizer()
        words = tokenizer.tokenize(text)
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        word_freq = {}
        pos = {}
        tagger = PerceptronTagger()
        tagged_words = tagger.tag(words)
        for word, tag in tagged_words:
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
            pos[word] = tag
        return word_freq, pos

# Streamlit app code
st.title("Word Frequency and POS Tagger")

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
            wordcloud.to_file(os.path.join(output_file_location, 'wordcloud.png'))

            # Display the word cloud
            st.image(os.path.join(output_file_location, 'wordcloud.png'))
            st.success("Word cloud generated successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
