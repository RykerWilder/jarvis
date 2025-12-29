import face_recognition
import cv2
import pickle
import os
import numpy as np
from pathlib import Path


class FaceAuthenticator:
    def __init__(self, data_file="face_data.dat"):
        self.data_file = data_file
        self.known_encoding = None
        self.is_registered = False

        # Load encoding if it exists
        if os.path.exists(self.data_file):
            self.load_face_data()

    def register_face(self, num_samples=5):
        print("Starting face registration...")
        print(f"{num_samples} samples of your face will be captured.")
        print("Look at the webcam and keep your face well illuminated.\n")

        video_capture = cv2.VideoCapture(0)
        encodings_list = []
        samples_captured = 0
        frame_count = 0

        while samples_captured < num_samples:
            ret, frame = video_capture.read()
            if not ret:
                print("Error accessing the webcam.")
                video_capture.release()
                cv2.destroyAllWindows()
                return False

            # Show frame with counter
            display_frame = frame.copy()
            cv2.putText(
                display_frame,
                f"Samples: {samples_captured}/{num_samples}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            cv2.putText(
                display_frame,
                "Press SPACE to capture",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
            cv2.imshow("Face Registration", display_frame)

            key = cv2.waitKey(1) & 0xFF

            # Capture on SPACE or automatically every 30 frames
            if key == ord(" ") or (frame_count % 30 == 0 and frame_count > 0):
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame, model="hog")

                if len(face_locations) == 0:
                    print("No face detected, please try again.")
                    continue

                if len(face_locations) > 1:
                    print("Multiple faces detected, make sure only you are in the frame.")
                    continue

                # Extract encoding
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                if len(face_encodings) > 0:
                    encodings_list.append(face_encodings[0])
                    samples_captured += 1
                    print(f"Sample {samples_captured}/{num_samples} captured.")

            # ESC to cancel
            if key == 27:
                print("Face registration cancelled.")
                video_capture.release()
                cv2.destroyAllWindows()
                return False

            frame_count += 1

        video_capture.release()
        cv2.destroyAllWindows()

        # Compute mean encoding for better accuracy
        self.known_encoding = np.mean(encodings_list, axis=0)
        self.save_face_data()
        self.is_registered = True

        print("Face registration completed successfully!")
        return True

    def verify_face(self, tolerance=0.6):
        if not self.is_registered:
            print("No face registered. Please run register_face() first.")
            return False

        video_capture = cv2.VideoCapture(0)
        authenticated = False
        attempts = 0
        max_attempts = 50  # ~5 seconds

        while attempts < max_attempts:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Show preview
            cv2.putText(
                frame,
                "Verifying face...",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2
            )
            cv2.imshow("Face Verification", frame)
            cv2.waitKey(1)

            # Process every 3rd frame for performance
            if attempts % 3 == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame, model="hog")
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        [self.known_encoding], encoding, tolerance=tolerance
                    )

                    if matches[0]:
                        authenticated = True
                        break

                if authenticated:
                    break

            attempts += 1

        video_capture.release()
        cv2.destroyAllWindows()

        return authenticated

    def save_face_data(self):
        with open(self.data_file, "wb") as f:
            pickle.dump(self.known_encoding, f)
        print(f"Face data saved to: {self.data_file}")

    def load_face_data(self):
        try:
            with open(self.data_file, "rb") as f:
                self.known_encoding = pickle.load(f)
            self.is_registered = True
            print(f"Face data loaded from: {self.data_file}")
        except Exception as e:
            print(f"Error loading face data: {e}")
            self.is_registered = False

    def delete_face_data(self):
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
            print("Face data deleted.")
        self.known_encoding = None
        self.is_registered = False

    def face_recognition_manager(self, num_samples=5, tolerance=0.6):

        #first time
        # self.register_face(num_samples=num_samples)

        if self.verify_face(tolerance=tolerance):
            print("Access granted")
        else:
            print("Access denied.")