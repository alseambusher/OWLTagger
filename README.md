#OWLTagger
Provides tags for a web services automatically from their OWLS documents using python
##Requirements
1. Linux system with python
2. sqlite3 library for python
3. Natural Language Toolkit (nltk) for python
4. To generate tags for new services you need internet to find Normalized Google Distance(ngd)
##OWLS docs
Place all the OWLS documents in the folder services/
##Clustering Technique
Two clustering techniques have been implemented
1. Default clustering technique can be used by changing the value of <code>K_MEANS_CLUSTERING</code> to <i>False</i> in config.py
2. To use K means set  <code>K_MEANS_CLUSTERING</code> to <i>True</i> and set the value of <code>K</code> to how many clusters you want
##Running
<code>python main.py \>out.htm</code>  
Now open the generated output in the browser
