import streamlit as st
from wordcloud import WordCloud
import pandas as pd
import tempfile
import os
import re
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize

#function to count the frequency of each word in a text file and identify the part of speech of each word
def word_frequency_list(file):
    # open the file
    with open(file, 'r') as f:
        # read the file
        text = f.read()
        # convert the text to lowercase
        text = text.lower()
        # remove symbols and special characters
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # tokenize the text into words
        words = word_tokenize(text)
        # remove stop words
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        # create a dictionary to store the word frequency
        word_freq = {}
        # create a dictionary to store the part of speech of each word
        pos = {}
        # tag the words with their part of speech
        tagged_words = pos_tag(words)
        # for each word in the text
        for word in tagged_words:
             # if the word is not in the dictionary and the word is not a digit
            if word[0] not in word_freq and not word[0].isdigit():
                # add the word to the dictionary with a frequency of 1
                word_freq[word[0]] = 1
                # add the part of speech to the dictionary
                pos[word[0]] = word[1]
            # if the word is in the dictionary
            elif word[0] in word_freq:
                # add 1 to the frequency
                word_freq[word[0]] += 1
        # return the word frequency dictionary
        return word_freq, pos

# Add a title
st.title('Word Count and Part of Speech Tagger')

# Add a file uploader
uploaded_file = st.file_uploader("Choose a text file", type="txt")

if uploaded_file is not None:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        # Write the uploaded file to the temporary file
        fp.write(uploaded_file.getvalue())
        temp_file_path = fp.name

    if st.button('Run POS Tagger and Word Counter'):
        try:
            # Call your function
            word_freq, pos = word_frequency_list(temp_file_path)

            # Create a data frame of the results
            df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
            df['POS'] = df['Word'].map(pos)

            st.success("POS Tagger and Word Counter ran successfully.")
            # Display the first ten rows of the data frame
            st.dataframe(df.head(10))
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Set the output file location to the directory of the current script
    output_file_location = os.path.dirname(os.path.realpath(__file__))

    if st.button('Export CSV'):
        try:
            # Call your function
            word_freq, pos = word_frequency_list(temp_file_path)

            # Create a data frame of the results
            df = pd.DataFrame(list(word_freq.items()), columns=['Word', 'Frequency'])
            df['POS'] = df['Word'].map(pos)

            # Output the dataframe to a CSV file
            df.to_csv(os.path.join(output_file_location, 'words.csv'))
            st.success("CSV exported successfully.")
            st.info("Your CSV file will be in the same folder that you put this app.")
        
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