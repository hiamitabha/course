#!/usr/bin/env python3
 
# Copyright (c) 2018 Amitabha Banerjee
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

"""The objective of this script is to teach how asynchronous operations can be used to mix and match animations thereby creating a new animation.

You can replace the animation strings with your choice of animations. Check the vectorAnimationsList.txt for a full report on animations supported by anki vector

This program is used for the demo in Chapter 7 of the course 'Learn AI with a
robot' at https://robotics.thinkific.com

To run this program:
Use python 3.7+
"""

import anki_vector
import time

_ANIMATION1 = 'anim_dancebeat_getout_01'
_ANIMATION2 = 'anim_fistbump_requestoncelong_01'

# Create the robot connection
with anki_vector.AsyncRobot() as robot:
    # Drive of charger
    drive_off_charger = robot.behavior.drive_off_charger()
    drive_off_charger.result()
   
    # Play the animations separately first 
    # Here is the list of animations 
    announce = robot.behavior.say_text("Separately")
    announce.result() 
    animation1 = robot.anim.play_animation(_ANIMATION1)
    animation1.result()
    animation2= robot.anim.play_animation(_ANIMATION2)
    animation2.result()
    announceTogether = robot.behavior.say_text("Together")
    animation1_without_lift = robot.anim.play_animation(_ANIMATION1,
                                                        ignore_lift_track=False) 
    animation2_again = robot.anim.play_animation(_ANIMATION2)
    announceTogether.result()
    animation1_without_lift.result()
    animation2_again.result()

    announce_finish = robot.behavior.say_text("Done with all animations")
    announce_finish.result()
