import hash
import os

template_dir = "xliff_templates"
outer_template = "OuterTemplate.xliff"
entry_template = "EntryTemplate.xliff"
output_dir = "output"

def load_template(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

class XliffEntry:
    def __init__(self, source:str, target = "") :
        self.entry_hash = hash.hash_string(source)
        self.source = source
        self.target = target

    def to_xml(self):
        template = load_template(os.path.join(template_dir, entry_template))
        return template.format(id=self.entry_hash,source=self.source, target = self.target)

class XliffFile:
    def __init__(self, name:str, entries = None):
        self.name = name
        self.entries = entries if entries else list()

    def add_entry(self, entry: XliffEntry):
        self.entries.append(entry)

    def to_xml(self):
        template = load_template(os.path.join(template_dir, outer_template))
        combined_entries = "\n".join([entry.to_xml() for entry in self.entries])
        return template.format(original=self.name + ".json", trans_units=combined_entries)

    def write_to_file(self):
        file_name = self.name + ".xliff"
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
            f.write(self.to_xml())