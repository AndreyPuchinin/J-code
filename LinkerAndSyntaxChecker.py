from CommandInclude import CommandInclude
from CommandGameField_test import CommandGameField
from CommandPath import CommandPath
from CommandNode import CommandNode
import json

class LinkerAndSyntaxChecker:
    def __init__(self, code):
        self._code = code
        self._errors = []  # Список для хранения ошибок
        self.check_syntax()
        self._commands_info = [
            {
                "include": {
                    "class": CommandInclude,
                    "name": "include",
                    "value_type": dict
                }
            },
            {
                "game_field": {
                    "class": CommandGameField,
                    "name": "game_field",
                    "value_type": list
                }
            }
        ]

    def _log_error(self, error_message):
        """
        Добавляет ошибку в список ошибок.
        :param error_message: Сообщение об ошибке.
        """
        self._errors.append(error_message)

    def print_errors(self):
        """
        Выводит все накопленные ошибки.
        """
        for error in self._errors:
            print(error)

    def check_syntax(self):
        """
        Проверяет синтаксис JSON-кода.
        :param code: Код в виде строки.
        :return: True, если синтаксис корректен, иначе False.
        """
        try:
            json.loads(self._code)
            return True
        except json.JSONDecodeError as e:
            self._log_error(f"Ошибка синтаксиса: {e}")
            return False

    def _is_command(self, key):
        """
        Проверяет, является ли ключ командой.
        :param key: Ключ для проверки.
        :return: True, если ключ — это команда, иначе False.
        """
        for cmd_info in self._commands_info:
            if key in cmd_info:
                return True
        return False

    def _clean_code(self, data):
        """
        Рекурсивно очищает код, оставляя только команды и их тела.
        :param data: Данные для обработки (словарь, список или значение).
        :return: Очищенные данные.
        """
        if isinstance(data, dict):
            # Обрабатываем словарь
            cleaned_data = {}
            for key, value in data.items():
                if self._is_command(key):  # Если ключ — это команда
                    # Рекурсивно обрабатываем тело команды
                    # Не надо, так как, если команда есть,
                    # её тело сохраняется полностью
                    #cleaned_value = self._clean_code(value)
                    cleaned_data[key] = data[key]
            return cleaned_data if cleaned_data else None
        elif isinstance(data, list):
            # Обрабатываем список
            cleaned_list = []
            for pos, item in enumerate(data):
                cleaned_item = self._clean_code(item)
                if cleaned_item != None and \
                   cleaned_item != [None] and \
                   not isinstance(cleaned_item, bool) and \
                   not isinstance(cleaned_item, str) and \
                   not isinstance(cleaned_item, int):
                    cleaned_list += [cleaned_item]
            return cleaned_list if cleaned_list else None
        else:
            # Возвращаем значение как есть (лепестки от веток)
            return data

    def _remove_stump_leaves(self, data):
        """
        Удаляет лепестки от пенька (значения-висячие вершины на верхнем уровне).
        :param data: Данные для обработки.
        :return: Очищенные данные.
        """

        # Если имеем дело с первым JSON-объектом НЕ как со списком:
        if not isinstance(data, list):
            return None

        # Если имеем дело с первым JSON-объектом как со словарем:
        if isinstance(data, dict):
            return data


        # Если имеем дело с первым JSON-объект как со споском:
        if isinstance(data, list):

            data_res = []

            # удаляем все лепестки
            for data_el in data:

                # если начальный JSON-объект == словарь
                if isinstance(data_el, dict) or isinstance(data_el, list):
                    # сохраняем его в копию
                    data_res += [data_el]

            return data_res

    def generate_cmd_J_map_with_parents(self, data=None, parent_path=None):
        """
        Создает J-карту команд с информацией о родителе, сохраняя только команды.
        :param data: Данные для обработки (словарь, список или значение).
        :param parent_path: Путь к родителю (список ключей или индексов).
        :return: J-карта команд.
        """
        if data is None:
            data = json.loads(self._code)  # Используем полный JSON-код

        if parent_path is None:
            parent_path = []

        if isinstance(data, dict):
            # Обрабатываем словарь
            command_map = {}
            for key, value in data.items():
                if self._is_command(key):
                    # Добавляем информацию о родителе
                    command_map[key] = {
                        "parent": parent_path,
                        "body": self.generate_cmd_J_map_with_parents(value, parent_path + [key])
                    }
                else:
                    # Если ключ не команда, просто копируем значение
                    command_map[key] = value
            return command_map
        elif isinstance(data, list):
            # Обрабатываем список
            command_map = []
            for index, item in enumerate(data):
                command_map.append(self.generate_cmd_J_map_with_parents(item, parent_path + [index]))
            return command_map
        else:
            # Возвращаем значение как есть (строки, числа, булевы значения)
            return data

    def generate_cmd_J_map(self):
        """
        Создает JSON-карту команд, удаляя всё, что не является командой.
        :param code: Код в виде строки.
        :return: JSON-карта команд.
        """
        if self._errors != []:
            return None

        # Копируем код для работы
        code_copy = json.loads(self._code)

        # Удаляем лепестки от пенька
        cleaned_code = self._remove_stump_leaves(code_copy)

        # Очищаем код, оставляя только команды и их тела
        if cleaned_code is not None:
            cleaned_code = self._clean_code(cleaned_code)

        # ВРЕМЕННО, ЭКСПЕРИМЕНТА РАДИ!! заменим cleaned_code на code_copy
        # cleaned_code = code_copy

        # Возвращаем JSON-карту команд
        return cleaned_code

    def generate_cmd_obj_map(self, command_map):
        """
        Преобразует J-карту команд в карту объектов команд, используя полный JSON-код для расчета позиций.
        :param command_map: J-карта команд.
        :return: Карта объектов команд.
        """
        if isinstance(command_map, dict):
            # Обрабатываем словарь
            command_tree = {}
            for key, value in command_map.items():
                if self._is_command(key):
                    # Создаем объект команды
                    command_info = self._get_command_info(key)
                    if command_info:
                        command_class = command_info["class"]
                        parent_path = value.get("parent", [])
                        cmd_path = self._create_command_path(parent_path)

                        # Определяем line и char_pos на основе полного JSON-кода
                        line, char_pos = self._get_command_position(cmd_path)

                        command_obj = command_class(
                            name=key,
                            value_type=command_info["value_type"],
                            action=self.generate_cmd_obj_map(value["body"]),
                            line=line,
                            char_pos=char_pos,
                            cmd_path=cmd_path
                        )
                        command_tree[key] = command_obj
                else:
                    # Если ключ не команда, просто копируем значение
                    command_tree[key] = value
            return command_tree
        elif isinstance(command_map, list):
            # Обрабатываем список
            command_tree = []
            for item in command_map:
                command_tree.append(self.generate_cmd_obj_map(item))
            return command_tree
        else:
            # Возвращаем значение как есть (строки, числа, булевы значения)
            return command_map

    def _get_command_position(self, cmd_path):
        """
        Определяет позицию команды в исходном коде на основе полного JSON-кода.
        :param cmd_path: Объект CommandPath, содержащий путь к команде.
        :return: Кортеж (line, char_pos).
        """
        if cmd_path:
            return cmd_path.get_line_and_pos(self._code)  # Используем полный JSON-код
        return None, None  # Если путь не определен, возвращаем ("<не найдена>", "<не найдена>")

    def _create_command_path(self, parent_path, rest_path=None, start_cmd_path=None):
        """
        Создает объект CommandPath на основе пути родителя, рекурсивно заполняя rest_path.
        :param parent_path: Путь к родителю (список ключей или индексов).
        :param rest_path: Следующий уровень пути (объект CommandPath).
        :return: Объект CommandPath.
        """

        cmd_path = None

        print("In")

        if rest_path is not None:
            print(rest_path._dict_name, parent_path)
        else:
            print(None, parent_path)

        if not parent_path:
            return rest_path  # Если путь пуст, возвращаем rest_path

        # Отлавливаем rest_path-висячую вершину (последнюю)
        if len(parent_path) <= 1:
            rest_path = None

        # Создаем текущий элемент цепочки
        first_step = parent_path[0]

        # Рекурсивно создаем остальные элементы цепочки
        if len(parent_path) > 1:
            rest_path = self._create_command_path(parent_path[1:], cmd_path, start_cmd_path)

        if isinstance(first_step, int):
            # Шаг — индекс в списке
            cmd_path = CommandPath(list, "", first_step, rest_path, start_cmd_path, self._code)
        elif isinstance(first_step, str):
            # Шаг — ключ в словаре
            print(first_step)
            cmd_path = CommandPath(dict, first_step, 0, rest_path, start_cmd_path, self._code)

        # Если звено корневое, сохраняем ссылку на него
        if start_cmd_path == None:
            start_cmd_path = cmd_path

        print("out")

        return cmd_path

    # def generate_cmd_obj_map(self, command_json):
    #     """
    #     Преобразует JSON-дерево команд в дерево объектов классов-наследников CommandNode.
    #     :param command_json: JSON-дерево команд.
    #     :return: Дерево объектов команд.
    #     """
    #     if isinstance(command_json, dict):
    #         # Обрабатываем словарь
    #         command_tree = {}
    #         for key, value in command_json.items():
    #             if self._is_command(key):
    #                 # Создаем объект команды
    #                 command_info = self._get_command_info(key)
    #                 print(value)
    #                 if command_info:
    #                     command_class = command_info["class"]
    #                     command_obj = command_class(
    #                         name=key,
    #                         value_type=command_info["value_type"],
    #                         action=self.generate_cmd_obj_map(value),
    #                         line=0,
    #                         char_pos=0,
    #                         cmd_path=CommandPath(command_info["value_type"], key, value["parent"], )  # Пример пути, можно адаптировать
    #                     )
    #                     command_tree[key] = command_obj
    #             else:
    #                 # Если ключ не команда, просто копируем значение
    #                 command_tree[key] = value
    #         return command_tree
    #     elif isinstance(command_json, list):
    #         # Обрабатываем список
    #         command_tree = []
    #         for item in command_json:
    #             command_tree.append(self.generate_cmd_obj_map(item))
    #         return command_tree
    #     else:
    #         # Возвращаем значение как есть (строки, числа, булевы значения)
    #         return command_json

    def _get_command_info(self, key):
        """
        Возвращает информацию о команде по ключу.
        :param key: Ключ команды.
        :return: Словарь с информацией о команде или None, если команда не найдена.
        """
        for cmd_info in self._commands_info:
            if key in cmd_info:
                return cmd_info[key]  # Возвращаем первый элемент списка (информацию о команде)
        return None

    def validate_command_tree(self, command_tree):
        """
        Рекурсивно вызывает метод Errors() для каждого объекта команды в дереве.
        :param command_tree: Дерево объектов команд.
        """
        if isinstance(command_tree, dict):
            for key, command_obj in command_tree.items():
                if isinstance(command_obj, CommandNode):
                    self._errors.extend(command_obj.Errors())  # Присоединяем результат Errors() к self._errors
                    self.validate_command_tree(command_obj._action)  # Рекурсивно проверяем вложенные команды
        elif isinstance(command_tree, list):
            for item in command_tree:
                self.validate_command_tree(item)

