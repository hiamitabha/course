"""The objective of this script is to make Vector explore his surroundings,
and then use Google Vision API to getect Labels and print out the list of
labels detected along with the confidence with which the labels are generated.

This program is used for the demo in Chapter 2 of the course 'Learn AI with a
robot' at https://robotics.thinkific.com

To run this program:
Use python 3.7+
Get a Google Cloud Platform (GCP) Google vision account. Download the json
which has your private key to access Google services.
Here is a reference: https://cloud.google.com/vision/docs/labels
export GOOGLE_APPLICATION_CREDENTIALS=google.json

Then run python3 ./label.py
"""
import threading
import time
import random
from io import BytesIO

import anki_vector
from anki_vector import events
from anki_vector.util import degrees, distance_mm, speed_mmps

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Adjust these parameters to tune what you want to explore
_LABEL_ACCEPTANCE_THRESHOLD = 0.8
_NUM_ROTATIONS = 8
_MAX_NUMBER_OBJECTS_DETECTED = 20


objectsDetected = dict()

def detect_labels(content):
    """
        Detect labels for supplied content
        @param content
        @return list of labels that exceed _LABEL_ACCEPTANCE_THRESHOLD
    """
    client = vision.ImageAnnotatorClient()
    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    results = []
    count = 0
    for label in labels:
        if label.score > _LABEL_ACCEPTANCE_THRESHOLD:
            results.append(label)
            count += 1
        if count > 1:
            break

    return results

def rotate_and_look_around(robot):
    """
        Rotate Vector and look around
    """
    print('Looking around...')
    # Turn a random number between 0 and 180
    turnDegrees = random.randint(0, 180)
    robot.behavior.turn_in_place(degrees(turnDegrees))
    robot.behavior.look_around_in_place()

def speakDetectedLabels(robot, labelAndScoreTuple):
    """
        Speak each of the detected labels
    """
    for item in labelAndScoreTuple:
        robot.behavior.say_text(item[0])

def on_new_camera_image(robot, event_type, event, threadEvent):
    """
        Event that is triggerred when a new image is captured by Vector
    """
    image = event.image.raw_image
    imageBuffer = BytesIO()
    image.save(imageBuffer, "JPEG")
    imageContent = imageBuffer.getvalue()
    labels = detect_labels(imageContent)
    for label in labels:
        currentObjectScore = objectsDetected.get(label.description)
        if currentObjectScore is not None:
            if currentObjectScore < label.score:
                # Lets update the score
                objectsDetected[label.description] = label.score
        else:
            # New object
            objectsDetected[label.description] = label.score
    threadEvent.set()

with anki_vector.Robot() as robot:
    robot.camera.init_camera_feed()
    robot.behavior.drive_off_charger()
    robot.behavior.drive_straight(distance_mm(200), speed_mmps(100))
    threadEvent = threading.Event()
    robot.events.subscribe(on_new_camera_image, events.Events.new_camera_image,
                           threadEvent)

    print("------ waiting for camera events, press ctrl+c to exit early ------")
    counter = _NUM_ROTATIONS
    try:
        while (counter != 0 and
               (len(objectsDetected.keys()) < _MAX_NUMBER_OBJECTS_DETECTED)):
            rotate_and_look_around(robot)
            time.sleep(2)
            if not threadEvent.wait(timeout=30):
                print("------ Did not receive a new camera image! ------")
            counter -= 1
    except KeyboardInterrupt:
        pass
    myTuple = [(k, v) for k, v in objectsDetected.items()]
    mySortedTuple = (sorted(myTuple, key=lambda x: x[1], reverse=True))
    print(mySortedTuple)
    speakDetectedLabels(robot, mySortedTuple)
    robot.behavior.drive_on_charger()
