import cv2

import mediapipe as mp


mp_hands = mp.solutions.hands

hands = mp_hands.Hands()

mp_draw = mp.solutions.drawing_utils

#Accesing the webcam

cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4


#Creating an infinite while loop which will only end if space bar is pressed

while True:

    #Reading the first frame of the image

    ret,img = cap.read()

    #Fliping the image to an opposite direction because image formed will be a mirror image

    img = cv2.flip(img, 1)

    #Setting the shape of the image

    h,w,c = img.shape
    results = hands.process(img)


    if results.multi_hand_landmarks:

        for hand_landmark in results.multi_hand_landmarks:

            #Accessing the landmarks by their position

            lm_list=[]
            for id ,lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)


            #Checking whether the fingers are fold
                
            for tip in finger_tips :
                x,y = lm_list[tip].x  ,lm_list[tip].y
                cv2.circle(img,(x,y),15,(255,0,0))

                if lm_list[tip].x < lm_list[tip-3] :
                    cv2.circle(img,(x,y),15,(255,0,0))
                    fold_status = True
                else :
                    fold_status = False


            #Displaying whether the gesture is like or dislike
                    
            if all(fold_status) :

                #For Like

                if lm_list[thumb_tip].y < lm_list[thumb_tip-1] < lm_list[thumb_tip-2] :

                    print("Like")

                    cv2.putText(img,"Like",(20,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

                #for Dislike
                    
                if lm_list[thumb_tip].y > lm_list[thumb_tip-1] > lm_list[thumb_tip-2] :

                    print("Dislike")

                    cv2.putText(img,"Dislike",(20,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

            #Displaying the final result of above code
                    
            mp_draw.draw_landmarks(img, hand_landmark,
                                   
            mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0,0,255),2,2),

            mp_draw.DrawingSpec((0,255,0),4,2))
    

    cv2.imshow("hand tracking", img)

    #Creating a key so that when space bar will pressed while loop will end

    key = cv2.waitKey(0)

    if key == 32 :
        break

cv2.destroyAllWindows()