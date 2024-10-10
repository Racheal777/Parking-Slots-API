import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, Depends, HTTPException,status

load_dotenv()





def send_messages(phone_number, message):
   try:
       url = f'https://smsc.hubtel.com/v1/messages/send?clientid={os.getenv("CLIENT_ID")}&clientsecret={os.getenv('CLIENT_SECRET')}&from={os.getenv('FROM')}&to={phone_number}&content={message}'

       response = requests.get(url)
       return response
   except Exception as err:
       raise HTTPException(status_code=500, detail=str(err))

