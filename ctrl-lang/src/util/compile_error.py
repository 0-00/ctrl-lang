
class CompileException(Exception):
    def __init__(self, msg, src_pos_line, src_pos_col, src_pos_length):
        self.msg = msg
        self.src_pos_line = src_pos_line
        self.src_pos_col = src_pos_col
        self.src_pos_length = src_pos_length
        super().__init__("")