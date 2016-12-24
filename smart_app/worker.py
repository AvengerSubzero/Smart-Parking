import boto3
import multiprocessing
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from geopy.geocoders import Nominatim

sqs = boto3.resource('sqs',region_name='us-west-2')
queue = sqs.get_queue_by_name(QueueName='parking_test')

host = ''#YOUR HOST
port = 443

#es = Elasticsearch()
es = Elasticsearch(
        hosts=[{'host': host,'port':port}],
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )

client = boto3.client('sns',region_name="us-west-2")

class Worker():

    def worker_function(self):
        flag = 0
        for message in queue.receive_messages(MessageAttributeNames=['id']):
            i=1
            user_obtained = message.body
            print(user_obtained)
            user_record = es.search(index='smart_user',doc_type='user_profile'
                ,body={"query": {"match":{
                        "username":user_obtained #Get from session
                      }}
            })
            id = message.message_attributes.get('id').get('StringValue')
            user=user_record['hits']['hits']
            source = user[0].get('_source')
            user_id = user[0].get('_id')
            phone_number = source.get('phone_number')
            points = source.get('points')
            points = str(10 + int(points))
            lat = id.split('#')[0]
            lon = id.split('#')[1]
            address = self.rev_geocode(lat,lon)
            if address is not None:
                es.update(index="smart_user",doc_type="user_profile",id=user_id,body = {"doc":{"points"
                    :points}})
                response = client.publish(
                    PhoneNumber='+1'+phone_number,
                    Message="We are glad that you found Parking at "+address+". Keep"\
                     "using our service. You have  Thank you"  
                )
                message.delete()
            if flag == 1:
                flag = 0
            else:
                print("No more messages")
                break

    def thread_pool(self):
        multiprocessing.Pool(10,self.worker_function(),(queue,))

    def rev_geocode(self,lat,lon):
        try:
            geolocator = Nominatim()
            location = geolocator.reverse("{}, {}".format(lat, lon))
            return location.address
        except:
            return None
