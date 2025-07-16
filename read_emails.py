import os
import json
from email import message_from_bytes
import base64
from typing import cast

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def auth():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else :
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds = flow.run_local_server(port = 0)
            
        with open('token.json','w') as token:
                token.write(creds.to_json())
        
    return build('gmail','v1', credentials=creds)

def fetch_latest_emails(service, max_results = 10):
    results = service.users().messages().list(userId = 'me', maxResults = max_results, q="in:inbox").execute()
    messages = results.get('messages',[])
    
    mail_texts = []
    
    for msg in messages:
        msg_data = service.users().messages().get(userId = 'me', id = msg['id'], format='raw').execute()
        raw_data = base64.urlsafe_b64decode(msg_data['raw'].encode("ASCII"))
        mail_msg = message_from_bytes(raw_data)
        
        subject = mail_msg.get('Subject', '')
        body = ''
        
        if mail_msg.is_multipart():
            for part in mail_msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = cast(bytes, part.get_payload(decode=True)).decode(errors='ignore')
                    break
        
        else :
            body = cast(bytes, mail_msg.get_payload(decode=True)).decode(errors='ignore')
            
        clean_text = subject + " " + body
        mail_texts.append(clean_text)
        
    return mail_texts
        
if __name__ == '__main__':
    service = auth()
    emails = fetch_latest_emails(service, max_results=10)
    
    for i, email in enumerate(emails,1):
        print(f"\n📧 Email #{i}:\n{'-'*40}\n{email[:500]}...\n")