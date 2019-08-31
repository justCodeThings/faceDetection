'''A face detection app that uses the OpenCV python wrapper and 
a face_recogniton library to detect faces, draw a red circle over and number over
them, print the coordinates of each face to the console, and save the face 
detecting session to the current directory.

The opencv-python, face_recognition, and pyautogui modules are required to 
run this program (although pyautogui may be omitted.  See line 33) '''

import cv2
import face_recognition
import pyautogui
import os

def change_res(width, height):
    # Change resolution for faster processing
    # Resolution of my webcam is 640x480
    video_capture.set(3, width)
    video_capture.set(4, height)
 
def rescale_frame(frame):
    # Passing an argument that looks like "percent=75" into rescale frame
    # while allow you to scale up an individual resolution.  But this generates
    # different sizes for different reolutions and I'm too lazy to work out some
    # math to make it look good.  Use this snippit if you're feeling single 
    # resolutional.
    '''width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)'''
    width = 640
    height = 480
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# Introductory messages and settings gathering
# Remove these if you don't want to use pyautogui but remember to
# reassign the variables.  Maybe remove output.  It's worthless without a prompt.
pyautogui.alert(text='Welcome to some face detection software run on OpenCV in Python.  Press \'q\' to quit at any time.', title='Face Detection')
resolution = pyautogui.confirm(text='Please select a resolution. (lower resolutions will result in better frame rate.  320x240 reccomended.)', title='Settings - Resolution', buttons=['640x480', '320x240', '240x180'])
output = pyautogui.confirm(text='Output face detection session as video? Video will be stored in '+str(os.getcwd())+' as output.avi.  Previous recordings will be overwritten.  Edit the code if you don\'t like it', title='Settings - Video Output')

# Initializing variables and settings
resolution = resolution.split('x')
width = int(resolution[0])
height = int(resolution[1])
if output == 'OK':
    # If user selects "OK" when prompted to save the face detecting session as 
    # a video, we'll save the video in this format.
    # Note: if the frame rate is fucked up then the video will appear sped up
    # because it will gather frames at interval and stitch them into a regular
    # speed video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 6.0, (width, height))
face_locations = []
num = []
cnt = 1

# Get a reference to webcam 
video_capture = cv2.VideoCapture(0)

# Change resolution to custom resolution
change_res(width, height)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Flip frame horizontally
    frame = cv2.flip(frame, 1)

    # Get frame size and print box around usable frame
    # Usable frame size at 320, 240 res at 200% is 260, 240
    # Data is not used in current code
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    full_data = frame.shape


    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)

    # Find the number of faces in frame and print the coordinates to the console
    faces = len(face_locations)
    print(face_locations)

    # Find one target face to circle and cross
    if len(face_locations) > 0:
        top, right, bottom, left = face_locations[0]
        y = int(bottom - ((bottom - top)/2))
        x = int(right - ((right - left)/2))

        # Drawing        
        #cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 1)
        cv2.circle(frame, (x, y), int((right - left)/2), (0,0,255), 2)
        cv2.line(frame,(0,y),(1000,y),(0,0,255), 2)
        cv2.line(frame,(x,0),(x,1000),(0,0,255), 2)

    # Find any remaining faces in screen and circle
    for top, right, bottom, left in face_locations:

        # Find center of faces
        y = int(bottom - ((bottom - top)/2))
        x = int(right - ((right - left)/2))

        # Drawing        
        #cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 1)
        cv2.circle(frame, (x, y), int((right - left)/2), (0,0,255), 2)
        '''cv2.line(frame,(0,y),(315,y),(0,0,255), 1)
        cv2.line(frame,(x,0),(x,360),(0,0,255), 1)'''
        font = cv2.FONT_HERSHEY_SIMPLEX

    if len(face_locations) > 0:
        for i in range(len(face_locations)):
            top, right, bottom, left = face_locations[i]
            cv2.putText(frame, str(i+1), (left, bottom + 15), font, 0.5,(255,255,255),1,cv2.LINE_AA)

    # Rescale frame size and return frame as frame150
    frame150 = rescale_frame(frame)

    # Display the resulting image
    cv2.imshow('Video', frame150)

    # Write stream to file output.avi
    out.write(frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam.  Terminate the program
video_capture.release()
out.release()
cv2.destroyAllWindows()