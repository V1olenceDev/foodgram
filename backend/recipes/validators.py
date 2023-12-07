from django.core.validators import RegexValidator

# Валидатор для проверки имени пользователя
name_validator = RegexValidator(
    regex=r'^[A-Za-zА-Яа-я\s]+$',
    message='Название должно содержать только буквы и пробелы.'
)

# Валидатор для проверки HEX-кода цвета
hex_validator = RegexValidator(
    regex=r'^#([a-fA-F0-9]{3,6})$',
    message='Поле должно содержать HEX-код выбранного цвета.'
)
