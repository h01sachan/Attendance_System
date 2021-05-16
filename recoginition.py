import cv2, time
from mtcnn.mtcnn import MTCNN

detector = MTCNN(scale_factor=0.65,min_face_size=30)


def recognise():
    capture = cv2.VideoCapture(0)
    n=0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        img = frame
        if n%3:
            cv2.imshow("Face Recognition",img)
            continue
            n+=1
        n=0
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        s=time.time()
        faces = detector.detect_faces(small_frame)
        print(time.time()-s)
        if len(faces)==0:
            img = cv2.putText(frame,"no face", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,255,0),2, cv2.LINE_AA)
            cv2.imshow("face recognition",img)
            continue
        x1,y1,w2,h2 = faces["box"]
        img = cv2.rectangle(img,(x1*4,y1*4),(w2*4,h2*4),(0,255,0),2)
        cv2.imshow("face recognition",img)
    capture.release()
    cv2.destroyAllWindows()
