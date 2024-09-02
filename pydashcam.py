import cv2
import datetime
import time
import os

def get_save_directory():
    # Initialize tkinter and hide the root window
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    # Open the directory selection dialog
    save_directory = filedialog.askdirectory()

    return save_directory 

def record_video_segment(save_directory="", segment_duration=60):
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Retrieve the frame rate of the webcam
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:  # Sometimes CAP_PROP_FPS might not return the correct value
        fps = 20.0  # Assuming a default value
    print(f"Frame rate: {fps}")
    fps = 20.0
    while True:

        # Ask the user to select the save directory
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        extension = ".avi"
        raw_filename = save_directory + "/" + timestamp + extension
        start_time = time.time()
        elapsed_time = 0
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  # XVID codec (raw video)
        out = cv2.VideoWriter(raw_filename, fourcc, fps, (640, 480))
        print(f"{raw_filename} recording started.")
        while elapsed_time < segment_duration:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image")
                break
            
                   

            # Get the current time
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            
            # Set the position for the text (bottom left corner)
            position = (10, frame.shape[0] - 10)

            # Set the font, scale, color, and thickness
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            color = (100, 255, 100)  # White color
            thickness = 1

            # Add the current time to the frame
            cv2.putText(frame, current_time, position, font, font_scale, color, thickness, cv2.LINE_AA)
            
            # save frame 
            out.write(frame) 
            
            # Save a frame every 1 second
            elapsed_time = time.time() - start_time
            '''
            if int(elapsed_time) % 1 == 0:
                # Generate a timestamped filename for the frame
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                png_filename = os.path.join(save_directory, f"{timestamp}.png")
                cv2.imwrite(png_filename, frame)
                print(f"Frame saved: {png_filename}")'''

            # Optionally display the frame (for debugging)
            # cv2.imshow('Frame', frame)

            # Wait for the next frame to be captured
            if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
                break
                
        out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    save_directory = get_save_directory()
    if save_directory == None:
        record_video_segment(segment_duration=60)
    else:
        record_video_segment(save_directory,segment_duration=60)
