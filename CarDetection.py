import cv2

rootpath = '/home/pi/ECE568/'
num_spots = 3
threshold = 0.65
dot_thickness = 40
line_thickness = 20
box_thickness = 5

# Pretrained classes in the model
classNames = {3: 'car'}

def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

# Loading model
model = cv2.dnn.readNetFromTensorflow(rootpath + 'models/frozen_inference_graph.pb',
                                      rootpath + 'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

def detect(image_name):
    image = cv2.imread(rootpath + "images/"+image_name)
    image_height, image_width, _ = image.shape

    model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
    output = model.forward()

    y_threshold = threshold*image_height
    spot_width = image_width/num_spots
    is_vacant = [True]*num_spots


    # Start detecting
    for detection in output[0, 0, :, :]:
        class_id, confidence, x1, y1, x2, y2 = detection[1:]
    
        if confidence > .4:
            if class_id == 3: #is car
            
                box_x1 = x1*image_width
                box_y1 = y1*image_height
                box_x2 = x2*image_width
                box_y2 = y2*image_height
            
                if (box_y2 > y_threshold): #is in parking space
                    box_center = (box_x1 + box_x2)/2
                    spot_idx = int(box_center/spot_width)
                    cv2.circle(image, (int(box_center), int(box_y2)), dot_thickness, (23, 230, 210), -1)
                    is_vacant[spot_idx] = False
                
                cv2.line(image, (0, int(y_threshold)), (image_width-1, int(y_threshold)), (0, 0, 255), line_thickness)
                cv2.rectangle(image, (int(box_x1), int(box_y1)), (int(box_x2), int(box_y2)), (23, 230, 210), box_thickness)

    print(image_name + " is_vacant:")
    print(is_vacant)

    cv2.imwrite(rootpath + "/static/result_" + image_name, image)
   


    vacant = False
    for v in is_vacant:
        if v:
            vacant = True
            break
    #return True if at least one spot is vacant
    return vacant
