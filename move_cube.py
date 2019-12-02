import anki_vector
import time
from anki_vector.util import distance_mm, speed_mmps

with anki_vector.Robot() as robot:
    # First disconnect and reconnect cube so that the connection is valid
    robot.world.disconnect_cube()
    time.sleep(3)
    robot.world.connect_cube()
    time.sleep(1)

    if robot.world.connected_light_cube:
        pickupObjectResponse = robot.behavior.pickup_object(robot.world.connected_light_cube)
        print (pickupObjectResponse)
        #if pickupObjectResponse.status == 1:
        if 1:
            robot.behavior.drive_straight(distance_mm(200), speed_mmps(100))
            placeObjectOnGroundResponse = robot.behavior.place_object_on_ground_here()
            # if placeObjectOnGroundResponse.status == 1:
            print (placeObjectOnGroundResponse)
            if 1:
               print ("Job complete")
            else:
               print ("Failed to place object on ground")
        else:
            print ("Unable to pick up object")

    else:
        print("Issue connecting to lightcube")




