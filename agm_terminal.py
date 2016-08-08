# -*- coding: utf-8 -*-

import sys, re
from bottle import route, run, template, request, response, post
import urllib, urllib2, json
from time import sleep

# Global variables
defConf = {}
newConf = {}

jInput = None

answers = []


def main():
  get_input()
  set_conf()
  get_answers()

  bye()


def get_input():
  global jInput

  jInput = json.loads(sys.argv[1])


def set_conf():
  global defConf
  global newConf

  get_default()

  newConf = jInput['conf']
  newConf.update(defConf)


def get_default():
  global defConf

  i_file = open('default.conf', 'r')
  sInput = i_file.read()
  i_file.close()

  defConf = json.loads(sInput)


def get_answers(): 
  global answers

  for x in jInput['queries']:
    arguments = {'default-graph-uri': newConf['graph_uri'], 'format': 'application/sparql-results+json', 'timeout':'0', 'debug':'on', 'query':''}

    query = x['query'].encode('utf-8')
    arguments['query'] = query + '\n'
    
    # Start requesting
    sleep(newConf['query_interval'])

    full_url = newConf['kb_addresses'] + '?' + urllib.urlencode(arguments)  
    sOutput = urllib.urlopen(full_url).read()

    try:
      jOutput = json.loads(sOutput)
      var = jOutput['head']['vars'][0]
      for binding in jOutput['results']['bindings']:
        answer = binding[var]['value'].encode('utf-8')
        answers.append({'query': query, 'answer': answer})
    except Exception as e:
      pass

    if len(answers) >= newConf['answer_num']:
      bye()


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