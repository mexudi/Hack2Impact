import cv2 # Import the OpenCV library
import numpy as np
import time
from text_to_speech import assistaneResponse # Import a function to generate an audio response


def color_recognition(image):
    
    """Recognizes the percentage of different colors in an image using HSV color space.

    Args:
        image: A numpy array representing an image.

    Returns:
        A dictionary containing the percentage of each color in the image.

    """
    # Define the boundaries of the colors in the HSV color space
    colors = {
        'red': ([0, 50, 50], [5, 255, 255]),
        'orange': ([10, 50, 50], [20, 255, 255]),
        'yellow': ([25, 50, 50], [35, 255, 255]),
        'green': ([36, 50, 50], [70, 255, 255]),
        'blue': ([90, 50, 50], [130, 255, 255]),
        'purple': ([140, 50, 50], [170, 255, 255]),
        'pink': ([170, 50, 50], [180, 255, 255]),
        'brown': ([0, 50, 50], [20, 255, 255]),
        'gray': ([0, 0, 0], [180, 50, 50]),
        'white': ([0, 0, 50], [180, 50, 255]),
        'black': ([0, 0, 0], [180, 255, 50])
    }
    
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Find the color regions in the image using the boundaries
    color_regions = {}
    total_pixels = hsv_image.shape[0] * hsv_image.shape[1]
    for color, (lower, upper) in colors.items():

        # Create a binary mask for the color region
        mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))

        # Count the number of non-zero pixels in the mask
        color_pixels = cv2.countNonZero(mask)

        # Calculate the percentage of the color in the image
        color_regions[color] = color_pixels / total_pixels * 100
    
    # Return the percentage of each color
    return color_regions

def color_detection():
    
    """Opens the camera and displays the percentage of different colors in the live feed. 

    The function runs for a fixed amount of time, and then returns the average percentages of each color
    present in the frames captured during this time period.

    Returns:
        None
    """

    # Initialize the video capture object
    video_capture = cv2.VideoCapture(0)

    # Initialize the timer
    start_time = time.time()
    run_time = 2

    # Initialize the list of color averages
    color_averages = []

    while time.time() - start_time < run_time:
        # Capture a frame from the camera
        ret, frame = video_capture.read()

        # Apply the color recognition algorithm to the frame
        color_percentages = color_recognition(frame)

        # Display the percentage of each color on the frame
        for color, percentage in color_percentages.items():
            # Add text to the frame with the color percentage information
            text = '{}: {:.2f}%'.format(color, percentage)
            cv2.putText(frame, text, (10, (list(color_percentages.keys()).index(color) + 1) * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

        # Display the frame
        cv2.imshow('Color Recognition', frame)

        # Add the color averages to the list
        color_averages.append(color_percentages)

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

    # Calculate the average of each color
    averages = {}
    for color in color_averages[0].keys():
        percentages = [d[color] for d in color_averages]
        averages[color] = sum(percentages) / len(percentages)

    # Print the list of color averages
    #print(averages)
    output_str = "The picture contains the following colors:"
    for color, value in averages.items():
        if value > 20:
            output_str += " For " + color +  " it is "+str(round(float(value)))+' percentage. '

    #print(output_str)
    assistaneResponse(output_str)