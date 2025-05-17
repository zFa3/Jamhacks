import cv2
import mediapipe as mp

def is_face_in_frame(cvframe: cv2.Mat) -> bool:

    # Init Mediapipe face mesh
    mp_face_mesh = mp.solutions.face_mesh

    # Mediapipe pose (face)
    mp_pose = mp.solutions.pose
    
    face_mesh = mp_face_mesh.FaceMesh(
        static_image_mode=False,
        # only need to track the driver's face
        max_num_faces=1,

        # improve the accuracy around difficult areas of the face
        refine_landmarks=True,

        # increase minimum confidence to prevent false positives
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    frame = cv2.cvtColor(cvframe, cv2.COLOR_BGR2RGB)

    # process the face

    results = face_mesh.process(frame)

    # if the face exists

    return results.multi_face_landmarks