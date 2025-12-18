from abc import ABC, abstractmethod

class CommandNode(ABC):
    def __init__(self, name, value_type, action, line, char_pos, command_path, file):
        self._name = name  # Имя команды (ключ в JSON)
        self._value_type = value_type  # Ожидаемый тип значения (list, dict, int, str и т.д.)
        self._action = action  # Значение команды (то, что после ":")
        self._line = line  # Номер строки
        self._char_pos = char_pos  # Позиция символа
        self._command_path = command_path  # Путь к команде
        self._file = file  # Файл, откуда взята команда
        self._errors = []  # Список для хранения ошибок

    @abstractmethod
    def Errors(self):
        """Абстрактный метод для проверки ошибок. Должен быть реализован в наследниках."""
        pass

    def get_cmd_path(self):
        return self._command_path

    def get_line(self):
        return self._line

    def get_char_pos(self):
        return self._char_pos

    def _collect_error_chain(self):
        """Собирает цепочку контекстов ошибок от корня до текущего узла.
        Сейчас нет явной структуры родителей, поэтому возвращаем только текущий узел.
        В будущем можно расширить, чтобы трассировать реальные вложенные файлы/контексты.
        """
        return [(self._file, self._line, self._char_pos, self._name)]

    def _format_error_line(self, file, line, pos, name, message):
        file_str = file if file is not None else "<неизвестен>"
        line_str = str(line) if line is not None else "<не найдена>"
        pos_str = str(pos) if pos is not None else "<не найдена>"
        return f"-Файл: \'{file_str}\'\n-Команда: {name}\n-Строка: {line_str}\n-Позиция: {pos_str}\n-Текст ошибки: {message}"

    def _log_error(self, message):
        """Форматированный вывод цепочки ошибок в виде нескольких строк.

        Формат:
        Ошибка команды!:
        RootFile, str, pos, command, Ошибка: <текст ошибки>
        InnerFile, str, pos, command, Ошибка: <текст ошибки>
        ...

        Пустая строка в конце для разделения.
        """
        chain = self._collect_error_chain()
        formatted_lines = ["Ошибка синтаксиса!" ]
        for file, line, pos, name in chain:
            formatted_lines.append(self._format_error_line(file, line, pos, name, message))
        formatted_lines.append("")  # пустая строка для разделения
        self._errors.extend(formatted_lines)

    def _type_check(self):
        """Проверка, соответствует ли тип значения ожидаемому."""
        if not isinstance(self._action, self._value_type):
            self._log_error(f"Ожидался тип команды {self._name} = {self._value_type}, получен {type(self._action)}.")
            return False
        return True

    def get_errors(self):
        """Возвращает список ошибок."""
        return self._errors
