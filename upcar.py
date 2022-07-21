import lcd
import sensor, image, time
import math
from pyb import Servo
from pyb import UART
import time
from pyb import Pin, Timer

tim = Timer(4, freq=50)

black=(2, 15, -40, 44, -28, 26)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(10)

lcd.init()
k_err=0
j=0#角度
i=1
x=[0,0,0]#色块的横坐标
y=[0,0,0]#色块的纵坐标
ROI=[(0,0,40,3  0),(40,0,40,30),(80,0,40,30),(120,0,40,30)]
Kp=-3
uart3 = UART(3, 115200)
Trun_Angle=0

flag=True
p = Pin('P7') # P7 has TIM4, CH1
tim = Timer(4, freq=50)
ch = tim.channel(1, Timer.PWM, pin=p)
while(True):

    img = sensor.snapshot()
    blob_s0=img.find_blobs([black],roi=ROI[0],area_threshold=300)
    blob_s1=img.find_blobs([black],roi=ROI[1],area_threshold=300)
    blob_s2=img.find_blobs([black],roi=ROI[2],area_threshold=300)
    blob_s3=img.find_blobs([black],roi=ROI[3],area_threshold=300)
    if blob_s0 and blob_s1 and blob_s2 and blob_s3:
        uart3.write('1')
        #flag=False
    if flag==True:
     if blobs:
         for blob in blobs:
            img.draw_cross(blob.cx(),blob.cy(),size=5,color=(255,0,0))
            img.draw_rectangle((blob.x(), blob.y(), blob.w(), blob.h()), color=(255,0,0))
            if i==1:
                if len(blobs)==1:
                    x[1]=0
                    x[2]=0
                    y[1]=0
                    y[2]=0
                    i=0
                x[0]=blob.cx()
                y[0]=blob.cy()
            elif i==2:
                if len(blobs)==2:
                    i=0
                x[1]=blob.cx()
                y[1]=blob.cy()
            elif i==3:
              if len(blobs)==3:
                i=0
              x[2]=blob.cx()
              y[2]=blob.cy()
            else:
                i=0
            i+=1
            #print(i)
         #print(x[0],y[0],x[1],y[1],x[2],x[2])
         dif=abs(y[0]-y[1])
         if abs(x[0]-x[1])!=0:
            slope=float(dif/(x[1]-x[0]))#斜率
            #print(slope)
         #else:
            #j=90
         #if j!=90:
         j = int(math.degrees(math.atan(slope)))
         #print(j)
         if j>0:
            k_err = 90-j
         else:
            k_err = -(90+j)
         th_err=(x[0]+x[1]+x[2])/3-img.width()/2
         output=th_err+k_err-20
         if output>60:
            output=60
         elif output<-80:
            output=-80
         print(int(th_err))
         ch.pulse_width_percent(7)
    lcd.display(img)
