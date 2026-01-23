import cv2

def draw_detections(frame, detections):
    """
    detections: [{"xyxy":[x1,y1,x2,y2], "conf":0.8, "name":"car"}, ...]
    """
    out=frame.copy()
    
    # 클래스별 색상
    color_map={
        # 사람
        "person":(0,0,255),         # 0
        # 차량
        "car":(0,255,0),            # 2
        "motorcycle":(0,255,0),     # 3
        "bus":(0,255,0),            # 5
        "truck":(0,255,0),          # 7
        # 신호등
        "traffic light":(255,0,0)   # 9
    }
    
    for d in detections:
        # default값
        x1,y1,x2,y2=d["xyxy"]
        conf=d.get("conf",0.0)
        name=d.get("name","object")
        color=color_map.get(name, (0,0,0))  # name이 color_map에 있으면 그 색을 쓰고, 없으면 검은색
        
        # bbox
        cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
        
        # 라벨 문자열
        label=f"{name} {conf:.2f}"
        (tw, th), baseline=cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        # 라벨 위치(기본은 bbox 위, 안되면 bbox 안쪽)
        y_text=y1-(th+baseline+6)
        if y_text < 0:
            y_text = y1+2
        # 라벨 배경 + 텍스트
        # [변경점] 라벨 배경색을 bbox 색상(color)과 동일하도록 변경
        cv2.rectangle(out, (x1, y_text), (x1 + tw + 6, y_text + th + baseline + 4), color, -1)
        cv2.putText(out, label, (x1+3, y_text+th+baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    return out