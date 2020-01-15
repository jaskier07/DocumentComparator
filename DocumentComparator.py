import os
import re
from tkinter.ttk import *

import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from IOUtils import IOUtils


class DocumentComparator:
    __PUNCTUATION = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
    __BAR_UPDATES = 5
    __token = nltk.tokenize.ToktokTokenizer()
    __bar_incrementation_value: None

    def compare_documents(self, paths_to_pdf_files, bar):
        nltk.download('stopwords')
        nltk.download('wordnet')
        __bar_incrementation_value = 200.0 / len(paths_to_pdf_files) / self.__BAR_UPDATES

        document_names = []
        document_contents = []
        for path in paths_to_pdf_files:
            document_names.append(os.path.basename(path))
            document_contents.append(IOUtils.pdf_to_text(path))
            self.__update_bar(bar)

        self.__update_bar(bar)
        corpus_preproc = []
        for text in document_contents:
            preprocessed_text = self.__clean_text(text)
            self.__update_bar(bar)
            preprocessed_text = self.__clean_punct(preprocessed_text)
            self.__update_bar(bar)
            preprocessed_text = self.__stop_words_remove(preprocessed_text)
            self.__update_bar(bar)
            preprocessed_text = self.__lemitize_words(preprocessed_text)
            self.__update_bar(bar)
            corpus_preproc.append(preprocessed_text)

        vect = TfidfVectorizer(stop_words="english", strip_accents='unicode')
        tfidf = vect.fit_transform(corpus_preproc)
        pairwise_similarity = tfidf * tfidf.T

        arr = pairwise_similarity.toarray()
        np.fill_diagonal(arr, np.nan)

        return arr

    def __update_bar(self, bar: Progressbar):
        bar['value'] = bar['value'] + 10
        bar.update()

    def __clean_text(self, text):
        text = text.lower()
        text = re.sub(r"what's", "what is ", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "can not ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r"\'scuse", " excuse ", text)
        text = re.sub(r"\'\n", " ", text)
        text = re.sub(r"\'\xa0", " ", text)
        text = re.sub('\s+', ' ', text)
        text = text.strip(' ')
        return text

    def __lemitize_words(self, text):
        words = self.__token.tokenize(text)
        lemma = nltk.stem.WordNetLemmatizer()

        list_lemma = []
        for w in words:
            x = lemma.lemmatize(w, pos="v")
            list_lemma.append(x)
        return ' '.join(map(str, list_lemma))

    def __stop_words_remove(self, text):
        stop_words = set(nltk.corpus.stopwords.words("english"))
        words = self.__token.tokenize(text)
        filtered = [w for w in words if not w in stop_words]
        return ' '.join(map(str, filtered))

    def __strip_list_noempty(self, mylist):
        new_list = (item.strip() if hasattr(item, 'strip') else item for item in mylist)
        return [item for item in new_list if item != '']

    def __clean_punct(self, text):
        words = self.__token.tokenize(text)
        punctuation_filtered = []
        regex = re.compile('[%s]' % re.escape(self.__PUNCTUATION))
        # FIXME Linia poniżej jest nieużywana, ma zostać?
        remove_punctuation = text.translate(str.maketrans('', '', self.__PUNCTUATION))
        for w in words:
            punctuation_filtered.append(regex.sub('', w))
        filtered_list = self.__strip_list_noempty(punctuation_filtered)
        return ' '.join(map(str, filtered_list))
