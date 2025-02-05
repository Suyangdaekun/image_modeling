def generate_measurement_report(measurements):
    report = []
    eyes = measurements['eyes']
    report.append(f"눈 분석:")
    report.append(f"- 왼쪽 눈: {eyes['left_width_px']}px (가로) × {eyes['left_height_px']}px (세로)")
    report.append(f"- 오른쪽 눈: {eyes['right_width_px']}px (가로) × {eyes['right_height_px']}px (세로)")
    if eyes['width_diff_px'] > 5 or eyes['height_diff_px'] > 3:
        report.append(f"- 양쪽 눈 크기 차이: 가로 {eyes['width_diff_px']}px, 세로 {eyes['height_diff_px']}px (짝짝이 눈 특성)")
    
    nose = measurements['nose']
    report.append(f"\n코 분석:")
    report.append(f"- 코 길이 (세로): {nose['length_px']}px")
    report.append(f"- 코 너비 (가로): {nose['width_px']}px")
    
    mouth = measurements['mouth']
    report.append(f"\n입 분석:")
    report.append(f"- 입 크기: {mouth['width_px']}px (가로) × {mouth['height_px']}px (세로)")
    if mouth['height_px'] != 0:
        ratio = mouth['width_px'] / mouth['height_px']
        report.append(f"- 입 가로/세로 비율: {ratio:.1f}:1")
    else:
        report.append("- 입 가로/세로 비율: 계산 불가 (높이가 0)")
    
    proportions = measurements['face_proportions']
    report.append("\n얼굴 비율 분석:")
    report.append(f"- 얼굴 전체 크기: {proportions['face_width_px']}px (가로) × {proportions['face_height_px']}px (세로)")
    
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
