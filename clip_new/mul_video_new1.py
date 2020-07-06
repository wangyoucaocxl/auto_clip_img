# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 18:22:23 2020

@author: 13373
"""

import cv2
import time
import os
import numpy as np
from threading import Thread


class Clip_samples:
    def __init__(self, my_disk_root, move_dir, move_size):
        #self.cap.set(3, 1280) #weight
        #self.cap.set(4, 720) #height
        self.fps = 10
        self.move_size = move_size
        self.myroot = my_disk_root
        self.move_dir = move_dir
        self.imdata = None
        self.move_step = 1000

    def read_im():
        pass
        #while 1:
            #tmp, self.imdata = self.cap.read()
        
    def add_eng_text(self, img):
        font = cv2.FONT_HERSHEY_SIMPLEX
        mystr1 = "ATTENTION: Exit->Esc; Clip all->A; Video all->B;"
        mystr2 = "Clip0-C; Clip1->D; Video0->E; Video1->F"
        #mystr = mystr.decode('utf8')
        cv2.putText(img, mystr1, (20,30), font, 0.7, (0,225,225), 2)
        cv2.putText(img, mystr2, (20,80), font, 0.7, (0,225,225), 2)
        
    def transform_date(self, timeStaplt):
        try:
            timeArray = time.localtime(int(timeStaplt))
            otherStyleTime = time.strftime("%Y%m%d%H%M%S", timeArray)
            return otherStyleTime
        except:
            return None 
    
    def save_video(self, cap, save_file):
        sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # fourcc = cv2.VideoWriter_fourcc(*'mpeg')
        myout = cv2.VideoWriter(save_file,fourcc,self.fps,sz)
        return myout

    #create file to save figure.
    def find_file(self, flag, video_id):
        newfile = time.strftime("%Y%m%d-%H", time.localtime(time.time())) + "-a" + str(len(flag)) 
        move_dir = self.move_dir + "{}".format(video_id)
        dir_path = os.path.join(move_dir, newfile)
        dir_path = os.path.abspath(dir_path)

        if not os.path.exists(dir_path):
            print("a")
            cmd ="mkdir -p {}".format(dir_path)
            os.system(cmd) #windows 创建递归文件夹会出错
            filename = dir_path
        else:
            filename = dir_path
                     
        #print(filenames)
        return filename

    def my_flag(self, myfile, mystr):
        with open(myfile, "a+") as f:
            f.write(mystr)
        with open(myfile, "r") as f:
            flag = f.readline()
        return flag
    
    def getdirsize(self, move_dir):
        size = 0
        for root, dirs, files in os.walk(move_dir):
            size += sum(os.path.getsize(os.path.join(root, name)) for name in files)
        return size/1024/1024  #M
    
    def do_move(self, video_id):
        print("="*50, 1, video_id)
        move_dir = self.move_dir + "{}".format(video_id)
        if not os.path.exists(self.myroot):
            print("my disk do not exist")
            self.my_flag("./log/log.log", "my disk do not exist {}\n".format(self.transform_date(time.time())))
        else:
            mysize = self.getdirsize(move_dir) 
            print(mysize)      
            if mysize > self.move_size:
                flag = self.my_flag("./log/flag_move.txt", "1") 
                to_file = self.myroot+"/move-{}".format(len(flag))
                cmd ="mkdir -p {}".format(to_file)
                print(cmd)
                os.system(cmd) #windows 创建递归文件夹会出错
                os.system("mv {} -t {}".format(move_dir, to_file))
                self.my_flag("./log/log.log", "move success {}\n".format(self.transform_date(time.time())))
        print("="*50, 2, video_id)

    def myclip(self):
        num = 0
        a = 0
        button = True
        write_ok = False
        #video_file = None
        lis = self.get_cam_num2()
        flag = self.my_flag("./log/flag_save.txt", "a")
        while True:
            num += 1
            ts = time.time()
            mms = int((ts - int(ts))*1000)
            tt = self.transform_date(ts)  
            #print(len(lis))
            if not lis:
                break
             
            for cam in lis:
                video_id = cam[0]
                cap = cam[1]
                #print(video_id, cap)
                if num % self.move_step == 5:
                    self.do_move(video_id)

                filename = self.find_file(flag, video_id)
                ret, img = cap.read()
                if not ret or img.shape[0] != 480:
                    cap.release()
                    cv2.destroyAllWindows()
                    return None

                cv2.namedWindow("Video{}".format(video_id), 0)
                cv2.resizeWindow("Video{}".format(video_id), 480, 360)
                cv2.moveWindow("Video{}".format(video_id), 600*video_id, 0)

                if button:
                    #setting clip time.
                    if num % 20 == 1:
                        cv2.imwrite(filename+'/P{}&{}&{}.jpg'.format(video_id, tt, mms), img)
   
                #self.add_eng_text(img_show)
                cv2.imshow("Video{}".format(video_id), img)          
            
            key = cv2.waitKey(50)
            if key == 27:
                cap.release()
                cv2.destroyAllWindows()
                break
    
    def mystart(self):
        t = Thread(target=self.myclip1)
        t.start()

    def get_cam_num1(self, set_num=10):
        for device in range(0, set_num):
            cap = cv2.VideoCapture(device)
            ret, img = cap.read()
            size = img.shape
            cap.release()
            cv2.destroyAllWindows()
            if size[0] == 480:
                count = count + 1
            else:
                break
        #print(count)
        return count

    def get_cam_num2(self):
        lis = []
        
        for i in os.listdir("/dev"):
            if i[:5] == 'video':
                a = [None, None]
                my_id = int(i[-1])
                print(my_id)
                a[0] = my_id
                a[1] = cv2.VideoCapture(my_id)
                lis.append(a)
        #print(lis)
        return lis

def main():
    my_disk_root = "/media/aidongone/MY_DISK"
    #my_disk_root = "/home/aidongone/my_data/move_data"
    move_dir = "/home/aidongone/my_data/sample/video" 
    move_size = 1024    # M
    
    obj = Clip_samples(my_disk_root, move_dir, move_size)
    obj.myclip()
        

if __name__ == "__main__":
    main()







