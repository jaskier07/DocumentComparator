import os
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

from IOUtils import IOUtils


class DocumentComparator:

    PUNCTUATION = '!"#$%&\'()*+,./:;<=>?@[\\]^_`{|}~'
    token = nltk.tokenize.ToktokTokenizer()

    def compare_documents(self, paths_to_pdf_files):
        nltk.download('stopwords')
        nltk.download('wordnet')

        document_names = []
        document_contents = []
        for path in paths_to_pdf_files:
            document_names.append(os.path.basename(path))
            document_contents.append(IOUtils.pdf_to_text(path))

        corpusPreproc = []
        for text in document_contents:
            preprocessed_text = self.__clean_text(text)
            preprocessed_text = self.__clean_punct(preprocessed_text)
            preprocessed_text = self.__stopWordsRemove(preprocessed_text)
            preprocessed_text = self.__lemitizeWords(preprocessed_text)
            corpusPreproc.append(preprocessed_text)

        vect = TfidfVectorizer(stop_words="english", strip_accents='unicode')
        tfidf = vect.fit_transform(corpusPreproc)
        pairwise_similarity = tfidf * tfidf.T

        arr = pairwise_similarity.toarray()
        np.fill_diagonal(arr, np.nan)

        print(arr)

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

    def __lemitizeWords(self, text):
        words = self.token.tokenize(text)
        lemma = nltk.stem.WordNetLemmatizer()

        listLemma = []
        for w in words:
            x = lemma.lemmatize(w, pos="v")
            listLemma.append(x)
        return ' '.join(map(str, listLemma))

    def __stopWordsRemove(self, text):
        stop_words = set(nltk.corpus.stopwords.words("english"))
        words = self.token.tokenize(text)
        filtered = [w for w in words if not w in stop_words]
        return ' '.join(map(str, filtered))

    def __strip_list_noempty(self, mylist):
        new_list = (item.strip() if hasattr(item, 'strip') else item for item in mylist)
        return [item for item in new_list if item != '']

    def __clean_punct(self, text):
        words = self.token.tokenize(text)
        punctuation_filtered = []
        regex = re.compile('[%s]' % re.escape(self.PUNCTUATION))
        remove_punctuation = text.translate(str.maketrans('', '', self.PUNCTUATION))
        for w in words:
            punctuation_filtered.append(regex.sub('', w))
        filtered_list = self.__strip_list_noempty(punctuation_filtered)
        return ' '.join(map(str, filtered_list))

