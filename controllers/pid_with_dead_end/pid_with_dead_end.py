"""pid_with_dead_end controller."""

from controller import Robot
import math

# create the Robot instance.
robot = Robot()
ds_val = [0,0,0,0,0,0,0,0]



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
ds_names = ["ps0","ps1","ps2","ps3","ps4","ps5","ps6","ps7"]
for i in range (len(ds_names)):
   ds_names[i] = robot.getDevice(ds_names[i])
   ds_names[i].enable(timestep)
   ds_names[i].getSamplingPeriod()



def go(left_spd,right_spd): # to drive the wheels
    left_motor.setVelocity(left_spd)
    right_motor.setVelocity(right_spd)

def read_ds():
   for i in range(len(ds_names)):
     ds_val[i] = ds_names[i].getValue()
   #print(ds_val)
   return ds_val
def pid():
   pid_ds_val = [0,0,0,0,0,0]
   
   for i in range(1,6):
      pid_ds_val[i-1] = ds_names[i].getValue()
      print(pid_ds_val[i-1])
      
   Kp= 8
   Ki = 0
   Kd = 1
   error = 0
   max_obstacle = 2500
   gain = [10,20,-30,30,-20,-10]

   
   for i in range (len(pid_ds_val)):
      if  pid_ds_val[i] < max_obstacle :
         error += gain[i] 
      else:
         pid_ds_val[i] = 0 
   pre_error = 0
   p= error
   i = i + error
   d = error - pre_error
   spd_correction = Kp*p + Ki * i + Kd * d
   print(spd_correction)

def left_wall_follow(wall_dist,lfs,rfs):
   sen_f = ds_names[6].getValue()
   sen_b = ds_names[4].getValue()
   
   if sen_f*(1/math.cos((math.pi) - 2.37)) > wall_dist :
      rfs += 0.5
   if sen_b *(1/math.cos(4.21-(math.pi))) < wall_dist:
      lfs += 0.5
   print(f'front = {sen_f*(1/math.cos((math.pi) - 2.37))} ... bacl = {sen_b *(1/math.cos(4.21-(math.pi)))}')
   go(lfs,rfs)

def left_wall(obstacle):
   if ds_names[5].getValue() < obstacle :
      go(-0.5,1.3)
   else:
      go(1,1)
   

   



# Main loop:
# - perform simulation steps until Webots is stopping the controller
lfp = 1
rfp= 1
while robot.step(timestep) != -1:
   print(f'05 : {ds_names[5].getValue()} 06 : {ds_names[6].getValue()} 06-6 {(1/math.cos(3.14-2.37))*ds_names[6].getValue()}')
   

  
     
   




# Enter here exit cleanup code.
