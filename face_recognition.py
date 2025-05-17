from __future__ import annotations
import cv2
import mediapipe as mp

class FaceRecognition:

    def __init__(self: FaceRecognition) -> None:
        ''' init function '''
        self.cvframe: cv2.Mat | None = None


        # Init Mediapipe face mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Mediapipe pose (face)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            # only need to track the driver's face
            max_num_faces=1,

            # improve the accuracy around difficult areas of the face
            refine_landmarks=True,

            # increase minimum confidence to prevent false positives
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def calculate_distance(x1: int, y1: int, x2: int, y2: int) -> float:
        ''' calculate euclidean distance between two points '''
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
    def returnlandmark_xyz(self: FaceRecognition, face_landmarks, index: int) -> list[int, int, float]:
        ''' return the x, y, z coords '''
        landmark_obj = list(face_landmarks.landmark)[index]
        h, w, _ = self.cvframe.shape
        x_px = int(landmark_obj.x * w)
        y_px = int(landmark_obj.y * h)
        z_rel = landmark_obj.z

        return x_px, y_px, z_rel

    def set_cvframe(self: FaceRecognition, cvframe: cv2.Mat) -> None:
        ''' set the open cv frame '''
        self.cvframe = cvframe
    
    def add_overlay(self: FaceRecognition, frame : cv2.Mat) -> cv2.Mat:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # process the face

        results = self.face_mesh.process(frame)

        # if the face exists

        if results.multi_face_landmarks:

            # draw each landmark on the overlay
            for face_landmarks in results.multi_face_landmarks:

                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_tesselation_style()
                )
                
                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_contours_style()
                )

                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style()
                )


        # return the rgb frame with an overlay
        return frame