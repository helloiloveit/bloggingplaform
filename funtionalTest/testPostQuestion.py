__author__ = 'huyheo'
from gluon.contrib.webclient import WebClient


client = WebClient('http://127.0.0.1:8002/welcome/default/', postbacks = True)


