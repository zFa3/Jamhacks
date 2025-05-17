# https://ai.google.dev/edge/mediapipe/solutions/vision/face_landmarker
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

        self.left_pan = []
        self.right_pan = []

        self.left_eye = []
        self.right_eye = []

        self.tilt = False

    def calculate_distance(self: FaceRecognition, x1: int, y1: int, x2: int, y2: int) -> float:
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
    
    def save_information(self: FaceRecognition, frame : cv2.Mat) -> None:

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # process the face
        results = self.face_mesh.process(frame)

        # if the face exists
        if results.multi_face_landmarks:

            # draw each landmark on the overlay
            for face_landmarks in results.multi_face_landmarks:

                # find the dimensions of the eyes to determine
                # if the driver has their eyes open or closed
                x, y, _ = self.returnlandmark_xyz(face_landmarks, 145)
                x2, y2, _ = self.returnlandmark_xyz(face_landmarks, 159)
                ldistance = self.calculate_distance(x, y, x2, y2)
                # print(f"Right Eye Distance: {ldistance:.4f}", end = "\t")

                x, y, _ = self.returnlandmark_xyz(face_landmarks, 386)
                x2, y2, _ = self.returnlandmark_xyz(face_landmarks, 374)
                rdistance = self.calculate_distance(x, y, x2, y2)
                # print(f"Left Eye Distance: {rdistance:.4f}")

                x, y, _ = self.returnlandmark_xyz(face_landmarks, 33)
                x2, y2, _ = self.returnlandmark_xyz(face_landmarks, 133)
                left_eye_width = self.calculate_distance(x, y, x2, y2)

                x, y, _ = self.returnlandmark_xyz(face_landmarks, 33)
                x2, y2, _ = self.returnlandmark_xyz(face_landmarks, 133)
                right_eye_width = self.calculate_distance(x, y, x2, y2)

                self.left_eye.append((ldistance/left_eye_width) * 100)
                self.right_eye.append((rdistance/right_eye_width) * 100)

                # check if the driver is facing forwards by
                # find the direction of the driver's sight

                # left landmark - left eye
                left_lx, left_ly, _ = self.returnlandmark_xyz(face_landmarks, 33)
                # right landmark - left eye
                left_rx, left_ry, _ = self.returnlandmark_xyz(face_landmarks, 133)

                # iris landmarks
                left_clx, left_cly, _ = self.returnlandmark_xyz(face_landmarks, 471)
                left_crx, left_cry, _ = self.returnlandmark_xyz(face_landmarks, 469)

                # do the same for the right eye
                right_lx, right_ly, _ = self.returnlandmark_xyz(face_landmarks, 463)
                right_rx, right_ry, _ = self.returnlandmark_xyz(face_landmarks, 263)
                right_clx, right_cly, _ = self.returnlandmark_xyz(face_landmarks, 476)
                right_crx, right_cry, _ = self.returnlandmark_xyz(face_landmarks, 474)

                # print eye pan
                self.left_pan.append(self.calculate_distance(left_clx, left_cly, left_lx, left_ly) - self.calculate_distance(left_crx, left_cry, left_rx, left_ry))
                self.right_pan.append(self.calculate_distance(right_clx, right_cly, right_lx, right_ly) - self.calculate_distance(right_crx, right_cry, right_rx, right_ry))

                self.tilt = abs(left_clx - left_crx) < abs(left_cly - left_cry) * (3 ** 0.5)

        else:

            self.left_pan.append(None)
            self.right_pan.append(None)

            self.left_eye.append(None)
            self.right_eye.append(None)       

            self.tilt = False     

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