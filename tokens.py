import nltk
from nltk.tokenize import RegexpTokenizer

lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()

from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = stemmer.stem_word(word)
    word = lemmatizer.lemmatize(word)
    return word

def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40
        and word.lower() not in stopwords)
    return accepted

def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
        yield term


def getTokens(doc):
	#doc = "do you know anything about MNNIT"
	tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
	toks = tokenizer.tokenize(doc)
	postoks = nltk.tag.pos_tag(toks)
	
	grammar = r"""
	    NBAR:
	        # Nouns and Adjectives, terminated with Nouns
	        {<VB.*>*<NN.*|JJ>*<NN.*>}

	    NP:
	        {<NBAR>}
	        # Above, connected with in/of/etc...
	        {<NBAR><IN><NBAR>}
	"""

	chunker = nltk.RegexpParser(grammar)
	tree = chunker.parse(postoks)
	terms = get_terms(tree)
	
	toRet = []
	for term in terms:
		for t in term:
			toRet.append(t)

	toRet = ' '.join(toRet)
	return toRet

if __name__=='__main__':
	while True:
		doc = raw_input(">> ")
		print(getTokens(doc))