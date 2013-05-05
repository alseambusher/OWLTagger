import nltk
"""
functions in this file
    get_sentence
    get_noun_phrase_tree
    lexical_analyzer
"""
def get_sentence(document):
    sentences=nltk.sent_tokenize(document)
    sentences=[nltk.word_tokenize(sent) for sent in sentences]
    sentences=[nltk.pos_tag(sent) for sent in sentences][0]
    #TODO change this grammar
    grammar="NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    #returns a tree and an array
    return cp.parse(sentences),sentences

def get_noun_phrase_tree(myTree, phrase="NP"):
    myPhrases = []
    if (myTree.node == phrase):
        myPhrases.append( myTree.copy(True) )
    for child in myTree:
        if (type(child) is nltk.tree.Tree):
            list_of_phrases = get_noun_phrase_tree(child, phrase)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)
    return myPhrases

def lexical_analyzer(string):
    data={'NP':[],'NN':[],'VB':[]}
    if not string:
        return data
    sentence_tree,sentence=get_sentence(string)
    myPhrases=get_noun_phrase_tree(sentence_tree)
    NP=[]
    for phrase in myPhrases:
        NP.append("")
        for word in phrase:
            NP[-1]+=" "+word[0]
        NP[-1]=NP[-1][1:]
    data['NP']=NP
    data['NN']=[ x for (x,y) in sentence if y[0]=="N" ]
    data['VB']=[ x for (x,y) in sentence if y[0]=="V" ]
    return data

