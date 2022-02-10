# Import external libraries
from distutils.command.config import config
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


    # Runs on startup to load settings and modules
    def setup(self) -> Configuration:
        """
        setting up Genesis
        """

        # Create configuration object
        config = Configuration()

        # create config file
        config.create_config()

        # check config global file
        config.check_global_config(self.CONFIG_HEADER_PATH)

        # load addons
        config.load_modules(self.CONFIG_PATH, self.MODS_DIR)

        # Return the configuration object
        return config


    def run(self):
        """
        run instance
        """

        try:
            while True:
                print("Main Loop!")

        except Exception as e:
            print(e)


# Create Genesis instance
if __name__ == "__main__":
    genesis = Genesis()
    genesis.run()