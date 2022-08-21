class TreeNode:
    def __init__(self, text, children):
        self.text = text
        self.children = children

    def get_rows(self):
        try:
            row = 0
            if not self.children:
                return 1
            for child in self.children:
                row += child.get_rows()
            return row
        except:
            print("error with node:", self.text, self.children)

    def get_cols(self):
        try:
            col = 0
            for child in self.children:
                col = max(child.get_cols(), col)
            return col + 1
        except:
            print("error with node:", self.text, self.children)

    def get_text_length(self):
        try:
            max_text = len(self.text)
            for child in self.children:
                max_text = max(child.get_text_length(), max_text)
            return max_text
        except:
            print("error with node:", self.text, self.children)


class TreeDrawing:
    def __init__(self, root):
        self.row = 0
        self.tree = root
        self.cols = root.get_cols()
        self.rows = root.get_rows()
        self.text_length = root.get_text_length() + 2
        self.table = [[None for i in range(self.cols)] for j in range(self.rows)]
        self.last_children = []
        self.traverse(root, 0)

    def traverse(self, node, depth):
        self.table[self.row][depth] = node
        if not node.children:
            self.row += 1
            return
        for child in node.children:
            self.traverse(child, depth + 1)
        self.last_children.append(node.children[-1])

    def __str__(self):
        s = ""
        ends_table = [["" for i in range(self.cols)] for j in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                end = " "
                if i > 0 and (ends_table[i - 1][j] == "┬"
                              or ends_table[i - 1][j] == "│"
                              or ends_table[i - 1][j] == "├"):
                    end = "│"

                if self.table[i][j]:
                    if len(self.table[i][j].children) > 1:
                        end = "┬"
                    elif len(self.table[i][j].children) == 1:
                        end = "─"
                else:
                    if j < self.cols - 1 and self.table[i][j+1]:
                        if self.table[i][j+1] in self.last_children:
                            end = "└"
                        else:
                            end = "├"
                ends_table[i][j] = end

        for i in range(self.rows):
            for j in range(self.cols):
                end = ends_table[i][j]
                if self.table[i][j]:
                    text = self.table[i][j].text
                    s += "─" * (self.text_length - len(text)) + text + end
                else:
                    s += " " * self.text_length + end
            s += "\n"
        return s
