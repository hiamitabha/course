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
import asyncio
import time
import argparse

chargerOccupied = False

def connectAsync(serial):
   # Create a Robot object
   robot = anki_vector.AsyncRobot(serial)
   # Connect to Vector
   robot.connect()
   return robot

def checkIfChargeRequired(robot):
   """Measure the battery voltage and check if robot requires charging
   """
   global chargerOccupied
   isChargingRequired = False
   if chargerOccupied:
      #Charger is occupied, so cannot charge right now
      return isChargingRequired
   batteryStateOp = robot.get_battery_state()
   batteryState = batteryStateOp.result()
   if batteryState:
      batteryVoltage = batteryState.battery_volts
   else:
      batteryVoltage = None
      # if we cannot measure the voltage, we dont charge
      return isChargingRequired
   print (batteryVoltage)
   if (batteryVoltage < 3.7):
      isChargingRequired = True
   return isChargingRequired

async def driveOffCharger(robot):
   """Drive off the charger if placed on it. MOves by a random rotation to ensure that there are no collissions
   """
   status = robot.status
   if status.is_on_charger:
      robot.behavior.drive_off_charger()
      return
   else:
      return 

async def returnToCharger(robot):
   """Returns to charger. 
   """
   op = robot.behavior.drive_on_charger()
   op.result()

def disconnect(robot):
   # Disconnect from Vector
   robot.disconnect()

async def worker(robot, id, lock):
   """Connect to the robots and run
   """
   print ("Starting worker for robot %d" %id)
   if not checkIfChargeRequired(robot):
      await driveOffCharger(robot)
   else:
      with await lock:
         await returnToCharger(robot)
         chargerOccupied = True
         print ("Charger occupied by robot %d" %id)
         time.sleep(120)
         await driveOffCharger(robot)
         chargerOccupied = False
   print ("Ending worker for robot %d" %id)
         
def parse():
   parser = argparse.ArgumentParser()
   parser.add_argument("-s", "--serial",
                       help="Serial Numbers")
   args = parser.parse_args()
   return args

async def main():
   global chargerOccupied
   args = parse()
   serialNumbers = args.serial.split(',')
   print (serialNumbers)
   startTime = time.time()
   robot1 = connectAsync(serialNumbers[0])
   await driveOffCharger(robot1)
   robot2 = connectAsync(serialNumbers[1])
   await driveOffCharger(robot2)
   chargerOccupied = False
   #This lock needs to be held as long as the robot is charging
   lock = asyncio.Lock()
   while True:
      await asyncio.wait([worker(robot1, 1, lock), worker(robot2, 2, lock)])
      time.sleep(30)
   duration = time.time() - startTime
   print (f"Duration is {duration} seconds")

if __name__ == "__main__":
   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())
   loop.close()

