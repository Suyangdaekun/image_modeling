import cv2
import mediapipe as mp
import numpy as np
from face_measurements import get_face_measurements
from report_generator import generate_measurement_report
from utils import visualize_landmarks

# MediaPipe 얼굴 메쉬 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7
)

def analyze_face(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"이미지 불러오기 실패: {image_path}")
    
    # MediaPipe를 사용하여 얼굴 랜드마크 추출
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
    
    # 얼굴 측정값 계산
    measurements = get_face_measurements(landmarks, img_width, img_height)
    
    # 보고서 생성
    return generate_measurement_report(measurements)