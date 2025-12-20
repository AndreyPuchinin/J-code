v? - value_type - не только str, int, list, dict! Также еще bool & None (они ведь доступны в джейсоне?)

? - CommandInclude._file_is_valid_json_check():
? - Проверка, что файл является валидным JSON.
V - ДОДЕЛАТЬ ПРОВЕРКУ ВСЕХ СТРОК!!

x - Допилить проверку вложенных инклюдов (через action)

v? - Разобраться с CommandPath

F - LinkerAndSyntaxChecker.txt != CommandInclude!!!
F - LinkerAndSyntaxChecker ЕСТЬ в файле!!

V - ГЛАВНАЯ ПРОБЛЕМА на сейчас: main 20

? - Где вызывается CommandPath.get_line_and_pos()?

? - CommandPath._simple_parse_brackets() вроде бы как завершен (проверил)

v - Убрать _clean_code & _remove_stump_leaves

=====================

v  - Выяснить, почему иногда позиция и строка == 0, 1, а иногда - работает, как надо.
!~ - Исправить!
v  --распарсить find_command_element, узнать, почему все ошибки на позициях "не найдено"
v  --отдельно обработать случай с UnknownCommand

Плохо работает логика bracket_map: идет разница в 1 пробел (для теста - game_field params на [[""]] работает, на [[[""]]] - НЕТ!)

Также ОШИБКА работы br_map()!!:

# КОРРЕКТНО:

cmd_path: [2, 0]
Step: 2
int
Found [: index=0, element=['[', 1, 1, 0]
Stepped to index=2, element=['"include"', 2, 2, 5]
Stepped to index=4, element=['"123"', 2, 2, 16]
Stepped to index=7, element=['"include"', 2, 3, 5]
Step: 0
int
Found [: index=12, element=['[', 4, 3, 28]
Stepped to index=18, element=['"game_field"', 3, 4, 6]

# НЕКОРРЕКТНО (уже в cmd_path[0] == 2!):

cmd_path: [2, 0, 'game_field', 0, 0]
Step: 2
int
Found [: index=0, element=['[', 1, 1, 0]
Stepped to index=2, element=['"include"', 2, 2, 5]
Stepped to index=4, element=['"123"', 2, 2, 16]
Stepped to index=7, element=['"include"', 2, 3, 5]
Step: 0
int
Found [: index=12, element=['[', 4, 3, 28]
Stepped to index=18, element=['"game_field"', 3, 4, 6]
Step: game_field
str
Found ':': index=19, element=[':', 3, 4, 18]
Found key: index=20, element=['[', 4, 4, 24]
Step: 0
int
Found [: index=20, element=['[', 4, 4, 24]
Stepped to index=22, element=['""', 5, 4, 26]
Step: 0
int
Found [: index=28, element=['[', 2, 6, 4]
Stepped to index=31, element=['true', 2, 6, 9]


ИТОГО: ОТЛАДИТЬ: CMD_PATH + BR_MAP()