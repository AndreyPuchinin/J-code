import json
from LinkerAndSyntaxChecker import LinkerAndSyntaxChecker

# Разделяем системный и пользовательский вывод
print()

# Читаем файл
with open("Games/BASE_CODE.json", 'r') as file:
    code = file.read()

# Создаем объект LinkerAndSyntaxChecker
linker = LinkerAndSyntaxChecker(code, "Games/BASE_CODE.json")

# Получаем код из json'а
loaded_code = json.loads(code)

# Генерируем J-карту с родительскими контекстами
cmd_J_map_with_parents = linker.generate_cmd_J_map_with_parents(loaded_code)

# Сохраняем промежуточную J-карту в файл
linker.log_json(cmd_J_map_with_parents, 'J-sub_code/cmd_J_map_with_parents.json')

# Преобразуем JSON-дерево в дерево объектов команд
cmd_obj_map = linker.generate_cmd_obj_map(cmd_J_map_with_parents)

# Сохраняем дерево объектов команд в файл
linker.log_json(cmd_obj_map, 'J-sub_code/cmd_obj_map.json')

# Проверяем все команды на ошибки
linker.validate_command_tree(cmd_obj_map)

linker.print_bracket_map('Games/BASE_CODE.json','J-sub_code/bracket_map.json')
print("Файлы с J-sub_code лежат в папке J-sub_code/")

# Получаем ошибки (если есть) и логируем в файл
errors_output = linker.get_errors()
if errors_output:
    linker.write_errors_to_file(errors_output, 'J-sub_code/errors.log')
    print("Ошибки записаны в J-sub_code/errors.log")
else:
    print("Ошибок не найдено.")