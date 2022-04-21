# Imports for YouTube
#import pafy
#import urllib.request
#from youtube_search import YoutubeSearch

# Imports GDA
import requests
import json

from utils.voice import Voice


class Module:

    """
    Module for playing music
    """

    def __init__(self, command: str, args: list, voice_instance: Voice, extras) -> None:
        # Initialise variables from the arguments
        self.command = command
        self.args = args
        self.voice = voice_instance
        self.extras = extras

        # Parent url for GDS server
        self.SERVER_URL = "http://digitalstreaming.home/"


    # Search and play using YouTube
    """
    def playYoutube(args, voice_instance):
            voice_instance.say("Playing on YouTube...")

            search_query = " ".join(args)
            result = YoutubeSearch(search_query, max_results=10).to_dict()[0]

            video_title = result["title"]
            url_suffix = result["url_suffix"]
            print(result)

            url = "http://www.youtube.com/" + url_suffix
            print("Here 1")
            video = pafy.new(url)
            print("Here 1.5")
            best = video.getbest()
            print("Here 2")
            play_url = best.url
            print("Here 3")
            voice_instance.say(f"playing {video_title}")
            voice_instance.play_media(play_url)
    """


    # Search and play using the GDA website
    def playGDA(self):
        # Tell user we are getting ready
        self.voice_instance.say("Connecting to GDS server...")

        # Create search query from speech
        search_query = " ".join(self.args)

        # Check whether playing an album
        playing_album = False
        if ("album" in search_query):
            # Remove album from search query
            search_query = search_query.replace(" album", "")

            # Send request to web server with query and get response
            response = requests.get(self.SERVER_URL+"audio/voicesearch.php?q="+search_query+"&album=true")

            # Set playing_album to true
            playing_album = True

        else:
            # Send request to web server with query and get response
            response = requests.get(self.SERVER_URL+"audio/voicesearch.php?q="+search_query)

        # Get child url from response
        try:
            raw_data_str = str(response.content.decode("utf-8"))

            # Convert the string to json array
            song_array = json.loads(raw_data_str)

            # Check if playing album
            if not playing_album:
                # Get the title and url from the first item on the list
                curr_song = song_array[0]
                #song_title = curr_song["title"]
                #song_artist = curr_song["artist"]
                child_url = curr_song["path"]

                # Check there is a result from the query
                if (len(song_array) > 0):
                    # Form speech string using song title
                    #speech = "playing "+song_title+" by "+song_artist
                    speech = "playing song"
                    # Annouce the song
                    self.voice_instance.say(speech)
                    # Play the song at the url
                    self.voice_instance.play_media(self.SERVER_URL+child_url)

                # Else couldn't find that song
                else:
                    self.voice_instance.say("I couldn't find that song on GDS")

                    # Try playing with YouTube
                    #playYoutube(args, voice_instance)

            else:
                ### Add all songs to vlc playlist ###

                # Create empty list to store urls in
                urls = []

                # Get the url for each item on the list
                for x in range(len(song_array)):
                    curr_song = song_array[x]
                    child_url = curr_song["path"]
                    full_url = self.SERVER_URL + child_url
                    # Add the url to the list
                    urls.append(full_url)

                # Check there is a result from the query
                if (len(song_array) > 0):
                    # Announce album
                    self.voice_instance.say("Playing album...")

                    # Play the song at the url
                    self.voice_instance.startPlaylist(urls)

                # Else couldn't find that song
                else:
                    self.voice_instance.say("I couldn't find that album on GDS")


        except Exception as e:
            print(e)
            self.voice_instance.say("Error playing song")
            #playYoutube(args, voice_instance)

    # Main procedure
    def run(self):
        if self.command == "play":
            # Check whether to resume playing or play new song
            if (len(self.args) > 0):
                # Search and play from GDA
                self.playGDA(self.args, self.voice_instance)
                #playYoutube(args, voice_instance)

            else:
                self.voice_instance.resume()

        elif self.command == "stop":
            # Stop the music
            self.voice_instance.stop()

        elif self.command == "pause":
            # Pause the music
            self.voice_instance.pause()

        elif self.command == "resume":
            # Resume playing the music
            self.voice_instance.resume()
