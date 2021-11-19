import boto3
import io
import csv
from PIL import Image, ImageDraw
#連結AWS帳號金鑰
with open('C:/Users/q1217/Desktop/AI大數據課程/AWSIoT_accessKeys.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        ACCESS_KEY = line[0]
        SECRET_KEY = line[1]
        
#上傳圖片至AWS進行偵測
##讀取檔案 先將圖像檔轉為二進位格式
photo='guest11.jpg'                
with open(photo, 'rb') as imgfile:
    imgbytes = imgfile.read()
    
##就可以登入帳戶連結至aws rekognition
client=boto3.client('rekognition', region_name='us-east-1', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

#偵測臉部數據
rekresp = client.detect_faces(Image={'Bytes': imgbytes}, Attributes=['ALL'])

#顯示分析結果
def detect_suspicious_people(photo):
    print('Detected  people in image '+photo)
    people_count = len(rekresp['FaceDetails'])
    return people_count


FILL_PINK = 'pink'
FILL_BLUE = 'blue'
FILL_RED = 'red'
FILL_YELLOW = 'yellow'
line_width = 3
    
#讀取圖片檔案
image = Image.open(open(photo, 'rb'))
stream = io.BytesIO()
image.save(stream, format=image.format)
imgWidth, imgHeight = image.size
draw = ImageDraw.Draw(image)
    
suspicious_people = rekresp['FaceDetails']
#對應每個人的ID就可以叫出中方方塊中的資訊，進而顯示出紅框
for person_id in range(len(suspicious_people)):
            suspicious_person = rekresp['FaceDetails'][person_id]
            Type = suspicious_person['Emotions'][0]['Type']   #rekognition會把信任值最高的表情排第一位
            
            box = suspicious_person['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']
            points = ((left, top), (left+width, top), (left+width, top+height), (left, top+height), (left, top))
            #對表情SAD做辨識(黃色框框)
            if str(Type) == 'SAD' :                            
                
                draw.line(points, fill=FILL_YELLOW, width=line_width)
            
            #對表情ANGRY做辨識(紅色框框)
            elif str(Type) == 'ANGRY':                         
                 
                 draw.line(points, fill=FILL_RED, width=line_width)
            
            #對表情FEAR做辨識(藍色框框)
            elif str(Type) == 'FEAR':                         
                 
                 draw.line(points, fill=FILL_BLUE, width=line_width)
            
            #對表情DISGUSTED做辨識(粉紅色框框)
            elif str(Type) == 'DISGUSTED':                         
                 
                 draw.line(points, fill=FILL_PINK, width=line_width)
            
                        
image.show()
image.save('123456.jpg') #畫好方塊的檔案
 

person_count = detect_suspicious_people(photo)
print('Persons detected:' + str(person_count))