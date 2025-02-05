def generate_measurement_report(measurements):
    report = []
    eyes = measurements['eyes']
    report.append(f"눈 분석:")
    report.append(f"- 왼쪽 눈: {eyes['left_width_px']}px (가로) × {eyes['left_height_px']}px (세로)")
    report.append(f"- 오른쪽 눈: {eyes['right_width_px']}px (가로) × {eyes['right_height_px']}px (세로)")
    
    # [추가] 눈 가로세로 비율 비교
    left_ratio = eyes['left_width_px'] / eyes['left_height_px'] if eyes['left_height_px'] !=0 else 0
    right_ratio = eyes['right_width_px'] / eyes['right_height_px'] if eyes['right_height_px'] !=0 else 0
    ratio_diff = abs(left_ratio - right_ratio)
    report.append(f"- 왼쪽 눈 가로세로 비율: {left_ratio:.1f}:1")
    report.append(f"- 오른쪽 눈 가로세로 비율: {right_ratio:.1f}:1")
    
    # [추가] 짝짝이 눈 판단
    if ratio_diff > 0.4:  # 비율 차이 기준
        report.append(f"⚠️ 짝짝이 눈 특성 (비율 차이: {ratio_diff:.1f})")
    elif ratio_diff > 0.2:
        report.append(f"- 약간의 눈 모양 차이 (비율 차이: {ratio_diff:.1f})")
    else:
        report.append("- 균형 잡힌 눈 모양")
    if eyes['width_diff_px'] > 5 or eyes['height_diff_px'] > 3:
        report.append(f"- 양쪽 눈 크기 차이: 가로 {eyes['width_diff_px']}px, 세로 {eyes['height_diff_px']}px (짝짝이 눈 특성)")
    # [추가] 코 비율 분석
    nose = measurements['nose']
    nose_ratio = nose['width_px'] / nose['length_px'] if nose['length_px'] !=0 else 0
    report.append(f"\n코 분석:")
    report.append(f"- 길이: {nose['length_px']}px, 너비: {nose['width_px']}px")
    report.append(f"- 너비/길이 비율: {nose_ratio:.1f}:1")
    if nose_ratio > 0.8:
        report.append("  → 넓적한 코 형태 (주먹코)")
    elif nose_ratio < 0.5:
        report.append("  → 가늘고 긴 코 형태 (민코)")
    else:
        report.append("  → 일반적인 코 비율")
    
    mouth = measurements['mouth']
    report.append(f"\n입 분석:")
    report.append(f"- 입 크기: {mouth['width_px']}px (가로) × {mouth['height_px']}px (세로)")
    if mouth['height_px'] != 0:
        ratio = mouth['width_px'] / mouth['height_px']
        report.append(f"- 입 가로/세로 비율: {ratio:.1f}:1")
        
        # [추가] 입 모양 분석
        if ratio > 3.0:
            report.append("  → 가로로 긴 입 (얇은 입술)")
        elif ratio > 2.0:
            report.append("  → 일반적인 입 모양")
        else:
            report.append("  → 세로로 두꺼운 입 (두꺼운 입술)")
    else:
        report.append("- 입 가로/세로 비율: 계산 불가 (높이가 0)")
    
    proportions = measurements['face_proportions']
    report.append("\n얼굴 비율 분석:")
    report.append(f"- 얼굴 전체 크기: {proportions['face_width_px']}px (가로) × {proportions['face_height_px']}px (세로)")
    
    # [추가] 얼굴 형태 분석
    face_ratio = proportions['face_width_px'] / proportions['face_height_px'] if proportions['face_height_px'] != 0 else 0
    report.append(f"- 얼굴 가로/세로 비율: {face_ratio:.1f}:1")
    if face_ratio > 1.0:
        report.append("  → 둥근 얼굴 형태 (가로가 긴 편)")
    elif face_ratio > 0.8:
        report.append("  → 타원형 얼굴 형태 (균형 잡힌 형태)")
    else:
        report.append("  → 긴 얼굴 형태 (세로가 긴 편)")
    
    eye_sym = proportions['eye_symmetry']
    report.append("\n눈 위치 분석:")
    report.append(f"- 왼쪽 눈 위치: 얼굴 왼쪽 끝에서 {eye_sym['left_eye_position_ratio']*100:.0f}% 지점")
    report.append(f"- 오른쪽 눈 위치: 얼굴 오른쪽 끝에서 {eye_sym['right_eye_position_ratio']*100:.0f}% 지점")
    if eye_sym['symmetry_balance'] < 0.05:
        report.append("- 양쪽 눈이 거의 완벽한 대칭을 이룹니다 (불균형 < 5%)")
    else:
        report.append(f"- 눈 위치 불균형: {eye_sym['symmetry_balance']*100:.0f}% (기준치 5% 초과)")
    
    report.append(f"- 눈 간격: 얼굴 가로 폭의 {proportions['eye_spacing_ratio']*100:.0f}%")
    
    nose_pos = proportions['nose_position']
    report.append("\n코 위치 분석:")
    report.append(f"- 코 수평 위치: 얼굴 왼쪽 끝에서 {nose_pos['horizontal_ratio']*100:.0f}% 지점")
    report.append(f"- 코 수직 위치: 이마 상단에서 {nose_pos['vertical_ratio']*100:.0f}% 지점")
    
    mouth_pos = proportions['mouth_position']
    report.append("\n입 위치 분석:")
    report.append(f"- 입 수평 위치: 얼굴 왼쪽 끝에서 {mouth_pos['horizontal_ratio']*100:.0f}% 지점")
    report.append(f"- 입 수직 위치: 이마 상단에서 {mouth_pos['vertical_ratio']*100:.0f}% 지점 (턱에서 {100 - mouth_pos['vertical_ratio']*100:.0f}% 지점)")
    
    return "\n".join(report)