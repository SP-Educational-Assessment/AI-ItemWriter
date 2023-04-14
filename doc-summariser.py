#!/usr/bin/env python
# coding: utf-8

# # Word Doc Summariser
# 
# Summarises a Word doc for a child to be no less than 1500 words

import os
import openai
from dotenv import load_dotenv
from docx import Document
import re

MIN_PARA_CHARS=300

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG")



def summarise4Child(text):
    summarisationPrompt = "Summarize this paragraph for an ten year old child, using a single complete sentence:\n\n"
    fullPrompt = ''.join([summarisationPrompt, text])
    numWords = len(re.findall(r'\w+', text))
    tokens = numWords // 2
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullPrompt,
        temperature=0.4,
        max_tokens=tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    
    firstChoice = response.choices[0]
    summary = firstChoice['text']
    
    return summary


def main():
    fileName = 'data/ChatGPT.docx'
    document = Document(fileName)
    summaryDoc = []
    totalWords = 0
    p = 1

    for para in document.paragraphs:
        text = para.text
        if len(text) > MIN_PARA_CHARS:
            textWords = len(re.findall(r'\w+', text))
            summary = summarise4Child(text)
            summaryWords = len(re.findall(r'\w+', summary))
            totalWords += summaryWords
            summaryDoc.append(summary)
            print("P{}: IN WORDS = {}, OUT WORDS = {}".format(p, textWords, summaryWords))
            p += 1

    # now write out to a new text document
    with open('summary.txt', 'w') as f:
        for s in summaryDoc:
            f.write(s)

    print("Total of {} words".format(totalWords))



if __name__ == "__main__":
    main()