from subprocess import call
from utils.recognition import myCommand


def shutdown(timers, voice_instance):
    speech = ""
    if (len(timers) > 1):
        speech = "Are you sure? You still have timers running!"
    else:
        speech = "Are you sure?"

    voice_instance.say(speech)
    confirmed = confirm()

    if (confirmed):
        voice_instance.say("Shutting down...")
        call("sudo shutdown -h now", shell=True)

    else:
        voice_instance.say("Shutdown cancelled...")

def restart(timers, voice_instance):
    speech = ""
    if (len(timers) > 1):
        speech = "Are you sure? You still have timers running!"
    else:
        speech = "Are you sure?"

    voice_instance.say(speech)
    confirmed = confirm()

    if (confirmed):
        voice_instance.say("Restarting...")
        call("sudo shutdown -r now", shell=True)

    else:
        voice_instance.say("Restart cancelled...")


def confirm():
    confirm = False
    speech = myCommand()

    positives = ["yes", "yeah", "extremely", "absolutely", "sure", "course"]
    for i in range(len(positives)):
        if (positives[i] in speech):
            confirm = True
    
    return confirm


def run(extras, cmd, args, voice_instance):
    if ("shut" in cmd):
        shutdown(extras, voice_instance)

    elif (cmd == "reboot") or (cmd == "restart"):
        restart(extras, voice_instance)