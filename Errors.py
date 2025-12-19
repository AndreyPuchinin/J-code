class ValidationError(Exception):
    """Structured validation error that carries a path to the problem.

    - message: human-readable message
    - path: list of path steps (keys and indices) describing location inside JSON
    - file, line, char_pos: optional source location of the command that owns this path
    """
    def __init__(self, message, path=None, file=None, line=None, char_pos=None,
                 param_substring=None, param_subposition=None, command=None):
        super().__init__(message)
        self.message = message
        self.path = list(path) if path is not None else []
        self.file = file
        self.line = line
        self.char_pos = char_pos
        # новые поля: индекс подстроки параметра (1-based, если применимо)
        # и позиция символа в исходнике для этой подстроки параметра
        self.param_substring = param_substring
        self.param_subposition = param_subposition
        self.command = command

    def format_lines(self):
        """Return formatted lines (list of strings) consistent with existing logging format."""
        lines = ["Ошибка синтаксиса!"]
        # Первая строка: файл/строка/позиция/имя команды, если присутствуют
        file_str = self.file if self.file is not None else "<неизвестен>"
        line_str = str(self.line) if self.line is not None else "<не найдена>"
        pos_str = str(self.char_pos) if self.char_pos is not None else "<не найдена>"

        # Если есть структурированный путь, включаем информацию о подстроке параметра
        if self.path:
            # объединяем шаги пути через '/'
            path_repr = '/'.join(map(str, self.path))
            lines.append(f"-Файл: '{file_str}'")
            # включаем имя команды, если оно передано
            if self.command is not None:
                lines.append(f"-Команда: {self.command}")
            lines.append(f"-Строка: {line_str}")
            lines.append(f"-Позиция: {pos_str}")
            if self.param_substring is not None:
                lines.append(f"-Подстрока параметра: {self.param_substring}")
            else:
                lines.append(f"-Подстрока параметра: {path_repr}")
            if self.param_subposition is not None:
                lines.append(f"-Подпозиция параметра: {self.param_subposition}")
            else:
                lines.append(f"-Подпозиция параметра: <не найдена>")
            lines.append(f"-Текст ошибки: {self.message}")
        else:
            # если структурированный путь отсутствует — всё равно выводим команду (если есть)
            if self.command is not None:
                lines.append(f"-Файл: '{file_str}'\\n-Команда: {self.command}\\n-Строка: {line_str}\\n-Позиция: {pos_str}\\n-Текст ошибки: {self.message}")
            else:
                lines.append(f"-Файл: '{file_str}'\\n-Строка: {line_str}\\n-Позиция: {pos_str}\\n-Текст ошибки: {self.message}")

        lines.append("")
        return lines
