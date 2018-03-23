import pygame
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) #motor 1
GPIO.setup(27, GPIO.OUT) #motor 2
GPIO.setup(23, GPIO.OUT) #motor 3
GPIO.setup(24, GPIO.OUT) #motor 4

pygame.init()

m1 = GPIO.PWM(17, 1000)
m2 = GPIO.PWM(27, 1000)
m3 = GPIO.PWM(23, 1000)
m4 = GPIO.PWM(24, 1000)

m1.start(0) #initializes the Duty Cycle of 0
m2.start(0)
m3.start(20) #bottom motors should start spinning on startup
m4.start(20)

j = pygame.joystick.Joystick(0)
j.init() #initilizes pygame controller, which is a PS4 Bluetooth controller in this case

print(datetime.datetime.now()) #displays the current time and name of the controller
print('Name: PS4 %s' % j.get_name())

hover = False #variable initializations
s1 = 0 #stores the speeds of the motors
s2 = 0
s3 = 0
s4 = 0
val_1 = 0
val_2 = 0
val_1_s = 0
val_2_s = 0
back_motors_enabled = False 
side_motors_enabled = False

try:
    while True:
        
        events = pygame.event.get() #get pygame event handlers

        #print("Left Stick: {%s %s}" % (j.get_axis(0), j.get_axis(1)))
        #print("Right Stick: {%s %s}" % (j.get_axis(2), j.get_axis(3)))

        if j.get_axis(0) > 0.8 and abs(j.get_axis(1)) < 0.3: #obtain direction of left joystick
            left_dir = "East"
            val_1 = 10 #turning right
        elif j.get_axis(0) > 0.3 and j.get_axis(1) > 0.3: #axes 0 and 1 determines the position of the left joystick
            left_dir = "Southeast"
            val_1 = 0 
        elif abs(j.get_axis(0)) < 0.3 and j.get_axis(1) > 0.8:
            left_dir = "South"
            val_1 = 0 #can't go backwards
        elif j.get_axis(0) < -0.3 and j.get_axis(1) > 0.3:
            left_dir = "Southwest"
            val_1 = 0
        elif j.get_axis(0) < -0.8 and abs(j.get_axis(1)) < 0.3:
            left_dir = "West"
            val_1 = 10 #turning left
        elif j.get_axis(0) < -0.3 and j.get_axis(1) < -0.3:
            left_dir = "Northwest"
            val_1 = 10
        elif abs(j.get_axis(0)) < 0.3 and j.get_axis(1) < -0.8:
            left_dir = "North"
            val_1 = 10
        elif abs(j.get_axis(0)) > 0.3 and j.get_axis(1) < -0.3:
            left_dir = "Northeast"
            val_1 = 10
        else:
            left_dir = 'Deadzone'
            val_1 = 0

        if j.get_axis(2) > 0.8 and abs(j.get_axis(5)) < 0.3: #obtain direction of right joystick
            r_dir = "East"
            val_2 = 10 #turning right
        elif j.get_axis(2) > 0.3 and j.get_axis(5) > 0.3: #axes 2 and 5 determine the position of the right joystick
            r_dir = "Southeast"
            val_2 = 0 
        elif abs(j.get_axis(2)) < 0.3 and j.get_axis(5) > 0.8:
            r_dir = "South"
            val_2 = 0 #can't go backwards
        elif j.get_axis(2) < -0.3 and j.get_axis(5) > 0.3:
            r_dir = "Southwest"
            val_2 = 0
        elif j.get_axis(2) < -0.8 and abs(j.get_axis(5)) < 0.3:
            r_dir = "West"
            val_2 = 10 #turning left
        elif j.get_axis(2) < -0.3 and j.get_axis(5) < -0.3:
            r_dir = "Northwest"
            val_2 = 10
        elif abs(j.get_axis(2)) < 0.3 and j.get_axis(5) < -0.8:
            r_dir = "North"
            val_2 = 10
        elif abs(j.get_axis(2)) > 0.3 and j.get_axis(5) < -0.3:
            r_dir = "Northeast"
            val_2 = 10
        else:
            r_dir = 'Deadzone' #Deadzone if the joystick is in the default position
            val_2 = 0

        print("{Left Pointer: %s} {Right Pointer: %s}" % (left_dir, r_dir)) #displays joystick directions for debug purposes

        if back_motors_enabled == True: #continously write to back motors if they are enabled
            s3 = 51
            s4 = 51
            m3.ChangeDutyCycle(20) #allows balloon to hover
            m4.ChangeDutyCycle(20)
            if left_dir == "North" or left_dir == "East" or left_dir == "Northeast":
                if val_1 == 50: #implements slow start for the motors, incrementing the Duty Cycle between time delays
                    val_1 -= 10
                val_1 += 10
            if r_dir == "North" or r_dir == "West" or r_dir == "Northwest":
                if val_2 == 50:
                    val_2 -= 10
                val_2 += 10
            m1.ChangeDutyCycle(val_1) #adjust duty cycle of the motors
            time.sleep(0.5)
            m2.ChangeDutyCycle(val_2)
            s1 = val_1
            s2 = val_2

        if side_motors_enabled == True: #continously write to the side motors while they are enabled
            val_1_s = val_1
            val_2_s = val_2
            s1 = 0
            s2 = 0
            m1.ChangeDutyCycle(0)
            m2.ChangeDutyCycle(0)
            #use only the left analog stick for this
            if left_dir == "North":
                val_1_s = 90
            elif left_dir == "Northwest" or left_dir == "Northeast":
                val_1_s = 70
            elif left_dir == "East" or left_dir == "West":
                val_1_s = 50
            else: 
                val_1_s = 10
                
            m3.ChangeDutyCycle(val_1_s)
            time.sleep(0.2)
            m4.ChangeDutyCycle(val_1_s)
            s3 = val_1_s
            s4 = s3
        
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if hover == False:
                    if j.get_button(6): #if the L2 button is pressed
                        print("L2 Pressed, now press R2")
                        if j.get_button(7):
                            print("Back Motor Control Enabled")
                            back_motors_enabled = True #enables back motors
                            side_motors_enabled = False

                    elif j.get_button(4): #if the L1 button is pressed
                        print("L1 Pressed, now press R1")
                        if j.get_button(5):
                            print("Side Motors Control Enabled")
                            side_motors_enabled = True #enables side motors
                            back_motors_enabled = False
                        
                if j.get_button(3): #if the triangle button is pressed
                    if hover == False:
                        hover = True
                        back_motors_enabled = False #writes to the side motors and allows the balloon to hover in the air
                        side_motors_enabled = False
                        print('Entering Hover Mode...')
                        m1.ChangeDutyCycle(0)
                        m2.ChangeDutyCycle(0)
                        m3.ChangeDutyCycle(50)
                        m4.ChangeDutyCycle(50) #hovers with motors 3+4 at 50% duty cycle

                        s1 = 0
                        s2 = 0
                        s3 = 51
                        s4 = 51
                    else:
                        hover = False
                        print('Disengaging...')

                      
        #print('Motor Speeds: M1 = %s%%, M2 = %s%%, M3 = %s%%, M4 = %s%%' % (s1, s2, s3, s4))
            #logic check

        time.sleep(0.5)

except KeyboardInterrupt:
    print("EXITING NOW") #cleans up GPIO connections and exit
    m1.stop()
    m2.stop()
    m3.stop()
    m4.stop()  
    GPIO.cleanup()
    j.quit()
