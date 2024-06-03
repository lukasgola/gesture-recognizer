"""
PRAWA REKA: GO, STOP, TURN RIGHT
LEWA REKA: TURN LEFT

Po wykryciu okreslonego zmieniana jest wiadomosc wysylana na AGV za pomocą socket'a.

[0xFF, 0x00, 0x00, 0x00] - GO
[0x00, 0xFF, 0x00, 0x00] - STOP
[0x00, 0x00, 0xFF, 0x00] - TURN LEFT
[0x00, 0x00, 0x00, 0xFF] - TURN RIGHT

"""

import cv2
import mediapipe as mp
import socket
import struct

# Initialize MediaPipe Drawing module for drawing landmarks
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open a video capture object (0 for the default camera)
cap = cv2.VideoCapture(0)

# Flag to avoid to gestures at the time
ready = True

# Socket setup
TCP_IP = '127.0.0.1'
TCP_PORT = 10000 
MESSAGE = bytes([0x00, 0xFF, 0x00, 0x00])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = (TCP_IP, TCP_PORT)
print(f"Connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)


# Function to recognize "thumb up" gesture
def is_thumb_up_right(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
    thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]

    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    if (thumb_tip.y < thumb_ip.y < thumb_mcp.y < thumb_cmc.y and
        index_tip.x > index_pip.x and
        middle_tip.x > middle_pip.x and
        ring_tip.x > ring_pip.x and
        pinky_tip.x > pinky_pip.x and
        index_tip.x < wrist.x and middle_tip.x < wrist.x and ring_tip.x < wrist.x and pinky_tip.x < wrist.x
        
        ):
        return True
    return False

def is_stop(hand_landmarks):

    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_dip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]


    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_dip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    if(middle_tip.y < middle_dip.y and middle_dip.y < middle_pip.y and middle_pip.y < middle_mcp.y and
        index_tip.y < index_dip.y and index_dip.y < index_pip.y and index_pip.y < index_mcp.y and
        ring_tip.y < ring_dip.y and ring_dip.y < ring_pip.y and ring_pip.y < ring_mcp.y and
        pinky_tip.y < pinky_dip.y and pinky_dip.y < pinky_pip.y and pinky_pip.y < pinky_mcp.y and
        index_mcp.x < middle_mcp.x < ring_mcp.x < pinky_mcp.x and
        wrist.x > index_mcp.x and
        wrist.x < pinky_mcp.x
        
        ):
        return True

    return False

def is_left(hand_landmarks):
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]

    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    if( middle_tip.x > wrist.x and middle_tip.x > middle_mcp.x and middle_tip.x > middle_pip.x and middle_tip.x > middle_dip.x and
       index_tip.x > wrist.x and index_tip.x > index_pip.x and
       ring_tip.x > wrist.x and ring_tip.x > ring_pip.x and
       pinky_tip.x > wrist.x and pinky_tip.x > pinky_pip.x and
       index_mcp.y < middle_mcp.y < ring_mcp.y < pinky_mcp.y
       ):
        return True

    return False


def is_right(hand_landmarks):
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_dip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]

    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]

    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    if( middle_tip.x < wrist.x and middle_tip.x < middle_mcp.x and middle_tip.x < middle_pip.x and middle_tip.x < middle_dip.x and
       index_tip.x < wrist.x and index_tip.x < index_pip.x and
       ring_tip.x < wrist.x and ring_tip.x < ring_pip.x and
       pinky_tip.x < wrist.x and pinky_tip.x < pinky_pip.x and
        index_mcp.y < middle_mcp.y < ring_mcp.y < pinky_mcp.y
       ):
        return True

    return False



while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        continue

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    
    # Convert the frame to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to detect hands
    results = hands.process(frame_rgb)
    
    # Check if hands are detected
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Determine handedness (left or right)
            if results.multi_handedness:
                # Get the handedness of the current hand
                handedness = results.multi_handedness[idx].classification[0].label
                if handedness == "Right":
                     # Check for "thumb up" gesture
                    if is_thumb_up_right(hand_landmarks) and ready :
                        cv2.putText(frame, "GO", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        MESSAGE = bytes([0xFF, 0x00, 0x00, 0x00])
                        ready = False
                    # Check for "stop" gesture
                    elif is_stop(hand_landmarks) and ready:
                        cv2.putText(frame, "STOP", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        MESSAGE = bytes([0x00, 0xFF, 0x00, 0x00])
                        ready = False
                        # Check for "turn right" gesture
                    elif is_right(hand_landmarks) and ready:
                        cv2.putText(frame, "RIGHT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        MESSAGE = bytes([0x00, 0x00, 0x00, 0xFF])
                        ready = False

                else:
                    # Check for "turn left" gesture
                    if is_left(hand_landmarks) and ready:
                        cv2.putText(frame, "LEFT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                        MESSAGE = bytes([0x00, 0x00, 0xFF, 0x00])
                        ready = False
            

        message = struct.pack('!I', len(MESSAGE)) + MESSAGE
        sock.sendall(message)
        print("Message sent", str(MESSAGE))

    ready = True

    # Display the frame with hand landmarks
    cv2.imshow('Hand Recognition', frame)
    
    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


sock.close()

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()

