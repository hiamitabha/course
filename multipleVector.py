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


# This the the IP address at which the Wavefront Proxy is installed. The
# assumption is that the Wavefront Proxy is installed on localhost. If the
# proxyis installed anywhere else, please set the IP address accordingly

import anki_vector
import asyncio
import time
import argparse
from multiprocessing import Pool

#Animations
_ANIMATION1 = 'anim_fistbump_requesttwice_01'
_ANIMATION2 = 'anim_fistbump_requestoncelong_01'

def connectAsync(serial):
   # Create a Robot object
   robot = anki_vector.AsyncRobot(serial)
   # Connect to Vector
   robot.connect()
   return robot

def connectSync(serial):
   # Create a Robot object
   robot = anki_vector.Robot(serial)
   # Connect to Vector
   robot.connect()
   return robot

def disconnect(robot):
   # Disconnect from Vector
   robot.disconnect()

def playAnimationsAsync(serial, animation):
   robot1 = connectAsync(serial[0])
   robot2 = connectAsync(serial[1]) 
   anim1 = robot1.anim.play_animation(animation[0])
   anim2 = robot2.anim.play_animation(animation[1])
   anim1.result()
   anim2.result()
   disconnect(robot1)
   disconnect(robot2)

def playAnimationOnRobotSync(input):
   (serial, animation) = input
   robot = connectSync(serial)
   robot.anim.play_animation(animation)
   disconnect(robot)

def playAnimationsMultiProcess(serial, animation):
   inputs = zip(serial, animation)
   with Pool(2) as pool:
      pool.map(playAnimationOnRobotSync, inputs)

def playAnimationsSync(serial, animation):
   inputs = zip(serial, animation)
   for (singleSerial, singleAnimation) in inputs:
      playAnimationOnRobotSync((singleSerial, singleAnimation))

def parse():
   parser = argparse.ArgumentParser()
   parser.add_argument("-s", "--serial",
                       help="Serial Numbers")
   parser.add_argument("-a", "--animation",
                       help="Animations. One per serial number",
                       default=_ANIMATION1 + ',' + _ANIMATION2)
   parser.add_argument("-m", "--mode",
                       help="Choose whether to connect to Vector"
                       " in the following modes: sync, async, multiprocess",
                       default="sync")
   args = parser.parse_args()
   return args

def main():
   args = parse()
   serialNumbers = args.serial.split(',')
   animations = args.animation.split(',')
   print (serialNumbers)
   print (animations)
   startTime = time.time()
   if args.mode == "async":
      playAnimationsAsync(serialNumbers, animations)
   elif args.mode == "sync":
      playAnimationsSync(serialNumbers, animations)
   elif args.mode == "multiprocess":
      playAnimationsMultiProcess(serialNumbers, animations)
   duration = time.time() - startTime
   print (f"Duration is {duration} seconds")
   time.sleep(1)

if __name__ == "__main__":
   main()

