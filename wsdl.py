#!/bin/env python
import xml.dom.minidom as dom
import config
from lexical_analysis import lexical_analyzer
from lib import get_tokens
class WSDL():
    def __init__(self,wsdl):
        self.tree=dom.parse(wsdl)
        self.file_name=wsdl
        self.operation=self.operation()
        self.documentation=self.documentation()
        self.service=self.service()
        self.all_tokens,self.service_tokens,self.operation_tokens,self.message_tokens,self.type_tokens,self.documentation_token=self.get_all_tokens()
        config.COMPUTED_WSDL[wsdl]=self
    def operation(self):
        data=[]
        for atomic_process in self.tree.getElementsByTagName("process:AtomicProcess"):
            port={}
            port['name']=atomic_process.getAttributeNode("rdf:ID").nodeValue
            port['input']=[]
            port['output']=[]
            for input_ in atomic_process.getElementsByTagName("process:hasInput"):
                for input_node in self.tree.getElementsByTagName("process:Input"):
                    if "#"+input_node.getAttributeNode("rdf:ID").nodeValue==input_.getAttributeNode("rdf:resource").nodeValue:
                        try:
                            port['input'].append({'type':input_node.getElementsByTagName("process:parameterType")[0].getAttributeNode("rdf:resource").nodeValue.split("#")[-1],'name':input_node.getAttributeNode("rdf:ID").nodeValue})
                        except:
                            pass
                        try:
                            port['input'].append({'type':input_node.getElementsByTagName("process:dataType")[0].getAttributeNode("rdf:resource").nodeValue.split("#")[-1],'name':input_node.getAttributeNode("rdf:ID").nodeValue})
                        except:
                            pass

            for input_ in atomic_process.getElementsByTagName("process:hasOutput"):
                for input_node in self.tree.getElementsByTagName("process:Output"):
                    if "#"+input_node.getAttributeNode("rdf:ID").nodeValue==input_.getAttributeNode("rdf:resource").nodeValue:
                        try:
                            port['output'].append({'type':input_node.getElementsByTagName("process:parameterType")[0].getAttributeNode("rdf:resource").nodeValue.split("#")[-1],'name':input_node.getAttributeNode("rdf:ID").nodeValue})
                        except:
                            pass
                        try:
                            port['output'].append({'type':input_node.getElementsByTagName("process:dataType")[0].getAttributeNode("rdf:resource").nodeValue.split("#")[-1],'name':input_node.getAttributeNode("rdf:ID").nodeValue})
                        except:
                            pass

            data.append(port)
        return data
    def documentation(self):
        return self.tree.getElementsByTagName("profile:textDescription")[0].firstChild.data.replace("\n","")
    def service(self):
        return self.tree.getElementsByTagName("profile:serviceName")[0].firstChild.data.replace("\n","").replace(" ","_")
    def get_all_tokens(self):
        service_tokens=get_tokens(self.service)
        operation_tokens=[]
        message_tokens=[]
        type_tokens=[]
        for operation in [ y for y in [ get_tokens(x['name']) for x in self.operation ] ]:
            for sub_operation in operation:
                operation_tokens.append(sub_operation)
        for message in [ x['input'] for x in self.operation ]+[ x['output'] for x in self.operation ]:
            for sub_message in message:
                message_tokens+=get_tokens(sub_message['name'])
        for _type in [ x['input'] for x in self.operation ]+[ x['output'] for x in self.operation ]:
            for sub_type in _type:
                type_tokens+=get_tokens(sub_type['type'])
        documentation_token=lexical_analyzer(self.documentation)
        all_tokens=service_tokens+operation_tokens+message_tokens+type_tokens+documentation_token['NP']+documentation_token['NN']+documentation_token['VB']
        #NOTE THAT DOCUMENTATION IS A DICTIONARY NOT AN ARRAY
        return all_tokens,service_tokens,operation_tokens,message_tokens,type_tokens,documentation_token
