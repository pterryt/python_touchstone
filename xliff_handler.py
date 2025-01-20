class XliffEntry:
    def __init__(self, entry_id: int, source:str, target = "") :
        self.id = entry_id
        self.source = source
        self.target = target

class XliffFile:
    def __init__(self, name:str, original_doc: str):
        self.name = name
        self.original_doc = original_doc
        self.entries = []

    def add_entry(self, entry: XliffEntry):
        self.entries.append(entry)

    def save_file(self):
        outer_template_path = "../xliff_templates/OuterTemplate.xliff"
        entry_template_path = "../xliff_templates/OuterTemplate.xliff"

    def load_xliffs(self):
        pass
