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
import json
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
        conversation = ConversationV1(
            username=convCreds['username'],
            password=convCreds['password'],
            version='2018-02-16'
        )
    except:
        return {
            'message': 'Please bind your conversation service'
        }

    # set up translator
    try:
        ltCreds = params['__bx_creds']['language_translator']
        translator = LanguageTranslatorV2(
            username=ltCreds['username'],
            password=ltCreds['password']
        )
    except:
        return {
            'message': 'Please bind your language translator service'
        }

    # check for empty or null string
    try:
        text = params['text']
        if not text:
            raise ValueError( 'Empty string passed!' )
    except:
        return {
            'message': 'Don\'t be shy... say something! (pass a value to the \'text\' param)'
        }

    # get conversation context if available
    try:
        context = json.loads( params['context'] )
    except:
        context = None

    # detect language
    res = translator.identify( text )
    if res['languages'][0]['confidence'] > 0.5:
        language = res['languages'][0]['language']
    else :
        language = 'en'

    # translate to english if needed
    if language != 'en':
        res = translator.translate( text, source=language, target='en' )
        text = res['translations'][0]['translation']

    # supply language as entity
    text += ' (@language:{})'.format( language )

    # hit conversation
    res = conversation.message(
        workspace_id=workspace,
        input={'text': text},
        context=context
    )
    newContext = res['context']
    output = res['output']
    message = res['output']['text'][0]
    intents = res['intents']

    # translate back to original language if needed
    if language != 'en':
        message = translator.translate( message, source='en', target=language )['translations'][0]['translation']
        output['text'][0] = message

    return {
        'message': message,
        'context': json.dumps( newContext ),
        'output': json.dumps( output ),
        'intents': json.dumps( intents ),
        'language': language
    }
