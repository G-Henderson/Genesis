from utils.everest.EverestTT import Timetable
from utils.voice import Voice


class Module:

    """
    Module for adjusting the volume the device
    """

    def __init__(self, command: str, args: list, voice_instance: Voice, extras) -> None:
        # Initialise variables from the arguments
        self.command = command
        self.args = args
        self.voice = voice_instance
        self.extras = extras

        # Setup other variables
        self.table = Timetable()

    # Main procedure
    def run(self) -> None:
        week = "b"
        if (self.args[0] != "tomorrow"):
            lessons = self.table.todaysLessons(week)
            speech = self.table.formSpeech("Today", lessons)
            self.voice_instance.say(speech)

        else:
            lessons = self.table.tomorrowsLessons(week)
            speech = self.table.formSpeech("Tomorrow", lessons)
            self.voice_instance.say(speech)
