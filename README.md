# OpenAI Doc Summariser

These scripts and notebooks allow you to summarise a Word document. You can also use it to create a set of test items.

The `doc-summariser.py` script expects to find a **ChatGPT.docx** Word file in the `data` directory. It reads through the file a paragraph at a time. It only processes paragraphs with more than 300 characters. It then uses GPT-3 to summarise each paragraph and write out a **summary.txt** file.