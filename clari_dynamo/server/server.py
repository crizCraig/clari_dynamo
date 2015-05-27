# -*- coding: utf-8 -*-

import os
import sys

# Hack for KMS patch - TODO: Remove after https://github.com/boto/boto/issues/2921
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/boto')

import cherrypy
from boto.dynamodb2.table import Table
from conf.constants import *

from clari_dynamo.clari_dynamo import ClariDynamo


class Server(object):
    def __init__(self, _db):
        self.db = _db

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def index(self):
        return HOME_TEXT

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def table(self, name):
        if cherrypy.request.method in ['PUT', 'POST']:
            data = cherrypy.request.json
            table = Table(name)
            self.db.put_item(table, data)
            cherrypy.log('creating a new item in ' + name)
        return {'success': True}

cherrypy.config.update({
    'server.socket_host':       '0.0.0.0',
    'server.socket_port':       int(os.environ.get('PORT', '55555')),
    'server.thread_pool':       150,  # Number of parallel requests
    'server.socket_queue_size': 200,  # Number of requests that can wait for a thread
    'server.socket_timeout':    20,
})


db_conf = {
    'aws_access_key_id':     AWS_ACCESS_KEY_ID,
    'aws_secret_access_key': AWS_SECRET_ACCESS_KEY,
    'is_remote':             IS_REMOTE,
    'is_secure':             IS_SECURE}

if IS_REMOTE:
    db_conf['host'] = 'localhost'
    db_conf['port'] = 8000

cherrypy.quickstart(Server(ClariDynamo(**db_conf)))
