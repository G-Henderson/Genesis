# Import external libraries
from utils.configuration import Configuration
from utils.voice import Voice
from utils.LEDArray import LEDArray
#from utils.updater import updater

class Genesis:

    """
    Class for main Genesis instance
    """

    def __init__(self):
        # Setup final global variables
        self.CONFIG_PATH = "config.json"
        self.CONFIG_HEADER_PATH = "config_header.json"
        self.MODS_DIR = "modules"

        # Setup Genesis
        self.genesis_config = self.setup()

        self.my_config = self.genesis_config.load_configuration()
        self.settings = self.my_config["settings"]
        self.position = self.settings["position"]
        self.platform = self.settings["platform"]

        # Create the LED instance
        self.led_array = LEDArray()

        # Create the voice instance
        self.voice = Voice(self.genesis_config, self.led_array)
        
        
    def parse_args(self, command: str, keyword: str) -> list:
        """
        Parse command arguments
        
        command: the command to parse
        keyword: the keyword that activate the command
        
        example: play song_name
        using keyword: play
        returns: [song_name]
        another example: play song_name by artist
        using keyword: play
        returns: [song_name, by, artist]
        """
        
        command_without_keywords = command.replace(keyword, "").strip()
        return command_without_keywords.split()
    
    
    # Executes the command based on the command word in the detected speech
    def execute_command(self, command: str):
        """
        execute user command

        command: the command to execute
        """

        print(f"Executing {command}")
        command_executed = False
        modules = self.my_config["modules"]

        # match command to addon
        for my_mod in modules:
            for command_to_listen_for in my_mod["commands"]:
                if command_to_listen_for in command:

                    name = my_mod['name']
                    my_addon_imported = __import__(
                        f"{self.MODS_DIR}.{name}.{my_mod['entry-point']}",
                        fromlist=[f"modules.{name}"],
                    )

                    # any possible errors should be handeled by developers
                    # within their addons, if an error is encountered, they
                    # will be ignored as to not halt/break the main instance
                    try:
                        # Parse extras to the addon (if required)
                        if str(name) == "homecontrol":
                            extra = self.homeHub
                        elif str(name) == "lists":
                            extra = self.homeHub
                        elif str(name) == "timers":
                            extra = self.timers
                        elif str(name) == "general":
                            extra = self.alarms
                        elif str(name) == "system":
                            extra = self.timers
                        else:
                            extra = "None"

                        my_return = my_addon_imported.run(
                            extra,
                            command_to_listen_for,
                            self.parse_args(command, command_to_listen_for),
                            self.voice_instance,
                        )

                        # Get the return of the addon (if necessary)
                        if str(name) == "homecontrol":
                            pass

                        elif str(name) == "timers":
                            if (my_return != None):
                                self.timers = my_return

                        elif str(name) == "general":
                            if (my_return != None):
                                self.alarms = my_return

                    except Exception as e:
                        print(e)

                    command_executed = True

        if not command_executed:
            self.voice_instance.say("Sorry, I didn't understand that")

        # Set wake-word file back to 0
        #f = open("wake-word.txt", "w")
        #f.write("0")
        #f.close()


    # Runs on startup to load settings and modules
    def setup(self) -> Configuration:
        """
        setting up Genesis
        """

        # Create configuration object
        config = Configuration()

        # Create the configuration file
        config.create_config()

        # Check the configuration file
        config.check_global_config(self.CONFIG_HEADER_PATH)

        # load modules
        config.load_modules(self.CONFIG_PATH, self.MODS_DIR)

        # Return the configuration object
        return config


    def run(self):
        """
        run instance
        """

        try:
            self.voice.say("Hello")

        except Exception as e:
            print(e)


# Create Genesis instance
if __name__ == "__main__":
    genesis = Genesis()
    genesis.run()
