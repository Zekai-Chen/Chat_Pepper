import requests

import json


class ApiBackend:

   def __init__(self):

       self.api_key = "sk-YsLQkQkg5zqrD4M85d8a4aE98c7d43C9B06c38D339E114Ea"

       self.headers = {

           "Authorization": "Bearer %s" % self.api_key,

           "Content-Type": "application/json"

       }

       self.url = "https://pro.aiskt.com/v1/chat/completions"


   def ask(self, question):

       data = {

           "model": "gpt-4-0613",

           "messages": [{"role": "user", "content": question}]

       }

       try:

           response = requests.post(self.url, headers=self.headers, json=data)

           if response.status_code == 200:

               response_data = response.json()

               return True, response_data['choices'][0]['message']['content'], None

           else:

               return False, None, "API returned %d: %s" % (response.status_code,response.text)

       except Exception as e:

           return False, None, str(e)


