# @author Charles Fee
#1/28/2019
import speech_recognition as sr
import os
import sys
import time
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import math
import spotipy
import json
from spotipy import util as util
from json.decoder import JSONDecodeError
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
username = 'PUT YOUR SPOTIFY USERNAME AS A STRING HERE'
#FOR CLIENT ID CLIENT SECRET AND REDIRECT URI GO TO YOUR SPOTIFY DEVELOPER'S DASHBOARD AND PASTE THEM IN AS STRINGS!!!!!!!!!!!
#YOU WILL NEED TO MAKE THE REDIRECT URI IN EDIT SETTINGS I made mine https://google.com/
#TO CHANGE VOLUME FOR Mac you use os.system("sudo osascript -e \"set Volume 10\"") ranges from 0-10 and replace the volUp volDown... accordingly
#TO CHANGE VOLUME FOR Linux use os.system("amixer sset \'Master\' 50%") 0% - 100% and replace the volUp volDown... accordingly
try:
    token = util.prompt_for_user_token(username, scope,client_id='', client_secret='', redirect_uri='')
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-"+username)
    token = util.prompt_for_user_token(username, scope,client_id='', client_secret='', redirect_uri='')
if token:
    spotifyObject = spotipy.Spotify(auth=token)
    devices = spotifyObject.devices()
    deviceID = devices['devices'][0]['id']
    def talkToMe(audio):
        "speaks audio passed as argument"
        os.system("PowerShell -Command \"Add-Type –AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'"+audio+"\');\"")
        #For Macs use os.system("say " + audio)
        #For Linux I think it's the same as Mac
        
    #listen for commands

    def myCommand():
        spotVol = 100
        spotifyObject.volume(spotVol)
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration = 1)
            audio = r.listen(source,None,3)

        try:
            command = r.recognize_google(audio).lower()
            print(command)
            if 'not google' in command:
                print('How may I help you')
                talkToMe('how may I help you')
                spotifyObject.volume(math.floor(.3*spotVol))
                return assistant(r)
            
        #loop back to continue to listen for commands
        except sr.UnknownValueError:
            myCommand()


    #if statements for executing commands
    def assistant(r):
        start_time = time.time()
        while start_time+15 != time.time():
            with sr.Microphone() as source:
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration = 1)
                audio = r.listen(source)
            try:
                c = r.recognize_google(audio).lower()
                
                print("You:"+c)
                if 'play ' in c:
                    if 'play ' in c:
                        c = c.replace('play ', '',1)
                    search = spotifyObject.search(q=c, limit = 1)
                    if len(search['tracks']['items']) !=0:
                        spotifyObject.start_playback(deviceID, None, [search['tracks']['items'][0]['uri']])
                        talkToMe("playing "+c)
                        break
                    else:
                        talkToMe("I could not find that song try again")
                elif 'list ' in c:
                    if 'list' in c:
                        c = c.replace('list ','',1)
                    search = spotifyObject.user_playlists(username)
                    playlist = ""
                    for i, t in enumerate(search['items']):
                        if c in t['name'].lower():
                            playlist = t['uri']
                            print(playlist)
                            break
                    if playlist == "":
                        search = spotifyObject.search(q=c,limit = 1,offset = 0, type = 'playlist')
                        playlist = search['playlists']['items'][0]['uri']
                    spotifyObject.start_playback(deviceID,playlist)
                    break
                elif 'volume up' in c:
                    volUp()
                    break
                elif 'volume down' in c:
                    volDown()
                    break
                elif 'mute' in c:
                    mute()
                    break
                elif 'unmute' in c:
                    unmute()
                elif 'pause' in c:
                    spotifyObject.pause_playback(deviceID)
                    break
                elif 'resume' in c:
                    spotifyObject.start_playback(deviceID)
                    break
                elif 'skip' in c:
                    spotifyObject.next_track(deviceID)
                    break
                elif 'shutdown' in c or 'shut down' in c:
                    spotifyObject.pause_playback(deviceID)
                    sys.exit()
                    break
            except sr.UnknownValueError:
                myCommand()
    def volUp():
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            currentVolume = volume.GetMasterVolume()
            if session.Process and session.Process.name() == "Spotify.exe" and (1-currentVolume)>=.1:
                volume.SetMasterVolume(currentVolume+.1,None)
            elif session.Process and session.Process.name() == "Spotify.exe":
                volume.SetMasterVolume(1,None)
    def volDown():
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            currentVolume = volume.GetMasterVolume()
            if session.Process and session.Process.name() == "Spotify.exe" and (1-currentVolume)<=.9:
                volume.SetMasterVolume(currentVolume-.1,None)
            elif session.Process and session.Process.name() == "Spotify.exe":
                volume.SetMasterVolume(0,None)
    def mute():
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            currentVolume = volume.GetMasterVolume()
            if session.Process and session.Process.name() == "Spotify.exe" and (1-currentVolume)<=.9:
                volume.SetMasterVolume(0,None)
    def unmute():
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            currentVolume = volume.GetMasterVolume()
            if session.Process and session.Process.name() == "Spotify.exe" and currentVolume == 0:
                volume.SetMasterVolume(.3,None)
            elif session.Process and session.Process.name() == "Spotify.exe":
                talkToMe("How dare you try to unmute me when I am not muted REEEEE")
    
    while True:
        myCommand()
else:
    print("Can't get token for", username)
