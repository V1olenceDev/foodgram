from django.core.validators import RegexValidator

# Валидатор для проверки HEX-кода цвета
hex_validator = RegexValidator(
    regex=r'^#([a-fA-F0-9]{3,6})$',
    message='Поле должно содержать HEX-код выбранного цвета.'
)
