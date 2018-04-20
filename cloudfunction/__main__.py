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
import time

# consts
BASE_LANGUAGE = 'en'
LT_HEADERS = {
    'X-Watson-Technology-Preview': '2017-07-01'
}
LT_THRESH = 0.5


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
    except:
        text = ''

    # get conversation context if available
    try:
        context = json.loads( params['context'] )
    except:
        context = None

    # detect language
    if text:
        res = translator.identify( text, headers=LT_HEADERS )
    else:
        res = None
    if res and res['languages'][0]['confidence'] > LT_THRESH:
        language = res['languages'][0]['language']
    else:
        language = BASE_LANGUAGE

    # translate to base language if needed
    if language != BASE_LANGUAGE:
        res = translator.translate(
            text,
            source=language,
            target=BASE_LANGUAGE,
            headers=LT_HEADERS
        )
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
    if language != BASE_LANGUAGE:
        res = translator.translate(
            message,
            source=BASE_LANGUAGE,
            target=language,
            headers=LT_HEADERS
        )
        message = res['translations'][0]['translation']
        output['text'][0] = message

    return {
        'message': message,
        'context': json.dumps( newContext ),
        'output': json.dumps( output ),
        'intents': json.dumps( intents ),
        'language': language
    }
