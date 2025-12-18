from LinkerAndSyntaxChecker import LinkerAndSyntaxChecker
# import json

# Читаем файл
with open("Games/BASE_CODE.json", 'r') as file:
    code = file.read()

# Создаем объект LinkerAndSyntaxChecker
linker = LinkerAndSyntaxChecker(code)

# Вводим J-карту команд
cmd_J_map = linker.generate_cmd_J_map()
print(cmd_J_map)
print()

cmd_J_map_with_parents = linker.generate_cmd_J_map_with_parents(cmd_J_map)
print(cmd_J_map_with_parents)
print()

# Преобразуем JSON-дерево в дерево объектов команд
cmd_obj_map = linker.generate_cmd_obj_map(cmd_J_map_with_parents)
print("!!!", cmd_obj_map)
print()

# Проверяем все команды на ошибки
linker.validate_command_tree(cmd_obj_map)

# Выводим ошибки, если они есть
linker.print_errors()
