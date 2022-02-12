import json
import os
import subprocess
import sys

CONFIG_FILE_PATH = "config.json"

class Configuration:

    """
    Class for setting up the configuration of the assistant
    """

    def __init__(self):
        """
        run on initialisation of the object
        """
        self.config_file_name = CONFIG_FILE_PATH
        self.config_header_name = "config_header.json"


    def setConfig_file_name(self, config_file_name: str):
        """
        set the config file path
        """
        self.config_file_name = config_file_name


    def getConfig_file_name(self) -> str:
        """
        return the config file path
        """
        return self.config_file_name


    def create_config(self):
        """
        create config file if it does not exist
        """

        # Create name of main config file
        header_file = self.config_header_name
        config_file = self.config_file_name
        # Setup the default values for the config file
        default_config = {
            "settings": {
            "name": "Genesis",
            "language": "en",
            "location": "kitchen",
            "platform": "rpi",
            "voice": "pico"
            },
            "modules": [
            ],
        }

        # Check whether the header file already exists
        if not os.path.exists(header_file):
            # If not then create the new file
            with open(header_file, "w") as header:
                # Write the default config to it
                json.dump(default_config, header)

        # Read the header config
        header_contents = self.load_configuration(header_file)

        # Write header config to main config file
        with open(config_file, "w") as config:
            # Write the default config to it
            json.dump(header_contents, config)


    def load_configuration(self, config_file_name=CONFIG_FILE_PATH) -> dict:
        """
        load json
        config_file_path: the file path of the config file
        """

        # Create empty variable to hold the contents of the config file
        config_dict = None

        # Open the config file specified in the parameters
        with open(config_file_name) as config:
            # Dump the contents of the file into a json variable
            config_dict = json.load(config)

        # Return the contents as a dict
        return config_dict


    def check_global_config(self, config_path: str):
        """
        checks the main json config for some
        required settings

        config_path: the file path of the config file
        """

        # Load the config from the configuration file
        config = self.load_configuration(config_path)
        # Create a list of settings required from the config file
        required_settings = ["name", "language", "location", "platform", "voice"]

        # Iterate through all the settings in the required list
        for setting in required_settings:
            # Check that the setting is present in the config file
            if setting not in config["settings"]:
                # If not, output an error message
                print(f"The setting '{setting}' is required and missing from config file!")
                # Kill the program
                exit()


    def check_module_config(self, config: dict):
        """
        checks the modules json config for some
        required settings

        config: the module config
        """

        # Get the module's name
        module_name = config["name"]
        # Create a list of valid keys
        valid_keys = [
            "name",
            "commands",
            "entry-point",
            "languages",
            "required_packages",
            "settings",
            "version",
        ]

        # Iterate through keys in the module's config
        for key in config:
            # Check if the current key is valid
            if key not in valid_keys:
                # Output error message
                print(f"Invalid key '{key}' in {module_name}'s config")
                # Kill the program
                exit()


    def get_module_configs(self, modules_dir: str) -> list:
        """
        get all the module configs

        modules_dir: the directory where modules are stored
        """

        return [
            self.load_configuration(os.path.join(subdir, file))
            for subdir, dirs, files in os.walk(modules_dir)
            for file in files
            if file == self.config_file_name
        ]


    def append_to_config(self, config_file_path: str, config_append: dict, key_name: str):
        """
        append data to config file

        config_file_path: the path for the config file
        config_append: the setting to append to a config file
        key_name: the name of the config setting
        """

        config = self.load_configuration(config_file_path)
        config[key_name] = config_append

        with open(config_file_path, "w") as config_file:
            json.dump(config, config_file, indent=2)


    def load_modules(self, config_file_path: str, modules_dir: str):
        """
        load modules to main config and load config header

        config_file_path: the main config file to load the modules to
        modules_dir: the directory where modules are store
        """

        module_configs = self.get_module_configs(modules_dir)

        config = self.load_configuration(config_file_path)

        for installed_module in config["modules"]:
            try:
                for setting_key, setting_value in installed_module["settings"].items():
                    for module_index in range(len(module_configs)):
                        if (module_configs[module_index]["name"] == installed_module["name"]):
                            module_configs[module_index]["settings"][setting_key] = setting_value
            except Exception as e:
                print("Setup Error:", str(e))

        self.append_to_config(config_file_path, module_configs, "modules")