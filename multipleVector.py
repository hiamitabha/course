import anki_vector
import asyncio
import time
import argparse

#Animations
_ANIM1 = 'anim_fistbump_requesttwice_01'
_ANIM2 = 'anim_fistbump_requestoncelong_01'

def connect(serial):
   # Create a Robot object
   robot = anki_vector.AsyncRobot(serial)
   # Connect to Vector
   robot.connect()
   # Start saying text asynchronously
   #sayFuture = robot.behavior.say_text("Hello World")
   # Make sure text has been spoken
   #sayFuture.result()
   return robot

def disconnect(robot):
   # Disconnect from Vector
   robot.disconnect()

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
   time.sleep(5)
   args = parse()
   robot1 = connect(args.serial1)
   robot2 = connect(args.serial2) 
   anim1 = robot1.anim.play_animation(args.animation1)
   anim2 = robot2.anim.play_animation(args.animation2)
   anim1.result()
   anim2.result()
   disconnect(robot1)
   disconnect(robot2)

if __name__ == "__main__":
   main() 
