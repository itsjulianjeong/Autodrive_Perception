from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="yolov8n.pt", conf=0.35, iou=0.45):
        self.model=YOLO(model_path)
        self.conf=conf
        self.iou=iou

        # COCO class id  
        # https://docs.ultralytics.com/datasets/detect/coco/#applications
        # 매핑으로 진행해도 되고 또는 self.model.names에 id -> name 매핑이 이미 들어있음
        # 매핑ver: (self.class_map={"person":0,"car":2,"motorcycle":3,"bus":5,"truck":7,"traffic light":9})
        self.interest_classes={
            "person",       # 0
            "car",          # 2
            "motorcycle",   # 3
            "bus",          # 5
            "truck",        # 7
            "traffic light" # 9
        }
    
    def sanitize_and_filter_box(self, x1, y1, x2, y2, W, H):
        # 좌표 정리(혹시라도 순서 뒤집힌 경우 방지)
        x1,x2=sorted([int(x1), int(x2)])
        y1,y2=sorted([int(y1), int(y2)])

        # 프레임 밖으로 나가면 클램핑
        x1=max(0, min(W-1, x1))
        y1=max(0, min(H-1, y1))
        x2=max(0, min(W-1, x2))
        y2=max(0, min(H-1, y2))

        w=x2-x1
        h=y2-y1
        if w<12 or h<12:
            return None

        area=w*h
        area_ratio=area/(W*H)

        # 너무 큰 박스(도로/건물 오탐) 제거
        if area_ratio>0.35:
            return None

        # 너무 긴/납작한 박스(도로/가로로 긴 구조물 오탐) 제거
        aspect=w/(h+1e-6)
        if aspect>6.0:
            return None

        return [x1,y1,x2,y2]
    
    def detect(self, frame, target_names=None):  
        """
        return:
            detections(list[dict]):
            [{"xyxy":[x1,y1,x2,y2], "conf":0.8, "cls":2, "name":"car"}, ...]
        """
        # YOLO 추론
        results=self.model.predict(
            source=frame,       # source: 입력 이미지(frame)
            conf=self.conf,     # conf(confidence threshold) 신뢰도 임계치
            iou=self.iou,       # iou(NMS IoU threshold)
            verbose=False,      # 로그 출력 여부 
        )

        # 여러 이미지를 넣을 수 있어서 결과는 list 형태,
        # 지금은 프레임 1개만 넣으므로 results[0]만 사용
        r=results[0]
        
        # 탐지된 박스가 없으면 빈 리스트 반환
        if r.boxes is None or len(r.boxes)==0:  
            return []
        
        """
        딥러닝 텐서에서 numpy 배열로 바꾸는 과정
        result.boxes.xyxy: 모델 내부 텐서로 좌표를 말하며
        .cpu(): GPU에 있으면 CPU로 가져오기
        .numpy(): numpy 배열로 변환해서 for문에 사용하기 좋도록
        """
        H,W=frame.shape[:2]
        boxes_xyxy=r.boxes.xyxy.cpu().numpy()  # 박스 좌표 (x1,y1,x2,y2 좌표)
        conf_scores=r.boxes.conf.cpu().numpy()  # confidence 점수
        class_ids=r.boxes.cls.cpu().numpy().astype(int)  # class id
        
        # dictionary 형태
        detections=[]
        
        for box_xyxy, conf_score, class_id in zip(boxes_xyxy, conf_scores, class_ids):
            name=self.model.names.get(int(class_id), str(class_id))

            # target 필터
            # target_names 지정되었다면 해당 클래스만 남기기
            if target_names is not None and name not in target_names:
                continue
            
            x1,y1,x2,y2=box_xyxy
            cleaned_box_xyxy=self.sanitize_and_filter_box(x1,y1,x2,y2,W,H)
            if cleaned_box_xyxy is None:
                continue
            
            detections.append({
                "xyxy": cleaned_box_xyxy,
                "conf": float(conf_score),
                "cls": int(class_id),
                "name": name
            })

        return detections