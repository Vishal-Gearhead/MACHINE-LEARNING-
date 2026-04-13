import streamlit as st
import pickle
import string
import nltk
from nltk.stem.porter import PorterStemmer

# 1. Initialize NLTK resources and Stemmer
ps = PorterStemmer()

# Handle NLTK downloads safely for offline/network issues
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')

# 2. Custom stopwords exactly as defined in your notebook
stopwords = {
    'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'it', 'they',
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did',
    'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because',
    'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
    'against', 'between', 'into', 'through', 'during', 'before', 'after',
    'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
    'over', 'under', 'again', 'further', 'then', 'once'
}


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)  # Use NLTK tokenizer to match notebook

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# 3. Load the Pickle files (ensure these are the NEW ones from Step 1)
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

import streamlit as st
import pickle
import string
import nltk
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

# Correct NLTK check
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# SAME stopwords as training
stopwords = {
    'i','me','my','we','our','you','your','he','she','it','they',
    'is','am','are','was','were','be','been','being',
    'have','has','had','do','does','did',
    'a','an','the','and','but','if','or','because',
    'as','until','while','of','at','by','for','with','about',
    'against','between','into','through','during','before','after',
    'above','below','to','from','up','down','in','out','on','off',
    'over','under','again','further','then','once'
}

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load correct files
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message", key="sms_input")

if st.button("Predict", key="predict_btn"):
    if input_sms.strip() == "":
        st.warning("Please enter a message.")
    else:
        transformed_sms = transform_text(input_sms)
        vector_input = tfidf.transform([transformed_sms])
        result = model.predict(vector_input)[0]

        if result == 1:
            st.error("Spam Detected")
        else:
            st.success("Not Spam")
