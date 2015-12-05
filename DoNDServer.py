import os  
import json  
import random  
import requests

from random import randint  
  
from flask import Flask  
from flask import request  
from flask import send_from_directory  

from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

from two1tools.two1tools.bittransfer import *
  
app = Flask(__name__)  
wallet = Wallet()  
payment = Payment(app, wallet)  
  
games = []
username = ''
# endpoint to look up files to buy  
@app.route('/play', methods=['GET'])  
def play(): 
	global games
	global username
	username = request.args.get('username')
	games = [{'id':'1', 'cases':[{'number':'1', "value":randint(0,1000)}, {'number':'2', "value":randint(0,1000)}, {'number':'3', "value":randint(0,1000)}, {'number':'4', "value":randint(0,1000)}, {'number':'5', "value":randint(0,1000)}, {'number':'6', "value":randint(0,1000)}, {'number':'7', "value":randint(0,1000)}, {'number':'8', "value":randint(0,1000)}, {'number':'9', "value":randint(0,1000)}, {'number':'10', "value":randint(0,1000)}]}]
	print(games[0])
	return json.dumps(games[0], default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route('/removeCase', methods=['GET'])  
def removeCase():
	selection = request.args.get('selection')
	cases = []
	cases[:] = [case for case in games[0]['cases'] if case.get('number') != selection]
	games[0]['cases'] = cases
	return json.dumps(games[0], default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route('/deal', methods=['GET'])  
def deal():
	prizes = []
	for case in range(len(games[0]['cases'])):
		prizes.append(games[0]['cases'][case]['value'])
	prize = sum(prizes) / len(prizes)
	print(prize)
	send_bittransfer(username,prize)
	return "Success"

@app.route('/finalCase', methods=['GET'])  
def finalCase():
	
	print(games[0]['cases'][0]["value"])
	prize = games[0]['cases'][0]["value"]
	send_bittransfer(username,prize)
	return "Success"

if __name__ == '__main__':  
    app.debug = True  
    app.run(host='0.0.0.0', port=3456) 