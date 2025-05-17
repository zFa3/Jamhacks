import cv2
import mediapipe as mp

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe Drawing utilities
mp_drawing = mp.solutions.drawing_utils

def is_person_in_frame(rgb_frame: cv2.Mat) -> bool:

    # Process the frame and get the body landmarks
    results = pose.process(rgb_frame)

    # Draw landmarks on the frame if any are found
    return results.pose_landmarks