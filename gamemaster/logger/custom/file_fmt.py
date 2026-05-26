from .date_fmt import _DEFAULT_DATE_FMT, _DateFormatter


class FileFormatter(_DateFormatter):
    def __init__(self):
        super().__init__("%(asctime)-26s - %(levelname)-8s - [ %(name)s ] %(message)s",
                         _DEFAULT_DATE_FMT)
