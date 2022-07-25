#!/usr/bin/env python3

import cv2
import numpy as np
import argparse
import RPi.GPIO as gpio



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gamma", help="input gamma", default="1.")
    parser.add_argument("-c", "--camera", help="number of camera", default=0)
    parser.add_argument("-r", "--rotate", help="rotate image: 90/180/270", default=0)
    args = parser.parse_args()
    return args

def adjusted(img, gamma=1.):
    inv = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** inv) * 255. for i in np.arange(0, 256)]
    ).astype("uint8")
    return cv2.LUT(img, table)

def white_balance(img):
    result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

def main():

    args = parse_args() 

    gpio.setmode(gpio.BCM)

    # define a video capture object
    vid = cv2.VideoCapture(int(args.camera))
    vid.set(3, 640) # width
    vid.set(4, 480) # height

    gamma = float(args.gamma)

    while(True):

        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        if ret == False:
            print("camera can't see")
            break

        if args.rotate == "90":
            frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
        if args.rotate == "270":
            frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        if args.rotate == "180":
            frame = cv2.rotate(frame, cv2.cv2.ROTATE_180)


        frame = adjusted(frame, gamma)
#        frame = white_balance(frame)


        # Display the resulting frame
        cv2.imshow('picamera', frame)

        if (np.sum(frame) < 45000000) and gamma < 2:
            gamma += 0.1
        if (np.sum(frame) > 100000000) and gamma > 0.5:
            gamma -= 0.1

        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#     After the loop release the cap object
    vid.release()
#     Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
