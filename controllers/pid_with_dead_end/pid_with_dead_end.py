"""pid_with_dead_end controller."""

from controller import Robot
import math

# create the Robot instance.
robot = Robot()
ds_val = [0,0,0,0,0,0,0,0]
state = 0 # when the robot starts state is 0 until it goes to left? right wall



# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


# setup motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# setup encoders 
left_ps_sensor = robot.getDevice("left wheel sensor")
left_ps_sensor.enable(timestep)
left_ps_sensor.getSamplingPeriod()

right_ps_sensor = robot.getDevice("right wheel sensor")
right_ps_sensor.enable(timestep)
right_ps_sensor.getSamplingPeriod()

#setup inertial unit
imu = robot.getDevice("inertial unit")
imu.enable(timestep)
imu.getSamplingPeriod()


#setup distance sensors
ds_names = ["ps0","ps1","ps2","ps3","ps4","ps5","ps6","ps7","ps8"]
for i in range (len(ds_names)):
   ds_names[i] = robot.getDevice(ds_names[i])
   ds_names[i].enable(timestep)
   ds_names[i].getSamplingPeriod()



def go(left_spd,right_spd): # to drive the wheels
    left_motor.setVelocity(left_spd)
    right_motor.setVelocity(right_spd)

def right_wall_follow ():
   front = ds_names[8].getValue()#Value gets highier when there's no obstacles
   fr_right = ds_names[1].getValue() # Value gets lower when there's no obstacles
   if fr_right < 3400 :
      lfs = 2
      rfs = 1
   
   elif fr_right > 3400 and front <400:
      lfs = 1
      rfs = 2
   else:
      lfs = 1
      rfs = 1
   go(lfs,rfs)


def left_wall_follow():
   front = ds_names[8].getValue()#Value gets highier when there's no obstacles
   fr_left = ds_names[6].getValue() # Value gets lower when there's no obstacles
   if fr_left < 3400 :
      lfs = 2
      rfs = 4
   
   elif fr_left > 3400 and front <400:
      lfs = 4
      rfs = 2
   else:
      lfs = 3
      rfs = 3
   go(lfs,rfs)




   



# Main loop:
# - perform simulation steps until Webots is stopping the controller
lfp = 1
rfp= 1
while robot.step(timestep) != -1:
   left_wall_follow()
   pass

  

  
     
   




# Enter here exit cleanup code.
