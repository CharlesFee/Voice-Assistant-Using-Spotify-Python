# Voice Assistant Using Spotify Python

Here is what you need to do:  
SPOTIFY PREMIUM IS NEEDED!  
1. Libraries  
install SpeechRecognition library  
install pycaw library  
install spotipy FROM THE GITHUB IT IS THE MOST UP TO DATE pip -install is an older version  
  
2. Change username to your spotify username as a string  
  
3. Make a Spotify Developer App https://developer.spotify.com  
go to edit settings in that app and make your redirect URI any URL I use https://google.com/  
  
4. Change IDs in code  
In the code there is client_id make that equal to your App's client ID as a string  
client_secret = App's client Secret as a string  
redirect_uri = App's redirect uri that you made in step 3 as a string  
  
5. If you are using OSX or Linux you will have to change the talkToMe(audio) function to use your  
computer's tts (I put it in comments in the function)  
For Macs use os.system("say " + audio)  
For Linux I think it's the same as Mac  
  
Also you will have to change the volUp/Down and mute/unmute  
For Mac you use os.system("sudo osascript -e \\"set Volume 10\\"") ranges from 0-10 and replace the volUp volDown... accordingly  
For Linux use os.system("amixer sset \\'Master\\' 50%") 0% - 100% and replace the volUp volDown... accordingly  
  
I haven't tested step 5 but if you are having trouble just look up changing volume through command line/terminal in Linux/Mac  