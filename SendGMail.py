#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def GetLabels():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

#try:
#    import argparse
#    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#except ImportError:
#    flags = None

def SendMessage(service, user_id, message): # Send an email message.
    try:
      message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
      print ('Message Id: %s' % message['id'])
      return message
    except errors.HttpError as error:
      print ('An error occurred: %s' % error)

def main( sender, recepient, subject, text_body ):
    store = oauth2client.file.Storage('credentials.json')
    credentials = store.get()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    testMessage = create_message( sender, recepient, subject, text_body )
    SendMessage( service, sender, testMessage )

if __name__ == '__main__':
    main( 'biotuba@gmail.com', 'biotuba@gmail.com', 'Test mail subject', 'Test mail body' )