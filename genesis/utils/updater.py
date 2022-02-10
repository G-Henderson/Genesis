# Imports
import os
from random import randint
import subprocess
import utils.Platforms as Platforms

class Updater:
    """
    Class for checking for updates
    """

    def __init__(self):
        self.PLATFORM = "rpi"

    def update(self, voice_instance):
        # Check what platform we are on
        if (self.PLATFORM == Platforms.RASPBERRY_PI):
            # Check for Raspberry Pi OS updates
            self.check_for_os_updates()

        # Check for Genesis updates
        if (self.check_for_genesis_updates()):
            self.update_code(self.voice_instance)

    def check_for_os_updates():
        """
        Procedure for checking for Raspberry Pi OS updates

        """
        command = "sudo apt update -y && sudo apt upgrade -y && sudo apt dist-upgrade -y && sudo apt full-upgrade -y"
        os.system(command)

    def check_for_updates():
        """
        Checks for updates by fetching and pulling the latest code from the GIT repo

        Returns true if a restart is required
        """

        # Setup return variable (default is false)
        restart = False

        # Fetch the latest code from the repo and check the status of the repo
        command = "cd /home/pi/Genesis; git fetch; git status -uno" # Setup command
        ret = subprocess.run(command, capture_output=True, shell=True) # Run command
        output = ret.stdout.decode().split("\n") # Get the output of the command
        my_stat = output[1]
        #print(my_stat)

        # Check if there are any changes
        if ("up to date" in my_stat):
            # If not output "no updates"
            print("No updates currently available...")

        else:
            # If so pull the latest code
            print("Update available...")
            os.system("cd /home/pi/Genesis && git fetch && git pull")

            # Set restart to true
            restart = True

        # Check for Raspberry Pi OS updates
        check_for_os_updates()

        # Return whether restart is required
        return restart

    def update_code(voice_instance):
        """
        Restarts the device and notifies the user

        voice_instance: the instance of the TTS module for user feedback
        """
        
        # Setup different responses
        responses = [
            "There is an update available. I am rebooting.",
            "There is a new update available. I will quickly restart.",
            "New version of Genesis available. Restarting to apply the update."
        ]

        # Pick random response
        my_rand = randint(0,len(responses)-1) # Generate random index from the list of responses
        speech = responses[my_rand] # Get response at that index

        # Say response
        voice_instance.say(speech)

        # Restart the device
        os.system("sudo shutdown -r now")