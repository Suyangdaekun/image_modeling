import cv2

def visualize_landmarks(image_path, landmarks, img_width, img_height):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"이미지 불러오기 실패: {image_path}")
    
    # 특정 랜드마크 강조
    left_eyebrow_indices = [55, 285]  # 입의 상하 지점
    for idx in left_eyebrow_indices:
        x, y = int(landmarks[idx][0]), int(landmarks[idx][1])
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # 빨간색 점으로 표시
        cv2.putText(img, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    right_eyebrow_indices = [2, 0]  # 입의 상하 지점
    for idx in right_eyebrow_indices:
        x, y = int(landmarks[idx][0]), int(landmarks[idx][1])
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # 빨간색 점으로 표시
        cv2.putText(img, str(idx), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 모든 랜드마크 표시
    for idx, landmark in enumerate(landmarks):
        x, y = int(landmark[0]), int(landmark[1])
        cv2.circle(img, (x, y), 2, (0, 255, 0), -1)  # 초록색 점으로 표시
    
    # resized_img = cv2.resize(img, (1000, 700))
    cv2.imshow("Landmarks", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()