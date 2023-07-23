import cv2
import numpy as np
import base64
import requests

twilioPhoneNumber = '+12179088838'
toPhoneNumber = '+916366060912'

def handleCallButtonPress():
    twilioAPIBaseUrl = 'https://api.twilio.com/2010-04-01'
    accountSid = yourAccSid #hidden for privacy
    authToken = yourAuthToken #hidden for privacy 
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

configs = cv2.dnn.readNet("yolov3_training_2000.weights", "yolov3_testing.cfg")
configs.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
configs.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
classes = ["Weapon"]


#gun 1: ./assets/gun-1.mp4
#gun 2: ./assets/gun-2.mp4
#no gun: ./assets/no_gun.mp4
cap = cv2.VideoCapture("./assets/gun-2.mp4")

while True:
    try:
        _, img = cap.read()
        height, width, channels = img.shape
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        configs.setInput(blob)
        
        layer_names = configs.getLayerNames()

        output_layers = [layer_names[i - 1] for i in configs.getUnconnectedOutLayers()]
        outs = configs.forward(output_layers)

        
        class_ids = []
        accs = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    accs.append(float(confidence))
                    class_ids.append(class_id)

        vals = cv2.dnn.NMSBoxes(boxes, accs, 0.5, 0.4)
        
        for i in range(len(boxes)):
            if i in vals:
                x, y, w, h = boxes[i]
                red = (0, 0, 255)
                cv2.rectangle(img, (x, y), (x + w, y + h), red, 2)

        
        if vals == 0:
            print("WEAPON FOUND")
            cv2.imwrite("gun_found.jpg", img)
            handleCallButtonPress()
            break
        key = cv2.waitKey(1)
        if key == 27:
            quit()
    except:
        print("NO WEAPON")
        quit()

cap.release()
cv2.destroyAllWindows()
