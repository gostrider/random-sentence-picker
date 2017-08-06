# sentence-picker

## Description
`sentence-picker` is a simple tool for random picking text sentence from given url.
It make use of `spacy` NLP library for returning sentence that most relevant to the title of the webpage.

For the current status, the **most relevant** picks are select based on
 - Words that appears from the whole url content more then/same as `argmax(word_occurrence) / 2` times


The words filtering criteria are based on:
 - Non-Stopwords
 - Non-Spacy's 'ADP', E.g. conjunction, subordinating or preposition
 - Non-Pronoun
 - Is python alpha characters
 - Custom words blacklist

For details implementation, please read:

picker.py
`important_words(sentences, model)`

## Install

Require: Python 3.6+
```
pip install -e git+https://github.com/gostrider/random-sentence-picker.git#egg=sentence_picker
```

## Usage
```
from sentence_picker import picker

example_url = 'some-url'

# Return webpage title and sentences that match page title
page_title, available_sentences = picker.run_picking(example_url)

# Iterate 10 times to see the picks
for _ in range(10):
    print(pick_sentence(page_title, available_sentences))
```
