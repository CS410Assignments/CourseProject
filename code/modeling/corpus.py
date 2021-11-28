import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize.punkt import PunktSentenceTokenizer
from gensim.models.phrases import Phrases
from gensim.corpora import Dictionary, MmCorpus
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.word2vec import Text8Corpus
import tempfile
import os
import re
import json

ENGLISH_CONNECTOR_WORDS = frozenset(
    " a an the "  # articles; we never care about these in MWEs
    " for of with without at from to in on by "  # prepositions; incomplete on purpose, to minimize FNs
    " and or "  # conjunctions; incomplete on purpose, to minimize FNs
    .split()
)

CORPUS_SPECIFIC_STOPWORDS = {'lecture', 'sound', 'music'}

nltk.data.path = [os.path.abspath('../../data/nltk_data')] + nltk.data.path
_tokenizer = RegexpTokenizer(r'\w+')
_sentence_tokenizer = PunktSentenceTokenizer()
_lemmatizer = WordNetLemmatizer()
_stoplist = set('for a of the and to in'.split())
_local_docs_path = os.path.abspath('../../data/transcripts')
_dictionary_path = os.path.abspath('../../tmp/dictionary.dict')
_corpus_path = os.path.abspath('../../tmp/corpus.mm')
_phrases_path = os.path.abspath('../../tmp/phrases.pkl')
_data_path = os.path.abspath('../../data')

def _get_docs(path):
	if os.path.isfile(path):
		with open(path, 'r') as doc:
			yield doc.read()
	else:			
		for root, dirs, files in os.walk(path):
			for name in files:
				with open(os.path.join(root, name), 'r') as doc:
					if name.endswith('.json'):
						yield slide_words(os.path.join(root, name))
					else:		
						yield doc.read()

def slide_words(path):
	with open(path) as file:
		data = json.loads(file)
		last_slide = data[len(data) - 1]
		if 'Additional Reading' in last_slide:
			last_slide = ''
		last_slide = last_slide.replace('Topics Covered in This Course', '')
		last_slide = last_slide.replace('Summary', '')
		data[len(data) - 1] = last_slide
		yield ' '.join([value for key, value in data.items() if key != '0'])

def _tokenize_doc(doc):
	doc = re.sub('\n', ' ', doc)
	doc = doc.lower()  # Convert to lowercase.
	doc = _tokenizer.tokenize(doc)  # Split into words.	
	doc = [token for token in doc if token not in stopwords.words('english')]
	doc = [token for token in doc if token not in STOPWORDS]
	doc = [token for token in doc if token not in CORPUS_SPECIFIC_STOPWORDS]
	doc = [token for token in doc if not token.isnumeric()]
	doc = [token for token in doc if len(token) > 1]
	return [_lemmatizer.lemmatize(topic) for topic in doc]

def _tokenize(path):
	for doc in _get_docs(path):
	  yield _tokenize_doc(doc)

def get_sentences(path):
	for doc in _get_docs(path):
		for sentence in _sentence_tokenizer.tokenize(doc):
			yield _tokenize_doc(sentence)

def _generate_phrases(path):
	return Phrases(get_sentences(path), min_count=5, connector_words=ENGLISH_CONNECTOR_WORDS)

def _generate_dict(tokens_file):
	return Dictionary([re.sub(os.linesep, '', line).split(',') for line in tokens_file.readlines()])

def _generate_corpus(tokens_file, dictionary):
	for doc in (re.sub(os.linesep, '', line).split(',') for line in tokens_file.readlines()):
		yield dictionary.doc2bow(doc)


def build_corpus(build_phrases = True):
	phrases = None
	if (build_phrases):
			phrases = _generate_phrases(os.path.join(_data_path, 'transcripts')).freeze()
			phrases.save(_phrases_path)

	with tempfile.TemporaryFile(mode = 'w+t') as fp:
		for path in [os.path.join(_data_path, 'transcripts'), os.path.join(_data_path, 'slides_raw_text')]:
			for doc in _tokenize(path):
				fp.write(','.join(doc))
				fp.write(os.linesep)
		if (build_phrases):
			fp.seek(0)
			for root, dirs, files in os.walk(os.path.join(_data_path, 'transcripts')):
				for name in files:
					sentences = get_sentences(os.path.join(root, name))
					for phrase in phrases[sentences]:
						re.sub(os.linesep, '', fp.readline()).split(',').append(phrase)
		fp.seek(0)
		dictionary = _generate_dict(fp)
		dictionary.save(_dictionary_path)
		fp.seek(0)
		MmCorpus.serialize(_corpus_path, _generate_corpus(fp, dictionary))


def get_prebuilt_dictionary():
	return Dictionary.load(_dictionary_path)	

def get_prebuilt_corpus():
	return MmCorpus(_corpus_path)

def get_prebuilt_phrases():
	return Phrases.load(_phrases_path)
