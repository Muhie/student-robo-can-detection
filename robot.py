import cv2
import numpy as np
from sr.robot3 import *
print("hello world")
import time



class Collybot(Robot):
    def __init__(self):
        super().__init__() #call robot contructor
        print("hello this is a test")
        self._auto_start = False
        self.fb = self.motor_boards['SR0WE7'] #Front motorboard
        self.bb = self.motor_boards['SR0JH18'] #Back motorboard
        # self.servo=self.servo_board.servos[0]
        self.fov = 60
        self.fl = 0
        self.fr = 0
        self.bl = 0
        self.br = 0
        self.motor_sf = 2
        self.master_power = 0
        self.classNames = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat', 'backpack', 'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table', 'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush']
        path = str(self.usbkey)
        self.path1 = path
        self.weightsPath = path+"/frozen_inference_graph.pb"
        self.configPath =path+"/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        print(self.weightsPath,self.configPath)
        self.net = cv2.dnn_DetectionModel(self.weightsPath,self.configPath)
        self.net.setInputSize(200,200)
        self.net.setInputScale(1.0/ 127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)
        self.runonce = 0
        self.stage = 0

    def power_H0(self):
        self.power_board.outputs[OUT_H0].is_enabled = True

    def depower_H0(self):
        self.power_board.outputs[OUT_H0].is_enabled = False

    def power_H1(self):
        self.power_board.outputs[OUT_H1].is_enabled = True

    def depower_H1(self):
        self.power_board.outputs[OUT_H1].is_enabled = False

    def power_L0(self):
        self.power_board.outputs[OUT_L0].is_enabled = True

    def depower_L0(self):
        self.power_board.outputs[OUT_L0].is_enabled = False

    def power_L1(self):
        self.power_board.outputs[OUT_L1].is_enabled = True

    def depower_L1(self):
        self.power_board.outputs[OUT_L1].is_enabled = False

    def power_L2(self):
        self.power_board.outputs[OUT_L2].is_enabled = True

    def depower_L2(self):
        self.power_board.outputs[OUT_L2].is_enabled = False

    def power_L3(self):
        self.power_board.outputs[OUT_L3].is_enabled = True

    def depower_L3(self):
        self.power_board.outputs[OUT_L3].is_enabled = False
    def ultra_Slow(self):
        self.master_power = 0.15
        print("changing to a ultra slow speeds")
        self.scale_conversion()
    
    def slow(self):
        self.master_power = 0.25
        print('Change to slow speed')
        self.scale_conversion()

    def medium(self):
        self.master_power = 0.35
        print('Change to medium speed')
        self.scale_conversion()

    def fast(self):
        self.master_power = 0.5
        print('Change to fast speed')
        self.scale_conversion()

    def scale_conversion(self):
        self.front_master_power = self.master_power/self.motor_sf
        self.back_master_power = self.master_power

    def move(self):
        self.power_H0()
        self.power_H1()
        self.fb.motors[1].power=self.fl
        self.fb.motors[0].power=self.fr
        self.bb.motors[0].power=self.bl
        self.bb.motors[1].power=self.br

    def forwards(self):
        print("moving forwards")
        self.fl = 1.05*self.front_master_power
        self.fr = self.front_master_power
        self.bl = 1.05*self.back_master_power
        self.br = self.back_master_power
        self.move()

    def backwards(self):
        print("moving backwards")
        self.fl = -self.front_master_power
        self.fr = -self.front_master_power
        self.bl = -self.back_master_power
        self.br = -self.back_master_power
        self.move()

    def left(self):
        print("moving left")
        self.fl = -2.6*self.front_master_power
        self.fr = 2.6*self.front_master_power
        self.bl = 1.5*self.back_master_power
        self.br = -1.5*self.back_master_power
        self.move()

    def right(self):
        print("moving right")
        self.fl = 2.6*self.front_master_power
        self.fr = -2.6*self.front_master_power
        self.bl = -1.5*self.back_master_power
        self.br = 1.5*self.back_master_power
        self.move()

    def stop(self):
        print("stopping")
        self.fl = 0
        self.fr = 0
        self.bl = 0
        self.br = 0
        self.move()

    def braking(self):
        print('Braking')
        self.fl = BRAKE
        self.fr = BRAKE
        self.bl = BRAKE
        self.br = BRAKE

    def movement_test(self):
        print("starting movement test")
        for i in range (0, 3):
            if i == 0:
                self.slow()
            elif i == 1:
                self.medium()
            else:
                self.fast()
            self.forwards()
            time.sleep(2)
            self.stop()
            time.sleep(1)

            self.backwards()
            time.sleep(2)
            self.stop()
            time.sleep(1)

            self.left()
            time.sleep(2)
            self.stop()
            time.sleep(1)

            self.right()
            time.sleep(2)
            self.stop()
            time.sleep(1)

    def forwards_test(self):
        self.forwards()
        time.sleep(2)
        self.stop()
        time.sleep(1)

    def marker(self):
        self.markers = self.camera.see()

    def marker_ids(self):
        self.markers = self.camera.see_ids()
    def stage2(self):
        self.rotateclockwise()
        time.sleep(4)
        self.canSeeker()
    
    def marker_test(self):
        print("starting marker test")
        while True:
            markers = self.camera.see()
            print("I can see", len(markers), "markers:")
            if markers:self.chase_the_markers_advanced()
            self.forwards_test()
            for m in markers:
                print(" - Marker #{0} is {1} metres away".format(m.id, m.distance))

    def chase_the_marker(self):
        print('Playing chase the marker')
        while True:
            markers = self.camera.see()
            if markers:
                while markers[0].distance > 1000:
                    self.stop()
                    self.slow()
                    self.forwards()
                    markers = self.camera.see()
                    if not markers:
                        self.stop()
                        break
                self.stop()

    def find_the_angle(self):
        for i in range(0, 50):
            markers = self.camera.see()
            if markers:
                print(markers[0].spherical)

    def chase_the_markers_advanced(self):
        moving = ''
        while self.stage == self.runonce:
            markers = self.camera.see()
            if markers:
                for marker in markers:
                    if marker.id == self.homemarker1 or marker.id == self.homemarker2:
                        while marker.distance >= 500:
                            if marker.distance <= 700:
                                self.stage += 1
                                self.start()
                                break
                            else:
                                print((marker.spherical))
                                print((marker.spherical)[0])
                                print((marker.spherical)[1])
                                if ((marker.spherical)[1]) < 0.1 and ((marker.spherical)[1]) > -0.1:
                                    if moving == 'forwards':
                                        self.stop()
                                        self.medium()
                                        self.forwards()
                                        time.sleep(0.2)
                                    else:
                                        self.stop()
                                        time.sleep(0.2)
                                        self.medium()
                                        self.forwards()
                                        time.sleep(0.2)
                                        moving = 'forwards'
                                    marker = self.camera.see()
                                    if not marker:
                                        self.stop()
                                        time.sleep(0.2)
                                        break

                                elif ((marker.spherical)[1]) > 0.1:
                                    if moving == 'left':
                                        self.stop()
                                        self.ultra_Slow()
                                        self.left()
                                        time.sleep(0.2)
                                    else:
                                        self.stop()
                                        time.sleep(0.2)
                                        self.ultra_Slow()
                                        self.left()
                                        time.sleep(0.2)
                                        moving = 'left'
                                    marker = self.camera.see()
                                    if not marker:
                                        self.stop()
                                        time.sleep(0.2)
                                        break

                                else:
                                    if moving == 'right':
                                        self.stop()
                                        self.ultra_Slow()
                                        self.right()
                                        time.sleep(0.2)
                                    else:
                                        self.stop()
                                        time.sleep(0.2)
                                        self.ultra_Slow()
                                        self.right()
                                        time.sleep(0.2)
                                        moving = 'right'
                                    markers = self.camera.see()
                                    if not markers:
                                        self.stop()
                                        time.sleep(0.2)
                                        break
                                    else:
                                        for marker in markers:
                                            if marker.id != self.homemarker1 or marker.id != self.homemarker2:
                                                break
                                        

                    self.stop()
                    time.sleep(0.2)

    def angle_testing(self):
        while True:
            markers = self.camera.see()
            if markers:
                if ((markers[0].spherical)[1]) > 0:
                    self.stop()
                    self.medium()
                    self.forwards()
                    time.sleep(0.25)
                    self.stop()
                if ((markers[0].spherical)[1]) < 0:
                    self.stop()
                    self.medium()
                    self.backwards()
                    time.sleep(0.25)
                    self.stop()

    def emergency(self):
        #emergency shutdown, logs power status of battery
        self.power_board.outputs.power_off()
        print(self.power_board.battery_sensor.current)
        print(self.power_board.battery_sensor.voltage)

    def locator(self):
        self.marker_ids()
        if len(self.markers) > 0:
            self.marker()
            if len(self.markers) > 0:
                print('To locate')

    def open_arm(self):
        self.depower_L1()
        self.power_L0()
        time.sleep(0.05)
        #self.depower_L0()

    def close_arm(self):
        self.depower_L0()
        self.power_L1()
        self.power_L0()
        time.sleep(0.05)
        self.depower_L0()
        self.depower_L1()
    
    # def servo_test(self):
    #     self.medium()
    #     self.servo.position=1
    #     time.sleep(5)
    #     self.servo.position=-1
    #     time.sleep(5)
    #     #self.spin_servo_clockwise()

    # def spin_servo_clockwise(self,rotations):
    #     for i in range(rotations):
    #         self.servo.position=1
    #         time.sleep(1)

    def rotateclockwise(self):
        self.slow()
        self.fl = -2*self.front_master_power
        self.fr = 2*self.front_master_power
        self.bl = -2*self.back_master_power
        self.br = 2*self.back_master_power
        self.move()

    def rotateanticlockwise(self):
        self.fl = 2*self.front_master_power
        self.fr = -2*self.front_master_power
        self.bl = 2*self.back_master_power
        self.br = -2*self.back_master_power
        self.move()

    def returntosender(self):
        self.rotateanticlockwise()
        #self.stage2()

    def can_Regonition(self):
        print("opening file!")
        img = cv2.imread(self.path1+"/can_Detection.png")
        classIds,confs,bbox = self.net.detect(img,confThreshold=0.25)
        if len(classIds) >= 1:
            for classId,confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
                can = self.classNames[classId-1]
                self.confs1 = confs
                self.img1 = img
                self.box1 = box
                boxy = np.array_str(box)
                coords = boxy.replace(' ', ',')
                formatted = coords.replace('[','')
                fullyformatted = formatted.replace(']','')
                self.boxposition = box
                if can == "bowl":
                    print("I found a can")
                    self.where_CanY()
                elif can == "cup":
                    print("I found a can")
                    print(fullyformatted)
                    self.where_CanY()
                else:
                    print("can not found")
                    self.braking()
                    self.stop()
                    pass

    def where_CanX(self):
        print(self.boxposition)
        if self.boxposition[0] >= 700:
            print("going left")
            self.left()
            time.sleep(0.4)
            self.stop()
        elif self.boxposition[0] >= 176 and self.boxposition[0] <= 699:
            print("in the centre")
            self.forwards()
            time.sleep(1.4)
            self.stop()
        elif self.boxposition[0] <= 175:
            print("going right!")
            self.right()
            time.sleep(0.25)
            self.stop()
        else:
            self.forwards()
            time.sleep(0.8)

    def where_CanY(self):
        if self.boxposition[3] < 200 and self.boxposition[3] > 0:
            print("we are very far away")
            self.slow()
            self.where_CanX()
            #self.DrawLines()
        elif self.boxposition[3] < 700 and self.boxposition[3] > 200: 
            print("getting closer")
            self.slow()
            self.where_CanX()
        elif self.boxposition[3] >= 700 and self.boxposition < 800:
            print("object detected is extremely close ")
            #self.braking()
            #self.stop()
        else:
            print("object is too far away ignoring")

    def canSeeker(self):
        #self.open_arm()
        for i in range(1,20):
            print("pass")
            print(i)
            try:
                self.camera.save(self.usbkey / "can_Detection.png")
                print("trying to find cans")
                self.can_Regonition()
            except:
                print("EXCEPT IS RUNING")
        #self.close_arm()
        self.stop()
        self.slow()
        self.returntosender()
        time.sleep(2)
        self.stop()
        self.chase_the_markers_advanced()

    def start(self):
        #self.emergency()
        self.depower_L0()
        self.depower_L1()
        if self.zone == 0:
            self.homemarker1 = 0
            self.homemarker2 = 27
        elif self.zone == 1:
            self.homemarker1 = 6
            self.homemarker2 = 7
        elif self.zone == 2:
            self.homemarker1 = 13
            self.homemarker2 = 14
        elif self.zone == 3:
            self.homemarker1 = 21
            self.homemarker2 = 20
        if self.stage == 0:
            #self.close_arm()
            time.sleep(1)
            self.open_arm()
            self.runonce = 0
            print("stage 1 initiated")
            time.sleep(1)
            self.scale_conversion()
            self.power_board.piezo.buzz(1, 1047)
            self.slow()
            self.forwards()
            time.sleep(8)
            self.stop()
            self.canSeeker()
        elif self.stage == 1:
            self.runonce = 1
            print("stage two initated")
            self.slow()
            self.rotateanticlockwise()
            time.sleep(2.5)
            self.slow()
            self.forwards()
            time.sleep(3.5)
            self.power_board.piezo.buzz(1, 1047)
            self.scale_conversion()
            self.canSeeker()
        elif self.stage == 2:
            self.scale_conversion()
            self.slow()
            self.rotateanticlockwise()
            time.sleep(2.5)
            self.forwards()
            time.sleep(3.5)

    def round_1(self):
        self.medium()
        self.forwards()
        time.sleep(3)
        self.stop()
        time.sleep(2)
        self.backwards()
        time.sleep(3)
        self.stop()
        time.sleep(5)
        
        
def main():
    jeff = Collybot()
    jeff.start()
if __name__ == '__main__':
    main()
