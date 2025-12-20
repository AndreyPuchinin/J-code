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