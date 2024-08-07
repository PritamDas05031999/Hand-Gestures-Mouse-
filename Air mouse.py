import cv2
import time
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE=False
wcam, hcam = 1920, 1080

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4,hcam)

hnad_detector = mp.solutions.hands.Hands()
drowing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

screen_width_speed = (screen_width + 600)
screen_height_speed = (screen_height + 600)

pTime = 0
index_y = 0
click_p = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    frame_height_speed = frame_height - 200
    frame_width_speed = frame_width - 200
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hnad_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drowing_utils.draw_landmarks(frame, hand)
            landmark = hand.landmark
            for id, landmark in enumerate(landmark):
                x = int(landmark.x * frame_width_speed)
                y = int(landmark.y * frame_height_speed)
                x_circle = int(landmark.x * frame_width)
                y_circle = int(landmark.y * frame_height)
                #print(x, y)
                if id == 6:
                    cv2.circle(img=frame, center=(x_circle, y_circle), radius=10, color=(0, 255, 255))
                    index_x = screen_width_speed / frame_width_speed * x
                    index_y = screen_height_speed / frame_height_speed * y
                    pyautogui.moveTo((index_x - 250), index_y)
                if id == 4:
                    cv2.circle(img=frame, center=(x_circle, y_circle), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width_speed / frame_width_speed * x
                    thumb_y = screen_height_speed / frame_height_speed * y
                    if abs(index_y - thumb_y) < 15:
                        click_p = click_p + 1
                        pyautogui.click()
                        pyautogui.sleep(0.5)
                        print(f"click {click_p}")

        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)

    cv2.imshow('Air mouse', frame)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == 27:
        break
