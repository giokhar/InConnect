import json, requests, random, re
from urllib.request import urlopen
from pprint import pprint

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views import generic
# import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from messenger.serializers import *
from .models import User, Chat

VERIFY_TOKEN = '12345678'
PAGE_ACCESS_TOKEN = "EAAK5tc826v8BACZAudQd8vZByLNgod6W7f99ZCpZCGXAEXZAvIjvWBhAciO7eaxmTBwtpxKQJuqkU5b8ovlfSeyOGDkBDz8dGfQIhtCF15gytQ11wfZCUhuds2x4ceSFKYBeGyZCVPhTBnmwCWXIL3Br2c8zTzpcxgv1JGQ54x6Fofwx3C5wBMa"
DEFAULT_RESPONSE_FOR_WAIT = "Please wait. No chatroom associated with this topic yet. "
DEFAULT_RESPONSE_FOR_START = "You can start your conversation."
DEFAULT_RESPONSE_FOR_END = "Your conversation has ended."

def getData(request, type_of):
	url 		= "http://" + request.get_host() + "/api/" + type_of +"/?format=json"
	jsonurl 	= urlopen(url)
	data		= json.loads(jsonurl.read())
	return data

def getTopic(sender_id):	
	my_user = User.objects.get(sender_id = sender_id)
	return my_user.topic

def setChatUser(chat_id, sender_two_id):
	my_chat = Chat.objects.filter(id=chat_id)
	my_chat.update(sender_two = sender_two_id, status=True)

def createChat(sender_one_id):
	topic = getTopic(sender_one_id)
	new_chat = Chat(sender_one=sender_one_id, topic=topic)
	new_chat.save()

def isIn(request, sender_id):
	for user in getData(request, "users"):
		if user['sender_id'] == sender_id:
			return True
	return False

def addUser(request, sender_id, sender_response):

	if not isIn(request, sender_id):
		new_user = User(sender_id=sender_id, topic=sender_response)
		new_user.save()

def addUserChat(request, message):

	sender_id = message['sender']['id']
	userIsInChat = False

	for chat in getData(request, "chats"):
		if chat['sender_one'] == sender_id or chat['sender_two'] == sender_id:
				userIsInChat = True
		if chat['status'] == False and getTopic(sender_id) == chat['topic'] and chat['sender_one'] != sender_id:
			setChatUser(chat['id'], sender_id)
			return

	if not userIsInChat:
		createChat(sender_id)

def clearDB(request, sender_id):

	for chat in getData(request, "chats"):
		if chat['sender_one'] == sender_id or chat['sender_two'] == sender_id:
			
			sendMessage(chat['sender_one'],DEFAULT_RESPONSE_FOR_END)
			sendMessage(chat['sender_two'],DEFAULT_RESPONSE_FOR_END)

			User.objects.filter(sender_id=chat['sender_one']).delete()
			if chat['sender_two'] != None:
				User.objects.filter(sender_id=chat['sender_two']).delete()
				
			Chat.objects.filter(id=chat['id']).delete()



def generateMessage(request, message):
	another_user_id = getConnection(request, message['sender']['id'])
	if another_user_id == None:
		sendMessage(message['sender']['id'], DEFAULT_RESPONSE_FOR_WAIT)
	else:
		if getTopic(message['sender']['id']) == message['message']['text']:
			sendMessage(another_user_id, DEFAULT_RESPONSE_FOR_START)
			sendMessage(message['sender']['id'], DEFAULT_RESPONSE_FOR_START)
		else:
			sendMessage(another_user_id, message['message']['text'])

def getConnection(request, sender_id):

	for chat in getData(request, "chats"):
		if chat['sender_one'] == sender_id:
			return chat['sender_two']
		elif chat['sender_two'] == sender_id:
			return chat['sender_one']

	return None

def generateTemplate(type, fbid, received_message):

	if type == "menu":
		return json.dumps({"persistent_menu":[{"locale":"default","composer_input_disabled":true,"call_to_actions":[{"title":"My Account","type":"nested","call_to_actions":[{"title":"Pay Bill","type":"postback","payload":"PAYBILL_PAYLOAD"},{"title":"History","type":"postback","payload":"HISTORY_PAYLOAD"},{"title":"Contact Info","type":"postback","payload":"CONTACT_INFO_PAYLOAD"}]},{"type":"web_url","title":"Latest News","url":"http://www.messenger.com/","webview_height_ratio":"full"}]},{"locale":"zh_CN","composer_input_disabled":false,"call_to_actions":[{"title":"Pay Bill","type":"postback","payload":"PAYBILL_PAYLOAD"}]}]})
	elif type == "reply":
		return json.dumps({"recipient":{"id":fbid},"message":{"text":received_message,"quick_replies":[{"content_type":"text","title":"End Conversation","payload":"End Conversation"}]}})

# # This function should be outside the BotsView class
def sendMessage(fbid, received_message):
	# Remove all punctuations, lower case the text and split it based on space
	
	user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
	user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
	user_details = requests.get(user_details_url, user_details_params).json()

	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = generateTemplate("reply", fbid, received_message) #"message":{"text":received_message}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	# pprint(status.json())
