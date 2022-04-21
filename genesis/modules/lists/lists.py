import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from utils.setup import load_config
from utils.settings import get_addon_settings
from utils.ListUtils import ListItem
from utils.ListUtils import MyList

import json
from time import sleep
from random import randint


USER_SETTINGS = get_addon_settings("lists")
HOST_NAME = USER_SETTINGS["hostname"]


# Creates a new list
def createList():
    pass


# Called during user interactions
def run(mqttObj, command, args, voice_instance):
    # Get the lists
    f = open("addons/lists/list-backup.txt", "r")
    file_contents = f.read()
    f.close()
    lists = json.loads(file_contents)
    print(lists)

    # Action to do
    cmd = args[0]

    if (cmd == "add"):
        # Get item to add
        my_item = ""
        i = 1
        while args[i] != 'to':
            if (i > 1):
                    my_item += " "

            my_item += args[i]
            i+=1
        
        # Get name of list
        my_name = ""
        for x in range(i+1, len(args)):
            if (x > 1):
                my_name += " "

            my_name += args[x]

        # Get list
        myList = MyList()
        found_list = False
        y = 0
        while (found_list != True) and (y < len(lists)):
            mlist = lists[y]
            list_name = mlist["name"].lower()
            if (list_name == my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (my_name in list_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name+" list"):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            y += 1

        if (found_list):
            myList.addItem(my_item, voice_instance, lists, y-1)
        else:
            responses = [
                "I couldn't find a list called"+my_name+". Would you like me to make one?",
                "I couldn't find a list called"+my_name+". Would you like me to create one?",
                "I couldn't find a list called"+my_name+". Should I make one?",
                "I couldn't find a list called"+my_name+". Should I create one?"
            ]

            my_index = randint(0,len(responses)-1)
            speech = responses[my_index]

            voice_instance.say(speech)


    elif (cmd == "remove") or (cmd == "delete"):
        # Get item to remove/delete
        my_item = ""
        i = 1
        while args[i] != 'from':
                if (i > 1):
                        my_item += " "

                my_item += args[i]
                i+=1

        # Get name of list
        my_name = ""
        for x in range(i+1, len(args)):
            if (x > 1):
                my_name += " "

            my_name += args[x]

        # Get list
        myList = MyList()
        found_list = False
        y = 0
        while (found_list != True) and (y < len(lists)):
            mlist = lists[y]
            list_name = mlist["name"].lower()
            if (list_name == my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (my_name in list_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name+" list"):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            y += 1

        if (found_list):
            myList.removeItem(my_item, voice_instance, lists, y-1)
        else:
            speech = "I couldn't find a list called"+my_name+"."
            voice_instance.say(speech)


    elif (cmd == "clear"):
        # Get name of list
        my_name = ""
        i=1
        for x in range(i, len(args)):
            if (x > 1):
                my_name += " "

            my_name += args[x]

        # Get list
        myList = MyList()
        found_list = False
        y = 0
        while (found_list != True) and (y < len(lists)):
            mlist = lists[y]
            list_name = mlist["name"].lower()
            if (list_name == my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (my_name in list_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name+" list"):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            y += 1

        if (found_list):
            myList.clearShopping(voice_instance, lists, y-1)
        else:
            speech = "I couldn't find a list called"+my_name+"."
            voice_instance.say(speech)


    elif (cmd == "read"):
        # Get name of list
        my_name = ""
        i=1
        for x in range(i, len(args)):
            if (x > 1):
                my_name += " "

            my_name += args[x]

        # Get list
        myList = MyList()
        found_list = False
        y = 0
        while (found_list != True) and (y < len(lists)):
            mlist = lists[y]
            list_name = mlist["name"].lower()
            if (list_name == my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (my_name in list_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name+" list"):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            y += 1

        if (found_list):
            myList.readMyList(voice_instance)
        else:
            speech = "I couldn't find a list called"+my_name+"."
            voice_instance.say(speech)


    elif (cmd == "is") or (cmd == "are"):
        # Get item to check
        my_item = ""
        i = 1
        while args[i] != 'on':
            if (i > 1):
                    my_item += " "

            my_item += args[i]
            i+=1
        
        # Get name of list
        my_name = ""
        for x in range(i+1, len(args)):
            if (x > 1):
                my_name += " "

            my_name += args[x]

        # Get list
        myList = MyList()
        found_list = False
        y = 0
        while (found_list != True) and (y < len(lists)):
            mlist = lists[y]
            list_name = mlist["name"].lower()
            if (list_name == my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (my_name in list_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            elif (list_name in my_name+" list"):
                found_list = True
                myList.setName(mlist["name"])
                myList.setMyList(mlist["list"])

            y += 1

        if (found_list):
            myList.checkList(my_item, voice_instance, lists, y-1)
        else:
            speech = "I couldn't find a list called"+my_name+"."
            voice_instance.say(speech)


    else:
        voice_instance.say("I am not sure I understand.")