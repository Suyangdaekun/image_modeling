import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 얼굴 메쉬 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

def get_facial_features(landmarks):
    features = {}
    
    # 눈 계산
    left_eye_outer = landmarks[33]
    left_eye_inner = landmarks[133]
    right_eye_outer = landmarks[362]
    right_eye_inner = landmarks[263]
    features['eye'] = (np.linalg.norm(left_eye_outer - left_eye_inner) +
                      np.linalg.norm(right_eye_outer - right_eye_inner)) / 2

    # 코 길이
    nose_top = landmarks[1]
    nose_tip = landmarks[4]
    features['nose'] = np.linalg.norm(nose_top - nose_tip)

    # 입술 두께
    upper_lip = landmarks[0]
    lower_lip = landmarks[17]
    features['lips'] = np.linalg.norm(upper_lip - lower_lip)

    # 이마 높이
    forehead_top = landmarks[10]
    glabella = landmarks[168]
    features['forehead'] = np.linalg.norm(forehead_top - glabella)

    return features

def generate_face_reading(features):
    reading = []
    
    if features['eye'] > 15:
        reading.append("크고 밝은 눈은 호기심이 많고 열린 마음을 나타냅니다.")
    else:
        reading.append("작고 날카로운 눈은 집중력과 분석력이 뛰어납니다.")

    if features['nose'] > 45:
        reading.append("긴 코는 강한 의지력과 리더십을 상징합니다.")
    else:
        reading.append("짧은 코는 창의성과 유연한 사고를 나타냅니다.")

    if features['lips'] > 12:
        reading.append("두꺼운 입술은 사교적이고 표현력이 풍부한 성격을 보여줍니다.")
    else:
        reading.append("얇은 입술은 신중함과 내성적인 특성을 나타냅니다.")

    if features['forehead'] > 65:
        reading.append("넓은 이마는 지적 능력과 통찰력이 뛰어납니다.")
    else:
        reading.append("좁은 이마는 빠른 실행력과 실용적인 사고를 보여줍니다.")

    return "\n".join(reading)

def analyze_face(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {image_path}")
    
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    if not results.multi_face_landmarks:
        return "얼굴을 찾을 수 없습니다."
    
    img_height, img_width, _ = img.shape
    results_text = []
    
    for face_landmarks in results.multi_face_landmarks:
        landmarks = np.array([[lm.x * img_width, lm.y * img_height, lm.z * img_width] 
                             for lm in face_landmarks.landmark])
        
        features = get_facial_features(landmarks)
        reading = generate_face_reading(features)
        results_text.append(reading)
    
    return "\n\n[분석 결과]\n" + "\n\n".join(results_text)

if __name__ == "__main__":
    # 1. 여기에 하드코딩으로 이미지 경로 설정
    image_path = "D:/Coding/AI4FW/image_modeling/suyang.png"  # ← 실제 경로로 변경 필수
    
    # 2. 분석 실행
    print("\n" + "="*50)
    print("관상 분석을 시작합니다...")
    
    try:
        result = analyze_face(image_path)
        print(result)
        print("="*50)
        print("\n※ 참고: 관상학은 과학적 근거가 없는 전통적인 민속학입니다. 재미로만 참고해주세요!")
    
    except Exception as e:
        print("\n" + "!"*50)
        print(f"오류 발생: {str(e)}")
        print("!"*50)
        print("문제 해결 방법:")
        print("- 이미지 경로 확인")
        print("- 파일 확장자 확인 (.jpg, .png)")
        print("- 이미지에 정면 얼굴 포함 확인")