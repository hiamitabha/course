"""./examinePicture is used to do object detection from Vector's camera
"""
# Copyright (c) 2020 Amitabha Banerjee
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import anki_vector
import argparse
import time
import requests
import base64
import io
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import threading

from anki_vector.util import degrees
from anki_vector import events
from util import loadKey, getDatasetName, getModelUuid

_SHOW_BOUNDING_BOX = True

def validatePicture(image, dataset, modelUuid, key):
   """Run inference on the provided image with the help of Roboflow
   inference API. Shows the image on screen, and then destroys is
   @param image: The image to run inference on
   @param dataset: The roboflow dataset
   @param modelUuid: The specific model in the dataset to run inference on
   """
   # Convert to JPEG Buffer
   buffered = io.BytesIO()
   image.save(buffered, quality=90, format="JPEG")

   # Base 64 Encode
   img_str = base64.b64encode(buffered.getvalue())
   img_str = img_str.decode("ascii")


   # Construct the Roboflow URL to do Inference
   upload_url = "".join([
      "https://detect.roboflow.com/",
      dataset,
      "/",
      modelUuid,
      "?api_key=",
      key, 
      "&format=json"
   ])


   # POST request to the API
   headers = {"Content-Type": "application/x-www-form-urlencoded"}
   r = requests.post(upload_url, data=img_str, headers=headers)
   preds = r.json()
   print (preds)
   detections = preds['predictions']

   draw = ImageDraw.Draw(image)
   font = ImageFont.load_default()
   if _SHOW_BOUNDING_BOX:
      for box in detections:
         color = "#4892EA"
         x1 = box['x'] - box['width'] / 2
         x2 = box['x'] + box['width'] / 2
         y1 = box['y'] - box['height'] / 2
         y2 = box['y'] + box['height'] / 2
         draw.rectangle([
            x1, y1, x2, y2
         ], outline=color, width=5)

         text = box['class']
         text_size = font.getsize(text)

         #set button size + 10px margins
         button_size = (text_size[0]+20, text_size[1]+20)
         button_img = Image.new('RGBA', button_size, color)
         # put text on button with 10px margins
         button_draw = ImageDraw.Draw(button_img)
         button_draw.text((10, 10), text, font=font, fill=(255,255,255,255))

         # put button on source image in position (0, 0)
         image.paste(button_img, (int(x1), int(y1)))
   image.show()
   time.sleep(2)

def on_new_raw_camera_image(robot, event_type, event, done,
                            dataset, modelId, key):
    """Process the event of a new image captured by Vector
    """
    print("Process new camera image")
    validatePicture(event.image, dataset, modelId, key)
    done.set()

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   args = anki_vector.util.parse_command_args(parser)
   
   #Loading all the details required for inference
   dataset = getDatasetName()
   model = getModelUuid()
   key = loadKey()
 
   with anki_vector.Robot(serial=args.serial) as robot:
      robot.behavior.set_head_angle(degrees(3.0))
      robot.camera.init_camera_feed()
      done = threading.Event()
      robot.events.subscribe(on_new_raw_camera_image, events.Events.new_raw_camera_image, done, dataset, model, key)

      print("------ waiting for camera events, press ctrl+c to exit early ------")

      if not done.wait(timeout=200):
         print("------ Was not able to process last image! ------")

   
