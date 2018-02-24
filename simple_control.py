import pygame
import time
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(4, GPIO.OUT) #motor 1
GPIO.setup(17, GPIO.OUT) #motor 2
GPIO.setup(27, GPIO.OUT) #motor 3
GPIO.setup(22, GPIO.OUT) #motor 4

m1 = GPIO.PWM(4, 0)
m2 = GPIO.PWM(17, 0)
m3 = GPIO.PWM(27, 0)
m4 = GPIO.PWM(22, 0)

m1.start(0)
m2.start(0)
m3.start(0)
m4.start(0)

pygame.init()

j = pygame.joystick.Joystick(0)
j.init()

print(datetime.datetime.now())
print('Name: PS4 %s' % j.get_name())

try:
    while True:
        
        events = pygame.event.get()

        #print("Left Stick: {%s %s}" % (j.get_axis(0), j.get_axis(1)))
        #print("Right Stick: {%s %s}" % (j.get_axis(2), j.get_axis(3)))

        if j.get_axis(0) > 0.8 and j.get_axis(1) < 0.2:
            l = "East"
            val_1 = 1 #turning right
        elif j.get_axis(0) > 0.2 and j.get_axis(1) > 0.2:
            l = "Southeast"
            val_1 = 0 
        elif j.get_axis(0) < 0.2 and j.get_axis(1) > 0.8:
            l = "South"
            val_1 = 0 #can't go backwards
        elif j.get_axis(0) < -0.2 and j.get_axis(1) > 0.2:
            l = "Southwest"
            val_1 = 0
        elif j.get_axis(0) < -0.8 and j.get_axis(1) < 0.2:
            l = "West"
            val_1 = 0 #turning left
        elif j.get_axis(0) < -0.2 and j.get_axis(1) < -0.2:
            l = "Northwest"
            val_1 = 0.3
        elif j.get_axis(0) < 0.2 and j.get_axis(1) < -0.8:
            l = "North"
            val_1 = 1
        elif j.get_axis(0) > 0.2 and j.get_axis(1) > 0.2:
            l = "Northeast"
            val_1 = 1

        if j.get_axis(2) > 0.8 and j.get_axis(3) < 0.2:
            r = "East"
            val_2 = 0 #turning right
        elif j.get_axis(2) > 0.2 and j.get_axis(3) > 0.2:
            r = "Southeast"
            val_2 = 0
        elif j.get_axis(2) < 0.2 and j.get_axis(3) > 0.8:
            r = "South"
            val_2 = 0
        elif j.get_axis(2) < -0.2 and j.get_axis(3) > 0.2:
            r = "Southwest"
            val_2 = 0
        elif j.get_axis(2) < -0.8 and j.get_axis(3) < 0.2:
            r = "West"
            val_2 = 1 #turning left
        elif j.get_axis(2) < -0.2 and j.get_axis(3) < -0.2:
            r = "Northwest"
            val_2 = 1
        elif j.get_axis(2) < 0.2 and j.get_axis(3) < -0.8:
            r = "North"
            val_2 = 1
        elif j.get_axis(2) > 0.2 and j.get_axis(3) > 0.2:
            r = "Northeast"
            val_2 = 0.3

        print("{Left Pointer: %s} {Right Pointer: %s}" % (l, r))
        
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(6):
                    print("L2 Pressed, now press R2") #back motor 1
                    if j.get_button(7):
                    print("R2 Pressed, control the back motors") #back motor
                    m1.ChangeDutyCycle(100)
                    m2.ChangeDutyCycle(100)
                    m1.ChangeFrequency(l)
                    m2.ChangeFrequency(r)

                elif j.get_button(4):
                    print("L1 Pressed, now press R1")
                    if j.get_button(5):
                    print("R1 Pressed, control lift now")
                    m3.ChangeDutyCycle(100)
                    m4.ChangeDutyCycle(100)
                    m3.ChangeFrequency(l)
                    m4.ChangeFrequency(r)
                
                
            elif event.type == pygame.JOYBUTTONUP:
                print("Button Released")
                m1.ChangeDutyCycle(0)
                m2.ChangeDutyCycle(0)
                m3.ChangeDutyCycle(0)
                m4.ChangeDutyCycle(0)

            time.sleep(1)

except KeyboardInterrupt:
    print("EXITING NOW")
    m1.stop()
    m2.stop()
    m3.stop()
    m4.stop()  
    GPIO.cleanup()
    j.quit()
