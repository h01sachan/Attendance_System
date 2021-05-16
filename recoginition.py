import cv2, time
from mtcnn.mtcnn import MTCNN

#MTCNN used as a detector
detector = MTCNN(scale_factor=0.65,min_face_size=30)

#this function accept the collection of faces and returns the coordinates of the face having largest area
def get_largest_face(faces):
    x,y,w,h=0,0,0,0
    for face in faces:
        x1,y1,w2,h2 = face["box"]
        if w*h < w2*h2:
            w,h=w2,h2
            x,y=x1,y1
    x2, y2 = x + w, y + h
    return x,y,x2,y2


#Function used to detect the faces and recoginize them
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
        # selecting largest of all faces only
        x1,y1,x2,y2 = get_largest_face(faces)
        #enclosing face in a rectangle
        img = cv2.rectangle(img,(x1*4,y1*4),(x2*4,y2*4),(0,255,0),2)
        cv2.imshow("face recognition",img)
        
    capture.release()
    cv2.destroyAllWindows()
