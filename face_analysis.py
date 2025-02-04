import cv2
import mediapipe as mp
import numpy as np
import warnings
from absl import logging

# 경고 메시지 필터링
warnings.filterwarnings("ignore", category=UserWarning)
logging.set_verbosity(logging.ERROR)  # absl 로그 레벨 설정

# MediaPipe 얼굴 메쉬 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7
)

def get_face_measurements(landmarks, img_width, img_height):
    # 눈 관련 랜드마크 인덱스 (MediaPipe Face Mesh 기준)
    LEFT_EYE = [33, 133]  # 왼쪽 눈 외각, 내각
    RIGHT_EYE = [362, 263]  # 오른쪽 눈 외각, 내각
    EYE_VERTICAL = [159, 145, 386, 374]  # 각 눈의 상하 지점 (왼쪽 위/아래, 오른쪽 위/아래)
    
    # 코 측정 지점
    NOSE_LENGTH = [168, 4]  # 코 시작점(미간) ~ 코 끝점
    NOSE_WIDTH = [358, 129]  # 코 양쪽 가장자리 (코의 가로 폭)
    
    # 입 측정 지점 (수정된 부분)
    MOUTH_WIDTH = [78, 308]  # 입 양쪽 끝
    MOUTH_HEIGHT = [13, 18]  # 입 상하 지점 (위/아래 중앙)

    measurements = {}
    
    # 왼쪽 눈 측정
    left_eye_width = np.linalg.norm(landmarks[LEFT_EYE[0]] - landmarks[LEFT_EYE[1]])
    left_eye_height = (np.linalg.norm(landmarks[EYE_VERTICAL[0]] - landmarks[EYE_VERTICAL[1]]) +
                       np.linalg.norm(landmarks[EYE_VERTICAL[2]] - landmarks[EYE_VERTICAL[3]])) / 2
    
    # 오른쪽 눈 측정
    right_eye_width = np.linalg.norm(landmarks[RIGHT_EYE[0]] - landmarks[RIGHT_EYE[1]])
    right_eye_height = (np.linalg.norm(landmarks[EYE_VERTICAL[2]] - landmarks[EYE_VERTICAL[3]]) +
                        np.linalg.norm(landmarks[EYE_VERTICAL[0]] - landmarks[EYE_VERTICAL[1]])) / 2
    
    measurements['eyes'] = {
        'left_width_px': int(left_eye_width),
        'left_height_px': int(left_eye_height),
        'right_width_px': int(right_eye_width),
        'right_height_px': int(right_eye_height),
        'width_diff_px': abs(int(left_eye_width) - int(right_eye_width)),
        'height_diff_px': abs(int(left_eye_height) - int(right_eye_height))
    }

    # 코 측정
    nose_length = np.linalg.norm(landmarks[NOSE_LENGTH[0]] - landmarks[NOSE_LENGTH[1]])  # 코 길이 (세로)
    nose_width = np.linalg.norm(landmarks[NOSE_WIDTH[0]] - landmarks[NOSE_WIDTH[1]])  # 코 너비 (가로)
    measurements['nose'] = {
        'length_px': int(nose_length),
        'width_px': int(nose_width)
    }

    # 입 측정 (수정된 부분)
    mouth_width = np.linalg.norm(landmarks[MOUTH_WIDTH[0]] - landmarks[MOUTH_WIDTH[1]])
    mouth_height = np.linalg.norm(landmarks[MOUTH_HEIGHT[0]] - landmarks[MOUTH_HEIGHT[1]])

    # 입 높이가 0인 경우 디버깅 정보 출력
    if mouth_height == 0:
        print("입 높이가 0으로 계산됨. 랜드마크 좌표 확인 필요:")
        print(f"MOUTH_HEIGHT[0]: {landmarks[MOUTH_HEIGHT[0]]}")
        print(f"MOUTH_HEIGHT[1]: {landmarks[MOUTH_HEIGHT[1]]}")

    measurements['mouth'] = {
        'width_px': int(mouth_width),
        'height_px': int(mouth_height)
    }
    return measurements

def generate_measurement_report(measurements):
    report = []
    # 눈 분석
    eyes = measurements['eyes']
    report.append(f"눈 분석:")
    report.append(f"- 왼쪽 눈: {eyes['left_width_px']}px (가로) × {eyes['left_height_px']}px (세로)")
    report.append(f"- 오른쪽 눈: {eyes['right_width_px']}px (가로) × {eyes['right_height_px']}px (세로)")
    if eyes['width_diff_px'] > 5 or eyes['height_diff_px'] > 3:
        report.append(f"- 양쪽 눈 크기 차이: 가로 {eyes['width_diff_px']}px, 세로 {eyes['height_diff_px']}px (짝짝이 눈 특성)")
    
    # 코 분석
    nose = measurements['nose']
    report.append(f"\n코 분석:")
    report.append(f"- 코 길이 (세로): {nose['length_px']}px")
    report.append(f"- 코 너비 (가로): {nose['width_px']}px")
    
    # 입 분석
    mouth = measurements['mouth']
    report.append(f"\n입 분석:")
    report.append(f"- 입 크기: {mouth['width_px']}px (가로) × {mouth['height_px']}px (세로)")
    if mouth['height_px'] != 0:
        ratio = mouth['width_px'] / mouth['height_px']
        report.append(f"- 입 가로/세로 비율: {ratio:.1f}:1")
    else:
        report.append("- 입 가로/세로 비율: 계산 불가 (높이가 0)")
    return "\n".join(report)

def visualize_landmarks(image_path, landmarks, img_width, img_height):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"이미지 불러오기 실패: {image_path}")
    
    # 특정 랜드마크 강조 (입 관련 랜드마크)
    mouth_indices = [13, 18]  # 입의 상하 지점
    for idx in mouth_indices:
        x, y = int(landmarks[idx][0]), int(landmarks[idx][1])
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # 빨간색 점으로 표시
        cv2.putText(img, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 모든 랜드마크 표시
    for idx, landmark in enumerate(landmarks):
        x, y = int(landmark[0]), int(landmark[1])
        cv2.circle(img, (x, y), 2, (0, 255, 0), -1)  # 초록색 점으로 표시
    
    cv2.imshow("Landmarks", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def analyze_face(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"이미지 불러오기 실패: {image_path}")
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return "얼굴 검출 실패"
    img_height, img_width, _ = img.shape
    face_landmarks = results.multi_face_landmarks[0]
    # 랜드마크 좌표 변환 (픽셀 단위)
    landmarks = np.array([[lm.x * img_width, lm.y * img_height, lm.z * img_width]
                          for lm in face_landmarks.landmark])
    
    # 랜드마크 시각화
    visualize_landmarks(image_path, landmarks, img_width, img_height)
    
    # 얼굴 분석
    measurements = get_face_measurements(landmarks, img_width, img_height)
    return generate_measurement_report(measurements)

if __name__ == "__main__":
    image_path = "D:/Coding/AI4FW/image_modeling/changseop.png"  # 실제 이미지 경로로 변경 필요
    try:
        result = analyze_face(image_path)
        print(result)
    except Exception as e:
        print(f"오류 발생: {str(e)}")