from django.core.validators import RegexValidator

regex_name_validator = RegexValidator(r'^[A-Za-zА-Яа-я\s]+$',
                                      'Разрешены только буквы и пробелы.')
