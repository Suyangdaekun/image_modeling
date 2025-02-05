import numpy as np

def get_face_measurements(landmarks, img_width, img_height):
    # 눈 관련 랜드마크 인덱스 (MediaPipe Face Mesh 기준)
    LEFT_EYE = [33, 133]  # 왼쪽 눈 외각, 내각
    RIGHT_EYE = [362, 263]  # 오른쪽 눈 외각, 내각
    EYE_VERTICAL = [159, 145, 386, 374]  # 각 눈의 상하 지점 (왼쪽 위/아래, 오른쪽 위/아래)
    
    # 코 측정 지점
    NOSE_LENGTH = [168, 4]  # 코 시작점(미간) ~ 코 끝점
    NOSE_WIDTH = [358, 129]  # 코 양쪽 가장자리 (코의 가로 폭)
    
    # 입 측정 지점
    MOUTH_WIDTH = [78, 308]  # 입 양쪽 끝
    MOUTH_HEIGHT = [13, 18]  # 입 상하 지점 (위/아래 중앙)
    
    # 얼굴 전체 측정 지점
    FACE_CONTOUR = [234, 454]  # 왼쪽/오른쪽 귀 부근 (얼굴 너비)
    FACE_VERTICAL = [10, 152]  # 이마 상단 ~ 턱 (얼굴 높이)
    
    measurements = {}
    
    # 얼굴 전체 크기 계산
    face_width = np.linalg.norm(landmarks[FACE_CONTOUR[0]] - landmarks[FACE_CONTOUR[1]])
    face_height = np.linalg.norm(landmarks[FACE_VERTICAL[0]] - landmarks[FACE_VERTICAL[1]])
    
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
    
    # 입 측정
    mouth_width = np.linalg.norm(landmarks[MOUTH_WIDTH[0]] - landmarks[MOUTH_WIDTH[1]])
    mouth_height = np.linalg.norm(landmarks[MOUTH_HEIGHT[0]] - landmarks[MOUTH_HEIGHT[1]])
    if mouth_height == 0:
        print("입 높이가 0으로 계산됨. 랜드마크 좌표 확인 필요:")
        print(f"MOUTH_HEIGHT[0]: {landmarks[MOUTH_HEIGHT[0]]}")
        print(f"MOUTH_HEIGHT[1]: {landmarks[MOUTH_HEIGHT[1]]}")
    measurements['mouth'] = {
        'width_px': int(mouth_width),
        'height_px': int(mouth_height)
    }
    
    # 얼굴 비율 계산
    left_eye_center = (landmarks[33] + landmarks[133]) / 2  # 왼쪽 눈 중심
    right_eye_center = (landmarks[362] + landmarks[263]) / 2  # 오른쪽 눈 중심
    
    eye_left_ratio = (left_eye_center[0] - landmarks[FACE_CONTOUR[0]][0]) / face_width
    eye_right_ratio = (landmarks[FACE_CONTOUR[1]][0] - right_eye_center[0]) / face_width
    inter_eye_distance = np.linalg.norm(left_eye_center - right_eye_center)
    eye_spacing_ratio = inter_eye_distance / face_width
    
    nose_tip = landmarks[4]  # 코 끝 랜드마크
    nose_horizontal_ratio = (nose_tip[0] - landmarks[FACE_CONTOUR[0]][0]) / face_width
    nose_vertical_ratio = (nose_tip[1] - landmarks[FACE_VERTICAL[0]][1]) / face_height
    
    mouth_center = (landmarks[13] + landmarks[18]) / 2
    mouth_horizontal_ratio = (mouth_center[0] - landmarks[FACE_CONTOUR[0]][0]) / face_width
    mouth_vertical_ratio = (mouth_center[1] - landmarks[FACE_VERTICAL[0]][1]) / face_height
    
    measurements['face_proportions'] = {
        'face_width_px': int(face_width),
        'face_height_px': int(face_height),
        'eye_symmetry': {
            'left_eye_position_ratio': round(eye_left_ratio, 2),
            'right_eye_position_ratio': round(eye_right_ratio, 2),
            'symmetry_balance': round(abs(eye_left_ratio - eye_right_ratio), 2)
        },
        'eye_spacing_ratio': round(eye_spacing_ratio, 2),
        'nose_position': {
            'horizontal_ratio': round(nose_horizontal_ratio, 2),
            'vertical_ratio': round(nose_vertical_ratio, 2)
        },
        'mouth_position': {
            'horizontal_ratio': round(mouth_horizontal_ratio, 2),
            'vertical_ratio': round(mouth_vertical_ratio, 2)
        }
    }
    return measurements