import cv2
import numpy as np
import argparse


class MaskDetection:
    def __init__(self, image_path):
        """
        Constructor method that initialize the MaskDetection object.

        Parameters:
        - image_path (str): Path to the input image file

        Initializes Haar cascade for face and mouth detection, sets threshold values,
        font and display settings, and reads and also flips the input image for further processing.

        """
        # Load Haar cascade for face and mouth detection
        self.face_cascade = cv2.CascadeClassifier(
            "data/haarcascade_frontalface_default.xml"
        )
        self.mouth_cascade = cv2.CascadeClassifier("data/haarcascade_mcs_mouth.xml")

        # Threshold for converting image to black and white (binary image)
        self.bw_threshold = 80

        # Font display for annotations
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.org = (25, 25)
        self.weared_mask_color_font = (255, 255, 100)
        self.not_weared_mask_color_font = (255, 255, 0)
        self.thickness = 2
        self.font_scale = 0.8
        self.weared_mask = "Wearing Mask"
        self.not_weared_mask = "Not Wearing Mask"

        # Read the input image
        self.img = cv2.imread(image_path)
        # self.img = cv2.flip(self.image, 1)

        # Convert the image into grayscale
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

    def detect_mask(self):
        """
        Method to perform mask detection on the initialized image.

        Applies face and mouth detection, check for the presence of faces and mouths,
        also annotates the image accordingly based on mask wearing status.

        """
        # Threshold the grayscale image to create a black and white image
        (thresh, black_white) = cv2.threshold(
            self.gray, self.bw_threshold, 255, cv2.THRESH_BINARY
        )

        # Detect faces in the grayscale and black and white images
        faces = self.face_cascade.detectMultiScale(self.gray, 1.3, 5)

        faces_bw = self.face_cascade.detectMultiScale(black_white, 1.3, 5)

        # Check if no faces are detected in both grayscale and black and white images
        if len(faces) == 0 and len(faces_bw) == 0:
            # It means that we cannot detect any face on the image
            cv2.putText(
                self.img,
                "No face detected",
                self.org,
                self.font,
                self.font_scale,
                self.weared_mask_color_font,
                self.thickness,
                cv2.LINE_AA,
            )
            print("No face detected")
        # Check if no faces are detected in the grayscale image but one is detectes in the black and white image
        elif len(faces) == 0 and len(faces_bw == 1):
            # It has been observed that for white mask covering mouth, with gray image face prediction is not happening
            cv2.putText(
                self.img,
                self.weared_mask,
                self.org,
                self.font,
                self.font_scale,
                self.weared_mask_color_font,
                self.thickness,
                cv2.LINE_AA,
            )
            print("Wearing Mask")
        else:    
            mouth = self.mouth_cascade.detectMultiScale(self.gray, 1.5, 5)

            # Check if no mouth is detected
            if len(mouth) == 0:
                # The face detected but lip not detected, which mean the person is wearing mask
                cv2.putText(
                    self.img,
                    self.weared_mask,
                    self.org,
                    self.font,
                    self.font_scale,
                    self.weared_mask_color_font,
                    self.thickness,
                    cv2.LINE_AA,
                )
                print("Wearing Mask")
            else:
                # The face and lip detected, which mean the person is not wearing mask
                cv2.putText(
                            self.img,
                            self.not_weared_mask,
                            self.org,
                            self.font,
                            self.font_scale,
                            self.not_weared_mask_color_font,
                            self.thickness,
                            cv2.LINE_AA,
                )
                print("Not Wearing Mask")


        cv2.imshow("Mask Detection", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def input():
    """
    Function to parse command line arguments and get the image path.

    Returns:
    - args: Object containing parsed arguments.

    Parses the command line arguments to retrieve the path to the input image file.

    """
    parser = argparse.ArgumentParser(description="Mask Detection")
    parser.add_argument("image_path", type=str, help="Path to the image file")
    return parser.parse_args()


if __name__ == "__main__":
    # Get input arguments and create MaskDetection object
    args = input()
    detector = MaskDetection(args.image_path)
    # Perform mask detection and display result
    detector.detect_mask()
