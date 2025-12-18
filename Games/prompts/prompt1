Я хочу, чтобы cmd_J_map_with_parents в main.py выписывал бы 
для текущего кода из BASE_CODE.json вместо строки

[
    True, 
    {'include': {'parent': [1], 'body': '123'}}, 
    
    {'include': 
        {'parent': [2], 'body': 
            {'include': {'parent': [2, 'include'], 'body': '123'}}
        }
    }, 
    [
        {'game_field': {'parent': [3, 0], 'body': ['']}}
    ], 
    '1', 
    [[], True]
]

строку

[
    {'UnknownCommand': {'parent': [0], 'body': True}}, 
    {'include': {'parent': [1], 'body': '123'}}, 
    {'include': {'parent': [2], 'body': 
        {'include': {'parent': [2, 'include'], 'body': '123'}}}
    }, 
    [
        {'game_field': {'parent': [3, 0], 'body': ['']}}
    ], 
    {'UnknownCommand': {'parent': [4], 'body': '1'}}, 
    {'UnknownCommand': {'parent': [5], 'body': []}}, 
    {'UnknownCommand': {'parent': [5, 0], 'body': []}}, 
    {'UnknownCommand': {'parent': [5, 1], 'body': True}}
]

То есть мне нужен класс UnknownCommand, который 
в self._name всегда кладет UnknownCommand, 
а в action = то, что находится в исходном коде 
на соответствующем месте (True/[]/'...'/...). 
Также класс UnknownCommand должен обрабатывать cmd_path, 
как это видно из второй строки, которую я привел. 

Пример:

для кода 

[
    {'dict_examp': [True]}
]

должна получиться карта команд:

[
    {'UnknownCommand': {'parent': [0], 'body': 'dict_examp'}}, 
    {'UnknownCommand': {'parent': [0,'dict_examp'], 'body': []}}, 
    {'UnknownCommand': {'parent': [0,'dict_examp',0], 'body': True}}
]