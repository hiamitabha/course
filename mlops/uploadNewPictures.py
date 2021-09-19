"""./uploadNewPictures.py can be used to take pictures from the
Anki robot's camera and upload it to the Roboflow dataset
"""
# Copyright (c) 2021 Amitabha Banerjee
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
import uuid
import json
from PIL import Image
from anki_vector.util import degrees

_DATASET_NAME = "vectorcompletedataset"

def uploadImageToRoboflow(image, imageName, roboflowKey):
   """Code to upload an image to Roboflow.
      Code is borrowed from the example at:
      https://docs.roboflow.com/adding-data/upload-api
      @param image Input image
   """ 
   # Convert to JPEG Buffer
   buffered = io.BytesIO()
   image.save(buffered, quality=90, format="JPEG")

   # Base 64 Encode
   img_str = base64.b64encode(buffered.getvalue())
   img_str = img_str.decode("ascii")

   # Construct the URL
   upload_url = "".join([
      "https://api.roboflow.com/dataset/",
      _DATASET_NAME,
      "/upload",
      "?api_key=",
      roboflowKey,
      "&name=",
      imageName,
      "&split=train"
      ])

   # POST to the API
   result = requests.post(upload_url, data=img_str, headers={
       "Content-Type": "application/x-www-form-urlencoded"
       })

   res = result.json()
   success = res.get('success')
   if not success:
      print(res)
   else:
      print("Image %s uploaded successfully!" % imageName)

def loadKey():
   with open('roboflow.json') as roboflow_file:
      data = json.load(roboflow_file) 
      key = data['key']
   return key

def takePicture(robot, roboflowKey):
   image = robot.camera.capture_single_image()
   uploadImageToRoboflow(image.raw_image,
                         "image_"+str(uuid.uuid4())+".jpeg",
                         roboflowKey)

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("-i", "--startIndex",
                       help="Start Index for pictures",
                       default=1)
   parser.add_argument("-e", "--endIndex",
                       help="End Index for pictures",
                       default=2)
   args = anki_vector.util.parse_command_args(parser)
   with anki_vector.Robot(serial=args.serial) as robot:
      robot.behavior.set_head_angle(degrees(3.0))
      key = loadKey()
      takePicture(robot, key)

   
