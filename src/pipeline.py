from src.perception.detector import YoloDetector
from src.utils.draw import draw_detections

def get_detector():
    if not hasattr(get_detector, "model"):
        """
        conf: confidence threshold, 신뢰도 임계치
              값이 높을수록 탐지 "신뢰도"가 높은 객체만 남음 -> 낮으면 많이 잡고(오탐↑), 높으면 덜 잡음(미탐↑)
        iou:  값이 낮을수록 더 공격적으로 제거 -> iou가 낮으면 조금만 겹쳐도 중복으로 판단해서 제거
              NMS(중복 박스 제거) 기준. 일반적으로 0.4~0.6 사이를 많이 사용
        """
        get_detector.model=YoloDetector(model_path="yolov8n.pt", conf=0.35, iou=0.45)
    return get_detector.model

def process_frame(frame, targets=None):
    """
    한 프레임을 받아서 인식 결과를 오버레이한 프레임을 반환.

    v0.1 단계 목표:
    - pretrained YOLO로 객체 탐지 수행
    - 탐지 결과(bbox, class, confidence)를 frame 위에 시각화

    Args:
        frame: OpenCV로 읽은 "BGR" 이미지 (numpy array)
        targets: 탐지 후 남길 클래스 이름 리스트 ("car", "person", "traffic light")

    Returns:
        out: bbox/라벨이 그려진 프레임 (numpy array)
    """
    # detector 가져오기
    detector=get_detector()
    
    # 객체 탐지 수행
    # detections는 dict 리스트 형태:
    # [{"xyxy":[x1,y1,x2,y2], "conf":0.82, "cls":2, "name":"car"}, ...]
    detections=detector.detect(frame, target_names=targets)
    
    # 탐지 결과를 프레임 위에 그리기
    out=draw_detections(frame, detections)
    
    return out