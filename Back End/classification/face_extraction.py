from facenet_pytorch import MTCNN, InceptionResnetV1  
from PIL import Image  
def face_extract(image_path, save_path):  
    mtcnn = MTCNN()  
    resnet = InceptionResnetV1(pretrained='vggface2').eval()  
    img = Image.open(image_path)  
    img_probs = mtcnn(img)  
    img_embedding = resnet(img_probs.unsqueeze(0))  
    resnet.classify = True  
    img_cropped = resnet(img_embedding.unsqueeze(0))  
    img_cropped.save(save_path)  
