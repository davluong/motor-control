import pygame
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT) #motor 1
GPIO.setup(22, GPIO.OUT) #motor 2
GPIO.setup(27, GPIO.OUT) #motor 3
GPIO.setup(4, GPIO.OUT) #motor 4

pygame.init()

m1 = GPIO.PWM(22, 1000000)
m2 = GPIO.PWM(17, 1000000)
m3 = GPIO.PWM(27, 1000000)
m4 = GPIO.PWM(4, 1000000)

m1.start(0)
m2.start(0)
m3.start(0)
m4.start(0)

j = pygame.joystick.Joystick(0)
j.init()

print(datetime.datetime.now())
print('Name: PS4 %s' % j.get_name())

hover = False
s1 = 0 #stores the speeds of the motors
s2 = 0
s3 = 0
s4 = 0
val_1 = 0
val_2 = 0
back_motors_enabled = False
side_motors_enabled = False

try:
    while True:
        
        events = pygame.event.get()

        #print("Left Stick: {%s %s}" % (j.get_axis(0), j.get_axis(1)))
        #print("Right Stick: {%s %s}" % (j.get_axis(2), j.get_axis(3)))

        if j.get_axis(0) > 0.8 and abs(j.get_axis(1)) < 0.3:
            left_dir = "East"
            val_1 = 100 #turning right
        elif j.get_axis(0) > 0.3 and j.get_axis(1) > 0.3:
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
            val_1 = 20 #turning left
        elif j.get_axis(0) < -0.3 and j.get_axis(1) < -0.3:
            left_dir = "Northwest"
            val_1 = 51
        elif abs(j.get_axis(0)) < 0.3 and j.get_axis(1) < -0.8:
            left_dir = "North"
            val_1 = 100
        elif abs(j.get_axis(0)) > 0.3 and j.get_axis(1) < -0.3:
            left_dir = "Northeast"
            val_1 = 100
        else:
            left_dir = 'Deadzone'
            val_1 = 0

        if j.get_axis(2) > 0.8 and abs(j.get_axis(5)) < 0.3:
            r_dir = "East"
            val_2 = 20 #turning right
        elif j.get_axis(2) > 0.3 and j.get_axis(5) > 0.3:
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
            val_2 = 100 #turning left
        elif j.get_axis(2) < -0.3 and j.get_axis(5) < -0.3:
            r_dir = "Northwest"
            val_2 = 100
        elif abs(j.get_axis(2)) < 0.3 and j.get_axis(5) < -0.8:
            r_dir = "North"
            val_2 = 100
        elif abs(j.get_axis(2)) > 0.3 and j.get_axis(5) < -0.3:
            r_dir = "Northeast"
            val_2 = 50
        else:
            r_dir = 'Deadzone'
            val_2 = 0

        print("{Left Pointer: %s} {Right Pointer: %s}" % (left_dir, r_dir))

        if back_motors_enabled == True:
            s3 = 51
            s4 = 51
            m3.ChangeDutyCycle(0) #allows balloon to hover
            m4.ChangeDutyCycle(0)
            m1.ChangeDutyCycle(val_1)
            m2.ChangeDutyCycle(val_2)
            s1 = val_1
            s2 = val_2

        if side_motors_enabled == True:
            s1 = 0
            s2 = 0
            m1.ChangeDutyCycle(0)
            m2.ChangeDutyCycle(0)
            #use only the left analog stick for this
            if val_1 <= 0:
                val_1 += 20
            if val_1 >= 100:
                val_1 = 90
            m3.ChangeDutyCycle(val_1)
            m4.ChangeDutyCycle(val_1)
            s3 = val_1
            s4 = s3
        
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if hover == False:
                    if j.get_button(6):
                        print("L2 Pressed, now press R2")
                        if j.get_button(7):
                            print("Back Motor Control Enabled")
                            back_motors_enabled = True
                            side_motors_enabled = False

                    elif j.get_button(3):
                        print("L1 Pressed, now press R1")
                        if j.get_button(4):
                            print("Side Motors Control Enabled")
                            side_motors_enabled = True
                            back_motors_enabled = False
                        
                if j.get_button(3): #if the triangle button is pressed
                    if hover == False:
                        hover = True
                        back_motors_enabled = False
                        side_motors_enabled = False
                        print('Entering Hover Mode...')
                        m1.ChangeDutyCycle(0)
                        m2.ChangeDutyCycle(0)
                        m3.ChangeDutyCycle(51)
                        m4.ChangeDutyCycle(51) #hovers with motors 3+4 at 50% duty cycle

                        s1 = 0
                        s2 = 0
                        s3 = 51
                        s4 = 51
                    else:
                        hover = False
                        print('Disengaging...')

                      
        print('Motor Speeds: M1 = %s%%, M2 = %s%%, M3 = %s%%, M4 = %s%%' % (s1, s2, s3, s4))
            #logic check

        if s1 >= 100 and s2 >= 100:
            dir1 = 'is going forward'
        elif s1 > s2:
            dir1 = 'is turning right'
        elif s2 > s1:
            dir1 = 'is turning left'
        else:
            dir1 = 'is not moving in the lateral direction'

        if s3 > 51:
            dir2 = 'is going up'
        elif s3 == 51:
            dir2 = 'is keeping steady'
        else:
            dir2 = 'is going down'

        print('The balloon %s and %s.' % (dir1, dir2))

        time.sleep(1)

except KeyboardInterrupt:
    print("EXITING NOW")
    m1.stop()
    m2.stop()
    m3.stop()
    m4.stop()  
    GPIO.cleanup()
    j.quit()
