import sys
import json
import os
import requests

#import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

# server address
def play(server_url = 'http://localhost:9393/'):
         
    # get the file listing from the server
    print("Welcome to DEAL or NO DEAL!");
    response = requests.get(url=server_url+'play?username=' + username)
    # print(json.loads(response.text)["cases"])
    case_list = json.loads(response.text)["cases"]
    prizes = []
    for case in range(len(case_list)):
        # prizes += case_list[case]['value']
        prizes.append(case_list[case]['value'])
    prizes.sort()
    print("Prizes Remaining:")
    print(prizes)
    print("Cases Remaining:")
    for case in range(len(case_list)):
        print("Case #{}".format(case_list[case]["number"]))
    try:
 #        # prompt the user to input the index number of the file to be purchased
        while len(case_list) > 1:
            print("Offer from the banker: " + str(sum(prizes) /len(prizes)))
            deal = input("Deal OR No Deal? ")
            if deal == "Deal":
                response = requests.get(url=server_url+'deal')
                print("Congrats, you win " + str(sum(prizes) / len(prizes)) + " satoshi.")
                return
            else:
                sel = input("Choose a case:")
         #        # check if the input index is valid key in file_list dict
                if int(sel) <= len(case_list):
                    print('You selected case #{}'.format(sel))
                else:
                    print("That is an invalid selection.")
         #        #create a 402 request with the server payout address
                sel_url = server_url+'removeCase?selection=' + str(sel)
                response = requests.get(url=sel_url)
                case_list = json.loads(response.text)["cases"]
                for case in range(len(case_list)):
                    print("Case #{}".format(case_list[case]["number"]))
                prizes = []
                for case in range(len(case_list)):
                    # prizes += case_list[case]['value']
                    prizes.append(case_list[case]['value'])
                prizes.sort()
                print("Prizes Remaining:")
                print(prizes)
        response = requests.get(url=server_url+'finalCase')
        print("Congrats, you win " + str(case_list[0]["value"]) + " satoshi.")
     #        if answer.status_code != 200:
     #        	print("Could not make an offchain payment. Please check that you have sufficient balance.")
     #        else:
     #            print('Congratulations, you just donated to charity!')


    except ValueError:
        print("That is an invalid input. Only numerical inputs are accepted.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    else:
        server_url = 'http://localhost:3456/'
    play(server_url)