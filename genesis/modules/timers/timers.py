import json
from time import sleep
import time

from utils.recognition import myCommand


# Adds the JSON object of a timer to the global timers JSON Array
def createTimer(amount, timer_label):
        try:
                new_data = {"label": timer_label, "duration": amount, "start": time.time()}
                return new_data

        except:
                return None

# Works out how long to set the timer for using values and units
def setTimer(data, voice_instance, extras):
    error = False
    new_res = None
    amountTime = 0
    if (len(data) > 1):
        if (('minute' in data[-1]) and (data[-2].isdigit())):
            amountTime = int(data[-2]) * 60
            units = "minutes"

        elif (('second' in data[-1]) and (data[-2].isdigit())):
            amountTime = int(data[-2])
            units = "seconds"

        elif (('hour' in data[-1]) and (data[-2].isdigit())):
            amountTime == (int(data[-2]) * 60) * 60
            units = "hours"

        elif ("-" in data[-1]):
            error = True
            temp_str = data[-1]
            temp = temp_str.split("-")
            new_res = temp

        else:
            error = True
            voice_instance.say('Sorry, how long?')
            new_res = myCommand().split()


    elif (len(data) > 0):
        if ("-" in data[-1]):
            error = True
            temp_str = data[-1]
            temp = temp_str.split("-")
            new_res = temp

        else:
            error = True
            voice_instance.say('Alright, how long for?')
            new_res = myCommand().split()
            print(error)

    else:
        error = True
        voice_instance.say('Alright, how long for?')
        new_res = myCommand().split()
        print(error)

    if (error == False):
        try:
            voice_instance.say("What is the timer for?")
            my_label = myCommand()

            speech_string = 'Alright, '+data[-2]+' '+units+' starting now!'
            voice_instance.say(speech_string)

            return createTimer(amountTime, my_label)

        except Exception as e:
            print(f" "+str(e))
            return None

    else:
        return setTimer(new_res, voice_instance, extras)


# Cancels a timer
def cancelTimer(timers, voice_instance):
    try:
        if (len(timers) == 0):
            voice_instance.say('There aren\'t any timers running!')

        elif (len(timers) == 1):
            timers.pop(0)
            voice_instance.say('I\'ve cancelled the timer')

        else:
            voice_instance.say('You have multiple timers running. Which timer should I cancel?')
            new_label = myCommand()
            found_timer = False
            for i in range(len(timers)):
                if (timers[i]['label'] in str(new_label)):
                    timers.pop(i)
                    found_timer = True
                elif (timers[i]['label'] in str(new_label)):
                    timers.pop(i)
                    found_timer = True

            if (found_timer):
                voice_instance.say('I\'ve cancelled the timer')
            else:
                voice_instance.say('I wasn\'t able to find your timer')

    except Exception as e:
        print(e)
        voice_instance.say('Problem cancelling timer!')

    return timers


# Works out the remaining time on the timer
def timeLeft(my_label, voice_instance, timers):
    try:
        if (len(timers) != 0):
            found_timer = False
            for i in range(len(timers)):
                now = time.time()
                my_duration = float(timers[i]["duration"])
                my_start = int(timers[i]["start"])
                if (timers[i]['label'] == str(my_label)):
                    new_num = now - my_start
                    time_left = round(my_duration - new_num)
                    found_timer = True
                    
            if (found_timer == True):
                return time_left

            else:
                voice_instance.say('I can\'t find that timer!')

        else:
            voice_instance.say('There aren\'t any timers running!')

    except:
        voice_instance.say('Problem checking time left!')


# User interaction part of working out time left on the timer 
def checkForTimers(timers, voice_instance):
    try:
        if (len(timers) == 0):
            voice_instance.say("There aren't any timers running!")

        else:
            my_timer_name = ""
            if (len(timers) > 1):
                voice_instance.say("Which timer would you like me to check?")
                my_timer_name = myCommand()

            else:
                my_timer_name = timers[0]['label']

            
            time_left = int(timeLeft(my_timer_name, voice_instance, timers))
            reported_value = int(round(time_left / 60, 0))
            speech = ""
            if (time_left <= 60):
                speech = 'There is '+str(time_left)+' seconds left on your timer'

            elif (reported_value == 1):
                speech = 'There is about a minute left on your timer'

            else:
                speech = 'There is about '+str(reported_value)+' minutes left on your timer'

            voice_instance.say(speech)

    except:
        pass


# Main function called by the main Genesis instance
def run(extras, command, args, voice_instance):
    if (command == "set a timer"):
        timer = setTimer(args, voice_instance, extras)
        timers = extras.append(timer)
        return timers
    elif (command == "how much time"):
        checkForTimers(extras, voice_instance)
        return None
    elif (command == "cancel"):
        timers = cancelTimer(extras, voice_instance)
        return timers
