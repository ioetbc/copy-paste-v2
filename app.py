import os, time
import cv2
import numpy as np
import inspect
import rumps
import os.path

class RunApp(rumps.App):
    @rumps.clicked("Run Work Lock")
    def prefs(self, _):
        def initiateLock():
            while True:
                time.sleep(1)
                cmd = "ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle}'"
                result = os.popen(cmd)
                str = result.read()
                idle_time = int(str.split(".")[0])
                print('user idle time', idle_time)
                seconds_face_not_detected = 0

                if idle_time >= 3:
                    while True:
                        front_face_cascade = cv2.CascadeClassifier('/Applications/dist/haarcascade_frontalface_default.xml')
                        profile_face_cascade = cv2.CascadeClassifier('/Applications/dist/haarcascade_profileface.xml')
                        eye_cascade = cv2.CascadeClassifier('/Applications/dist/haarcascade_eye.xml')

                        cap = cv2.VideoCapture(0)
                        ret, img = cap.read()
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                        front_face = front_face_cascade.detectMultiScale(gray, 1.3, 5)
                        profile_face = profile_face_cascade.detectMultiScale(gray, 1.3, 5)
                        eye = eye_cascade.detectMultiScale(gray, 1.3, 5)

                        person_detected = False

                        for (x, y, w, h) in front_face:
                            # cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            print('front face detected')
                            # cv2.imshow('img', img)
                            for (x, y, w, h) in eye:
                                # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                person_detected = True
                                print('eye detected')
                                print('person_detected:', person_detected)
                                # cv2.imshow('img', img)

                                seconds_face_not_detected = 0
                                cap.release()
                                cv2.destroyAllWindows()
                                print('waiting 5 seconds tobe called again if no activity')
                                time.sleep(5)
                                initiateLock()
                                break

                        for (x, y, w, h) in profile_face:
                            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            person_detected = True
                            print('face_detected profile face', person_detected)
                            seconds_face_not_detected = 0
                            cap.release()
                            cv2.destroyAllWindows()
                            print('waiting 5 seconds tobe called again if no activity')
                            time.sleep(5)
                            initiateLock()
                            break

                        if not person_detected:
                            seconds_face_not_detected += 1

                            if seconds_face_not_detected > 10:
                                print('LOCK SCREEN')
                                cap.release()
                                cv2.destroyAllWindows()
                                os.system("/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend")
                                break

                        # cv2.imshow('img', img)
                        print('FACE_DETECTED', person_detected)
                        print('seconds_face_not_detected', seconds_face_not_detected)

                        k = cv2.waitKey(30) & 0xff
                        if k == 27:
                            break
        initiateLock()

if __name__ == "__main__":
    RunApp("🙈").run()
