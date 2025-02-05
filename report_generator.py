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
    
    if eye_face_ratio > 3:
        report.append("  → 큰 눈 (얼굴에서 차지하는 비율이 높음)")
    elif eye_face_ratio > 1.5:
        report.append("  → 일반적인 크기의 눈")
    else:
        report.append("  → 작은 눈 (얼굴에서 차지하는 비율이 낮음)")
    
    # 눈 가로세로 비율 비교
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

    eye_width_ratio = ((eyes['left_width_px'] + eyes['right_width_px']) / 2) / face_proportions['face_width_px'] if (eyes['left_width_px'] + eyes['right_width_px'] / 2) != 0 else 0
    report.append(f"- 눈의 너비/얼굴의 너비: {eye_width_ratio:.1f}:1")
    if eye_width_ratio > 0.25:
        report.append("  → 사교적인 눈")
    elif eye_width_ratio < 0.15:
        report.append("  → 신중한 눈")
    else:
        report.append("  → 일반적인 눈 비율")

    # 코 분석
    nose = measurements['nose']
    nose_area = nose['width_px'] * nose['length_px']
    nose_face_ratio = (nose_area / face_area) * 100 if face_area != 0 else 0
    
    report.append(f"\n코 분석:")
    report.append(f"- 길이: {nose['length_px']}px, 너비: {nose['width_px']}px")
    report.append(f"- 코 면적: {nose_area} px²")
    report.append(f"- 코가 얼굴에서 차지하는 비율: {nose_face_ratio:.1f}%")
    if nose_face_ratio > 10:
        report.append("  → 큰 코 (얼굴에서 차지하는 비율이 높음)")
    elif nose_face_ratio > 7:
        report.append("  → 일반적인 크기의 코")
    else:
        report.append("  → 작은 코 (얼굴에서 차지하는 비율이 낮음)")
    
    nose_height_ratio = nose['length_px'] / face_proportions['face_height_px'] if nose['length_px'] != 0 else 0
    report.append(f"- 코의 높이/얼굴 높이: {nose_height_ratio:.1f}:1")
    if nose_height_ratio > 0.35:
        report.append("  → 두드러진 코(독특한 인상)")
    elif nose_height_ratio < 0.25:
        report.append("  → 민코(납작한 코)")
    else:
        report.append("  → 일반적인 코 비율")

    nose_width_ratio = nose['width_px'] / ((eyes['left_width_px'] + eyes['right_width_px']) / 2) if nose['width_px'] != 0 else 0
    report.append(f"- 코의 너비/눈의 너비: {nose_width_ratio:.1f}:1")
    if nose_width_ratio > 1.7:
        report.append("  → 주먹코")
    elif nose_width_ratio < 1.3:
        report.append("  → 날카로운 코")
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
    
    if mouth_face_ratio > 4:
        report.append("  → 큰 입 (얼굴에서 차지하는 비율이 높음)")
    elif mouth_face_ratio > 2:
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

    # 이마 분석 추가
    forehead = measurements.get('forehead', {})
    forehead_width_px = forehead.get('width_px', 0)
    forehead_height_px = forehead.get('height_px', 0)
    forehead_area = forehead_width_px * forehead_height_px
    forehead_face_ratio = (forehead_area / face_area) * 100 if face_area != 0 else 0
    
    report.append(f"\n이마 분석:")
    if forehead_width_px == 0 or forehead_height_px == 0:
        report.append("  → 데이터 부족: 이마 정보를 제공해주세요.")
    else:
        report.append(f"- 이마 크기: {forehead_width_px}px (가로) × {forehead_height_px}px (세로)")
        report.append(f"- 이마 면적: {forehead_area} px²")
        report.append(f"- 이마가 얼굴에서 차지하는 비율: {forehead_face_ratio:.1f}%")
        
        if forehead_face_ratio > 25:
            report.append("  → 넓은 이마 (얼굴에서 차지하는 비율이 높음)")
        elif forehead_face_ratio > 15:
            report.append("  → 일반적인 크기의 이마")
        else:
            report.append("  → 좁은 이마 (얼굴에서 차지하는 비율이 낮음)")

    # 눈썹 분석 추가
    eyebrows = measurements.get('eyebrows', {})
    left_eyebrow_length = eyebrows.get('left_length_px', 0)
    right_eyebrow_length = eyebrows.get('right_length_px', 0)
    avg_eyebrow_length = (left_eyebrow_length + right_eyebrow_length) / 2 if left_eyebrow_length + right_eyebrow_length > 0 else 0
    
    report.append(f"\n눈썹 분석:")
    if left_eyebrow_length == 0 or right_eyebrow_length == 0:
        report.append("  → 데이터 부족: 눈썹 정보를 제공해주세요.")
    else:
        report.append(f"- 왼쪽 눈썹 길이: {left_eyebrow_length}px")
        report.append(f"- 오른쪽 눈썹 길이: {right_eyebrow_length}px")
        report.append(f"- 평균 눈썹 길이: {avg_eyebrow_length:.1f}px")
        
        if avg_eyebrow_length > 60:
            report.append("  → 긴 눈썹 (일반적으로 긴 형태)")
        elif avg_eyebrow_length > 40:
            report.append("  → 중간 길이의 눈썹")
        else:
            report.append("  → 짧은 눈썹 (짧고 굵은 형태)")

    # 미간 분석 추가
    philtrum = measurements.get('philtrum', {})
    philtrum_length = philtrum.get('length_px', 0)
    philtrum_face_ratio = (philtrum_length / face_proportions['face_height_px']) * 100 if face_proportions['face_height_px'] != 0 else 0
    
    report.append(f"\n미간 분석:")
    if philtrum_length == 0:
        report.append("  → 데이터 부족: 미간 정보를 제공해주세요.")
    else:
        report.append(f"- 미간 길이: {philtrum_length}px")
        report.append(f"- 미간이 얼굴 세로 길이에서 차지하는 비율: {philtrum_face_ratio:.1f}%")
        
        if philtrum_face_ratio > 10:
            report.append("  → 긴 미간 (얼굴 세로 길이에 비해 길어 보임)")
        elif philtrum_face_ratio > 7:
            report.append("  → 일반적인 길이의 미간")
        else:
            report.append("  → 짧은 미간 (얼굴 세로 길이에 비해 짧아 보임)")

    # 인중 분석 추가
    nasolabial = measurements.get('nasolabial', {})
    nasolabial_length = nasolabial.get('length_px', 0)
    nasolabial_face_ratio = (nasolabial_length / face_proportions['face_height_px']) * 100 if face_proportions['face_height_px'] != 0 else 0
    
    report.append(f"\n인중 분석:")
    if nasolabial_length == 0:
        report.append("  → 데이터 부족: 인중 정보를 제공해주세요.")
    else:
        report.append(f"- 인중 길이: {nasolabial_length}px")
        report.append(f"- 인중이 얼굴 세로 길이에서 차지하는 비율: {nasolabial_face_ratio:.1f}%")
        
        if nasolabial_face_ratio > 8:
            report.append("  → 긴 인중 (얼굴 세로 길이에 비해 길어 보임)")
        elif nasolabial_face_ratio > 5:
            report.append("  → 일반적인 길이의 인중")
        else:
            report.append("  → 짧은 인중 (얼굴 세로 길이에 비해 짧아 보임)")
    
    # 턱 분석 추가
    jaw = measurements.get('jaw', {})
    jaw_width_px = jaw.get('width_px', 0)
    jaw_height_px = jaw.get('height_px', 0)
    jaw_area = jaw_width_px * jaw_height_px
    jaw_face_ratio = (jaw_area / face_area) * 100 if face_area != 0 else 0
    jaw_ratio = jaw_width_px / jaw_height_px if jaw_height_px != 0 else 0
    
    report.append(f"\n턱 분석:")
    if jaw_width_px == 0 or jaw_height_px == 0:
        report.append("  → 데이터 부족: 턱 정보를 제공해주세요.")
    else:
        report.append(f"- 턱 크기: {jaw_width_px}px (가로) × {jaw_height_px}px (세로)")
        report.append(f"- 턱 면적: {jaw_area} px²")
        report.append(f"- 턱이 얼굴에서 차지하는 비율: {jaw_face_ratio:.1f}%")
        report.append(f"- 턱 가로/세로 비율: {jaw_ratio:.1f}:1")
        
        if jaw_ratio > 2.0:
            report.append("  → 넓적한 턱 형태 (각진 턱)")
        elif jaw_ratio > 1.3:
            report.append("  → 일반적인 턱 형태")
        else:
            report.append("  → 뾰족한 턱 형태 (뾰족턱)")
    
    # 볼 분석 추가
    cheeks = measurements.get('cheeks', {})
    left_cheek_width_px = cheeks.get('left_width_px', 0)
    left_cheek_height_px = cheeks.get('left_height_px', 0)
    right_cheek_width_px = cheeks.get('right_width_px', 0)
    right_cheek_height_px = cheeks.get('right_height_px', 0)
    left_cheek_area = left_cheek_width_px * left_cheek_height_px
    right_cheek_area = right_cheek_width_px * right_cheek_height_px
    total_cheek_area = left_cheek_area + right_cheek_area
    cheek_face_ratio = (total_cheek_area / face_area) * 100 if face_area != 0 else 0
    
    report.append(f"\n볼 분석:")
    if left_cheek_width_px == 0 or left_cheek_height_px == 0 or right_cheek_width_px == 0 or right_cheek_height_px == 0:
        report.append("  → 데이터 부족: 볼 정보를 제공해주세요.")
    else:
        report.append(f"- 왼쪽 볼 크기: {left_cheek_width_px}px (가로) × {left_cheek_height_px}px (세로), 면적: {left_cheek_area} px²")
        report.append(f"- 오른쪽 볼 크기: {right_cheek_width_px}px (가로) × {right_cheek_height_px}px (세로), 면적: {right_cheek_area} px²")
        report.append(f"- 두 볼의 총 면적: {total_cheek_area} px²")
        report.append(f"- 볼이 얼굴에서 차지하는 비율: {cheek_face_ratio:.1f}%")
        
        if cheek_face_ratio > 30:
            report.append("  → 큰 볼 (얼굴에서 차지하는 비율이 높음)")
        elif cheek_face_ratio > 20:
            report.append("  → 일반적인 크기의 볼")
        else:
            report.append("  → 작은 볼 (얼굴에서 차지하는 비율이 낮음)")
    
    return "\n".join(report)