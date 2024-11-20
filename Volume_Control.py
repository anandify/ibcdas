import cv2
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import Hand_Tracking_Module as htm

class GestureVolumeControl:
    def __init__(self):
        # Initialize video capture
        self.cap = cv2.VideoCapture(0)
        
        # Initialize hand tracking
        self.hand_detector = htm.Hand_Tracking(dconf=0.9)
        
        # Initialize audio controls
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = interface.QueryInterface(IAudioEndpointVolume)
        
        # Get volume range
        volume_range = self.volume.GetVolumeRange()
        self.min_vol = volume_range[0]
        self.max_vol = volume_range[1]
        
        # Initialize display variables
        self.bar_vol = 400
        self.per_vol = 0
        self.prev_time = 0
        
        # Window name constant
        self.WINDOW_NAME = "Volume Control"

    def calculate_distance(self, p1, p2):
        """Calculate distance between two points"""
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def draw_volume_bar(self, img, bar_height, percentage):
        """Draw volume visualization"""
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 2)
        cv2.rectangle(img, (50, int(bar_height)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(percentage)}%', (40, 450), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    def draw_fps(self, img):
        """Calculate and draw FPS"""
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        cv2.putText(img, f'FPS: {int(fps)}', (10, 40), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    def process_hand_landmarks(self, img, landmarks):
        """Process hand landmarks and update volume"""
        # Get thumb and index finger positions
        thumb_x, thumb_y = landmarks[4][1], landmarks[4][2]
        index_x, index_y = landmarks[8][1], landmarks[8][2]
        
        # Calculate center point
        center_x = (thumb_x + index_x) // 2
        center_y = (thumb_y + index_y) // 2
        
        # Draw points and lines
        cv2.circle(img, (thumb_x, thumb_y), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (index_x, index_y), 5, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (255, 0, 0), 2)
        cv2.circle(img, (center_x, center_y), 5, (255, 0, 0), cv2.FILLED)
        
        # Calculate length and convert to volume
        length = self.calculate_distance((thumb_x, thumb_y), (index_x, index_y))
        
        # Hand range 25 - 200
        # Volume range -65.25 - 0
        vol = np.interp(length, [25, 200], [self.min_vol, self.max_vol])
        self.bar_vol = np.interp(length, [25, 200], [400, 150])
        self.per_vol = np.interp(length, [25, 200], [0, 100])
        
        # Set volume
        self.volume.SetMasterVolumeLevel(vol, None)
        
        # Visual feedback for minimum volume
        if length < 25:
            cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), cv2.FILLED)

    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()

    def setup_window(self):
        """Setup the display window"""
        cv2.namedWindow(self.WINDOW_NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.WINDOW_NAME, 1525, 800)

    def run(self):
        """Main loop for the gesture control system"""
        self.setup_window()
        
        while True:
            success, img = self.cap.read()
            if not success:
                break
                
            # Process hand tracking
            img = self.hand_detector.Hand_Finding(img)
            landmarks = self.hand_detector.Pos_Finding(img)
            
            if landmarks:
                self.process_hand_landmarks(img, landmarks)
            
            # Draw volume visualization
            self.draw_volume_bar(img, self.bar_vol, self.per_vol)
            self.draw_fps(img)
            
            # Display window
            cv2.imshow(self.WINDOW_NAME, img)
            
            # Check for ESC key (27) or window close button
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or cv2.getWindowProperty(self.WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break
        
        self.cleanup()

if __name__ == "__main__":
    try:
        controller = GestureVolumeControl()
        controller.run()
    except Exception as e:
        print(f"Error occurred: {e}")
        # Ensure cleanup happens even if an error occurs
        controller.cleanup()