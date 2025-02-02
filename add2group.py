#!/bin/env python3
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserNotMutualContactError, FloodWaitError, UserIdInvalidError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os, sys
import csv
import traceback
import time
import random
import pickle
import csv


re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
	print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

			version : 1.0
		""")

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
	api_id = cpass['cred']['id']
	api_hash = cpass['cred']['hash']
	phone = cpass['cred']['phone']
	client = TelegramClient(phone, api_id, api_hash)
except KeyError:
	os.system('clear')
	banner()
	print(re+"[!] run python3 setup.py first !!\n")
	sys.exit(1)

client.connect()
if not client.is_user_authorized():
	client.send_code_request(phone)
	os.system('clear')
	banner()
	client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
 
input_file = 'members_coc.csv'
users = []
with open(input_file, encoding='UTF-8') as f:
	rows = csv.reader(f,delimiter=",",lineterminator="\n")
	next(rows, None)
	for row in rows:
		user = {}
		user['username'] = row[0]
		user['id'] = int(row[1])
		user['access_hash'] = int(row[2])
		user['name'] = row[3]
		users.append(user)
 
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
			 offset_date=last_date,
			 offset_id=0,
			 offset_peer=InputPeerEmpty(),
			 limit=chunk_size,
			 hash = 0
		 ))
chats.extend(result.chats)
 
for chat in chats:
	try:
		if chat.megagroup== True and chat.title=='Coc market place':
			groups.append(chat)
	except:
		continue
target_group_entity = InputPeerChannel(groups[0].id,groups[0].access_hash)
 
mode = 2
n = 0


# user_to_add = InputPeerUser(users[0]['id'], user[0]['access_hash'])
# user_to_add = InputPeerUser(1968817380, -5006610720952129287)
# user_to_add = client.get_input_entity(users[0]['username'])
# ret = client(InviteToChannelRequest(target_group_entity,[user_to_add]))


invite_sent_list = []
invite_sent_list_saved = []
with open('invite_sent_list.csv', newline='\n') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		invite_sent_list_saved.append(row[0])

# with open("invite_sent_list.pkl", "rb") as file:
# 	invite_sent_list_saved = pickle.load(file)
invite_sent_list.extend(invite_sent_list_saved)
print(gr+"Loaded {} bans".format(len(invite_sent_list)))

for user in users:
	n += 1
	result = None
	time.sleep(2)
	try:
		print(gr+"Trying to add id {} and hash {} to group {}".format(user['id'], user['access_hash'], target_group_entity))
		if str(user['id']) not in invite_sent_list:
			if user['id'] == "":
				continue
			user_to_add = InputPeerUser(user['id'], user['access_hash'])
			result = client(InviteToChannelRequest(target_group_entity,[user_to_add]))
			print(gr+"Request sent to telegram")
			time.sleep(random.randrange(5, 10))
		if result is not None and str(user['id']) not in invite_sent_list:
			invite_sent_list.append(user_to_add)
			print(gr+"Success added and saving to pickle {} into pickle".format(user['id']))
			with open('invite_sent_list.csv','a') as fd:
				fd.write(str(user['id'])+"\n")
			time.sleep(random.randrange(5, 10))
		else:
			print(gr+"Not appending, already in file")
	except PeerFloodError as e:
		print(e)
		sys.exit(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
	except FloodWaitError as e:
		print(e)
		sys.exit(re+"[!] Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after some time.")
	except UserIdInvalidError as e:
		print(e)
		with open('invite_sent_list.csv','a') as fd:
			fd.write(str(user['id'])+"\n")
		print(gr+"UserIdInvalidError {} into pickle".format(user['id']))
	except UserPrivacyRestrictedError:
		print(re+"You don't have permission to add {} and hash {} to group {}".format(user['id'], user['access_hash'], target_group_entity))
		invite_sent_list.append(user_to_add)
		with open('invite_sent_list.csv','a') as fd:
			fd.write(str(user['id'])+"\n")
		print(gr+"Saved {} into pickle".format(user['id']))
	except UserNotMutualContactError:
		print(re+"You don't have permission to add {} and hash {} to group {}".format(user['id'], user['access_hash'], target_group_entity))
		invite_sent_list.append(user_to_add)
		with open('invite_sent_list.csv','a') as fd:
			fd.write(str(user['id'])+"\n")
		print(gr+"Saved {} into pickle".format(user['id']))
	except:
		traceback.print_exc()
		print(re+"[!] Unexpected Error")
		continue
