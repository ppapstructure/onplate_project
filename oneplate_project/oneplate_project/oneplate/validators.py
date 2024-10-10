import string
from django.core.exceptions import ValidationError

'''
이후 이미지 크기 제한 설정
def validate_image(image):
    file_size = image.file.size
    limit_kb = 500  # 500KB 크기 제한
    if file_size > limit_kb * 1024:
        raise ValidationError("이미지 파일 크기는 500KB 이하로 제한됩니다.")
'''

def contains_special_character(value):
    for char in value:
        if char in string.punctuation:
            return True
    return False

def validate_no_special_characters(value):
    if contains_special_character(value):
        raise ValidationError("특수문자를 포함할 수 없습니다.")