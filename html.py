#!/bin/env python
import os
def distance_matrix(distance_matrix):
    print "<br /><h1>DISTANCE MATRIX</h1><br />"
    print "<table class='table'>"
    print "<tr><th></th>"
    for distance1 in distance_matrix.iterkeys():
        print "<th>"+distance1.split("/")[-1]+"</th>"
    print "</tr>"
    for distance1 in distance_matrix.iterkeys():
        print "<tr>"
        print "<th>"+distance1.split("/")[-1]+"</th>"
        for distance2 in distance_matrix.iterkeys():
            print "<td>"+str(distance_matrix[distance1][distance2])+"</td>"
        print "</tr>"
    print "</table>"

def cluster(clusters):
    print "<br /><h1>CLUSTERS</h1><br />"
    for _cluster in clusters:
        print "<div class='cluster_box'>"
        print "<br />".join([ x.split("/")[-1] for x in _cluster])
        print "</div>"

def tokens(token_weight):
    print "<br /><h1>TAGS</h1><br />"
    print "<table class='table'>"
    print "<tr><th>Service</th><th>Details</th></tr>"
    for tok_weight in token_weight.iterkeys():
        print "<tr>"
        print "<td>"+tok_weight.split("/")[-1]+"</td>"
        print "<td>"
        print "<table class='table' style='width:600px'>"
        print "<tr><th>Token</th><th>Weight</th></tr>"
        for token in reversed(token_weight[tok_weight]):
            print "<tr><td>"+token[0]+"</td><td>"+str(token[1])+"</td></tr>"
        print "</table>"
        print "</td>"
        print "</tr>"
    print "</table>"
def enriched_tag(enriched_tags):
    print "<br /><h1>ENRICHED TAGS</h1><br/>"
    print "<table class='table'>"
    print "<tr><th>Service</th><th>Tags</th></tr>"
    for enriched in enriched_tags.iterkeys():
        print "<tr>"
        print "<td>"+enriched.split("/")[-1]+"</td>"
        print "<td><table class='table' style='width:600px'>"
        print "<tr><th>Tag</th><th>Weight</th></tr>"
        for tag in reversed(list(enriched_tags[enriched])):
            print "<tr><td>"+tag[0]+"</td><td>"+str(tag[1])+"</td></tr>"
        print "</td><tr>"
        print "</table>"
    print "</table>"

def header():
    os.system("cat html/header.htm")

def footer():
    print "</body>"
    print "</html>"
