import json
import os

from CommandNode import CommandNode

class CommandPath:
    def __init__(self, cmd_type, dict_name, pos_in_list=0, rest_path=None, root=None, code=None, commands=None):
        self._cmd_type = cmd_type  # Тип команды (dict или list)
        self._dict_name = dict_name  # Имя словаря (ключ в JSON)
        self._pos_in_list = pos_in_list  # Позиция в списке (если команда находится в списке)
        self._rest_path = rest_path  # Рекурсивная ссылка на следующий уровень пути
        self._commands = commands or []  # Список зарезервированных команд
        if root == None:
            # Если звено корневое
            # Кладем код в начальное звено цепи
            # И пропускаем ссылку на базовое стартовое перичное звено цепи
            # (которого пока и нет, и которое мы и инициализируем)
            self._code = code
            self._root = None
        else:
            # Если звено не корневое,
            # Получаем ссылку на код базового стартого первичного звена цепи
            # И сохраняем ссылку на базовое стартовое перичное звено цепи
            # (в нем есть код)
            self._code = root.get_code()
            self._root = root

    def get_code(self):
        return self._code

    def _get_path(self):
        """Возвращает путь к команде в виде списка."""
        path = []
        current = self

        # Обрабатываем остальные уровни пути
        while current._rest_path:
            if current._cmd_type == dict:
                path.append(current._dict_name)
            elif current._cmd_type == list:
                path.append(current._pos_in_list)
            current = current._rest_path

        return list(reversed(path))

    def get_line_and_pos(self):
        """
        Вычисляет строку и позицию команды на основе пути и кода.
        :return: Кортеж (line, char_pos).
        """
        # Получаем список зарезервированных команд
        reserved_commands = [list(cmd.keys())[0] for cmd in self._commands]
        
        # Определяем текущую команду
        current_command = self._dict_name
        if current_command in reserved_commands:
            # ДОЛЖНО СРАБАТЫВАТЬ ВСЕГДА!!!
            # НЕЗАРЕЗЕРВИРОВАННЫХ КОММАНД НЕ ДОЛЖНО БЫТЬ!!!
            full_path = self._get_path()[::-1]
            bracket_map = self.get_bracket_map()
            command_element = self.find_command_element(full_path, bracket_map, reserved_commands)
            if command_element[0]: #in f"\"{reserved_commands}\"":
                line = command_element[2]
                char_pos = command_element[3]
                return line, char_pos
            
        # Пока возвращаем None, так как расчет позиции еще не реализован
        return None, None        

    def find_command_element(self, cmd_path, bracket_map, reserved_commands):
        index = 0
        for i, step in enumerate(cmd_path):
            if isinstance(step, int):
                # Найти ближайшую '['
                while index < len(bracket_map) and bracket_map[index][0] != '[':
                    index += 1
                if index >= len(bracket_map):
                    return None
                # Отсчитать step элементов после '['
                for _ in range(step):  # +1 чтобы дойти до step-го элемента (0-based)
                    index += 1
                    while bracket_map[index][0] == '{' or \
                          bracket_map[index][0] == ':' or \
                          bracket_map[index][0] == '}' or \
                          bracket_map[index][0] == ']' or \
                          bracket_map[index][0] == '[':
                        index += 1
                    if index >= len(bracket_map):
                        return None
                # Теперь index на step-том элементе, который должен быть '{'
            elif isinstance(step, str):
                # Найти следующий ключ step
                while index < len(bracket_map) and bracket_map[index][0] != f'"{step}"':
                    index += 1
                if index >= len(bracket_map):
                    return None
                # Перепрыгнуть ':'
                index += 1
                if bracket_map[index][0] != ':':
                    return None
                if index >= len(bracket_map):
                    return None
            # Если последний шаг, вернуть этот элемент
            if i == len(cmd_path) - 1:
                return bracket_map[index]
        return None  

    def _simple_parse_brackets(self, level=0, start_index=0, start_line=1, start_char_pos=0):
        """
        Рекурсивно анализирует код и строит карту скобок, ключей и значений с их уровнем, строкой и позицией.
        :param code: Код в виде строки.
        :param level: Текущий уровень вложенности.
        :param start_index: Начальный индекс для анализа.
        :param start_line: Начальная строка.
        :param start_char_pos: Начальная позиция в строке.
        :return: Список элементов с их уровнем, строкой и позицией, а также индекс, на котором остановились.
        """
        i = start_index
        current_line = start_line
        current_char_pos = start_char_pos
        element_map = []  # Список для хранения элементов с их уровнем, строкой и позицией

        while i < len(self._code):
            if self._code[i] == '\n':  # Новая строка
                current_line += 1
                current_char_pos = 0
                i += 1
                continue

            if self._code[i] in ['{', '[']:  # Нашли открывающую скобку
                element_map.append([self._code[i], level + 1, current_line, current_char_pos])
                i += 1
                current_char_pos += 1
                # Рекурсивно обрабатываем вложенные скобки
                nested_map, i, current_line, current_char_pos = self._simple_parse_brackets(
                    level + 1, i, current_line, current_char_pos
                )
                element_map.extend(nested_map)
            elif self._code[i] in ['}', ']']:  # Нашли закрывающую скобку
                element_map.append([self._code[i], level, current_line, current_char_pos])
                i += 1
                current_char_pos += 1
                return element_map, i, current_line, current_char_pos
            elif self._code[i] == '"':  # Нашли начало строки (ключ или значение)
                # Ищем конец строки
                end_quote_pos = self._code.find('"', i + 1)
                if end_quote_pos == -1:
                    self._log_error(f"Незакрытая кавычка в строке {current_line}, позиция {current_char_pos}.")
                    return element_map, i, current_line, current_char_pos
                # Извлекаем строку
                string_content = self._code[i:end_quote_pos + 1]
                element_map.append([string_content, level, current_line, current_char_pos])
                i = end_quote_pos + 1
                current_char_pos += len(string_content)
            elif self._code[i] == ':':  # Нашли :
                element_map.append([self._code[i], level, current_line, current_char_pos])
                i += 1
                current_char_pos += 1
            elif self._code[i].strip() and self._code[i] not in [',', ':',' ', '\n']:  # Нашли ключ или значение
                # Ищем конец ключа или значения
                end_pos = i
                while end_pos < len(self._code) and self._code[end_pos] not in [',', ':', '}', ']', '\n', ' ', '"']:
                    end_pos += 1
                element = self._code[i:end_pos].strip()
                element_map.append([element, level, current_line, current_char_pos])
                i = end_pos
                current_char_pos += len(element)
            else:  # Пропускаем пробелы, запятые и другие символы
                i += 1
                current_char_pos += 1

        return element_map # , i, current_line, current_char_pos

    def print_bracket_map(self, file_path):
        """
        Читает JSON-файл и выводит карту скобок.
        :param file_path: Путь к файлу.
        """
        try:
            # Получаем карту скобок через геттер
            bracket_map = self.get_bracket_map()

            # Если не удалось получить карту — выходим
            if bracket_map is None:
                return None

            # Создаем директорию для файла, если необходимо
            dir_name = os.path.dirname(file_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            # Записываем карту в указанный файл в формате JSON
            with open(file_path, 'w', encoding='utf-8') as out_f:
                json.dump(bracket_map, out_f, ensure_ascii=False, indent=4)

            return bracket_map
        except Exception as e:
            try:
                self._log_error(f"Ошибка при формировании/записи карты скобок '{file_path}': {e}")
            except Exception:
                pass

    def get_bracket_map(self):
        """Возвращает карту скобок, не выводя её и не записывая в файл."""
        try:
            bracket_map = self._simple_parse_brackets()
            return bracket_map
        except Exception as e:
            try:
                self._log_error(f"Ошибка при формировании карты скобок: {e}")
            except Exception:
                pass
            return None
