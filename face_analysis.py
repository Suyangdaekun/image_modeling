import cv2
import mediapipe as mp
import numpy as np

# MediaPipe 얼굴 메쉬 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7
)

def get_facial_proportions(landmarks, img_width, img_height):
    # 전통 관상학 궁위 기준 측정값 계산
    proportions = {
        # 관록궁(이마)
        '관록궁': {
            'width': np.linalg.norm(landmarks[21] - landmarks[251]),
            'height': np.linalg.norm(landmarks[10] - landmarks[168])
        },
        
        # 재백궁(코)
        '재백궁': {
            'length': np.linalg.norm(landmarks[4] - landmarks[168]),
            'straightness': np.mean([landmarks[168][1], landmarks[6][1], landmarks[4][1]])
        },
        
        # 복덕궁(왼쪽 뺨)
        '복덕궁': {
            'fullness': np.linalg.norm(landmarks[132] - landmarks[93])
        },
        
        # 천상궁(오른쪽 뺨)
        '천상궁': {
            'fullness': np.linalg.norm(landmarks[361] - landmarks[323])
        },
        
        # 인중(인중)
        '인중': {
            'depth': landmarks[0][2] - landmarks[17][2],
            'length': np.linalg.norm(landmarks[0] - landmarks[17])
        }
    }
    
    # 상대적 비율 계산
    face_width = np.linalg.norm(landmarks[454] - landmarks[234])
    for key in proportions:
        for subkey in proportions[key]:
            proportions[key][subkey] /= face_width  # 얼굴 너비 기준 정규화
            
    return proportions

def generate_face_reading(proportions):
    analysis = []
    
    # 관록궁 분석 (이마)
    관록_평균 = (proportions['관록궁']['width'] + proportions['관록궁']['height']) / 2
    if 관록_평균 > 0.35:
        analysis.append("[관록궁] 넓고 높은 이마")
    else:
        analysis.append("[관록궁] 협소한 이마")

    # 재백궁 분석 (코)
    if proportions['재백궁']['length'] > 0.28:
        analysis.append("[재백궁] 길고 직선적인 코")
    elif proportions['재백궁']['straightness'] < 0.15:
        analysis.append("[재백궁] 곡선형 코")

    # 복덕/천상궁 분석 (볼)
    양측_차이 = abs(proportions['복덕궁']['fullness'] - proportions['천상궁']['fullness'])
    if 양측_차이 < 0.05:
        analysis.append("[복덕/천상궁] 균형 잡힌 볼")
    else:
        analysis.append("[복덕/천상궁] 불균형 볼")

    # 인중 분석
    if proportions['인중']['depth'] > 0.08:
        analysis.append("[인중] 깊고 긴 인중")
    else:
        analysis.append("[인중] 얕은 인중")

    return "\n".join(analysis)

def analyze_face(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"이미지 불러오기 실패: {image_path}")
    
    results = face_mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        return "얼굴 검출 실패"
    
    img_height, img_width, _ = img.shape
    face_landmarks = results.multi_face_landmarks[0]
    
    # 랜드마크 정규화 좌표 변환
    landmarks = np.array([[lm.x * img_width, lm.y * img_height, lm.z * img_width] 
                         for lm in face_landmarks.landmark])
    
    proportions = get_facial_proportions(landmarks, img_width, img_height)
    return generate_face_reading(proportions)

if __name__ == "__main__":
    # 하드코딩 이미지 경로 (image_modeling 폴더 기준)
    image_path = "D:/Coding/AI4FW/image_modeling/suyang.png"  # ← image_modeling 폴더 내 이미지 경로
    
    try:
        result = analyze_face(image_path)
        print(result)
    except Exception as e:
        print(f"오류 발생: {str(e)}")