import os
import config
import itertools
from lib import get_NGD,get_tokens
from wsdl import WSDL
"""
functions in this document
    get_similarity
    get_similarity_name
    get_similarity_type
    get_similarity_element
    get_similarity_input_output
    get_similarity_operation
    similarity_wsdl
    get_distance_matrix
    get_all_clusters
"""
#get similarity
def get_similarity(Vs1,Vs2):
    sum_=0
    for t1 in Vs1:
        for t2 in Vs2:
            sum_+=1-get_NGD(t1,t2)
    try:
        return sum_/(len(Vs1)*len(Vs2))
    except ZeroDivisionError:
        return 0

#similarity for service name / operation name /element name/ documentation
def get_similarity_name(name1,name2):
    return get_similarity(get_tokens(name1),get_tokens(name2))

#this gives the similarity of input/output types using operation
def get_similarity_type(operation1,operation2,_type="input"):
    operation1_types=[]
    operation2_types=[]
    for _input in operation1[_type]:
        for token in get_tokens(_input['type']):
            operation1_types.append(token.lower())
    for _input in operation2[_type]:
        for token in get_tokens(_input['type']):
            operation2_types.append(token.lower())

    # we are removing all 'type' in tokens
    O1_intersection_O2=len(filter(set(operation1_types).__contains__,operation2_types))
    try:
        return (2*O1_intersection_O2)/(len(operation1_types)+len(operation2_types))
    except:
        return 0

#this gives similarity of i/o names of elements in operation
def get_similarity_element(operation1,operation2,_type="input"):
    operation1_element=[]
    operation2_element=[]
    for _input in operation1[_type]:
        for token in get_tokens(_input['name']):
            operation1_element.append(token.lower())
    for _input in operation2[_type]:
        for token in get_tokens(_input['name']):
            operation2_element.append(token.lower())

    return get_similarity(operation1_element,operation2_element)

def get_similarity_input_output(operation1,operation2,_type="input"):
    return 0.5*(get_similarity_type(operation1,operation2,_type)+get_similarity_element(operation1,operation2,_type))

#pass array of operations
def get_similarity_operation(operationSet1,operationSet2):
    _sum=0
    for operation in operationSet1:
        _sum+=max([ 0.4*get_similarity_name(x['name'],operation['name'])+0.3*get_similarity_input_output(x,operation)+0.3*get_similarity_input_output(x,operation,"output") for x in operationSet2])
    for operation in operationSet2:
        _sum+=max([ 0.4*get_similarity_name(x['name'],operation['name'])+0.3*get_similarity_input_output(x,operation)+0.3*get_similarity_input_output(x,operation,"output") for x in operationSet1])
    return _sum/(len(operationSet1)+len(operationSet2))

def similarity_wsdl(wsdl1,wsdl2):
    return config.WEIGHT_SERVICE*get_similarity_name(wsdl1.service,wsdl2.service
                                                     )+config.WEIGHT_OPERATION* get_similarity_operation(wsdl1.operation,wsdl2.operation)

def get_distance_matrix():
    wsdl_files=os.listdir(config.SERVICES_FOLDER)
    distance_matrix={}
    for service in wsdl_files:
        service=config.SERVICES_FOLDER+service
        distance_matrix[service]={}
    for service1 in wsdl_files:
        service1=config.SERVICES_FOLDER+service1
        for service2 in wsdl_files:
            service2=config.SERVICES_FOLDER+service2
            if service1==service2:
                distance_matrix[service1][service2]=-1
            else:
                distance_matrix[service1][service2]=similarity_wsdl(WSDL(service1),WSDL(service2))
    return distance_matrix

#this gives cluster matrix along with the distances
def get_all_clusters(distance_matrix=[]):
    #initialize clusters
    clusters_matrix=distance_matrix
    """
    clusters_matrix={}
    clusters_matrix["1"]={}
    clusters_matrix["2"]={}
    clusters_matrix["3"]={}
    clusters_matrix["1"]["1"]=-1
    clusters_matrix["1"]["2"]=.2
    clusters_matrix["1"]["3"]=.45
    clusters_matrix["2"]["1"]=.2
    clusters_matrix["2"]["2"]=-1
    clusters_matrix["2"]["3"]=.6
    clusters_matrix["3"]["1"]=.45
    clusters_matrix["3"]["2"]=.6
    clusters_matrix["3"]["3"]=-1
    """
    while True:
        max_weight=[-1,"",""]
        for row in clusters_matrix.iterkeys():
            for col in clusters_matrix.iterkeys():
                if clusters_matrix[row][col]>max_weight[0]:
                    max_weight=[clusters_matrix[row][col],row,col]
        old_cluster=clusters_matrix.copy()

        if max_weight[0]>config.CLUSTERING_WEIGHT_THRESHOLD:
            clusters_matrix[max_weight[1]+","+max_weight[2]]={}
            for row in old_cluster.iterkeys():
                clusters_matrix[row][max_weight[1]+","+max_weight[2]]=max(clusters_matrix[row][max_weight[1]],clusters_matrix[row][max_weight[2]])
                clusters_matrix[max_weight[1]+","+max_weight[2]][row]=max(clusters_matrix[row][max_weight[1]],clusters_matrix[row][max_weight[2]])
            clusters_matrix[max_weight[1]+","+max_weight[2]][max_weight[1]+","+max_weight[2]]=-1
            clusters_matrix.pop(max_weight[1])
            clusters_matrix.pop(max_weight[2])
            old_cluster=clusters_matrix.copy()
            for row in old_cluster.iterkeys():
                try:
                    clusters_matrix[row].pop(max_weight[1])
                    clusters_matrix[row].pop(max_weight[2])
                except:
                    pass
        else:
            break
    #OUTPUT format [ ['1'] ,['3','2'], ['4','5','6'] ]
    return [x.split(",") for x in clusters_matrix.iterkeys()]
def get_all_clusters_k_means(distance_matrix=[]):
    #initialize clusters
    combinations=itertools.combinations([ distance for distance in distance_matrix.iterkeys()],config.K)
    wsdls=[ distance for distance in distance_matrix.iterkeys() ]
    max_weight=-1
    final_cluster=[]
    for combo in combinations:
        new_cluster=[[x] for x in combo]
        remaining=wsdls[:]
        for new in new_cluster:
            remaining.remove(new[0])
        for element in remaining:
            temp_max=-1
            index=-1
            for x in range(0,len(new_cluster)):
                if distance_matrix[new_cluster[x][0]][element]>temp_max:
                    temp_max=distance_matrix[new_cluster[x][0]][element]
                    index=x
            new_cluster[index].append(element)
        if temp_max>max_weight:
            max_weight=temp_max
            final_cluster=new_cluster[:]
    return final_cluster
