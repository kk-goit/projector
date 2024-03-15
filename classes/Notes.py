from collections import UserDict, defaultdict
from classes.Fields import *

class Notes(UserDict[int, Note]):
    def __init__(self):
        super().__init__()
        self.max_index = 0

    def __get_by_index(self, index: str) -> Note:
        if self.data.get(self.__parse_index(index)):
            return self.data.get(index)

        raise KeyError(f"There is no note with an index {index}")

    def __parse_index(self, index: str) -> int:
        try:
            index = int(index)
            if index > 0:
                return index
            else:
                raise IncorrectNoteIndexError("Index can't be < 1.")
        except ValueError:
            raise IncorrectNoteIndexError("Index should be an integer.")

    def add(self, note: Note):
        self.data[self.max_index + 1] = note
        self.max_index += 1
        return self.max_index

    def delete(self, index: str):
        del self.data[self.__parse_index(index)]

    def list(self, data: dict[int, Note] = None):
        data = self.data if data is None else data
        if len(data) > 0:
            listed = ""
            for index, note in data.items():
                listed += f"{index} - {note.get_preview()}\n"
            return listed
        else:
            raise NotesNotFoundError("Unable to locate any notes.")  # TODO; make it better for search

    def search(self, substr: str):
        matched: dict[int, Note] = {}
        for index, note in self.data.items():
            if substr in str(note):
                matched[index] = note

        return self.list(matched)

    def show(self, index: str):
        return str(self.__get_by_index(index))

    def change_note(self, index: str, new_text: str):
        if new_text == '':
            raise IncorrectFormatException("Note can't be empty")
        self.data[self.__parse_index(index)] = Note(new_text)
        
        
