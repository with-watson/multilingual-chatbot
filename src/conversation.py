# wrapper around watson conversation

# lib
from watson_developer_cloud import ConversationV1
import json
import requests


class Conversation:
    def __init__( self, key=None, namespace=None ):
        self.namespace = namespace
        self.key = key
        self.lastContext = {}
        self.lastOutput = {}
        self.base = 'https://openwhisk.ng.bluemix.net/api/v1'

        response = self.MakeRequest( '', {} )

        self.lastContext = response['context']
        self.lastOutput = response['output']['text'][0]

    # hit conversation service and return response
    def MakeRequest( self, msg, context ):
        body = {'text': msg,
                'context': context}
        response = requests.post( '{}/namespaces/{}/actions/translator'.format( self.base, self.namespace ),
                                  data=body )
        return response.json()

    def Converse( self ):
        msg = input( self.lastOutput + '\n' )
        res = self.MakeRequest( msg, self.lastContext )
        self.lastContext = res['context']
        self.lastOutput = res['output']['text'][0]
