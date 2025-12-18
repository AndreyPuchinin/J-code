import json
from CommandNode import CommandNode

class CommandInclude(CommandNode):
    def __init__(self, name, value_type, action, line, char_pos, cmd_path, file):
        super().__init__(name, value_type, action, line, char_pos, cmd_path, file)

    def _file_exists_check(self):
        """Проверка, что файл существует."""
        try:
            with open(self._action, 'r') as _:
                return True
        except:
            self._log_error(f"Файл '{self._action}' не найден.")
            return False

    def _file_is_valid_json_check(self):
        """Проверка, что файл является валидным JSON."""
        try:
            with open(self._action, 'r') as file:
                json.load(file)
                return True
        except json.JSONDecodeError as e:
            self._log_error(f"Ошибка в файле '{self._action}': {e}")  # Логируем конкретную ошибку JSON
            return False

    def Errors(self):
        """Реализация метода Errors для команды include."""
        if self._type_check():  # Проверка типа
            if self._file_exists_check():  # Проверка существования файла
                self._file_is_valid_json_check()  # Проверка валидности JSON
        return self.get_errors()
