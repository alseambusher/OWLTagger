import config
from HANDMADE_TAGS import HANDMADE_TAGS
import math
import operator
import clustering
import lib
from wsdl import WSDL
"""
Functions in this file
    get_weight_structure
    get_weight_lexical
    get_weight_frequency
    total_token_weight
    tag_enriching
"""
def get_weight_structure(wsdl):
    all_tokens,service_tokens,operation_tokens,message_tokens,type_tokens,documentation_token=wsdl.all_tokens,wsdl.service_tokens,wsdl.operation_tokens,wsdl.message_tokens,wsdl.type_tokens,wsdl.documentation_token
    weight_service=1.0
    weight_documentation=1.0/16
    weight_operation=weight_service/(len(wsdl.operation)-1+2)
    weight_message=weight_operation/(len([ x['input'] for x in wsdl.operation ]+[ x['output'] for x in wsdl.operation ])-1+2)
    weight_type=weight_message/(len([ x['input'] for x in wsdl.operation ]+[ x['output'] for x in wsdl.operation ])-1+2)
    weight={}
    for x in documentation_token['NP']+documentation_token['VB']+documentation_token['NN']:
        weight[x]=weight_documentation
    for x in type_tokens:
        weight[x]=weight_type
    for x in message_tokens:
        weight[x]=weight_message
    for x in operation_tokens:
        weight[x]=weight_operation
    for x in service_tokens:
        weight[x]=weight_service
    return weight

def get_weight_lexical(wsdl):
    all_tokens=wsdl.all_tokens
    weight={}
    for x in all_tokens:
        if x in config.STOP_WORDS:
            weight[x]=0
        else:
            weight[x]=1
    return weight

def get_weight_frequency(wsdl,clusters):
    for sub in clusters:
        if wsdl.file_name in sub:
            cluster=sub
            break
    all_tokens_frequency={}
    all_tokens_frequency_max=-1
    for token in wsdl.all_tokens:
        all_tokens_frequency[token]=wsdl.all_tokens.count(token)
        all_tokens_frequency_max=max(all_tokens_frequency_max,wsdl.all_tokens.count(token))
    document_frequency={}
    #TODO TEST THIS
    cluster_wsdl=[]
    for x in cluster:
        try:
            cluster_wsdl.append(config.COMPUTED_WSDL[x])
        except:
            cluster_wsdl.append(WSDL(x))
    for token in wsdl.all_tokens:
        for other_wsdl in cluster_wsdl:
            if token in other_wsdl.all_tokens:
                try:
                    document_frequency[token]+=1
                except:
                    document_frequency[token]=1
    weight={}
    for token in wsdl.all_tokens:
        weight[token]=(0.5+all_tokens_frequency[token]/all_tokens_frequency_max)*math.log10(0.5+len(cluster)/document_frequency[token])
    return weight

def total_token_weight(wsdl,clusters):
    total={}
    weight_structure=get_weight_structure(wsdl)
    weight_lexical=get_weight_lexical(wsdl)
    weight_frequency=get_weight_frequency(wsdl,clusters)

    total=weight_structure
    for token in weight_lexical.iterkeys():
        total[token]+=weight_lexical[token]
    for token in weight_frequency.iterkeys():
        total[token]+=weight_frequency[token]
    #NOTE THAT THIS DOESNT RETURN A DICTIONARY!!
    return sorted(total.iteritems(), key=operator.itemgetter(1))

def tag_enriching(wsdl,clusters,distance_matrix):
    for sub in clusters:
        if wsdl.file_name in sub:
            cluster=sub
            cluster.remove(wsdl.file_name)
            break
    score={}
    for service in cluster:
        for tag in HANDMADE_TAGS[wsdl.file_name]:
            score[tag]=distance_matrix[service][wsdl.file_name]+clustering.get_similarity(wsdl.service_tokens,lib.get_tokens(tag))
    return sorted(score.iteritems(), key=operator.itemgetter(1))
