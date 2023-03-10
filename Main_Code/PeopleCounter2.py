##People Counter
import numpy as np
import cv2 as cv
import Person
import time
import winsound

try:
    log = open('log.csv',"w")
except:
    print( "Cannot open log file")

#Input and output counters
cnt_up = 0
cnt_down = 0
cnt_piggy = 0
cnt_tail = 0

#video source
#cap = cv.VideoCapture(0)
cap = cv.VideoCapture('TestVideo.mp4')
#camera = PiCamera()
##camera.resolution = (160,120)
##camera.framerate = 5
##rawCapture = PiRGBArray(camera, size=(160,120))
##time.sleep(0.1)

#video properties
##cap.set(3,160) #Width
##cap.set(4,120) #Height

#Print the capture properties to console
for i in range(19):
    print( i, cap.get(i))

h = 480
w = 640
frameArea = h*w
areaTH = frameArea/250
print( 'Area Threshold', areaTH)

#input/output lines
line_up = int(2*(h/5))
line_down   = int(3*(h/5))

up_limit =   int(1*(h/5))
down_limit = int(4*(h/5))

print("rosybrown y:", str(line_down))
print("lightblue y:", str(line_up))
line_down_color = (230, 216, 173)
line_up_color = (180, 180, 238)
pt1 =  [0, line_down];
pt2 =  [w, line_down];
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up];
pt4 =  [w, line_up];
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit];
pt6 =  [w, up_limit];
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit];
pt8 =  [w, down_limit];
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

#background subtractor
fgbg = cv.createBackgroundSubtractorMOG2(detectShadows = True)

#Structuring elements for morphological filters
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

#Variables
font = cv.FONT_HERSHEY_SIMPLEX
persons = []
max_p_age = 5
pid = 1
time_list = [] # records of line crossing timestamps
Piggybacking_check = None #stores the information of the last person crossed a line
while(cap.isOpened()):
##for image in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Read an image from the video source
    ret, frame = cap.read()
##    frame = image.array

    for i in persons:
        i.age_one() #age every person one frame
    #########################
    #   PRE-PROCESSING  #
    #########################
    
    #Apply background subtraction
    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    #Binarization to remove shadows (gray color)
    try:
        ret,imBin= cv.threshold(fgmask,200,255,cv.THRESH_BINARY)
        ret,imBin2 = cv.threshold(fgmask2,200,255,cv.THRESH_BINARY)
        #Opening (erode->dilate) to remove noise.
        mask = cv.morphologyEx(imBin, cv.MORPH_OPEN, kernelOp)
        mask2 = cv.morphologyEx(imBin2, cv.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) to join white regions.
        mask =  cv.morphologyEx(mask , cv.MORPH_CLOSE, kernelCl)
        mask2 = cv.morphologyEx(mask2, cv.MORPH_CLOSE, kernelCl)
    except:
        print('EOF')
        print( 'UP:',cnt_up)
        print('DOWN:',cnt_down)
        print('Tailgating: ', cnt_tail)
        print('Piggybacking: ', cnt_piggy)
        break
    #################
    #   CONTOURS  #
    #################
    
    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    contours0, hierarchy = cv.findContours(mask2,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours0:
        area = cv.contourArea(cnt)
        if area > areaTH:
            #################
            #   TRACKING    #
            #################
            
            #It remains to add conditions for multi-persons, exits and screen entrances.
            
            M = cv.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv.boundingRect(cnt)
            new = True
            if cy in range(up_limit,down_limit):
                for i in persons:
                    if abs(x-i.getX()) <= w and abs(y-i.getY()) <= h:
                        # the object is close to one that was detected before
                        new = False
                        i.updateCoords(cx,cy)   #updates coordinates on the object and resets age
                        if i.going_UP(line_down,line_up) == True:
                            cnt_up += 1
                            t = time.time() # time in seconds.millseconds
                            str_t = time.strftime('%c', time.localtime(t) ) # convert time to readable string value
                            print( "ID:",i.getId(),'crossed going up at',str_t)
                            log.write("ID: "+str(i.getId())+' crossed going up at ' + str_t + '\n')
                            
                            # Piggybacking recorder
                            if Piggybacking_check and Piggybacking_check[1] == 'up' and t - Piggybacking_check[2] < 0.5: # less then half a second or 500 millseconds
                                print(f"Piggybacking detected between person {i.getId()} and {Piggybacking_check[0]}\nBoth are going up on --> {str_t}")
                                log.write(f"Piggybacking detected between person {i.getId()} and {Piggybacking_check[0]}\nBoth are going up on --> {str_t}\n")
                                cnt_piggy +=1
                                #messagebox.showinfo("Piggybacking detected!!")
                                winsound.Beep(2500, 1000)
                            Piggybacking_check = [i.getId(), 'up', t]
                            
                            # Tailgating recorder
                            if time_list:
                                for r in time_list:
                                    if abs(t - r[2]) <= 3 and r[0] != i.getId() and r[1] == 'up':
                                        print(f'\tTailgating detected!! between {r[0]} and {i.getId()}')
                                        log.write(f'\tTailgating detected!! between {r[0]} and {i.getId()}\n')
                                        cnt_tail +=1
                            time_list.append([i.getId(), 'up', t])
                            
                        elif i.going_DOWN(line_down,line_up) == True:
                            cnt_down += 1
                            t = time.time()
                            str_t = time.strftime('%c', time.localtime(t) )
                            print( "ID:",i.getId(),'crossed going down at',str_t)
                            log.write("ID: " + str(i.getId()) + ' crossed going down at ' + str_t + '\n')
                            
                            # Piggybacking recorder
                            if Piggybacking_check and Piggybacking_check[1] == 'down' and t - Piggybacking_check[2] < 0.5: # less then half a second or 500 millseconds
                                print(f"Piggybacking detected between person {i.getId()} and {Piggybacking_check[0]}\nBoth are going down on --> {str_t}")
                                log.write(f"Piggybacking detected between person {i.getId()} and {Piggybacking_check[0]}\nBoth are going down on --> {str_t}\n")
                                cnt_piggy +=1
                                winsound.Beep(2500, 1000)
                            Piggybacking_check = [i.getId(),'down', t]
                            
                            # Tailgating recorder
                            if time_list:
                                for r in time_list:
                                    if  abs(t - r[2]) <= 3 and r[0] != i.getId() and r[1] == 'down':
                                        print(f'\tTailgating detected!! between {r[0]} and {i.getId()}')
                                        log.write(f'\tTailgating detected!! between {r[0]} and {i.getId()}')
                                        cnt_tail +=1
                            time_list.append([i.getId(), 'down', t])
                            
                        break
                    if i.getState() == '1':
                        if i.getDir() == 'down' and i.getY() > down_limit:
                            i.setDone()
                        elif i.getDir() == 'up' and i.getY() < up_limit:
                            i.setDone()
                    if i.timedOut():
                        #remove i from persons list
                        index = persons.index(i)
                        persons.pop(index)
                        del i     #free the memory of i
                if new == True:
                    p = Person.MyPerson(pid,cx,cy, max_p_age)
                    persons.append(p)
                    pid += 1     
            #################
            #   DRAWINGS    #
            #################
            cv.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)            
            #cv.drawContours(frame, cnt, -1, (0,255,0), 3)
            
    #END for cnt in contours0
            
    #########################
    # DRAW TRAJECTORIES  #
    #########################
    for i in persons:
##        if len(i.getTracks()) >= 2:
##            pts = np.array(i.getTracks(), np.int32)
##            pts = pts.reshape((-1,1,2))
##            frame = cv.polylines(frame,[pts],False,i.getRGB())
##        if i.getId() == 9:
##            print str(i.getX()), ',', str(i.getY())
        cv.putText(frame, str(i.getId()),(i.getX(),i.getY()),font,0.3,i.getRGB(),1,cv.LINE_AA)
        
        
    #################
    #   IMAGES   #
    #################
    str_up = 'UP: '+ str(cnt_up)
    str_down = 'DOWN: '+ str(cnt_down)
    frame = cv.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
    frame = cv.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
    frame = cv.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
    frame = cv.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
    #cv.putText(frame, str_up ,(10,40),font,0.5,(255,255,255),2,cv.LINE_AA)
    #cv.putText(frame, str_up ,(10,40),font,0.5,(0,0,255),1,cv.LINE_AA)
    #cv.putText(frame, str_down ,(10,90),font,0.5,(255,255,255),2,cv.LINE_AA)
    #cv.putText(frame, str_down ,(10,90),font,0.5,(255,0,0),1,cv.LINE_AA)
    
    # Display piggybacking and tailgating information on the video
    str_piggy = 'Piggybacking: '+ str(cnt_piggy)
    str_tail = 'Tailgating: '+str(cnt_tail)
    #cv.putText(frame, str_piggy ,(200,40),font,0.5,(255,255,255),2,cv.LINE_AA)
    #cv.putText(frame, str_piggy ,(200,40),font,0.5,(0,0,255),1,cv.LINE_AA)
    #cv.putText(frame, str_tail ,(200,90),font,0.5,(255,255,255),2,cv.LINE_AA)
    #cv.putText(frame, str_tail ,(200,90),font,0.5,(255,0,0),1,cv.LINE_AA)

    cv.imshow('Frame',frame)
    cv.imshow('Mask',mask)    
    

## rawCapture.truncate(0)
     #press ESC to exit
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
#END while(cap.isOpened())
    
#################
#   CLEANING   #
#################
log.flush()
log.close()
cap.release()
cv.destroyAllWindows()
