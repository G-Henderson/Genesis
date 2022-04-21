from utils.configuration import Configuration

def get_module_settings(config: Configuration, module_name: str) -> dict:
    """
    Get settings for a specified module

    module_name: the name of the module
    """

    module_settings = None
    modules = config.load_configuration()["modules"]

    for mod in modules:
        if module_name == mod["name"]:
            module_settings = mod["settings"]
            break

    return module_settings