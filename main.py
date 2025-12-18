import json
from LinkerAndSyntaxChecker import LinkerAndSyntaxChecker
# import json

# Читаем файл
with open("Games/BASE_CODE.json", 'r') as file:
    code = file.read()

# Создаем объект LinkerAndSyntaxChecker
linker = LinkerAndSyntaxChecker(code, "Games/BASE_CODE.json")

# Вводим J-карту команд
cmd_J_map = linker.generate_cmd_J_map()
print()
print(f"cmd_J_map = {json.dumps(cmd_J_map, indent=4)}")
print()

cmd_J_map_with_parents = linker.generate_cmd_J_map_with_parents(cmd_J_map)
print(f"cmd_J_map_with_parents = {json.dumps(cmd_J_map_with_parents, indent=4)}")
print()

# Преобразуем JSON-дерево в дерево объектов команд
cmd_obj_map = linker.generate_cmd_obj_map(cmd_J_map_with_parents)
print(f"cmd_obj_map = {json.dumps(cmd_obj_map, indent=4)}")
print()

# Проверяем все команды на ошибки
linker.validate_command_tree(cmd_obj_map)

# Выводим ошибки, если они есть
linker.print_errors()
