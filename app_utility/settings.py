# -*- coding: utf-8 -*-
import configparser
import os

cfile = os.path.join(os.path.dirname(__file__), 'config.ini')
cfg = configparser.ConfigParser()
cfg.read(cfile)

try:
    cfg.has_section('API')
except:
    raise Exception('Config File was not read.')

def get_urlroot():
    urlroot = "https://fmpcloud.io/api/v3/"
    return urlroot

def get_urlrootfmp():
    urlrootfmp = "https://financialmodelingprep.com/api/v3/"
    return urlrootfmp

def get_apikey():
    apikey = "cd3e1246d56d3d97c08705e74f21ea2e"
    return apikey

def set_apikey(apikey):
    cfg['API']['api_key'] = apikey
    with open(cfile, 'w') as configfile:
        cfg.write(configfile)
