# Imports
from random import randint # To generate random response


# Forms the speech and tells the user the answer to the question
def reply(voice_instance, answer):
    # Create list of responses
    responses = ["The answer is", "", "It's", "It is"]

    # Check if the answer is a whole number
    if (answer.is_integer()):
        answer = int(answer)

    # Choose random response
    response_num = randint(0,len(responses)-1)
    response = responses[response_num]

    # Convert the answer to a string
    ans_str = str(answer)

    # Add the answer to the response
    response = response + " " + ans_str

    # Say response
    voice_instance.say(response)


# Does addition
def addition(args, voice_instance, extras):
    # Setup empty list to contain values to add
    nums = []

    # Iterate through the args looking for numbers
    for i in range(len(args)):
        # Put current value into container variable
        curr_value = args[i]
        # Check if the current value is a float
        is_float = False
        try:
            float_val = float(curr_value)
            is_float = True
        except ValueError:
            is_float = False

        # If it is a float then
        if (is_float):
            # Append it to the list
            nums.append(float_val)

    # Check there are values to add
    if (len(nums) > 1):
        # Add all of the number in the list
        total = 0
        for i in range(len(nums)):
            # Add to the total
            total += nums[i]

        # Tell the user the answer
        reply(voice_instance, total)

    # Error message
    else:
        voice_instance.say("I'm not sure...")

# Does subtraction
def subtraction(args, voice_instance, extras):
    # Setup empty list to contain values to add
    nums = []

    # Iterate through the args looking for numbers
    for i in range(len(args)):
        # Put current value into container variable
        curr_value = args[i]
        # Check if the current value is a float
        is_float = False
        try:
            float_val = float(curr_value)
            is_float = True
        except ValueError:
            is_float = False

        # If it is a float then
        if (is_float):
            # Append it to the list
            nums.append(float_val)

    # Check there are values to add
    if (len(nums) > 1):
        # Add all of the number in the list
        total = nums[i]
        for i in range(1,len(nums)):
            # Add to the total
            total += nums[i]

        # Tell the user the answer
        reply(voice_instance, total)

    # Error message
    else:
        voice_instance.say("I'm not sure...")

# Main subroutine called from the main program
def run(extras, command, args, voice_instance):
    if ((command == "+") or (command == "add") or (command == "plus")) and ("list" not in args):
        addition(args, voice_instance, extras)

    elif (command == "-") or (command == "take away") or (command == "minus"):
        subtraction(args, voice_instance, extras)
