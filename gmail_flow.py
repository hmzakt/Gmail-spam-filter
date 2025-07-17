import os
import json
import re
from email import message_from_bytes
import base64
from typing import cast

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

import joblib
    
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

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
    msg_ids=[]
    
    for msg in messages:
        msg_id = msg['id']
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
        msg_ids.append(msg_id)
        
    return mail_texts, msg_ids

def move_to_spam(service, msg_id):
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={
            'addLabelIds': ['SPAM'],
            'removeLabelIds': ['INBOX']
        }
    ).execute()

        
if __name__ == '__main__':
    service = auth()
    emails, msg_ids = fetch_latest_emails(service, max_results=10)

    def clean_email_text(text):
        text = text.lower()  
        text = re.sub(r'\n', ' ', text)  
        text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)  
        text = re.sub(r'\W', ' ', text)  
        text = re.sub(r'\s+', ' ', text).strip()  
        return text

    preprocessed_emails = [clean_email_text(email) for email in emails]

    model = joblib.load("spam_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    
    mails_X = vectorizer.transform(preprocessed_emails)
    predictions = model.predict(mails_X)
    
    for i, (label, msg_id) in enumerate(zip(predictions, msg_ids), 1):
        tag = "SPAM" if label else "NOT SPAM"
        print(f"\nEmail #{i} - {tag}")
        print("-" * 40)
        print(emails[i-1][:500] + "...\n")

        if label == 1:
            move_to_spam(service, msg_id)
