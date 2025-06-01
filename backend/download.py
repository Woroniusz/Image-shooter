import os
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo
import cv2

save_dir = 'zoo/detectron2'
config_name = 'COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml'
cfg = get_cfg()
cfg.merge_from_file(os.path.join(save_dir, 'faster_rcnn_R_50_FPN_3x.yaml'))
cfg.MODEL.WEIGHTS = 'zoo/detectron2/model.pt'
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
cfg.MODEL.DEVICE = 'cpu'  # lub "", jeśli nie masz GPU

predictor = DefaultPredictor(cfg)

img = cv2.imread('/home/pawel/Documents/Biskupia.png')
outputs = predictor(img)
print(outputs['instances'].pred_classes, outputs['instances'].scores)
