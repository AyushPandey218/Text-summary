import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from googletrans import Translator

# Initialize Translator
translator = Translator()

def translate_text(text, dest_lang='en'):
    # Detect language and translate to the specified language (English)
    detected_lang = translator.detect(text).lang
    translated_text = translator.translate(text, src=detected_lang, dest=dest_lang).text
    return translated_text, detected_lang

def summarizer(rawdocs):
    # Step 1: Translate input text to English
    rawdocs_english, original_lang = translate_text(rawdocs, 'en')

    # Step 2: Summarization logic
    stopwords = list(STOP_WORDS)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rawdocs_english)

    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            word_freq[word.text] = word_freq.get(word.text, 0) + 1

    max_freq = max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]
    sent_scores = {sent: sum(word_freq.get(word.text, 0) for word in sent) for sent in sent_tokens}
    select_len = int(len(sent_tokens) * 0.3)
    summary = ' '.join([sent.text for sent in nlargest(select_len, sent_scores, key=sent_scores.get)])

    # Step 3: Translate summary back to the original language
    summary_translated = translator.translate(summary, src='en', dest=original_lang).text
    return summary_translated, rawdocs, len(rawdocs.split(' ')), len(summary_translated.split(' '))