import hydra
import torch
import cv2
from random import randint
import numpy as np
from ultralytics import YOLO
from ultralytics.utils import DEFAULT_CFG, ROOT
from ultralytics.utils.checks import check_imgsz

from SORT import *

tracker = None

def init_tracker():
    global tracker
    
    sort_max_age = 5 
    sort_min_hits = 2
    sort_iou_thresh = 0.2
    tracker = Sort(max_age=sort_max_age,min_hits=sort_min_hits,iou_threshold=sort_iou_thresh)

rand_color_list = []
    

def random_color_list():
    global rand_color_list
    rand_color_list = []
    for i in range(0,5005):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        rand_color = (r, g, b)
        rand_color_list.append(rand_color)
    #......................................
        

def draw_boxes(img, bbox, identities=None, categories=None, names=None,offset=(0, 0)):
    
    for i, box in enumerate(bbox):
        
        x1, y1, x2, y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]
        
        cat = int(categories[i]) if categories is not None else 0
        id = int(identities[i]) if identities is not None else 0
        
        data = (int((box[0]+box[2])/2),(int((box[1]+box[3])/2)))
        label = names[cat]
        
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,20), 2)
        
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), (255,144,30), -1)
        cv2.putText(img, label, (x1, y1 - 5),cv2.FONT_HERSHEY_SIMPLEX, 
                    0.6, [255, 255, 255], 1)
        
        cv2.circle(img, data, 3, (255,255,255),-1)   #centroid of box
        
    return img

def predict(model_path="yolov8n.pt", source=0, imgsz=640):
    init_tracker()
    random_color_list()

    model = YOLO(model_path)

    results = model.predict(source=source, imgsz=imgsz, stream=True)

    for result in results:
        frame = result.orig_img.copy()
        detections = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()

        dets_to_sort = np.empty((0, 6))

        for det, score, cls in zip(detections, scores, classes):
            x1, y1, x2, y2 = det
            dets_to_sort = np.vstack((dets_to_sort, np.array([x1, y1, x2, y2, score, cls])))

        # Update tracker
        tracked_dets = tracker.update(dets_to_sort)
        tracks = tracker.getTrackers()

        for track in tracks:
            for i in range(len(track.centroidarr) - 1):
                pt1 = (int(track.centroidarr[i][0]), int(track.centroidarr[i][1]))
                pt2 = (int(track.centroidarr[i+1][0]), int(track.centroidarr[i+1][1]))
                color = rand_color_list[track.id % len(rand_color_list)]  # wrap around if id too big
                cv2.line(frame, pt1, pt2, color, thickness=3)

        if len(tracked_dets) > 0:
            bbox_xyxy = tracked_dets[:, :4]
            identities = tracked_dets[:, 8]
            categories = tracked_dets[:, 4]
            draw_boxes(frame, bbox_xyxy, identities, categories, model.names)

        cv2.imshow("Tracked Output", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    predict()