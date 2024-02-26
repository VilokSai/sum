import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


def Extractive(text):
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    # print(doc)
    token = [token.text for token in doc]
    # print(token)
    word_freq = {}

    for word in doc:

        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:

            if word.text not in word_freq.keys():
                word_freq[word.text] = 1

            else:
                word_freq[word.text] += 1

    # print(word_freq)

    max_freq = max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # print(word_freq)

    sent_tokens = [sent for sent in doc.sents]

    sent_score = {}

    for sent in sent_tokens:

        for word in sent:

            if word.text in word_freq.keys():

                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text]

                else:
                    sent_score[sent] += word_freq[word.text]

    # print(sent_score)

    select_len = int(len(sent_tokens) * 0.4)

    from heapq import nlargest

    summary = nlargest(select_len,sent_score,key = sent_score.get)

    final_summary = [word.text for word in summary]

    summary = ' '.join(final_summary)

    return summary, doc, len(text.split(' ')), len(summary.split(' '))

def Abstractive(text,min,max):
  min = int(min)
  max = int(max)

  model = T5ForConditionalGeneration.from_pretrained('t5-3b')

  tokenizer = T5Tokenizer.from_pretrained("t5-3b", use_fast=True)

  device = torch.device('cpu')

  pre_processed_text= text.strip().replace('\n','')

  t5_input_text = 'summarize:' + pre_processed_text

  tokenized_text = tokenizer.encode(t5_input_text, return_tensors='pt').to(device)

  summary_ids = model.generate(tokenized_text, min_length = min, max_length= max)

  summary = tokenizer.decode(summary_ids[0],skip_special_tokens=True)

  return summary,text,len(text.split(' ')), len(summary.split(' '))

