from utils.EverestTT import Timetable

table = Timetable()

def run(extras, command, args, voice_instance):
    week = "b"
    if (args[0] != "tomorrow"):
        lessons = table.todaysLessons(week)
        speech = table.formSpeech("Today", lessons)
        voice_instance.say(speech)

    else:
        lessons = table.tomorrowsLessons(week)
        speech = table.formSpeech("Tomorrow", lessons)
        voice_instance.say(speech)
