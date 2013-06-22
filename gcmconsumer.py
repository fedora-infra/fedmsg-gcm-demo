import sys
import fedmsg.consumers
import yaml

class GCMConsumer(fedmsg.consumers.FedmsgConsumer):
    topic = 'org.fedoraproject.prod.*'
    config_key = 'gcmconsumer'

    def __init__(self, *args, **kw):
        super(GCMConsumer, self).__init__(*args, **kw)

    def get_registration_ids_for_topic(self, topic):
        '''Get the Android/GCM registration IDs for all users who subscribe to a
           particular topic. We load the config each time so that we can change
           it on the fly to add users without having to miss any messages.'''
        config = yaml.load(file('/home/ricky/devel/fedora/fedmsg-gcm-demo/config.yaml', 'r'))
        return filter(None, [user['registration_id'] if topic in user['topics'] else None for user in config['users']])

    def consume(self, msg):
        users = self.get_registration_ids_for_topic(msg['topic'])
        if users:
            print "* SENDING MESSAGE TO USER(S)"
        print msg['topic']
