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
    
    
    def execute_command(self, command: str):
        """
        Execute the user's command
        command: the command to execute
        """

        print(f"Executing {command}")
        command_executed = False
        mods = self.config["modules"]

        # Search through mods for command
        for mod in mods:
            for command_to_listen_for in mod["commands"]:
                if command_to_listen_for in command:

                    my_mod = __import__(
                        f"{self.MODS_DIR}.{mod['name']}.{mod['entry-point']}",
                        fromlist=["modules"],
                    )

                    # Any possible errors should be handled by the individual modules
                    # within the modules, if an error is encountered, they
                    # will be ignored as to not halt/break the main instance
                    try:
                        my_mod.run(
                            command_to_listen_for,
                            self.parse_args(command, command_to_listen_for),
                            self.voice,
                        )
                    except:
                        pass

                    command_executed = True

        if not command_executed:
            self.voice.say("Sorry, I didn't understand that")


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
