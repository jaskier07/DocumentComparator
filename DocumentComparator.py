import os
import re
from tkinter.ttk import *

import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
from hashlib import sha256

from IOUtils import IOUtils


class DocumentComparator:
    __PUNCTUATION = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
    __BAR_UPDATES = 5
    __CACHE_DIR_NAME = 'cache'
    __token = nltk.tokenize.ToktokTokenizer()
    __bar_incrementation_value = None

    def compare_documents(self, paths_to_pdf_files, bar):
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.__bar_incrementation_value = 100.0 / len(paths_to_pdf_files) / self.__BAR_UPDATES

        documents = {}
        documents_sizes = {}
        for path in paths_to_pdf_files:
            document_name = os.path.basename(path)
            document_file_size = os.path.getsize(path)
            doc_file = self.__get_file_path(document_name, document_file_size)
            document_content = ''
            if not doc_file.exists():
                document_content = IOUtils.pdf_to_text(path)
            documents[document_name] = document_content
            documents_sizes[document_name] = document_file_size
            self.__update_bar(bar)

        # Create a directory if it doesn't already exist
        cache_dir = Path(self.__CACHE_DIR_NAME)
        if not cache_dir.exists():
            Path(cache_dir).mkdir(parents=True)

        self.__update_bar(bar)
        corpus_preproc = []
        for doc_name, doc_content in documents.items():
            doc_file = self.__get_file_path(doc_name, documents_sizes[doc_name])
            if len(doc_content) == 0:
                cached_content = doc_file.read_text()
                corpus_preproc.append(cached_content)
                self.__update_bar(bar, steps_added=4)
            else:
                preprocessed_text = self.__clean_text(doc_content)
                self.__update_bar(bar)
                preprocessed_text = self.__clean_punct(preprocessed_text)
                self.__update_bar(bar)
                preprocessed_text = self.__stop_words_remove(preprocessed_text)
                self.__update_bar(bar)
                preprocessed_text = self.__lemitize_words(preprocessed_text)
                self.__update_bar(bar)
                corpus_preproc.append(preprocessed_text)
                doc_file.write_text(preprocessed_text, errors='xmlcharrefreplace')

        tfidf = self.__get_tfidf_vect_result(corpus_preproc)
        count = self.__get_count_vect_result(corpus_preproc)

        return self.__get_weighted_arr(tfidf, count)

    def __get_tfidf_vect_result(self, corpus):
        vectorizer = TfidfVectorizer(strip_accents='unicode')
        tfidf = vectorizer.fit_transform(corpus)
        sim_array = cosine_similarity(tfidf)
        np.fill_diagonal(sim_array, np.nan)
        return sim_array

    def __get_count_vect_result(self, corpus):
        vectorizer = CountVectorizer()
        count = vectorizer.fit_transform(corpus)
        sim_array = cosine_similarity(count)
        np.fill_diagonal(sim_array, np.nan)
        return sim_array

    def __get_weighted_arr(self, first_arr, second_arr, first_weight=0.7, second_weight=0.3):
        return first_arr * first_weight + second_arr * second_weight

    def __update_bar(self, bar: Progressbar, steps_added=1):
        bar['value'] = bar['value'] + self.__bar_incrementation_value * steps_added
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
        text = re.sub(r"\'\xaa", " ", text)
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
        remove_punctuation = text.translate(str.maketrans('', '', self.__PUNCTUATION))
        for w in words:
            punctuation_filtered.append(regex.sub('', w))
        filtered_list = self.__strip_list_noempty(punctuation_filtered)
        return ' '.join(map(str, filtered_list))

    def __get_file_path(self, filename, file_size):
        hashed_value = filename[:-4] + str(file_size)
        filename_hash = sha256(hashed_value.encode('utf-8')).hexdigest()
        return Path(self.__CACHE_DIR_NAME + '/' + filename_hash)
