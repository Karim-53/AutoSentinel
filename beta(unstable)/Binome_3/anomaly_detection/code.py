import cv2
import numpy as np
from copy import deepcopy
import time
from sklearn.cluster import AffinityPropagation
import types
import os
import shutil

class Queue:
    def __init__(self):
        self.items = [] #for exmp self={ 'gentleman': 'malek' , 'the beautiful girl' : 'ahlem' , 'numbr' : 2 } ; self.items()=[(gentleman,malek),(the beautiful girm, ahlem ) , (num, 2)]

    def isEmpty(self):
        return self.items == [] # je pense que c'est claire , self.items() return a list , donc si la liste est vide isEmpty return true sinon elle return false 

    def enqueue(self, item):
        self.items.insert(0,item) # ajouter un element au debut de la liste 

    def dequeue(self):
        return self.items.pop() # suprimer le dernier element de la liste 

    def size(self):
        return len(self.items) # length
print('en attente de demarrer le drone')
while(os.stat("input.txt").st_size == 0):
    time.sleep(10)
input_file=open('input.txt', 'r')

while(input_file.read() != "start"):
    time.sleep(1)
input_file.close()
shutil.os.remove(r'C:\Users\malek\Desktop\INDP 2\pist\anomaly_detection\input.txt')
input_file=open('input.txt', 'w')
input_file.close()
print('en attente du nbr de stations N')
while(os.stat("input.txt").st_size == 0):
    time.sleep(5)

input_file=open('input.txt', 'r')
N=input_file.read()
input_file.close()
shutil.os.remove(r'C:\Users\malek\Desktop\INDP 2\pist\anomaly_detection\input.txt')
input_file=open('input.txt', 'w')
input_file.close()

print('en attente du video')

while(os.stat("input.txt").st_size == 0):
    time.sleep(5)

input_file=open('input.txt', 'r')
i_file=input_file.read()
input_file.close()

shutil.os.remove(r'C:\Users\malek\Desktop\INDP 2\pist\anomaly_detection\input.txt')

input_file=open('input.txt', 'w')
input_file.close()


sumq=[]
buf_back=[]
colq=[]
count=[]
initialisation=0
while(i_file != "end"):
    initialisation+=1
    i=int(i_file)
    VideoNumberInt=i
    VideoNumberString=i_file
    VideoName=VideoNumberString+'.mp4'
    print(VideoName)
    cap = cv2.VideoCapture(VideoName) # importer le video
    if( initialisation <= int(N)):
        count.append(0) #count[i-1]s the no of frames read till now
    nframe = 300 #no of frames needed to initialize the background
    cols = 160
    rows = 160
    flag = 0
    move = 0
    avg = np.zeros([160,160],dtype=np.uint8) # definir une image 'avg' dans tous ces pixels sont null , uint Unsigned integer (0 to 255)
    avg_temp = np.zeros([160,160],np.uint) # bon j'ai pas trouver la deffirence entre le uint8 et le uint , mais finalement sa sere à definir une plage d'entier 
    if( initialisation <= int(N)):
        sumq.append(np.zeros([160,160],np.uint)) # the same thing
    cur_back = np.zeros([160,160],dtype=np.uint8) # definir une image cur_back , dans tous ces pixels sont null
    if( initialisation <= int(N)):
        buf_back.append(np.zeros([160,160],dtype=np.uint8)) # definir une image buf_back , dans tous ces pixels sont null
    if( initialisation <= int(N)):
        colq.append(Queue()) # definir une pile des threads qui suit le loi de fifo 

    #to form clusters
    count_5=0
    arr=np.zeros(shape=(0, 2), dtype=np.uint8) # definir un tableau 'arr' de deux colones 
    cur_cent=last_cent=[0,0]
    def dist(cur_cent, last_cent):
        dis=(cur_cent[0]-last_cent[0])**2 + (cur_cent[1] - last_cent[1])**2 # calculer la somme de la variation au carré des deux pixel 
        return dis
    cluster_centres_q = np.zeros(shape=(0,2),dtype=np.int64) # on vas travaillé sur un cluster de deux pixels
    ret, pure_img = cap.read() # on extraire le 'cout'éme frame du video qui sera enregistrer dans la variable pure_img , ret , est un variable booleanretourner par la fonction read  
    while(cap.isOpened() and ret==True): # tanque la video qu'on souhaite traiter est en boucle 
            #time.sleep(0.1)
            count[i-1] = count[i-1] + 1 # on va commencer à traiter les frame , du coup il faux incrémenter le count[i-1] à chaque fois qu'on est entrain de traiter une frame ( count[i-1] represente le nbr des frame traiter )
            #print(count[i-1])
            #print(nframe)
            img = cv2.resize(pure_img,(160,160)) # grase à resize on arrive à resizer notre image sans perdre la forme generale de l'image , c'est dans le sense ou on est pas entrais deretrancher les pixels d'une facon stupide bon maby il vas engondrer une certaine distortion l'orsqu'on zoom , euuh mais bon :p
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convertir l'image en une image noire et blanch 
    
            colq[i-1].enqueue(gray) # aywah ahiya :D , tana na7chiw il image ' des années 60 :p ' fil pila mte3na 
            if(count[i-1] < nframe):
                    #avg[:]=0 #no need as avg is initialized to be zero matrix
                    sumq[i-1] = sumq[i-1] + gray # il est entrain de superposer les differentes frame 

            else: # une fois nodkhol lil else , ca veux dire que j'ai construit mon propre background 
                    temp = colq[i-1].dequeue() # yibda yijbid fil les frames ta3 el background 
                    sumq[i-1] = sumq[i-1] + gray - temp # yzid ce qui a changé entre le frame du background wil frame ali 9e3id yikhdim fih
                    avg_temp = sumq[i-1]/nframe # bon mafhimtich 3leh ya9sim el 7a9 :D , ama mahiyech importante , puisque nnframe deja cst , nitsawir ,il est entrai de normaliser haja kima haka

            high_value_indices = avg_temp>255 # 7asilou puisque ahna mil se3a on ajout de la deffirence , fama des pixel , ynajmo yfoutou 255 ce qui n'est pas logique 
            avg_temp[high_value_indices] = 255 # kif kif 
            avg=avg_temp 
            avg=avg.astype(np.uint8) #7asilou lahna badal el type bech twali image

#       print(gray)
#       print(sumq)
#       print(avg)
#
#       print(avg.shape)
        #print(avg_show.shape)


            cur_back = avg 
            if(flag == 0):
                    #buf_back[:] = 0 #no need as buf_back is initialized to be zero matrix
                    flag = 10 # pour eliminer le cas ou nframe=1 
            if(flag == 10 and count[i-1] >= nframe):
                    buf_back[i-1] = cur_back # doub maya3mil hekom el nframe , yimchi ya3ti lil buf_back el deffirence mabin el back w awil frame 5dheha ba3d el back 
                    flag = 20 
    
            sub = cv2.absdiff(cur_back,buf_back[i-1]) # voila lahna nhoto la difference entre le background wil frame ali 9e3din nitraitiw fiha 

            img_show = cv2.resize(img,(400,400)) 
        #img_show = img_show.astype(int)
        #print(img_show.shape)
        #print(img_show)
        #time.sleep(1)
            cv2.imshow("img",img_show) # affichage de l'image originale 

            gray_show = cv2.resize(gray,(400,400)) 
        #gray_show = gray_show.astype(int)
            cv2.imshow("gray",gray_show)

        #print(cur_back)
            cur_back_show = cv2.resize(cur_back,(400,400))
        #cur_back_show = cur_back_show.astype(int)
        #print(cur_back_show)
            cv2.imshow("cur_back_show",cur_back_show)

            buf_back_show = cv2.resize(buf_back[i-1],(400,400))
        #buf_back_show = buf_back_show.astype(int)
            cv2.imshow("buf_back_show",buf_back_show)

            sub = cv2.resize(sub,(400,400))
        #sub=sub.astype(int)
            cv2.imshow("Abandoned Objects",sub) # affichage de l'ivolution de la distortion du back

            ret_s,sub_t = cv2.threshold(sub,50,255,0) # codage : pour tous pixels entre 50 et 255 en luis attribut un 0 sinon 1
            mask = np.zeros(gray.shape,np.uint8)

            louka, contours, hier = cv2.findContours(sub_t,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #im2, contours, hier = cv2.findContours(sub_t,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            count_5 += 1
            malek=0;
            for cnt in contours: # count[i-1]ouRS IS A LISTE OF object and in each element we find a liste of element which represente the different value of pixel who forme the contours of this object
                    if 300<cv2.contourArea(cnt)<5000: # si le piremetre entre 200 et 5000
                            #cv2.drawContours(sub,[cnt],0,(0,255,0),2) 
                            cv2.drawContours(mask,[cnt],0,255,-1) 
                            M = cv2.moments(cnt)
                            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00']) # localiser le centroid de l'objet ( centre de masse ) 
                            file_output = open('output.txt', 'w')
                            file_output.write('video num : ')
                            file_output.write(str(i))
                            file_output.write(' ====> un anomaly est detecter dans la position suivante : x=')
                            file_output.write(str(cx))
                            file_output.write(',  y=')
                            file_output.write(str(cy))
                            file_output.close()
                            cv2.circle(sub,(cx,cy),10,255,-1) # 
                            if(count_5<=5):
                                    arr = np.append(arr, [[cx,cy]], axis=0) # localiser la position de l'objet dans l'image 


            print(arr)
            print(count_5)

            if(count_5==5):
                    count_5 = 0
                    print (len(arr))
                    if (len(arr) == 0): # il n y a pas d'objet 
                            pass
                    else:
                            affin = AffinityPropagation()
                            affin.fit_predict(arr)
                            centroids = affin.cluster_centers_
                            labels = affin.labels_
                            max_label_index = labels.argmax()
                            biggest_clust_ind = labels[max_label_index]
                            print(labels)
                            print(centroids)
                      #  print("len_labels",len(labels),"biggest cluster's index", biggest_clust_ind, "len_centroids", len(centroids))
                            print("+++++++++++++++++++++++++++++++++++++",type(biggest_clust_ind),"++++++++++++++++++++++++++++++++++++++++++")
                            if( type(biggest_clust_ind)!=np.ndarray):
                                    biggest_clust_cent = centroids[biggest_clust_ind]
                                    cx = np.uint8(biggest_clust_cent[0])
                                    cy = np.uint8(biggest_clust_cent[1])
                                    cv2.rectangle(sub,(cx-15,cy-15),(cx+15,cy+15),(255,255,255),1)
                                    cv2.rectangle(img,(cx-7,cy-7),(cx+7,cy+7),(0,255,0),2)
                                    cv2.drawContours(sub, contours, -1, (0,255,0), 3)
                                #finallly reinitializing the np_array arr
                                    last_cent = cur_cent
                                    cur_cent = [cx,cy]
                                    cluster_centres_q = np.append(cluster_centres_q, [cur_cent], axis=0)
                                    print("++++++++++++++++++++++++++++++++", len(cluster_centres_q),"++++++++++++++++++++++++++++++++++++")
                            else:
                                    pass
                            arr=np.zeros(shape=(0, 2), dtype=np.uint8)
            dista=dist(cur_cent, last_cent)
       # print("distance b/w centroid of last & current frame",dista)

         #if(0 < dista < 25 ):
            if(cur_cent==last_cent and last_cent!=[0,0]):
                    cv2.rectangle(sub,(cx-15,cy-15),(cx+15,cy+15),(255,255,255),1)
                    cv2.rectangle(img,(cx-7,cy-7),(cx+7,cy+7),(0,255,0),2)
                    print("---------------------------------------------------------------------------")

            if(len(cluster_centres_q)>=1):
                    temp_a = deepcopy(cluster_centres_q[0])
                    temp_b = cluster_centres_q[-1]
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    if(1==1):
                            print ("warning, abandoned object detected")
                            print("maleek")
                            #font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            text_x = cx-10 #position of text
                            text_y = cy-20 #position of text
                            cv2.putText(sub,"Warning", (text_x,text_y),font,1, (255,255,255)) #Draw the text
                    cluster_centres_q = cluster_centres_q[1:]


            avg_show = cv2.resize(avg,(400,400))
#           cv2.imshow("avg",avg_show)
            cv2.imshow("Abandoned Objects",sub)
            if(move==0):
                    move=1
                    cv2.moveWindow("gray", 400,20)
                    cv2.moveWindow("img", 0,20)
                    cv2.moveWindow("cur_back_show", 800,20)
                    cv2.moveWindow("buf_back_show", 400,420)
                    cv2.moveWindow("Abandoned Objects", 20,220)
                    cv2.moveWindow("avg", 800,420)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            ret, pure_img = cap.read() # on extraire le 'cout'éme frame du video qui sera enregistrer dans la variable pure_img , ret , est un variable booleanretourner par la fonction read
                

    cap.release()
    cv2.destroyAllWindows()
    print('j ai terminé ce video et je suis dans l attente du prochain video')
    while(os.stat("input.txt").st_size == 0):
        time.sleep(1)
    input_file=open('input.txt', 'r')
    i_file=input_file.read()
    input_file.close()

    shutil.os.remove(r'C:\Users\malek\Desktop\INDP 2\pist\anomaly_detection\input.txt')

    input_file=open('input.txt', 'w')
    input_file.close()
