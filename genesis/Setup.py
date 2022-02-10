# Import external libraries
import os

# Setup final global variables

class Setup:

    """
    Class for initial setup of Genesis
    """

    def __init__(self):
        pass

    def run_setup(self):
        command = "sudo setup/install_raspberry_pi_requirements.sh"
        os.system(command)

    def install_pip(self):
        # Install python 3 requirements
        command = "sudo pip3 install -r setup/requirements.txt"
        os.system(command)

        # Install python 2 requirements
        command = "sudo pip install -r setup/requirements.txt"
        os.system(command)

    def setup(self):
        """
        run instance
        """

        try:
            self.install_pip()
            self.run_setup()

        except Exception as e:
            print(e)


# Create Genesis instance
if __name__ == "__main__":
    system = Setup()
    system.setup()