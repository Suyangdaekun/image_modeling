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
    MOUTH_WIDTH = [76, 306]  # 입 양쪽 끝
    MOUTH_HEIGHT = [0, 17]  # 입 상하 지점 (위/아래 중앙)
    
    # 얼굴 전체 측정 지점
    FACE_CONTOUR = [234, 454]  # 왼쪽/오른쪽 귀 부근 (얼굴 너비)
    FACE_VERTICAL = [10, 152]  # 이마 상단 ~ 턱 (얼굴 높이)
    
    # 새로운 랜드마크 인덱스 추가
    FOREHEAD = [10, 8]  # 이마 상단과 하단
    FOREHEAD_WIDTH = [54, 284]  # 이마 좌우 끝점
    
    EYEBROWS = {
        'left': [70, 55],  # 왼쪽 눈썹 시작과 끝
        'right': [285, 300]    # 오른쪽 눈썹 시작과 끝
    }
    
    GLABELLA = [55, 285]  # 미간은 왼쪽 눈썹 오른끝에서 오른쪽 눈썹 왼끝까지

    PHILTRUM = [2, 0]  # 인중은 코끝에서 입술까지
    
    JAW = {
        'top': [17],      # 턱 상단
        'bottom': [152],   # 턱 하단
        'width': [150, 379]  # 턱 좌우 폭
    }
    
    CHEEKS = {
        'left': [116, 192],   # 왼쪽 볼 상하
        'right': [345, 416],  # 오른쪽 볼 상하
        'width': [93, 323]   # 볼 좌우 최대 폭
    }

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
    
    # 이마 측정
    forehead_height = np.linalg.norm(landmarks[FOREHEAD[0]] - landmarks[FOREHEAD[1]])
    forehead_width = np.linalg.norm(landmarks[FOREHEAD_WIDTH[0]] - landmarks[FOREHEAD_WIDTH[1]])
    measurements['forehead'] = {
        'width_px': int(forehead_width),
        'height_px': int(forehead_height)
    }
    
    # 눈썹 측정
    left_eyebrow_length = np.linalg.norm(landmarks[EYEBROWS['left'][0]] - landmarks[EYEBROWS['left'][1]])
    right_eyebrow_length = np.linalg.norm(landmarks[EYEBROWS['right'][0]] - landmarks[EYEBROWS['right'][1]])
    measurements['eyebrows'] = {
        'left_length_px': int(left_eyebrow_length),
        'right_length_px': int(right_eyebrow_length)
    }
    
    # 미간 측정
    glabella_length = np.linalg.norm(landmarks[GLABELLA[0]] - landmarks[GLABELLA[1]])
    measurements['glabella'] = {
        'length_px': int(glabella_length)
    }

    # 인중 측정
    philtrum_length = np.linalg.norm(landmarks[PHILTRUM[0]] - landmarks[PHILTRUM[1]])
    measurements['philtrum'] = {
        'length_px': int(philtrum_length)
    }
    
    # 턱 측정
    jaw_height = np.linalg.norm(landmarks[JAW['top'][0]] - landmarks[JAW['bottom'][0]])
    jaw_width = np.linalg.norm(landmarks[JAW['width'][0]] - landmarks[JAW['width'][1]])
    measurements['jaw'] = {
        'width_px': int(jaw_width),
        'height_px': int(jaw_height)
    }
    
    # 볼 측정
    left_cheek_height = np.linalg.norm(landmarks[CHEEKS['left'][0]] - landmarks[CHEEKS['left'][1]])
    right_cheek_height = np.linalg.norm(landmarks[CHEEKS['right'][0]] - landmarks[CHEEKS['right'][1]])
    cheek_width = np.linalg.norm(landmarks[CHEEKS['width'][0]] - landmarks[CHEEKS['width'][1]])
    
    measurements['cheeks'] = {
        'left_width_px': int(cheek_width / 3),
        'left_height_px': int(left_cheek_height),
        'right_width_px': int(cheek_width / 3),
        'right_height_px': int(right_cheek_height)
    }

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