from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import time
from datetime import datetime, timedelta
import os
from pprint import pprint
from decimal import Decimal
from geoposition import Geoposition
from django.template import RequestContext
from elasticsearch import Elasticsearch,RequestsHttpConnection
import re
import boto3
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.core.exceptions import *
from geopy.geocoders import Nominatim
import uuid, OpenSSL
import random
import sys
import math

host = 'search-smartpark-nvyav6u3qsvw3d2aa5rlpwoxb4.us-west-2.es.amazonaws.com'
port = 443

#es = Elasticsearch()
es = Elasticsearch(
        hosts=[{'host': host,'port':port}],
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )

sqs = boto3.resource('sqs',region_name='us-west-2')
queue = sqs.get_queue_by_name(QueueName='parking_test')
client = boto3.client('sns',region_name="us-west-2")

def generateRandomLocation():
    radius = 10000  # Choose your own radius
    radiusInDegrees = radius / 111300
    r = radiusInDegrees
    x0 = 40.760591
    y0 = -73.980014

    num_rows = 30
    for i in range(num_rows):  # Choose number of Lat Long to be generated

        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))

        w = r * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)

        xLat = x + x0
        yLong = y + y0
        print('%d,%.5f,%.5f \n' % (num_rows,xLat, yLong))
        doc = { 
                "location":{
                    "lat": str(xLat), 
                    "lon": str(yLong)  
                },
                "user": 'aup',
                "timestamp":datetime.now()
        }
        es.index(index='smart_test',doc_type='park',id = str(xLat)+'#'+str(yLong),body=doc)
    return HttpResponse('Done')

generateRandomLocation()