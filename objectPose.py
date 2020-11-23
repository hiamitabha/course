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

import time
import argparse
import anki_vector
from anki_vector.events import Events
from anki_vector.util import degrees

def handle_object_appeared(robot, event_type, event):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    print(f"Vector started seeing an object: \n{event.obj}")

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   args = anki_vector.util.parse_command_args(parser)
   with anki_vector.Robot(serial=args.serial,
                          default_logging=False,
                          show_viewer=True,
			  enable_nav_map_feed=True) as robot:
      # Place Vector's cube where he can see it
      robot.events.subscribe(handle_object_appeared, Events.object_appeared)
      robot.behavior.set_lift_height(0.0)
      robot.behavior.set_head_angle(degrees(0.0))

      time.sleep(120.0)
