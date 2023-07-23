import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import os
import base64
import requests
import pyrebase
from model import tensor

twilioPhoneNumber = '+12179088838'
toPhoneNumber = '+916366060912'



firebaseConfig = {
    "apiKey": "AIzaSyBMesKBiA-teWfY0yUm5ffbhQgm-rDisVY",
    "authDomain": "stemisthacks2023.firebaseapp.com",
    "projectId": "stemisthacks2023",
    "storageBucket": "stemisthacks2023.appspot.com",
    "messagingSenderId": "1067109385061",
    "appId": "1:1067109385061:web:093bcd5f1fa42cbde5978c",
    'databaseURL' : "https://stemisthacks2023-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()

def main(file_path):
    sample_rate, signal = wavfile.read(file_path)
    if len(signal.shape) > 1:
        signal = signal[:, 0]
    fft_result = np.fft.rfft(signal)
    magnitudes = np.abs(fft_result)
    num_samples = len(signal)
    frequency_axis = np.fft.rfftfreq(num_samples, d=1.0 / sample_rate)
    max_magnitude_index = np.argmax(magnitudes)
    max_magnitude_frequency = frequency_axis[max_magnitude_index]
    return max_magnitude_frequency

def handleCallButtonPress():
    twilioAPIBaseUrl = 'https://api.twilio.com/2010-04-01'
    accountSid = 'ACc00dd309196ccc63c81655e4fef9c573'
    authToken = '56b94eb886ffca3fcdad3eb0a2d9f217'
    twilioPhoneNumberFormatted = requests.utils.quote(twilioPhoneNumber)
    toPhoneNumberFormatted = requests.utils.quote(toPhoneNumber)
    callUrl = f'{twilioAPIBaseUrl}/Accounts/{accountSid}/Calls.json'

    authHeader = {
        'Authorization': 'Basic ' + base64.b64encode(f'{accountSid}:{authToken}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    formData = f'To={toPhoneNumberFormatted}&From={twilioPhoneNumberFormatted}&Url=https://handler.twilio.com/twiml/EH4a24acea3c5df1809a3232e5dfea9320'

    response = requests.post(callUrl, headers=authHeader, data=formData)

    if response.ok:
        data = response.json()
        sid = data.get('sid')
    else:
        print('Error making the call:', response.text)

'''
with open("gunshot_freqs.txt", "w") as f:
    f.write("")

folders = os.listdir('C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\gunshot_audio_2')
for folder in folders:
    with open("gunshot_freqs.txt", "a") as f:
        f.write(folder + "\n")
    li = []
    files = os.listdir('C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\gunshot_audio_2\\' + folder)
    for file in files:
        
        x = main('C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\gunshot_audio_2' + "\\" + folder + '\\' + file)
        if(folder == "AK-12"):
            #400 - 500
            if(x >= 400 and x <= 500):
                li.append(x)
        elif(folder == "Zastava M92"):
            #100 - 200
            if(x >= 100 and x <= 200):
                li.append(x)
        elif(folder == "IMI Desert Eagle"):
            #0 - 100
            if(x >= 0 and x <= 100):
                li.append(x)
    with open("gunshot_freqs.txt", "a") as f:
        for i in li:
            f.write(str(i))
            f.write("\n")
        f.write("\n\n")
    median = np.median(li)
    print(folder)
    print(median)
'''

#after analyzying the median values of the audio data - the values in the ranges dict have been selected as they provided the most accurate results
#guns that are found:
#AK-12
#AK-47
#M4
#M16
#M249
#MG-42
#MP5
#Machine Gun

ranges_dict = {
    "AK" : [400, 700],
    "Machine Gun" : [0, 200],
}

#doesnt work: "C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\ac.wav"
#doesnt work: "C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\bird.wav"
#work: "C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\assets\\gunshot_audio_2\\AK-12\\3 (1).wav"
#work: "C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\assets\\gunshot_audio_2\\M4\\4 (1).wav"
audio_file = "C:\\Users\\ashwi\\OneDrive\\Documents\\hackathon prep\\hackathon\\assets\\gunshot_audio_2\\M4\\4 (1).wav"
if(tensor(audio_file)):
    x = main(audio_file)
    handleCallButtonPress()
    gun_type = None
    for i in ranges_dict:
        lower, higher = ranges_dict[i]
        if(x >= lower and x <= higher):
            gun_type = i

    user = '12184295106498076'
    gunshot_location = database.child('locations').child(user).child('location').get().val()
    data = {
        'location' : gunshot_location,
        'gunType' : gun_type
    }

    gunshot = database.child("Gunshot").set(data)
