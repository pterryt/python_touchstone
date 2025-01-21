import hash
import os

template_dir = "xliff_templates"
outer_template = "OuterTemplate.xliff"
entry_template = "EntryTemplate.xliff"
output_dir = "output"

# load the template from file
def load_template(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

# class for holding the data for each translation unit
class XliffEntry:
    def __init__(self, source:str, target = "") :
        self.entry_hash = hash.hash_string(source)
        self.source = source
        self.target = target

    # function for converting the item to xml
    def to_xml(self):
        template = load_template(os.path.join(template_dir, entry_template))
        return template.format(id=self.entry_hash,source=self.source, target = self.target)

# class for holding multiple xliff entries
# could be a seen as xliff equivalent of a database
class XliffFile:
    def __init__(self, name:str, entries = None):
        self.name = name
        self.entries = entries if entries else list()

    # just a simple interface for adding a file
    def add_entry(self, entry: XliffEntry):
        self.entries.append(entry)

    # function for converting the all the entries in the xliff object to a single file
    def to_xml(self):
        # templates are in the template folder and are the basis for what our xliffs will look like
        # consider them just the text of the final product but with empty spaces denoted by {variable name}
        # where we can enter variables
        # using pythons built-in format function with templates is easier the files from scratch
        template = load_template(os.path.join(template_dir, outer_template))
        combined_entries = "\n".join([entry.to_xml() for entry in self.entries])
        return template.format(original=self.name + ".json", trans_units=combined_entries)

    # after to_xml converts to data to the correct format, we save it to file with this function
    def write_to_file(self):
        file_name = self.name + ".xliff"
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, file_name), "w", encoding="utf-8") as f:
            f.write(self.to_xml())