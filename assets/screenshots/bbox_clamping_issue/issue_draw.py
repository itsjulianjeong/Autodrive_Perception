import cv2

def draw_detections(frame, detections):
    """
    detections: [{"xyxy":[x1,y1,x2,y2], "conf":0.8, "name":"car"}, ...]
    """
    out=frame.copy()
    H,W=out.shape[:2]
    
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
        x1,y1,x2,y2=d["xyxy"]
        conf=d.get("conf",0.0)
        name=d.get("name","obj")
        
        # 좌표 클램핑
        # x1/y1이 음수거나, x2/y2가 W(width)/H(height) 넘어가는 케이스가 있어서
        # draw가 깨지거나 박스가 이상해 보일 수 있어서 프레임 밖으로 나가는 걸 방지시킴
        x1=max(0, min(W-1, x1))
        y1=max(0, min(H-1, x1))
        x2=max(0, min(W-1, x2))
        y2=max(0, min(H-1, y2))
        
        color=color_map.get(name, (0,255,0))
        
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
        cv2.rectangle(out, (x1, y_text), (x1 + tw + 6, y_text + th + baseline + 4), (0, 255, 0), -1)
        cv2.putText(out, label, (x1+3, y_text+th+baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    return out