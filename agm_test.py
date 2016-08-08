# -*- coding: utf-8 -*-

import sys, os, json

tgm = 'http://121.254.173.77:1555/templategeneration/templator/'
dm = 'http://121.254.173.77:2357/agdistis/run'
tgm_stub = 'http://121.254.173.77:2360/ko/tgm/stub/service'
dm_stub = 'http://121.254.173.77:2361/ko/dm/stub/service'
qgm = 'http://121.254.173.77:38401/queries'
kb = 'http://dbpedia.org/sparql'


input_string = "{'conf': {'answer_num': 5, 'query_interval': 0.0}, 'queries': [{'query': 'SELECT ?v4 WHERE { ?v4 ?v2 <http://dbpedia.org/resource/Seoul> ; ?v7 <http://dbpedia.org/ontology/River> . } '}]}"
input_string = '"' + input_string.replace("'", "\\\"") + '"'

os.system('python agm_terminal.py ' + input_string)