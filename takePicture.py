"""./takePicture.py can be used to take pictures from the Anki robot's camera
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
from anki_vector.util import degrees

def takePicture(robot, indexStart, indexEnd):
   while indexEnd >= indexStart:
      image = robot.camera.capture_single_image()
      image.raw_image.save("pictures/picture%d.jpeg" %indexEnd, "JPEG")
      print ("Written picture %d" %indexEnd)
      indexEnd -= 1

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("-i", "--startIndex",
                       help="Start Index for pictures",
                       default=1)
   parser.add_argument("-e", "--endIndex",
                       help="End Index for pictures",
                       default=20)
   args = anki_vector.util.parse_command_args(parser)
   with anki_vector.Robot(serial=args.serial) as robot:
      robot.behavior.set_head_angle(degrees(3.0))
      takePicture(robot, int(args.startIndex), int(args.endIndex))

   
