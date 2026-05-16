class ConfigParser:
    def __init__(self):
        self._data = {}
        print("Loaded custom configparser")

    def read(self, filename):
        self._data = {}
        try:
            with open(filename, 'r') as f:
                current_section = None
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or line.startswith(';'):
                        continue
                    if line.startswith('[') and line.endswith(']'):
                        current_section = line[1:-1].strip()
                        self._data[current_section] = {}
                    elif '=' in line and current_section:
                        key, val = line.split('=', 1)
                        self._data[current_section][key.strip()] = val.strip()
            return [filename]
        except OSError:
            return []

    def add_section(self, section):
        if section not in self._data:
            self._data[section] = {}

    def sections(self):
        return list(self._data.keys())

    def __getitem__(self, section):
        if section not in self._data:
            raise KeyError(section)
        return self._data[section]

    def __contains__(self, section):
        return section in self._data

    def write(self, file_object):
        for section, options in self._data.items():
            file_object.write(f"[{section}]\n")
            for key, val in options.items():
                file_object.write(f"{key} = {val}\n")
            file_object.write("\n")
