from ssl import cert_time_to_seconds
import pyttsx3
import speech_recognition as sr
import smtplib
import selenium.webdriver as webdriver
import cv2
import numpy as np
import time

engine = pyttsx3.init('sapi5') 

voices = engine.getProperty('voices') # getting different voices

engine.setProperty('voice',voices[0].id) # first voice chosen
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


dict = {'dad':'aysec2512@gmail.com','mom':'aysec2513@gmail.com','person':'person@gmail.com'}

def listen(): 

    #it takes microphone input from the user and returns string output

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Iam listening.....")

        r.pause_threshold=1

        audio = r.listen(source)

    try:

        print("Recognizing.....")

        query = r.recognize_google(audio, language = 'en-in') # setting language

        print(f"User said:{query}\n")

        

    except Exception as e:

       speak("Say that again please...")
       print(e)
       return "None"

    return(query) # user's speech returned as string

def sendEmail(to,content):

    server = smtplib.SMTP('smtp.gmail.com',587) # create a SMTP object for connection with server

    server.ehlo()

    server.starttls() #TLS connection required by gmail

    server.login('aysec2513@gmail.com','170899Ay')

    server.sendmail('aysec2513@gmail.com',to,content) # from, to, content

def camera():
                                    speak('The camera is opened because we need to confirm this request ')
                                    net = cv2.dnn.readNet('yolov3_custom_last.weights', 'yolov3_custom.cfg')
                                    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                                    classes = []
                                    with open("classes.txt", "r") as f:
                                        classes = f.read().splitlines()

                                    cap = cv2.VideoCapture(0)
                                    font = cv2.FONT_HERSHEY_PLAIN
                                    colors = np.random.uniform(0, 255, size=(100, 3))

                                    while True:
                                        _, img = cap.read()

                                        height, width, _ = img.shape

                                        blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
                                        net.setInput(blob)
                                        output_layers_names = net.getUnconnectedOutLayersNames()
                                        layerOutputs = net.forward(output_layers_names)

                                        boxes = []
                                        confidences = []
                                        class_ids = []

                                        for output in layerOutputs:
                                            for detection in output:
                                                scores = detection[5:]
                                                class_id = np.argmax(scores)
                                                confidence = scores[class_id]
                                                if confidence > 0.5:
                                                    center_x = int(detection[0]*width)
                                                    center_y = int(detection[1]*height)
                                                    w = int(detection[2]*width)
                                                    h = int(detection[3]*height)

                                                    x = int(center_x - w/2)
                                                    y = int(center_y - h/2)

                                                    boxes.append([x, y, w, h])
                                                    confidences.append((float(confidence)))
                                                    class_ids.append(class_id)

                                        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)
                                       
                                        if len(indexes)>0:
                                            for i in indexes.flatten():
                                                    x, y, w, h = boxes[i]
                                                    label = str(classes[class_ids[i]])
                                                    confidence = str(round(confidences[i],2))
                                                    color = colors[i]
                                                    cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
                                                    cv2.putText(img, label + " " + confidence, (x, y+20), font, 2, (255,255,0), 1)
                                                    if(class_ids[i]==0):              
                                                        gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
                                                        faces = face_cascade.detectMultiScale (gray, 1.3, 5) 
                                                        for (x, y, w, h) in faces:
                                                            cv2.rectangle (img, (x-50, y-50), (x + w+50, y + 50+h), (0, 0,255), 3)
                                                            cv2.putText (img, "Success", (x+50, y-50), font, 2, (255, 255, 255), 3)          
                                                        time.sleep(2)
                                                        speak('Ms. Ayse, this process is success. Your mail is sended.')
                                                        return True
                                            break 
                                        else:
                                            speak("only ayse use this program. If you want to quit press the q key in the keybord.") 
                                                                                                                                               
                                        cv2.imshow('Image', img)

                                        if cv2.waitKey (1) & 0xFF == ord ('q'):
                                            break
                                    cap.release()
                                    cv2.destroyAllWindows()
                                    return False

if __name__ == "__main__": 
    speak("Welcome the send mail program with speech command") 
    while(True):  # run infinite loop
        speak('Who do you want to send mail')
        query = listen().lower()
        devam=True
        if 'to' in query:

            try:
                while(devam==True):
                    name = list(query.split()) # extract receiver's name

                    name = name[name.index('to')+1]
                    to = dict[name]
                    konu='Sending mail adres is',to,'. Do you confirm that?'
                    speak(konu)
                    print(konu)
                    cevap=listen().lower()
                    print(cevap)
                    if(cevap=='yes'):
                        to1=to
                        speak("what should i say")
                        content = listen()
                        while(devam==True):
                            konu='Mail text is ', content, 'Do you confirm that?'
                            speak(konu)
                            cevap=listen().lower()

                            if(cevap=='yes'):
                                    content1=content
                                    bayrak=camera()
                                    if(bayrak==True):
                                        sendEmail(to1,content1)
                                        speak("email has been sent")
                                        devam =False
                                    else:
                                        speak('Only one person use this program.')
                                        devam=False                                                                                                                 
                                    break
                            elif(cevap=='no'):
                                while(devam==True):                       
                                    speak('Please say again mail text')                                                     
                                    speak("what should i say")
                                    content = listen()
                                    while(devam==True):
                                        konu='Mail text is ', content, 'Do you confirm that?'
                                        speak(konu)
                                        cevap=listen().lower()
                                        if(cevap=='yes'):
                                            content1=content 
                                            bayrak=camera()                           
                                            if(bayrak==True):
                                                sendEmail(to1,content1)
                                                speak("email has been sent")
                                                devam=False
                                            else:
                                                speak('Only one person use this program.')
                                                devam=False
                                                break
                                            break
                    elif(cevap=='no'):                                          
                                    speak('Say again who you want to send email')                       
                                    to=listen().lower()
                                    to = dict[name]
                                    while(devam==True):
                                        konu='Mail gönderilecek adres:',to,' ONAYLIYOR MUSUNUZ'
                                        speak(konu)
                                        cevap=listen().lower()
                                        if(cevap=='yes'):
                                            to1=to
                                            speak("what should i say")
                                            content = listen()
                                            while(devam==True):
                                                konu='Gönderilecek mail is ', content, 'ONAYLIYOR MUSUNUZ'
                                                speak(konu)
                                                cevap=listen().lower()
                                                if(cevap=='yes'):
                                                    content1=content
                                                    bayrak=camera()
                                                    if(bayrak==True):
                                                        sendEmail(to1,content1)
                                                        speak("email has been sent")
                                                        devam=False
                                                    else:
                                                        speak('Only one person use this program.')
                                                        devam=False
                                                        break
                                                    break
                                        elif(cevap=='no'):
                                            while(devam==True):                       
                                                speak('Please say again mail text')                                                     
                                                speak("what should i say")
                                                content = listen()                                                
                                                while(devam==True):
                                                    konu='Mail text is ', content, 'Do you confirm that?'
                                                    speak(konu)
                                                    cevap=listen().lower()
                                                    if(cevap=='yes'):
                                                        content1=content 
                                                        bayrak=camera()
                                                        if(bayrak==True):
                                                            sendEmail(to1,content1)
                                                            speak("email has been sent")
                                                            devam=False
                                                            break
                                                        else:
                                                            speak('Only one person use this program.')
                                                            devam=False
                                                            break
                        
                

            except Exception as e:

                print(e)

                speak("sorry unable to send the email at the moment.Try again")