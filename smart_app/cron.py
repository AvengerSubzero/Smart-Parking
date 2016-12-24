from django_cron import CronJobBase, Schedule

def worker_function():
    i = 0
    print('Here')
    while True:
        for message in queue.receive_messages(MessageAttributeNames=['location']):
            i=1
            user_obtained = message.body
            user_record = es.search(index='smart_user',doc_type='user_profile'
                ,body={"query": {"match":{
                        "user":user_obtained  #Get from session
                      }}
            })
            user=user_record['hits']['hits']
            source = park_spot.get('_source')
            phone_number = source.get('phone_number')
            print(phone_number)
            response = client.publish(
                PhoneNumber=phone_number,
                Message="We are glad that you found Parking " \
                  ". Keep using our service. Thank you",
            )
            #message.delete()
        if i==1:
            i=0
        else:
            print("waiting")
            pass



class DeleteParking(CronJobBase):
    RUN_EVERY_MINS = 1 

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'smart_app.cron_job'    # a unique code

    def do(self):
        print("Hello")    # do your thing here
