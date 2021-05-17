import cv2, time , pickle, os
from mtcnn.mtcnn import MTCNN
from PIL import Image
from numpy import asarray, degrees
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
from matplotlib import pyplot
from scipy.spatial.distance import cosine

#MTCNN used as a detector
detector = MTCNN(scale_factor=0.65,min_face_size=30)

#vggface model for face embedding to recognise face
model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')


def dataset():
    """
    returns dict containing names and face embeddings of known people
    """
    with open('dataset_faces.dat', 'rb') as f:
        all_face_embeddings = pickle.load(f)
    return all_face_embeddings

def extract_face(filename):

    """
    returns the face after extraction and
    returned face is largest among all the extracted faces
    """
    pixels = pyplot.imread(filename)
    faces = detector.detect_faces(pixels)
    if len(faces)==0:
        return False
    x1,y1,x2,y2 = get_largest_face(faces)
    face = pixels[y1:y2, x1:x2]
    return face

def save_from_folder(path):

    """
    saved faces details from the folder
    """

    files = os.listdir(path)
    faces = [extract_face(path+'/'+file) for file in files]
    embeddings = get_embedding(faces)
    all_face_embeddings = {}
    for i,emb in enumerate(embeddings):
        all_face_embeddings[files[i][:-3]] = emb
        with open('dataset_faces.dat', 'wb') as f:
            pickle.dump(all_face_embeddings, f)

def save_embedding(emb,name):

    """
    function for saving 
    we used pickle to store it in a file
    """
    all_face_embeddings = dataset()
    all_face_embeddings[name] = emb
    with open('dataset_faces.dat', 'wb') as f:
        pickle.dump(all_face_embeddings, f)
    return 

def save_from_file(filename,name):

    face = extract_face(filename)
    embedding = get_embedding([face])[0]
    save_embedding(embedding,name) 

def save_face(emb,name):
    
    """
    function to save face
    """
    save_embedding(emb,name)

def identify(known_embedding):
    """
    Recognise face by comparing it with all faces present in dataset
    parameters:
        -> known_embedding : embedding of face to be recognised
    returns:
        True, str(name) : if person is identified
        False, "unknown" : if face is not identified
    """
    all_face_embeddings = dataset()
    names = list(all_face_embeddings.keys())
    embeddings = list(all_face_embeddings.values())
    for i,embedding in enumerate(embeddings):
        if is_match(embedding,known_embedding):
            return True,names[i]
    return False,"unknown"


def get_largest_face(faces):
    """
    accept the list of faces and returns the coordinates of the face having largest area
    parameters:
        -> faces : list of faces
    returns:
        x1,y1,x2,y2 : coordinates of largest face
    """
    x,y,w,h=0,0,0,0
    for face in faces:
        x1,y1,w2,h2 = face["box"]
        if w*h < w2*h2:
            w,h=w2,h2
            x,y=x1,y1
    x2, y2 = x + w, y + h
    return x,y,x2,y2


def get_embedding(faces):
    """
    returns embedding of faces using vggface model
    parametes:
        -> faces : list of faces whose embeddings are required
    returns:
        enbedding of faces
    """
    face_array = []
    for face in faces:
        image = Image.fromarray(face)
        image = image.resize((224, 224))
        face_array.append(asarray(image))
    samples = asarray(face_array, 'float32')
    samples = preprocess_input(samples, version=2)
    yhat = model.predict(samples)
    return yhat


def is_match(known_embedding, candidate_embedding, thresh=0.5):
    """
    compare the cosine distance b\w known face encoding and candidate face encoding 
    and tells whether the face are of same person or not
    parameters :  
        -> known_embedding (embedding of face of known person)
        -> candidate_embedding (embedding of face of unknown person)
        -> thersh (thershold for face matching)
    returns:
        True if same person
        False if different person
    """
    score = cosine(known_embedding, candidate_embedding)
    if score <= thresh:
        return True
    else:
        return False




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
        # reducing frame size to speed up face detection
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
        face = small_frame[y1:y2, x1:x2]
        emb = get_embedding([face])[0] #finding embedding of face
        found,id = identify(emb) # reconising face
        if found:
            img = cv2.putText(frame,f"Welcome {id}", (x1*4,y1*4), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,255,0),2, cv2.LINE_AA)
        else:
            img = cv2.putText(frame,"NOT ALLOWED", (x1*4,y1*4), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,255,0),2, cv2.LINE_AA)
        cv2.imshow("face recognition",img)
        
    capture.release()
    cv2.destroyAllWindows()

recognise()