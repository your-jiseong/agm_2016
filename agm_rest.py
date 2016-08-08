# -*- coding: utf-8 -*-

import sys, re, subprocess
from subprocess import Popen, PIPE
from bottle import route, run, template, request, response, post
import urllib, urllib2
import json

def enable_cors(fn):
  def _enable_cors(*args, **kwargs):
      # set CORS headers
      response.headers['Access-Control-Allow-Origin'] = '*'
      response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
      response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

      if request.method != 'OPTIONS':
          # actual request; reply with the actual response
          return fn(*args, **kwargs)
        
  return _enable_cors

@route(path='/agm', method=['OPTIONS', 'POST'])
@enable_cors
def query():
  i_text = request.body.read()
  i_json = json.loads(i_text)

  i_text = json.dumps(i_json)  

  # Executing controller & reading the results of the controller
  i_text = i_text.replace("\\", "\\\\")
  i_text = i_text.replace("\"", "\\\"")
  i_text = '"' + i_text + '"'
  
  print 'Input:', i_text
  cmd = 'python agm_terminal.py ' + i_text  
  p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
  stdout, stderr = p.communicate()
  o_text = stdout
  print 'Output:', o_text
  
  # Returning the results in JSON format
  #response.headers['Content-type'] = 'application/json'
  return o_text

run(server='cherrypy', host='121.254.173.77', port=7745)