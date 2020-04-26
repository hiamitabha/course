#!/usr/bin/env python3
 
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

"""The objective of this script is to show how to connect to Vector and play a desired animation.
"""

import anki_vector
import time
from optparse import OptionParser

def play_animation(animation):
   """
      Connect to Vector and play the given animation
   """
   with anki_vector.Robot() as robot:
      robot.behavior.drive_off_charger()
      robot.anim.play_animation(animation)
      #Wait for some time before exit
      time.sleep(10)

def main():
   parser = OptionParser()
   parser.add_option("-a", "--animation", 
                     help="The specific animation that needs to be played.")

   (options, args) = parser.parse_args()
   play_animation(options.animation)

if __name__ == "__main__":
   main()

