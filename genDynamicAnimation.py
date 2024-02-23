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

"""The objective of this script is to teach how asynchronous operations can be used to mix and match animations thereby creating a new animation.

You can replace the animation strings with your choice of animations. Check the vectorAnimationsList.txt for a full report on animations supported by anki vector

This program is used for the demo in Chapter 7 of the course 'Learn AI with a
robot' at https://robotics.thinkific.com

To run this program:
Use python 3.7+
"""

import anki_vector
import time
import argparse

_ANIMATION1 = 'anim_holiday_hyn_confetti_01'
_ANIMATION2 = 'anim_fistbump_requesttwice_01'
_ANIMATION3 = 'anim_dancebeat_getout_02'

# Create the robot connection
def play_animations(args):
    """
    Play the animations provided in the input args
    :param: Input arguments after post processing
    """
    with anki_vector.AsyncRobot(args.serial) as robot:
        # Drive of charger
        drive_off_charger = robot.behavior.drive_off_charger()
        drive_off_charger.result()

        # Play the animations separately first
        # Here is the list of animations
        announce = robot.behavior.say_text("Separately")
        announce.result()
        animation1 = robot.anim.play_animation(args.animationwithoutlift)
        animation1.result()
        animation2= robot.anim.play_animation(args.animationwithoutbody)
        animation2.result()
        animation3= robot.anim.play_animation(args.animationwithouthead)
        animation3.result()
        announceTogether = robot.behavior.say_text("Now Together")
        animation_without_lift = robot.anim.play_animation(args.animationwithoutlift,
                                                            ignore_lift_track=True)
        animation_without_body = robot.anim.play_animation(args.animationwithoutbody,
                                                            ignore_body_track=True)
        animation_without_head = robot.anim.play_animation(args.animationwithouthead,
                                                            ignore_head_track=True)
        announceTogether.result()
        animation1_without_lift.result()
        animation2_without_body.result()
        animation3_without_head.result()

        announce_finish = robot.behavior.say_text("Done with all animations")
        announce_finish.result()

def parse():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--animationwithoutlift",
                       help="Animation to be played without the lift track",
                       default=_ANIMATION1)
    parser.add_argument("-b", "--animationwithoutbody",
                        help="Animation to be played without the body track",
                        default=_ANIMATION2)
    parser.add_argument("-he", "--animationwithouthead",
                        help="Animation to be played without the head track",
                        default=_ANIMATION3)
    args = anki_vector.util.parse_command_args(parser)
    return args

if __name__ == "__main__":
    args = parse()
    play_animations(args)

