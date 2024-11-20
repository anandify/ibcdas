import cv2
import numpy as np

def get_dominant_color(image, n_colors):
    """Find the dominant color in the image using k-means clustering."""
    pixels = np.float32(image).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.1)
    _, labels, centroids = cv2.kmeans(pixels, n_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    label_counts = np.bincount(labels.flatten())
    dominant_color = centroids[np.argmax(label_counts)]
    return dominant_color

def onMouse(event, x, y, flags, param):
    """Mouse callback function to set the clicked flag."""
    if event == cv2.EVENT_LBUTTONUP:
        param[0] = True

def main():
    # Open camera capture
    cameraCapture = cv2.VideoCapture(0)
    if not cameraCapture.isOpened():
        print("Error: Camera not accessible")
        return

    # Create window and set to fullscreen
    cv2.namedWindow('camera', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    clicked = [False]  # Use a list to pass the flag to the callback function
    cv2.setMouseCallback('camera', onMouse, param=clicked)

    while not clicked[0]:
        success, frame = cameraCapture.read()
        if not success:
            print("Error: Failed to capture image")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(gray, 37)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50, param1=120, param2=40, minRadius=0, maxRadius=0)

        sign_name = None  # Default to None

        if circles is not None:
            circles = np.uint16(np.around(circles))
            max_r, max_i = 0, 0
            for i in range(len(circles[0, :, 2])):
                if circles[0, :, 2][i] > 50 and circles[0, :, 2][i] > max_r:
                    max_i = i
                    max_r = circles[0, :, 2][i]
            x, y, r = circles[0, :, :][max_i]

            if y > r and x > r:
                square = frame[y-r:y+r, x-r:x+r]
                dominant_color = get_dominant_color(square, 2)

                if dominant_color[2] > 100:  # Check for red color (STOP)
                    sign_name = "STOP"
                elif dominant_color[0] > 80:  # Check for blue color (DIRECTION)
                    # Define zones for directional checks
                    h, w = square.shape[:2]
                    zone_0 = square[h*3//8:h*5//8, w*1//8:w*3//8]
                    zone_1 = square[h*1//8:h*3//8, w*3//8:w*5//8]
                    zone_2 = square[h*3//8:h*5//8, w*5//8:w*7//8]

                    zone_0_color = get_dominant_color(zone_0, 1)
                    zone_1_color = get_dominant_color(zone_1, 1)
                    zone_2_color = get_dominant_color(zone_2, 1)

                    if zone_1_color[2] < 60:  # Check if middle zone is not red
                        if np.sum(zone_0_color) > np.sum(zone_2_color):
                            sign_name = "LEFT"
                        else:
                            sign_name = "RIGHT"
                    else:
                        if np.sum(zone_1_color) > np.sum(zone_0_color) and np.sum(zone_1_color) > np.sum(zone_2_color):
                            sign_name = "FORWARD"
                        elif np.sum(zone_0_color) > np.sum(zone_2_color):
                            sign_name = "FORWARD AND LEFT"
                        else:
                            sign_name = "FORWARD AND RIGHT"

            # Draw the circles found
            for i in circles[0, :]:
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

        # Display the sign name if it's valid
        if sign_name:
            cv2.putText(frame, sign_name, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('camera', frame)
        
        # Check for close window events (Esc key or window close button)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or clicked[0]:  # 27 is the Esc key
            break

    # Clean up
    cv2.destroyAllWindows()
    cameraCapture.release()

if __name__ == '__main__':
    main()