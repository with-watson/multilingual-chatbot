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
from watson_developer_cloud import ConversationV1


def main(dict):
    return { 'message': 'Hello world!!!!' }
