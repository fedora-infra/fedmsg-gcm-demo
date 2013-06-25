import fedmsg.consumers
import json
import requests
import sys
import yaml

class GCMConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.*'
    config_key = 'gcmconsumer'

    def __init__(self, *args, **kw):
        self.config_file = '/home/ricky/devel/fedora/fedmsg-gcm-demo/config.yaml'
        self.config = yaml.load(file(self.config_file, 'r'))
        super(GCMConsumer, self).__init__(*args, **kw)

    def _get_registration_ids_for_topic(self, topic):
        '''Get the Android/GCM registration IDs for all users who subscribe to a
           particular topic. We load the config each time so that we can change
           it on the fly to add users without having to miss any messages.'''
        self.config = yaml.load(file(self.config_file, 'r'))
        return filter(None, [user['registration_id'] if topic in user['topics'] else None for user in self.config['users']])

    def _send_gcm(self, data, ids):
        '''Send a message to GCM for specific registration IDs.'''
        headers = {
            'Authorization': 'key=%s' % self.config['api_key'],
            'content-type': 'application/json'
        }
        body = {
            'registration_ids': ids,
            'data': data
        }
        request = requests.post(
            self.config['post_url'],
            data=json.dumps(body),
            headers=headers)
        return request

    def consume(self, msg):
        users = self._get_registration_ids_for_topic(msg['topic'])
        for user in users:
            print "* SENDING MESSAGE TO USER: %s" % user
            response = self._send_gcm(
                {
                    'topic': msg['topic']
                },
                [user])
            print response.text
            print response.status_code
            print response

        print msg['topic']
