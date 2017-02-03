# -*- coding: utf-8 -*-

import sys, re, random, string
from operator import itemgetter
from subprocess import Popen, PIPE
from bottle import route, run, template, request, response, post
import urllib, urllib2
import json
import socket

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
  iText = request.body.read()

  fName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
  iFile = open(fName, 'w+')
  iFile.write(iText)
  iFile.close()

  print 'Input:', iText

  cmd = 'python agm_terminal.py ' + fName  
  p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
  stdout, stderr = p.communicate()
  oText = stdout

  print 'Output:', oText

  cmd = 'rm ' + fName
  p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
  stdout, stderr = p.communicate()

  return oText

run(server='cherrypy', host=socket.gethostbyname(socket.gethostname()), port=7745)