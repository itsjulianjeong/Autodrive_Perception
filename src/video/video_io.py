import cv2

# 영상 경로가 존재해도 코덱 문제로 열리지 않는 경우가 가끔 있기 때문에 방어코드
def open_video(INPUT_DIR):
    # 동영상 열기
    vid=cv2.VideoCapture(INPUT_DIR)    
    if not vid.isOpened():
        # raise 에러 발생
        raise FileNotFoundError(f"영상 파일을 열 수 없습니다: {INPUT_DIR}")
    return vid

def get_video_props(vid):
    # cv2.CAP_PROP_FRAME_WIDTH: 프레임 폭
    W=int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))  
    # cv2.CAP_PROP_FRAME_HEIGHT: 프레임 높이
    H=int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # cv2.CAP_PROP_FPS: 초당 프레임의 수
    FPS=vid.get(cv2.CAP_PROP_FPS)
    
    # VideoWriter에 FPS=0이 들어가면 저장 영상이 비정상적으로 생성되거나 재생이 이상해질 수 있기에
    # 기본값을 하나를 가장 흔한 비디오 프레임인 30으로 지정
    if FPS==0: FPS=30.0  
    return W, H, FPS

# 동영상 저장 cv2.VideoWriter 클래스
def create_writer(OUTPUT_DIR,W,H,FPS):
    # Fourcc(FourCharacterCode) 지정 필요
    # 동영상 파일의 코덱, 압축 방식, 색상, 픽셀 포맷 등을 정의하는 정수 값
    fourcc=cv2.VideoWriter_fourcc(*"mp4v")
    writer=cv2.VideoWriter(OUTPUT_DIR,fourcc,FPS,(W,H))
    return writer

