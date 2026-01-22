# Changelog

## v0.1 - MVP (Video Perception Baseline)
- mp4 입력 -> 프레임 단위 처리 -> mp4 출력 파이프라인 구성
- pretrained YOLO 기반 객체 탐지(bbox) 데모 구현
- 탐지 결과 프레임 오버레이 시각화
- CLI 기반 실행 옵션(--show / --save)
- 기본 프로젝트 구조 및 모듈 분리(pipeline / perception / utils)

> 목표: 실제 주행 영상에서 **End-to-End로 안정적으로 동작하는 인식 파이프라인 확보**

---

## v0.2 - Detection Stabilization
- bbox 표시 로직 안정화(좌표 왜곡 이슈 수정)
- confidence threshold 조정 및 테스트
- 불필요한 오탐 제거를 위한 필터링 전략 검토
- 실험 기록(experiments/) 정리 및 비교 문서화

---

## v0.3 - Traffic Context Understanding (Planned)
- 신호등 탐지 결과 기반 색상 판단(HSV)
- ROI 기반 중요도 반영(주행 차선 중심 영역)
- 간단한 시간축 안정화(Temporal smoothing)

---

## v0.4 - Lane & Decision Layer (Planned)
- OpenCV 기반 차선 인식(ROI + Edge + Hough)
- 차선 중심 오프셋 계산
- STOP / CAUTION / GO 상태 규칙 정의(제어 없이 상태만 표시)

---

## v0.5 - Tracking & Risk Estimation (Planned)
- SORT 기반 객체 ID 유지
- 앞차 접근 위험도(상대 bbox 면적 변화율) 계산
- 프레임 단위 이벤트 캡처 옵션 추가

---

## v1.0 - Release Target
- 다양한 도로/시간대 영상에서 동작 검증
- 파라미터 튜닝 및 FPS 안정화
- README/실험 결과 정리 및 데모 영상 정리
