#!/usr/bin/python3.8
# -*- coding: UTF-8 -*-

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']

def GetService():
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

    return build('gmail', 'v1', credentials=creds)

# Call the Gmail API
def ShowLabels():
    results = GetService().users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

def create_message(sender, to, subject, message_text): # Create a message for an email.
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(bytes(str(message), "utf-8"))
    return {'raw': raw.decode()}

def SendMessage(service, user_id, message): # Send an email message.
    try:
      message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
      print ('Message Id: %s' % message['id'])
      return message
    except errors.HttpError as error:
      print ('An error occurred: %s' % error)

def main():
    service = GetService()
    testMessage = create_message( "biotuba@gmail.com", "poppyaxe@gmail.com", "Test Subject", "I Love You" )
    SendMessage( service, "biotuba@gmail.com", testMessage )

if __name__ == '__main__':
    main()
