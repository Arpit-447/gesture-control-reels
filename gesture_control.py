import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

# -------------------- INITIAL SETUP --------------------

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

last_action_time = 0
delay = 1.2

# Gesture smoothing variables
prev_gesture = None
gesture_start_time = 0
hold_time = 0.3

# Move cursor to center
screen_w, screen_h = pyautogui.size()
pyautogui.moveTo(screen_w // 2, screen_h // 2)

# 

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    action_text = ""

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        current_time = time.time()

        # SMOOTHING LOGIC 
        current_gesture = tuple(fingers)

        if current_gesture == prev_gesture:
            if time.time() - gesture_start_time > hold_time:
                stable = True
            else:
                stable = False
        else:
            prev_gesture = current_gesture
            gesture_start_time = time.time()
            stable = False
        # ------------------------------------------------

        # Exit
        if stable and fingers == [0,1,0,0,1]:
            print("Exiting Program...")
            break

        # Pause
        elif stable and fingers == [1,1,1,1,1]:
            if current_time - last_action_time > delay:
                pyautogui.click()
                action_text = "Pause"
                last_action_time = current_time

        # Scroll Up
        elif stable and fingers == [0,1,0,0,0]:
            if current_time - last_action_time > delay:
                pyautogui.scroll(400)
                action_text = "Scroll Up"
                last_action_time = current_time

        # Scroll Down
        elif stable and fingers == [0,0,0,0,0]:
            if current_time - last_action_time > delay:
                pyautogui.scroll(-400)
                action_text = "Scroll Down"
                last_action_time = current_time

        # Like
        elif stable and fingers[1:] == [0,0,0,0]:

            lmList = hand["lmList"]

            x1, y1 = lmList[4][0], lmList[4][1]
            x2, y2 = lmList[8][0], lmList[8][1]

            length, _, img = detector.findDistance((x1,y1), (x2,y2), img)

            if 80 < length < 220:
                if current_time - last_action_time > delay:
                    pyautogui.typewrite("l")
                    action_text = "Like"
                    last_action_time = current_time

        # Mute
        elif stable and fingers == [0,1,1,0,0]:
            if current_time - last_action_time > delay:
                pyautogui.press("volumemute")
                action_text = "Mute 🔇"
                last_action_time = current_time

        # Volume Control
        elif fingers == [1,1,0,0,0]:

            lmList = hand["lmList"]

            x1, y1 = lmList[4][0], lmList[4][1]
            x2, y2 = lmList[8][0], lmList[8][1]

            length, _, img = detector.findDistance((x1,y1), (x2,y2), img)

            if current_time - last_action_time > 0.1:

                if length > 180:
                    pyautogui.press("volumeup")
                    action_text = "Vol +"

                elif length < 150:
                    pyautogui.press("volumedown")
                    action_text = "Vol -"

                last_action_time = current_time

    

    if action_text != "":
        cv2.putText(img, action_text, (950, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

    cv2.imshow("Gesture Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()