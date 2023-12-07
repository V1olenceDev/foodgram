from django.core.validators import RegexValidator

name_validator = RegexValidator(r'^[A-Za-zА-Яа-я\s]+$',
                                'Разрешены только буквы и пробелы.')
hex_validator = RegexValidator('^#([a-fA-F0-9]{3,6})$',
                               'Поле должно содержать '
                               'HEX-код выбранного цвета.')
