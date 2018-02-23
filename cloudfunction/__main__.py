#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from watson_developer_cloud import ConversationV1, LanguageTranslatorV2


def main( params ):
    # get conversation workspace id
    try:
        workspace = params['conversation_workspace_id']
    except:
        return {
            'message': 'Please bind your conversation workspace ID as parameter'
        }

    # set up conversation
    try:
        convCreds = params['__bx_creds']['conversation']
        conversation = ConversationV1( username=convCreds['username'],
                                       password=convCreds['password'],
                                       version='2018-02-16' )
    except:
        return {
            'message': 'Please bind your conversation service'
        }

    # set up translator
    try:
        ltCreds = params['__bx_creds']['language_translator']
        translator = LanguageTranslatorV2( username=ltCreds['username'],
                                           password=ltCreds['password'] )
    except:
        return {
            'message': 'Please bind your language translator service'
        }


    # detect language

    return {'message': 'Hello world!!!!'}
