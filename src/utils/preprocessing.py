def clean_text(text):
    import re
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'\W+', ' ', text)  # Remove non-word characters
    return text.strip()  # Remove leading and trailing whitespace

def tokenize(text):
    return text.split()  # Split text into tokens based on whitespace

def preprocess_text(text):
    cleaned_text = clean_text(text)  # Clean the text
    tokens = tokenize(cleaned_text)  # Tokenize the cleaned text
    return tokens  # Return the list of tokens