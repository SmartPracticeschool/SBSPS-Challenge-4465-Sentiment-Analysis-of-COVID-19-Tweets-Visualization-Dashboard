from flask import Flask,render_template,url_for,request,redirect, make_response
import random
import json
from time import time
from random import random
from flask import Flask, render_template, make_response
app = Flask(__name__)
from textblob import TextBlob
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
from tweepy.streaming import StreamListener
import threading

ACCESS_TOKEN = '2261270106-vrPqTCE3iFNi6rGwUUQAhFYMLH1xXbxrgTWuumw'
ACCESS_TOKEN_SECRET = 'd0fVkCHnChJFaYnt0eyuuCblpjACdBxemVsIi6vuwo7tf'
CONSUMER_KEY ='skrrhvZmeKNuZvI0Z1sGgWQMJ'
CONSUMER_SECRET = 'RkFVEBn66lianCo1XgmxJohHQXbtkgrrPQ9KejqrU5MnVLs8b5'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth, wait_on_rate_limit=True,
          wait_on_rate_limit_notify=True)
lst=[]
total=[0,0,0,0] 
text=[]               
class Listener(StreamListener):
	def __init__(self, output_file="ats.txt"):
		super(Listener,self).__init__()
		self.output_file = output_file
    #@app.route('/data', methods=["GET", "POST"])    
	def on_status(self,status):
  	  	#print(status.text)
		if not hasattr(status, "retweeted_status"):
			analysis = TextBlob(status.text)
    		#print(analysis.sentiment[0])
			if analysis.sentiment[0]>0:
				lst.append(analysis.sentiment[0])
				lst.append(0)
				lst.append(0)
          		
			elif analysis.sentiment[0]<0:
				lst.append(0)
				lst.append(analysis.sentiment[0])
				lst.append(0)
			else:
				lst.append(0)
				lst.append(0)
				lst.append(0)  	  	
  	  	#return data()
			text.append(status.text)
	def on_error(self, status_code):
        #print(status_code)
		return False 

		
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')


@app.route('/data', methods=["GET", "POST"])
def data():
    # Data Format
    # [TIME, Temperature, Humidity]
    cnt=0	    
    t1 = threading.Thread(target=tr)
    t1.start()
    Temperature = random() * 1
    Humidity = random() * 1
    if len(lst)>3:
        print(lst[cnt],lst[cnt+1],lst[cnt+2])
        total[2]+=1
        if lst[0]>0:
            total[0]+=1
        if lst[1]<0:
            total[1]+=1	
        if lst[0] == 0 and lst[1] == 0 and lst[2] == 0:
            total[3]+=1
        data = [time() * 1000, lst[cnt],lst[cnt+1],total[0],total[1],total[3],total[2],text[0]]
        lst.pop(0)
        lst.pop(0)
        lst.pop(0)
    else:
        data=[time()*1000,0,0,total[0],total[1],total[3],total[2],"NULL"]
    if len(text)>0:
        text.pop(0)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

def tr():
	output = open('at.txt', 'w')
	listener = Listener(output_file=output)
	tra=["#Unlock1.0","#Lockdown2.0","#Lockdown3.0", "#coronaupdatesindia","#coronavirusindia","#indiafightscorona"]
	stream = Stream(auth=api.auth, listener=listener,tweet_mode='extended')
	stream.filter(languages=['en'],track=tra,locations = [66.17,8.27,90.37,32.92],is_async=True)         
 
if __name__ == "__main__":
    app.run(debug=True)
    

