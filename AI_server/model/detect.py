def detect_language(text):
    korean_count = sum(1 for char in text if '가' <= char <= '힣')
    english_count = sum(1 for char in text if 'a' <= char.lower() <= 'z')

    if korean_count > english_count:
        return 'kor'
    elif english_count > korean_count:
        return 'eng'