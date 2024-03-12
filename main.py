import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Drawing module for drawing landmarks
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open a video capture object (0 for the default camera)
cap = cv2.VideoCapture(0)

# Initialize variables for gesture recognition
prev_gesture = None

# Function to calculate Euclidean distance between two points
def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

# Landmark indices for the points you want to measure distance between
point1_index = mp_hands.HandLandmark.THUMB_TIP
point2_index = mp_hands.HandLandmark.INDEX_FINGER_TIP

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        continue

    # Flip the frame horizontally
    #frame = cv2.flip(frame, 1)
    
    # Convert the frame to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to detect hands
    results = hands.process(frame_rgb)
    
    # Check if hands are detected
    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

            # Determine handedness (left or right)
            if results.multi_handedness:
                # Get the handedness of the current hand
                handedness = results.multi_handedness[idx].classification[0].label
                if handedness == "Right":
                    handedness = "Left"
                else:
                    handedness = "Right"
                # Overlay handedness as text on the frame
                cv2.putText(frame, handedness, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA)
            
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            
            # Get the coordinates of the two points
            point1 = hand_landmarks.landmark[point1_index]
            point2 = hand_landmarks.landmark[point2_index]
            
            # Calculate the distance between the two points
            distance = calculate_distance(point1, point2)
            
            # Draw landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Overlay the distance as text on the frame
            cv2.putText(frame, f"Distance: {distance:.2f} units", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA)
            
    
    # Display the frame with hand landmarks
    cv2.imshow('Hand Recognition', frame)
    
    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()
