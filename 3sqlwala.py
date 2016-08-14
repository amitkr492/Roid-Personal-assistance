import re
import sqlite3
from collections import Counter
from string import punctuation
from math import sqrt
from nltk.tokenize import word_tokenize,sent_tokenize
import requests
import html2text
from summarise import *
from tokens import *
import warnings
warnings.filterwarnings("ignore")

# initialize the connection to the database
connection = sqlite3.connect('hamara.sqlite')
cursor = connection.cursor()
thVal = 6
toksInserted = {}

# create the tables needed by the program
try:
    # create the table containing the words
    cursor.execute('''
        CREATE TABLE `words` (
            `word`  TEXT UNIQUE
        )
    ''')
    # create the table containing the sentences
    cursor.execute('''
       CREATE TABLE `sents` (
            `sent` TEXT
        )''')
    # create association between weighted words and the next sentence
    cursor.execute('''
        CREATE TABLE `assoc` (
            `word_row`   INTEGER,
            `sent_row`   INTEGER,
            `weight`    INTEGER
        )
    ''')
except:
    pass

def getSent(inp):
    cursor.execute("select sent from sents where rowid='%s'" %inp)
    out = cursor.fetchone()
    return out[0]

def insertToken(inp):
    cursor.execute("select rowid from words where word='%s'" %inp)
    out = cursor.fetchone()
    if not out:
        out = cursor.execute("insert into words (word) values ('%s')"%inp)
        if out:
            toksInserted[inp] = cursor.lastrowid
            connection.commit()
            #print("inserted!!")
    else:
        toksInserted[inp] = out[0]
        #print("exists!!")

def insertAssoc(tok,sent,weight):
    lst = [tok,sent,weight]
    out = cursor.execute("insert into assoc (word_row,sent_row,weight) values('"+str(tok)+"','"+str(sent)+"','"+str(weight)+"')")
    if out:
        connection.commit()
        return cursor.lastrowid
    return -1

def insertSent(sent):
    out = cursor.execute("insert into sents (sent) values (?)", (sent,))
    if out:
        connection.commit()
        return cursor.lastrowid
    return -1

def getRowId(inp,colName):
    table = colName + "s"
    cursor.execute('SELECT rowid FROM ' + table + ' WHERE ' + colName + ' = ?', (inp,))
    out = cursor.fetchone()
    if out:
        return out[0]
    
    return -1


def sqlChat(H,B=""):
    flag = False
    dupValue = H

    B = getTokens(dupValue)
    myToks = B.split()
    sentIds = []
    dic = {}
    #print(myToks)
    for toks in myToks:
        #print(toks)  #finding the sentence row number and weight if the this association.
        cursor.execute("select sent_row, weight from assoc where word_row=(select rowid from words where word like '%s')" %toks)
        out = cursor.fetchall()     #fetching the all attribute
        #print(dic)

        if out:									#we have to understand this part
            for take in out:					#
                #print(take)					#
                if dic.has_key(take[0]):		#
                    dic[take[0]] += take[1]		#
                else:							#
                    dic[take[0]] = take[1]		#

    dic[-1] = 5
    #print(dic)
    maxSentW = max(dic,key=dic.get)
    sent = ""
    if dic[maxSentW] >= thVal:
        sent = getSent(maxSentW)					#sending the answer to user
        return [sent,1]

    # now, we don't have any answer. We search on google for the ans
    #print("Fetching answers online . . .")

    try:
        urls = getUrls(dupValue,1)
    except urllib2.URLError:
        badConnect()
        return [sent,0]
    #print(urls)
    if len(urls) > 0:
        try:
            H = getFirstAns(urls,H) # getting best answer from fetched urls
            sent = H
        except TimeoutError:
            badConnect()
    else:
        badConnect()

    if sent == "":
        return [sent,0]

    #print(urls,sent)

    #print(sent)
    sentRow = insertSent(sent)
    if sentRow == -1:
        print("Error Occured : Couldn't establish connection with Database")
        return [sent,1]

    #rating = float(raw_input("\n\nRate this answer (out of 10)>>> "))

    rating = 8				#defining the constant rating
    if len(myToks):
        weight = rating/(len(myToks))			#
    else:
        weight = rating
    for tok in myToks:
        insertToken(tok)
        #print(toksInserted)
        ret = insertAssoc(toksInserted[tok],sentRow,weight)
        if ret == -1:
            print("Error Occured : Couldn't establish connection with Database")
            return [sent,2]
    
    return [sent,2]                    

if __name__=='__main__':
    while True:
        doc = raw_input(">> ")
        retVal = sqlChat(doc)
        if retVal[1] != 2:
            print(retVal[0])