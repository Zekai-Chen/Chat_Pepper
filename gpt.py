#!/usr/bin/env python2.7
from lwe import ApiBackend
import socket
#from livewhisper1 import StreamHandler
from naoqi import ALProxy
import naoqi
import argparse
import requests
import os
bot = ApiBackend()
#handler = StreamHandler()
import paramiko
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, default="192.168.1.71",
                   help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
parser.add_argument("--port", type=int, default=9559,
                   help="Naoqi port number")
args = parser.parse_args()
session = naoqi.Session()

try:
   session.connect("tcp://" + args.ip + ":" + str(args.port))
except RuntimeError:
   print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
           "Please check your script arguments. Run with -h option for help.")
   sys.exit(1)                 
def put_file(machinename, username, password, dirname, filename, data):
   ssh = paramiko.SSHClient()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect(machinename, username=username, password=password)
   sftp = ssh.open_sftp()
   try:
       sftp.mkdir(dirname)
   except IOError:
       pass
   f = sftp.open(dirname + '/' + filename, 'w')
   f.write(data)
   f.close()
   ssh.close()

#get the question in text 
def get_question():
   question = "Not received"
   try:
       UDP_IP = "127.0.0.1"
       UDP_PORT = 5005
       BUFFER_SIZE = 1024
       MESSAGE = "Hello"
       sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

       print("UDP server up and listening on {}:{}".format(UDP_IP, UDP_PORT))
       #question = handler.listen()
       #result = subprocess.check_output(['/home/lwq/anaconda3/bin/python', 'livewhisper1.py'])
       sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
       data, addr = sock.recvfrom(BUFFER_SIZE)
       question = data
       print("Received message:", question)
       #question = result.decode("utf-8")
   except (KeyboardInterrupt, SystemExit): pass
   finally:
       print("\n\033[93mLoading response...\033[0m")
       if os.path.exists('dictate.wav'): os.remove('dictate.wav')

   # import whisper
   # model = whisper.load_model("base")
   # result = model.transcribe("sound-question.mp3 or .wav")
   
   # with open("transcription.txt", "w") as file:
   #   question = file.write(result["text"])
   #return "What is the capital of france?"
   return question 
   
#send the question to chat gpt and get the answer
def ask_question(question):
   success, response, message = bot.ask(question)
   if success:
       print(response)
   else:
       print("No response")
       raise RuntimeError(message)
   return response

#send answer to pepeper
def output_response(response):
   print("\n\033[93mSending to Pepper..\033[0m")
   #try:
   tts = session.service("ALTextToSpeech")

   tts.setLanguage("English")
   print(type(response))
   
   response = response.encode('utf-8').decode('utf-8')
   tts.say(response)
   #except Exception as e:
       #print("Failed to send message to Pepper :" + str(e))
   #put_file("192.168.1.71", "nao", "nao", "/home/nao/", "stuff.txt", response)
   #with open("stuff.txt", "w") as file:
   #   file.write(response)
   print("\n\033[93mResponse Sent..\033[0m")




old_response = "hi"

try:
   while True:
       
       question = get_question() #always get question in text
       response = ask_question(question) #store chat gpts answer
       if response != old_response:
           old_response = response
           output_response(response) #send response
except (KeyboardInterrupt, SystemExit): pass
finally:
   print("\n\033[93mQuitting...\033[0m")
   if os.path.exists('dictate.wav'): os.remove('dictate.wav')
   output_response("Goodbye")


