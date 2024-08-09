class Notes:
    def insert(self, file_path: str, note_path: str):
        with open(file_path, "r") as f:
            with open(note_path, "w") as n:
                n.write(f.read())
