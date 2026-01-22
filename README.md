# Autodrive Perception Module (Video-based)

전방 주행 영상(mp4)을 입력으로 받아 **차선 인식 + 객체 탐지(차량/보행자/신호등) + 신호등 색상 판단**을 수행하고,
결과를 프레임 오버레이 형태로 출력 영상(mp4)으로 저장하는 **주행 환경 인식(Perception) 모듈 데모**입니다.
실시간으로 화면에 보여주고 + 옵션으로 저장까지 진행합니다.  

CLI 형태로 만들어서 영상만 바꿔서 계속해서 테스트를 진행하는 모듈의 형태를 띱니다.  
```bash
python main.py --input "assets/demo_input/test1.mp4" --show 1 --save 1
python main.py --input "assets/demo_input/test2.mp4" --show 1 --save 0
```

---

## 목표
- mp4 입력 -> 프레임 단위 인식 결과를 오버레이하여 mp4로 저장
- 객체 탐지: 차량/보행자/신호등 중심
- 차선 인식: 중앙 오프셋(차선 중심 유지 지표) 출력
- 신호등: 탐지 bbox 내부 색상 분석으로 RED/YELLOW/GREEN 상태 판단
- 간단 의사결정: STOP / CAUTION / GO 상태 출력(실제 제어는 하지 않음)

---

## 데모 결과
- 입력: `assets/demo_input/input.mp4`
- 출력: `outputs/videos/output_demo.mp4`

예시 스크린샷: `assets/screenshots/`

---

## 설계 포인트
### 1) Detection은 pretrained 모델을 baseline으로 설정
- 재학습 비용 없이 baseline을 확보하는 방향을 목표로 하며,
- 실제 주행 영상에서 발생하는 **오탐/미탐/깜빡임**을 줄이는 안정화 로직에 초점을 둠.

### 2) 신뢰도(Confidence) 및 ROI 기반 필터링
- 클래스별 confidence threshold를 분리하여 오탐 줄이기.
- 화면 하단 중심 영역(ROI)에 들어오는 객체에 더 높은 중요도 부여.

### 3) 시간축(Temporal) 안정화
- 프레임 단위 결과의 깜빡임을 줄이기 위해 이동평균 / 다수결 / N-프레임 연속 조건 등을 적용.

---

## 프로젝트 구조
- `main.py` : 실행 엔트리
- `src/perception/`: detector, lane, traffic light
- `src/decision/`: STOP/CAUTION/GO rules
- `outputs/`: 결과 영상 저장
- `experiments/`: threshold/ROI/smoothing 실험 기록

---

## 설치
```bash
conda create -n autodriveENV python=3.10 -y
conda activate autodriveENV
pip install -r requirements.txt
```

---

## 실행
```bash
python main.py --input "assets/demo_input/input.mp4" --show 1 --save 1 --output "outputs/videos/output_demo.mp4"
```

---

## 실험 기록
- experiments/roi_comparison.md
- experiments/confidence_threshold_test.md
- experiments/traffic_light_smoothing.md

---

## 한계점 및 향후 개선

- 단안 카메라 기반이므로 실제 거리(m) 산출 대신 bbox 기반 상대 위험도만 제공합니다.  
- 바닥 방향 화살표/도로 마킹 인식은 추후 fine-tuning 또는 segmentation 기반으로 확장 가능합니다.  
- Tracking(SORT) 적용을 통해 객체 ID 유지 및 접근 판단 안정화를 개선할 수 있습니다.  

---




<!--
### 프로젝트 구조
---
```bash
Autodrive_Perception/
├── main.py                         # 엔트리포인트: mp4 입력 → output 저장
├── .gitignore
├── requirements.txt                
├── README.md
├── CHANGELOG.md
├── assets/
│   ├── demo_input/                 # (샘플) 입력 영상
│   └── screenshots/                # 결과 캡처 이미지
├── outputs/
│   ├── videos/                     # output_demo.mp4 저장
│   └── frames/                     # 이벤트 프레임 캡처
├── experiments/
│   ├── template_experiment.md
│   ├── roi_comparison.md
│   ├── confidence_threshold_test.md
│   └── traffic_light_smoothing.md
├── src/
│   ├── __init__.py
│   ├── config.py                   # 임계값/ROI/fps 등 설정값
│   ├── pipeline.py                 # 전체 파이프라인 orchestration
│   ├── video/                      # 입출력
│   │   ├── __init__.py
│   │   └── video_io.py             # VideoCapture/Writer, fps handling
│   ├── perception/                 # 인식
│   │   ├── __init__.py
│   │   ├── detector.py             # YOLO 래퍼(추론 결과 표준화)
│   │   ├── lane.py                 # 차선 검출 + 중앙오프셋
│   │   └── traffic_light.py        # 신호등 색상 판단 + smoothing
│   ├── decision/                   # 판단
│   │   ├── __init__.py
│   │   └── rules.py                # STOP/CAUTION/GO 상태 로직
│   └── utils/                      # 공통 유틸
│       ├── __init__.py
│       ├── draw.py                 # bbox/차선/텍스트 오버레이
│       └── timing.py               # FPS 측정, frame skip 등
└── tests/
    └── smoke_test.py               # 간단 실행 테스트
```
-->