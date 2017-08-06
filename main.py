from collections import Counter
from random import choice

import requests
import spacy
from bs4 import BeautifulSoup


def d(**kwargs):
    """
    { 'key': value, ... } => d(key=value, ...)

    :param kwargs: [String -> Value] Valid named arguments
    :return: [Dict] Dictionary of named arguments
    """
    return kwargs


def get_only_paragraph(soup):
    """
    Extract website content from <p> tag only.

    :param soup: [Object] BeautifulSoup object with parser
    :return:
    """

    return soup.findAll('p')


def is_ascii(sentence):
    """
    Allow sentence in English characters only, skip others.

    :param sentence: [String] String with unknown characters
    :return: [Optional[String]] String in ascii or None if out of ascii range
    """
    try:
        return sentence.encode('ascii')
    except UnicodeEncodeError:
        pass


def noise_words():
    """
    Exclude words for better term frequency of sentences.

    :return: [List[String]] Words that affect tf-idf counting
    """
    return ['-PRON-', 'this', 'the', 'to', 'like', 'have', 'but', 'example']


""" Module functions """


def get_website_content(url):
    """
    Get url website all text content.

    :param url: [String] Url of target website
    :return: [Dict] Title of the website & all text of the website in sentences
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    return d(title=soup.title.string,
             content=[p.get_text(strip=True) for p in get_only_paragraph(soup)])


def parse_ascii_sentences(sentences):
    """
    Encode each sentences in ascii format, skip single words.

    :param sentences: [List[String]] Total sentences in unknown format
    :return: [List[String]] List of sentences in valid English format
    """
    return [is_ascii(sentence) for sentence in sentences if ' ' in sentence]


def important_words(sentences, model):
    """
    Return (Important words, original sentence) pair from document.

    :param sentences: [List[String]] Total sentences of website
    :param model: [Object] NLP model for each sentence
    :return: [List[(List[String], String)]]
    """
    sentence_with_summary = []
    for sentence in sentences:
        if sentence:
            sentence_words = []
            sentence_str = str(sentence, encoding='utf-8')
            for word in model(sentence_str):
                if word.is_alpha and word.pos_ != 'ADP' and len(word) > 1 \
                        and word.lemma_ not in noise_words() \
                        and word.text not in spacy.en.language_data.STOP_WORDS:
                    sentence_words += [word.text]
            sentence_with_summary += [(sentence_words, sentence_str)]
    return sentence_with_summary


def important_words_in_sentences(sentences, word_counts):
    """
    Words in each document which occurs more than once.

    :param sentences: [List[List[String]]] Words in each sentences
    :param word_counts: [Counter] Count for each words in total sentences
    :return: [List[List[String]]] Words occurs more than once in sentences
    """
    return [[word for word in sentence if word_counts[word] > 1]
            for sentence in sentences]


def topic_words(sentences, more_then=None):
    """
    Return words occurs larger or equal to average maximum counts.
    E.g. 10 counts = 10 / 2 = 5 = (words occurs >= 5)

    :param sentences: [List[List[String]]] Important words in each sentence
    :param more_then: [Int] Threshold for removing less significant words
    :return: [List[(String, Int)] Significant words with count
    """

    def word_count(pair):
        """
        Return numeric count of each word.

        :param pair: [Tuple] (word, count)
        :return: [Int] count
        """
        return pair[1]

    words_count = Counter((word for sentence in sentences for word in sentence))
    threshold = more_then if more_then else int(words_count.most_common(1)[0][1] / 2)
    return sorted(filter(lambda p: word_count(p) >= threshold, words_count.items()),
                  key=word_count, reverse=True)


def sentences_with_topic_words(sentences, words):
    """
    Return sentences contain topic words.

    :param sentences: [List[(List[String], String)]] Important words with original sentences pairs
    :param words: [Set] Topic words
    :return: [List[String]] List of sentence contain topic words
    """
    return list({pair[1] for pair in sentences if pair and set(pair[0]).intersection(words)})


def pick_sentence(title, sentences):
    """
    Pack website title and random choice of sentences from the website.

    :param title: [String] Title of the website
    :param sentences: [List[String]] Random pick one of the sentences
    :return: [Dict] Dictionary with two results
    """
    return d(title=title, sentence=choice(sentences))


if __name__ == '__main__':
    url = 'https://www.infoq.com/news/2017/07/ieee-programming-language-rankin'
    # url = 'https://www.engadget.com/2017/08/04/marcus-hutchins-kronos-malwaretech/'
    page_content = get_website_content(url)
    parsed_content = parse_ascii_sentences(page_content['content'])
    common_words = important_words(parsed_content, spacy.load('en'))
    common_words_count = Counter([word for p in common_words for word in p[0]])
    parsed_sentence = important_words_in_sentences((p[0] for p in common_words), common_words_count)
    words_sentence_pair = list(zip(parsed_sentence, (p[1] for p in common_words)))
    important_words_count = topic_words((p[0] for p in common_words))
    words_only = {word[0] for word in important_words_count}
    available_sentences = sentences_with_topic_words(words_sentence_pair, words_only)
    for _ in range(10):
        print(pick_sentence(page_content['title'], available_sentences))
    pass
