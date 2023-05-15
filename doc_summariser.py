"""Summarises a Word doc for a child to be no less than 1500 words."""

#!/usr/bin/env python3
# coding: utf-8

import os
import re

import openai
import spacy
from docx import Document
from dotenv import load_dotenv

MIN_PARA_CHARS = 300

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG")

nlp = spacy.load("en_core_web_sm")
stopMarks = set("?!.")


def return_full_sentences(text):
    """
    Tokenizes the input text into sentences and returns only those that end
    with certain punctuation marks.

    Args:
    text (str): The input text to be tokenized.

    Returns:
    str: A string containing all the full sentences found in the input text,
    joined together with a single space.

    Raises:
    ValueError: If the input text is empty or None.
    """

    doc = nlp(text)
    sentences = [s.text for s in doc.sents if s.text[-1:] in stopMarks]
    return " ".join(sentences)


def summarise_4_child(text):
    """
    Summarises the text input for a 10 year old child.

    Args:
    text (str): The input text to be summarised.

    Returns:
    str: A string containing the summary.

    Raises:
    ValueError: If the input text is empty or None.
    """

    summarisation_prompt = "Summarize this paragraph for a ten year old child:\n\n"
    full_prompt = "".join([summarisation_prompt, text])
    num_words = len(re.findall(r"\w+", text))
    tokens = (
        num_words // 2
    )  # output summary should be no more than half the original text length

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=full_prompt,
        temperature=0.4,
        max_tokens=tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    first_choice = response.choices[0]
    summary = return_full_sentences(first_choice["text"])

    return summary


def main():
    """
    The main function that summarizes the text content of a given Word document file.

    Returns:
    None

    Raises:
    IOError: If the input Word document file cannot be found or opened.
    """

    file_name = "data/ChatGPT.docx"
    document = Document(file_name)
    summary_doc = []
    total_words = 0
    p = 1

    for para in document.paragraphs:
        text = para.text
        if len(text) > MIN_PARA_CHARS:
            text_words = len(re.findall(r"\w+", text))
            summary = summarise_4_child(text)
            summary_words = len(re.findall(r"\w+", summary))
            total_words += summary_words
            summary_doc.append(summary)
            print(f"P{p}: IN WORDS = {text_words}, OUT WORDS = {summary_words}")
            p += 1

    # now write out to a new text document
    with open("summary.txt", "w", encoding="utf-8") as f:
        for s in summary_doc:
            f.write(s)

    print(f"Total of {total_words} words")


if __name__ == "__main__":
    main()
