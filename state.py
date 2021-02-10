class State:

    def __init__(self, type):
        if type == "GB":
            self.division_type = "Gb"
            self.division_value = 1000000000
        elif type == "MB":
            self.division_type = "Mb"
            self.division_value = 1000000
        elif type == "KB":
            self.division_type = "Kb"
            self.division_value = 1000
        elif type == "B":
            self.division_type = "Bytes"
            self.division_value = 0
        else:
            self.division_type = "Bytes"
            self.division_value = 0