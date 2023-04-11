#!/usr/bin/env python
# coding: utf-8

# # Word Doc Summariser
# 
# Summarises a Word doc for a child.

import os
import openai
from dotenv import load_dotenv
import re

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def summarise4Child(text):
    summarisationPrompt = "Summarize this for an eleven year old child:\n\n"
    fullPrompt = ''.join([summarisationPrompt, text])
    numWords = len(re.findall(r'\w+', text))
    tokens = numWords * 2
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullPrompt,
        temperature=0.7,
        max_tokens=tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0)
    
    firstChoice = response.choices[0]
    summary = firstChoice['text']
    
    return summary


with open('data/abstract.txt', 'r') as file:
    abstract = file.read().replace('\n', '')
abstractSummary = summarise4Child(abstract)

with open('data/introduction.txt', 'r') as file:
    introduction = file.read().replace('\n', '')
introSummary = summarise4Child(introduction)

summary = ''.join([abstractSummary, '\n\n', introSummary])

print(summary)
