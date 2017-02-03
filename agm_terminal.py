# -*- coding: utf-8 -*-

import sys, re
from operator import itemgetter
from bottle import route, run, template, request, response, post
import urllib, urllib2, json
from time import sleep

# Global variables
defConf = {}
newConf = {}

jInput = None

answers = []


def main():
	try:
		get_input()
		set_conf()
		get_answers()		

		bye()

	except Exception as e:
		o_file = open('error-report.txt', 'w+')
		o_file.write(str(e))
		o_file.close()


def get_input():
	global jInput

	fName = sys.argv[1]

	with open(fName) as json_file:
		jInput = json.load(json_file)


def set_conf():
	global defConf
	global newConf

	get_default()

	newConf = defConf
	newConf.update(jInput['conf'])


def get_default():
	global defConf

	i_file = open('default.conf', 'r')
	sInput = i_file.read()
	i_file.close()

	defConf = json.loads(sInput)


def get_answers(): 
	global answers

	exist = {}

	queries = jInput['queries']
	sorted_queries = sorted(queries, key=itemgetter('score'), reverse=True)

	#i_file = open('log', 'w+') # log

	for x in sorted_queries:
		if len(answers) >= int(newConf['answer_num']):
			#i_file.close() # log
			bye()

		#i_file.write(json.dumps(x['query']) + ' ' + json.dumps(x['score']) + '\n') # log

		arguments = {'default-graph-uri': newConf['graph_uri'], 'format': 'application/sparql-results+json', 'timeout':'0', 'debug':'on', 'query':''}
		query = x['query'].encode('utf-8')
		score = x['score']
		arguments['query'] = query + '\n'

		# Start requesting
		sleep(newConf['query_interval'])

		full_url = newConf['kb_addresses'] + '?' + urllib.urlencode(arguments)  
		sOutput = urllib.urlopen(full_url).read()

		#i_file.write(sOutput + '\n\n') # log

		try:
			jOutput = json.loads(sOutput)
			var = jOutput['head']['vars'][0]
			for binding in jOutput['results']['bindings']:
				try:
					answer = binding[var]['value'].encode('utf-8')
				except:
					answer = binding[var]['value']
				
				try:
					exist[answer]
				except KeyError:
					exist[answer] = True

					answers.append({'query': query, 'answer': answer, 'score': score})

		except Exception as e:
			pass


def send_getrequest(url):
	opener = urllib2.build_opener()
	request = urllib2.Request(url, headers={'Content-Type': 'application/json'})
	return opener.open(request).read()
	

def send_postrequest(url, input_string):
	opener = urllib2.build_opener()
	request = urllib2.Request(url, data=input_string, headers={'Content-Type': 'application/json'})
	return opener.open(request).read()


def bye():
	output = json.dumps(answers, indent=5, separators=(',', ': '))

	sys.stdout.write(output)
	sys.stdout.flush()
	sys.exit(0)


main()