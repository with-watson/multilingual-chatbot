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
from watson_developer_cloud import ConversationV1, LanguageTranslatorV3
import time

# consts
BASE_LANGUAGE = 'en'
LT_THRESH = 0.4
LT_PAIRS = {
    'ar': 'Arabic',
    'zh': 'Chinese (Simplified)',
    'zht': 'Chinese (Traditional)',
    'nl': 'Dutch',
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'pl': 'Polish',
    'pt': 'Portuguese (Brazil)',
    'ru': 'Russian',
    'es': 'Spanish',
    'tr': 'Turkish'
}


def main( params ):
    # get conversation workspace id
    try:
        workspace = params['conversation_workspace_id']
    except:
        return {
            'message': 'Please bind your conversation workspace ID as parameter',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
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
            'message': 'Please bind your conversation service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    # set up translator
    try:
        ltCreds = params['__bx_creds']['language_translator']
        translator = LanguageTranslatorV3(
            username=ltCreds['username'],
            password=ltCreds['password']
        )
    except:
        return {
            'message': 'Please bind your language translator service',
            'context': '{}',
            'output': '{}',
            'intents': '{}',
            'language': ''
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
        context = {}

    # detect language
    if text:
        res = translator.identify( text )
    else:
        res = None
    if res and res['languages'][0]['confidence'] > LT_THRESH:
        language = res['languages'][0]['language']
    elif res is None:
        language = BASE_LANGUAGE
    else:
        return {
            'message': 'Sorry, I am not able to detect the language you are speaking. Please try rephrasing.',
            'context': json.dumps( context ),
            'output': '{}',
            'intents': '{}',
            'language': ''
        }

    # validate support for language
    if language not in LT_PAIRS.keys():
        return {
            'message': 'Sorry, I do not know how to translate between {} and {} yet.'.format(
                BASE_LANGUAGE, language
            ),
            'context': json.dumps( context ),
            'output': '{}',
            'intents': '{}',
            'language': language
        }

    # translate to base language if needed
    if language != BASE_LANGUAGE:
        res = translator.translate(
            text,
            source=language,
            target=BASE_LANGUAGE
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
    output_text = [text for text in res['output']['text'] if text]
    message = output_text[0]
    output['text'] = output_text
    intents = res['intents']

    # translate back to original language if needed
    if language != BASE_LANGUAGE:
        res = translator.translate(
            output_text,
            source=BASE_LANGUAGE,
            target=language
        )
        output_text = [t['translation'] for t in res['translations']]
        message = output_text[0]
        output['text'] = output_text

    return {
        'message': message,
        'context': json.dumps( newContext ),
        'output': json.dumps( output ),
        'intents': json.dumps( intents ),
        'language': language
    }
