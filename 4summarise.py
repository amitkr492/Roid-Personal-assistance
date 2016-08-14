from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import urllib2
from searcher import search
from timeout import timeout
from timeout import TimeoutError
from goose import Goose

LANGUAGE = "english"
SENTENCES_COUNT = 10

#for printing urls found in google
try:
    def getUrls(query, no = 5):
    	urls = []
    	for url in search(query, num = no,stop = 1):
    		urls.append(url)
    	return urls
except UnboundLocalError:
    pass

def badConnect():
    print("OOpssy... bad connection")

@timeout(10)
def getReply(url,inp):
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sents = []
    print(parser.document)
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        sents.append(sentence)

    return sents
    #inp = inp.split()

def getFirstAns(url,inp=""):
    gooser = Goose()                  #using them goose for extracting the articles
    article = gooser.extract(url=url[0])
    text = article.cleaned_text.split(".")
    return ".".join(text[:4])					#taking first 4 lines of them articles

if __name__=="__main__":
    while True:
        inp = raw_input("search >> ")
        urls = getUrls(inp)
        for url in urls:
            print (url)
            try:
                print(getFirstAns(url,inp)) 
            except TimeoutError:
                print("Your connection's too slow")