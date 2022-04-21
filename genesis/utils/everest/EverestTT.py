# A class to return lessons for specified time/date
import json
import datetime

class Timetable():
  def __init__(self):
    self.filename = "timetable.txt"
    self.WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]

  # Returns a list of the lessons today
  # The week parameter can either be 'a' or 'b' depending on which week the timetable is on.
  def todaysLessons(self, week):
    # Creates the empty lesson list
    new_string = []

    now = datetime.datetime.now()
    day = now.strftime("%A").lower()

    if (day in self.WEEKDAYS):
      # Reads timetable string from file
      file = open(self.filename, "r")
      # Puts each line into array
      my_array = file.readlines()
      # Converts the first item in the array to a json array
      json_obj = json.loads(my_array[0])
      # Gets the list of lessons from the day of that week
      new_string = json_obj[week][day]
      # Close the file
      file.close()

    # Returns the list
    return new_string

  # Returns a list of the lessons tomorrow
  # The week parameter can either be 'a' or 'b' depending on which week the timetable is on.
  def tomorrowsLessons(self, week):
    # Create empty string variable
    new_string = ""

    # Get today's date information using datetime library
    now = datetime.datetime.now()
    # Get today's name of the week
    today = now.strftime("%A").lower()
    
    # Check if it is a weekday
    if (today in self.WEEKDAYS):
      # Check which number day of the week it is
      index = self.WEEKDAYS.index(today)
      # Check if it is not Friday
      if (index < (len(self.WEEKDAYS)-1)):
        # Set tomorrow's day name
        day = self.WEEKDAYS[index+1]
      else:
        # Set the day name for tomorrow to 'weekend'
        day = "weekend"
    
    # Check if it is a Sunday
    elif (today == "sunday"):
      # Set tomorrow's date to Monday
      day = self.WEEKDAYS[0]

    # Check if it is saturday
    elif (today == "saturday"):
      # Set tomorrow's date to Sunday
      day = "sunday"

    # Check if tomorrow's date is a week day
    if (day in self.WEEKDAYS):
      # If so, open the timetable file in read mode
      file = open(self.filename, "r")
      # Read it into an array
      my_array = file.readlines()
      # Convert the first line into a JSON string
      json_obj = json.loads(my_array[0])
      # Get the list of subjects for the day from the json string
      new_string = json_obj[week][day]
      # Close the file
      file.close()

    # Return the list of lessons
    return new_string

  # Forms a string to display the lessons
  # The my_day parameter can either be 'today' or 'tomorrow'. The lessons paramter should be the list of lessons for that day.
  def formSpeech(self, my_day, lessons):
    # Create start of the string
    speech_string = my_day+" you have"
    # Check if there are lessons that day
    if (len(lessons) > 0):
      # Loop through all of the lessons
      for my_lesson in range(len(lessons)):
        # Check to see if possible to be double
        if (my_lesson < (len(lessons)-1)):
          # Check if it is a double lesson
          if (lessons[my_lesson+1] == lessons[my_lesson]):
            # If so add the double to the output string
            speech_string += " double " +lessons[my_lesson]

          # Check if it is possible to be second half of double
          elif (my_lesson > 0):
            # Check to see if it is the second half of a double
            if (lessons[my_lesson-1] != lessons[my_lesson]):
              # If not a double then add single lesson to output string
              speech_string += " "+lessons[my_lesson]

          else:
            # If not possible then add to output string
            speech_string += " "+lessons[my_lesson]

        # Check to see if it is the second half of a double
        elif (my_lesson > 0):
          # Check to see if it is the second half of a double
          if (lessons[my_lesson-1] != lessons[my_lesson]):
            # If not a double then add single lesson to output string
            speech_string += " "+lessons[my_lesson]

    else:
      # If there aren't any lessons then notify the user
      print("You have no lessons today!")

    return speech_string
