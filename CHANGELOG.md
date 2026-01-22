# Changelog

## v0.1 - MVP (End-to-End)
- mp4 입력/출력 파이프라인 구성
- 객체 탐지(bbox) + 오버레이 출력
- 차선 인식(OpenCV) + 중앙 오프셋 표시
- 신호등 bbox 기반 색상 판단(HSV) 기본 구현
- 결과 영상(output mp4) 저장

## v0.2 - Stabilization
- confidence threshold 정책 정리(클래스별 분리)
- ROI 기반 중요도 반영(하단 중앙 위험 구역)
- Temporal smoothing(이동평균/다수결) 적용으로 깜빡임 감소

## v0.3 - Decision Layer
- STOP / CAUTION / GO 상태 규칙 정의
- 이벤트 발생 시 프레임 캡처 저장 옵션 추가

## v0.4 - Tracking (Planned)
- SORT 기반 객체 ID 유지
- 앞차 접근 점수(면적 변화율 기반) 안정화

## v1.0 - Release Target (Planned)
- 다양한 주행 영상에서 동작 검증 및 예외 처리 강화
- 성능 최적화(FPS 개선) 및 파라미터 튜닝