import os
import cv2
import argparse
# 동영상 io 처리 모듈
from src.video.video_io import open_video, get_video_props, create_writer
from src.pipeline import process_frame

INPUT_DIR = "assets/demo_input/SeoulDrive_Test.mp4"
OUTPUT_DIR = "outputs/videos/output_demo.mp4"

def parse_args():
    # 인스턴스 생성
    parser=argparse.ArgumentParser(description="Autodrive Perception")
    
    # 입력받을 인자값
    parser.add_argument("--show", type=int, default=1)  # 1이면 화면에 표시
    parser.add_argument("--save", type=int, default=0)  # 1이면 결과 영상 저장
    
    return parser.parse_args()

def main():
    args=parse_args()
    
    # 없으면 경고 메시지 이후 종료
    if not os.path.exists(INPUT_DIR):
        print(f"!!! 입력 영상이 존재하지 않습니다: {INPUT_DIR} !!!")
        return
    
    # 동영상 열기
    vid=open_video(INPUT_DIR)
    
    # 프레임 폭, 높이, 프레임 수 얻기
    W,H,FPS=get_video_props(vid)

    """
    writer는 if args.save == 1: 안에서만 생성되는데,  
    아래에서 if writer is not None:을 쓰려면, writer라는 변수가 항상 존재해야 함
    만약 writer=None 없으면 args.save == 0일 때 writer가 아예 정의되지 않아서
    아래에서 writer를 참조하면 UnboundLocalError가 날 수 있음
    따라서 보통 생성될 수도, 아닐 수도 있는 객체는 None으로 초기화하고
    나중에 if writer is not None: 으로 분기함
    """
    # writer None으로 초기화
    writer=None  
    
    # --save 1
    if args.save==1:
        os.makedirs(os.path.dirname(OUTPUT_DIR), exist_ok=True)
        writer=create_writer(OUTPUT_DIR,W,H,FPS)

    print("========== 영상 처리 시작 ==========")
    print(f"해상도: {W}x{H}")
    print(f"FPS: {FPS:.2f}")

    while True:
        # 비디오의 한 프레임씩 읽기.
        # 제대로 프레임을 읽었는지 여부에 따라 is_read -> True/False
        is_read, frame=vid.read()
        if not is_read: break

        # 후에 코드 추가 예정
        frame=process_frame(frame)

        # --show 1
        if args.show==1:
            cv2.imshow("Autodrive Perception", frame)
            # 'q' 입력시 종료
            if cv2.waitKey(1) & 0xFF==ord("q"): break
            
        """
        프레임마다 저장할지 말지 결정
        while은 프레임 단위 반복, writer.write(frame)는 프레임 1장 저장
        그래서 여기서의 의미는 저장 모드라면, 이 프레임을 파일에 써라
        만약 이 조건이 없다면?
        --save 0일 때 writer는 None, writer.write(frame) 호출 -> 에러 발생
        그래서 프레임 처리 단계에서 보호가 필요함.
        """
        if writer is not None:
            writer.write(frame)
            
    # 동영상 객체 release
    vid.release()
    
    # Write후에 반드시 release를 해줘야함
    if writer is not None:
        writer.release()
        
    # 창 사용했으니 닫아주기
    cv2.destroyAllWindows()

    print("!!! 영상 처리 종료 !!!")

if __name__=="__main__":
    main()