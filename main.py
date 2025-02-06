from analyze_face import analyze_face

if __name__ == "__main__":
    image_path = "D:\Coding\AI4FW\image_modeling\sample_images\donghun.jpg"  # 실제 이미지 경로로 변경 필요
    try:
        result = analyze_face(image_path)
        print(result)
    except Exception as e:
        print(f"오류 발생: {str(e)}")