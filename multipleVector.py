import anki_vector
import asyncio
import time
import argparse
from multiprocessing import Pool

#Animations
_ANIM1 = 'anim_fistbump_requesttwice_01'
_ANIM2 = 'anim_fistbump_requestoncelong_01'

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

def playAnimationOnRobotSync(serial, animation):
   robot = connectSync(serial)
   robot.anim.play_animation(animation)
   disconnect(robot)
   

def playAnimationsMultiProcess(serial, animation):
   inputs = zip(serial, animation)
   print (inputs)
   with Pool(2) as pool:
      pool.map(playAnimationOnRobotSync, inputs)

def playAnimationsSync(serial, animation):
   inputs = zip(serial, animation)
   print (inputs)
   for (singleSerial, singleAnimation) in inputs:
      playAnimationOnRobotSync(singleSerial, singleAnimation)

def parse():
   parser = argparse.ArgumentParser()
   parser.add_argument("-s1", "--serial1",
                       help="Serial Number of the first robot",
                       default=_VECTOR1_SERIAL)
   parser.add_argument("-s2", "--serial2",
                       help="Serial Number of the second robot",
                       default=_VECTOR2_SERIAL)
   parser.add_argument("-a1", "--animation1",
                       help="Animation required of the first robot",
                       default=_ANIM1)
   parser.add_argument("-a2", "--animation2",
                       help="Animation required of the second robot",
                       default=_ANIM2)
   args = parser.parse_args()
   return args

def main():
   args = parse()
   #playAnimationsAsync([args.serial1, args.serial2],[args.animation1, args.animation2])
   playAnimationsSync([args.serial1, args.serial2],[args.animation1, args.animation2])

if __name__ == "__main__":
   main() 
