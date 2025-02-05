def generate_measurement_report(measurements):
    report = []
    eyes = measurements['eyes']
    face_proportions = measurements['face_proportions']
    
    # 얼굴 전체 면적 계산
    face_area = face_proportions['face_width_px'] * face_proportions['face_height_px']
    
    report.append(f"얼굴 전체 크기: {face_proportions['face_width_px']}px (가로) × {face_proportions['face_height_px']}px (세로)")
    report.append(f"- 얼굴 전체 면적: {face_area} px²")
    
    # 얼굴 비율 분석
    face_ratio = face_proportions['face_width_px'] / face_proportions['face_height_px'] if face_proportions['face_height_px'] != 0 else 0
    report.append("얼굴 비율 분석:")
    report.append(f"- 얼굴 가로/세로 비율: {face_ratio:.1f}:1")
    if face_ratio > 1.0:
        report.append("  → 둥근 얼굴 형태 (가로가 긴 편)")
    elif face_ratio > 0.8:
        report.append("  → 타원형 얼굴 형태 (균형 잡힌 형태)")
    else:
        report.append("  → 긴 얼굴 형태 (세로가 긴 편)")
    
    # 눈 분석
    report.append(f"\n눈 분석:")
    left_eye_area = eyes['left_width_px'] * eyes['left_height_px']
    right_eye_area = eyes['right_width_px'] * eyes['right_height_px']
    total_eye_area = left_eye_area + right_eye_area
    eye_face_ratio = (total_eye_area / face_area) * 100 if face_area != 0 else 0
    
    report.append(f"- 왼쪽 눈: {eyes['left_width_px']}px (가로) × {eyes['left_height_px']}px (세로), 면적: {left_eye_area} px²")
    report.append(f"- 오른쪽 눈: {eyes['right_width_px']}px (가로) × {eyes['right_height_px']}px (세로), 면적: {right_eye_area} px²")
    report.append(f"- 두 눈의 총 면적: {total_eye_area} px²")
    report.append(f"- 두 눈이 얼굴에서 차지하는 비율: {eye_face_ratio:.1f}%")
    
    if eye_face_ratio > 15:
        report.append("  → 큰 눈 (얼굴에서 차지하는 비율이 높음)")
    elif eye_face_ratio > 10:
        report.append("  → 일반적인 크기의 눈")
    else:
        report.append("  → 작은 눈 (얼굴에서 차지하는 비율이 낮음)")
    
    # [추가] 눈 가로세로 비율 비교
    left_ratio = eyes['left_width_px'] / eyes['left_height_px'] if eyes['left_height_px'] != 0 else 0
    right_ratio = eyes['right_width_px'] / eyes['right_height_px'] if eyes['right_height_px'] != 0 else 0
    ratio_diff = abs(left_ratio - right_ratio)
    report.append(f"- 왼쪽 눈 가로세로 비율: {left_ratio:.1f}:1")
    report.append(f"- 오른쪽 눈 가로세로 비율: {right_ratio:.1f}:1")
    
    if ratio_diff > 0.4:
        report.append(f"⚠️ 짝짝이 눈 특성 (비율 차이: {ratio_diff:.1f})")
    elif ratio_diff > 0.2:
        report.append(f"- 약간의 눈 모양 차이 (비율 차이: {ratio_diff:.1f})")
    else:
        report.append("- 균형 잡힌 눈 모양")
    
    # 코 분석
    nose = measurements['nose']
    nose_area = nose['width_px'] * nose['length_px']
    nose_face_ratio = (nose_area / face_area) * 100 if face_area != 0 else 0
    
    report.append(f"\n코 분석:")
    report.append(f"- 길이: {nose['length_px']}px, 너비: {nose['width_px']}px")
    report.append(f"- 코 면적: {nose_area} px²")
    report.append(f"- 코가 얼굴에서 차지하는 비율: {nose_face_ratio:.1f}%")
    
    if nose_face_ratio > 8:
        report.append("  → 큰 코 (얼굴에서 차지하는 비율이 높음)")
    elif nose_face_ratio > 5:
        report.append("  → 일반적인 크기의 코")
    else:
        report.append("  → 작은 코 (얼굴에서 차지하는 비율이 낮음)")
    
    nose_ratio = nose['width_px'] / nose['length_px'] if nose['length_px'] != 0 else 0
    report.append(f"- 너비/길이 비율: {nose_ratio:.1f}:1")
    if nose_ratio > 0.8:
        report.append("  → 넓적한 코 형태 (주먹코)")
    elif nose_ratio < 0.5:
        report.append("  → 가늘고 긴 코 형태 (민코)")
    else:
        report.append("  → 일반적인 코 비율")
    
    # 입 분석
    mouth = measurements['mouth']
    mouth_area = mouth['width_px'] * mouth['height_px']
    mouth_face_ratio = (mouth_area / face_area) * 100 if face_area != 0 else 0
    
    report.append(f"\n입 분석:")
    report.append(f"- 입 크기: {mouth['width_px']}px (가로) × {mouth['height_px']}px (세로)")
    report.append(f"- 입 면적: {mouth_area} px²")
    report.append(f"- 입이 얼굴에서 차지하는 비율: {mouth_face_ratio:.1f}%")
    
    if mouth_face_ratio > 6:
        report.append("  → 큰 입 (얼굴에서 차지하는 비율이 높음)")
    elif mouth_face_ratio > 3:
        report.append("  → 일반적인 크기의 입")
    else:
        report.append("  → 작은 입 (얼굴에서 차지하는 비율이 낮음)")
    
    if mouth['height_px'] != 0:
        ratio = mouth['width_px'] / mouth['height_px']
        report.append(f"- 입 가로/세로 비율: {ratio:.1f}:1")
        if ratio > 3.0:
            report.append("  → 가로로 긴 입 (얇은 입술)")
        elif ratio > 2.0:
            report.append("  → 일반적인 입 모양")
        else:
            report.append("  → 세로로 두꺼운 입 (두꺼운 입술)")
    else:
        report.append("- 입 가로/세로 비율: 계산 불가 (높이가 0)")
    
    return "\n".join(report)