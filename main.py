import cv2

# Pretrained classes in the model
classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}


def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value


# Loading model
model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                      'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

image_name = "36"
image = cv2.imread("images/"+image_name+".jpg")
image_height, image_width, _ = image.shape

model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
output = model.forward()
#print(output[0,0,:,:].shape)

num_spots = 3
y_threshold = 0.65*image_height
spot_width = image_width/num_spots
is_vacant = [True]*num_spots

for detection in output[0, 0, :, :]:
    class_id, confidence, x1, y1, x2, y2 = detection[1:]
    
    if confidence > .4:
        if class_id == 3: #is car
            class_name=id_class_name(class_id,classNames)
            #print(str(str(class_id) + " " + str(confidence)  + " " + class_name))
            
            box_x1 = x1*image_width
            box_y1 = y1*image_height
            box_x2 = x2*image_width
            box_y2 = y2*image_height
            
            if (box_y2 > y_threshold): #is in parking space
                box_center = (box_x1 + box_x2)/2
                spot_idx = int(box_center/spot_width)
                cv2.circle(image, (int(box_center), int(box_y2)), 40, (23, 230, 210), -1)
                is_vacant[spot_idx] = False
                
            cv2.line(image, (0, int(y_threshold)), (image_width-1, int(y_threshold)), (0, 0, 255), 20)
            cv2.rectangle(image, (int(box_x1), int(box_y1)), (int(box_x2), int(box_y2)), (23, 230, 210), thickness=5)
            #cv2.putText(image,class_name,(int(box_x1), int(box_y1+.05*image_height)),cv2.FONT_HERSHEY_SIMPLEX,(.002*image_width),(0, 0, 255), 5)

print("image" + image_name + " is_vacant:")
print(is_vacant)

#image = cv2.resize(image, (400,360))
#cv2.imshow('image', image)
cv2.imwrite(image_name+"_result.jpg",image)

#cv2.waitKey(0)
#cv2.destroyAllWindows()
