import cv2
import mediapipe as mp
import time
class Hand_Tracking():
    def __init__(self, mode=False, maxh=2, comp=1, dconf=0.5, tconf=0.5):
        self.mode=mode
        self.maxh=maxh
        self.comp=comp
        self.dconf=dconf
        self.tconf=tconf
        self.mph=mp.solutions.hands
        self.h=self.mph.Hands(self.mode, self.maxh, self.comp, self.dconf, self.tconf)
        self.mpd=mp.solutions.drawing_utils
    def Hand_Finding(self, img, flag=True):
        iRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res=self.h.process(iRGB)
        if self.res.multi_hand_landmarks:
            for lms in self.res.multi_hand_landmarks:
                if flag:
                    self.mpd.draw_landmarks(img, lms, self.mph.HAND_CONNECTIONS)
        return img
    def Pos_Finding(self, img, hno=0):
        landlist=[]
        if self.res.multi_hand_landmarks:
            hand=self.res.multi_hand_landmarks[hno]
            for id, lm in enumerate(hand.landmark):
                he, wi, ch=img.shape
                cx=int(lm.x*wi)
                cy=int(lm.y*he)
                landlist.append([id, cx, cy])
        return landlist
def main():
    timep=0
    timec=0
    c=cv2.VideoCapture(0)
    d=Hand_Tracking()
    while True:
        s, img=c.read()
        img=d.Hand_Finding(img)
        landlist=d.Pos_Finding(img)
        if len(landlist)!=0:
            print(landlist[4])
        timec=time.time()
        fps=1/(timec-timep)
        timep=timec
        cv2.putText(img, str(int(fps)), (10, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 255), 2)
        cv2.imshow("Gesture Recognition", img)
        cv2.waitKey(1)
if __name__=="__main__":
    main()
