from django.core.validators import RegexValidator

name_validator = RegexValidator(
    regex=r'^[A-Za-zА-Яа-я\s]+$',
    message='Название должно содержать только буквы и пробелы.'
)
