#!/bin/env python
import urllib
import urllib2
import json
import math
import sqlite3
import config
from config import DB
"""
functions in this document
1. get_tokens
2. get_NGD
3. gsearch_count
4. get_NGD_from_db
5. new_NGD_entry
"""
def get_tokens(string):
    #remove spaces in begining and ending places
    string=str(string).strip().replace("\n"," ")
    string=string.replace("@","%").replace("_","%").replace(" ","%")
    for char in range(ord('A'),ord('Z')+1):
        string=string.replace(chr(char),"%"+chr(char))
    for num in range(0,10):
        string=string.replace(str(num),"%"+str(num))
    tokens=string.split("%")
    #merge CAPS
    caps=""
    delete_tokens=[]
    for i in range(0,len(tokens)):
        try:
            if not caps and len(tokens[i])==1 and tokens[i] in [ chr(x) for x in range(ord("A"),ord("Z")+1) ]:
                caps=tokens[i]
            elif caps and tokens[i][0] in [ chr(x) for x in range(ord("A"),ord("Z")+1) ]:
                delete_tokens.append(tokens[i-1])
                tokens[i]=tokens[i-1]+tokens[i]
            else:
                caps=""
        except:
            caps=""

    #now merge numbers
    num=None
    for i in range(0,len(tokens)):
        try:
            if not num and len(tokens[i])==1 and tokens[i] in [ str(x) for x in range(0,10) ]:
                num=tokens[i]
            elif num and tokens[i][0] in [ str(x) for x in range(0,10) ]:
                delete_tokens.append(tokens[i-1])
                tokens[i]=tokens[i-1]+tokens[i]
            else:
                num=None
        except:
            pass

    for delete in delete_tokens:
        tokens.remove(delete)
    #remove duplicates and nulls and return
    for token in tokens:
        if token in config.STOP_WORDS:
            tokens.remove(token)
    return filter(None,list(set(tokens)))

#NGD
def get_NGD(string1,string2):
    string1=string1.lower()
    string2=string2.lower()
    if string1==string2:
        return 0
    #if already in database return
    NGD_pre_calculated=get_NGD_from_db(string1,string2)
    if NGD_pre_calculated:
        if NGD_pre_calculated<0:
            return 0
        if NGD_pre_calculated>1:
            return 1
        else:
            return NGD_pre_calculated
    m = 45000000000
    try:
        n0 = int(gsearch_count(string1))
        n1 = int(gsearch_count(string2))
        n2 = int(gsearch_count(string1+" "+string2))
        l1 = max(math.log10(n0),math.log10(n1))-math.log10(n2)
        l2 = math.log10(m)-min(math.log10(n0),math.log10(n1))
        NGD=l1/l2
    except ValueError:
        print "adding new entry %s %s %d"%(string1,string2,1)
        new_NGD_entry(string1,string2,1)
        return 1
    print "adding new entry %s %s %s"%(string1,string2,str(NGD))
    new_NGD_entry(string1,string2,NGD)
    if l1/l2>1:
        NGD=1
    if l1/l2<0:
        NGD=0
    #Now store NGD
    return NGD

#google search count
def gsearch_count(searchfor):
    query = urllib.urlencode({'q': searchfor.lower()})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
    search_request=urllib2.Request(url)
    search_request.add_header('User-Agent',
                              'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.19) '
                              'Gecko/20081202 Firefox (Debian-2.0.0.19-0etch1)')
    search_request.add_header('Referer','http://www.facebook.com/')
    #search_request.add_header('X-Forwarded-For','173.252.110.27')

    search_response = urllib2.urlopen(search_request)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']
    try:
        return data['cursor']['estimatedResultCount']
    except:
        try:
            if data['cursor']['moreResultsUrl']:
                return 0
        except:
            print results
            exit(1)

def get_NGD_from_db(string1,string2):
    connect=sqlite3.connect(DB)
    cursor=connect.cursor()
    cursor.execute("select distance from ngd where (word1='"+string1+"' and word2='"+string2+"') or (word1='"+string2+"' and word2='"+string1+"')")
    data=cursor.fetchone()
    if data:
        return data[0]
    else:
        return None

def new_NGD_entry(string1,string2,distance):
    connect=sqlite3.connect(DB)
    cursor=connect.cursor()
    cursor.execute("insert into ngd values('"+string1+"','"+string2+"',"+str(distance)+")")
    connect.commit()
