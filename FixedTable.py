### The Table Class
        
class Table:
    def __init__(
        self,
        content,
        space_left=1,
        space_right=1,
        orientation="left",
        min_width=None,
        max_width=None,
        same_sized_cols=False,
        empty_cells=["", "#empty"],
        empty_lists=[[], [""], ["#empty"]],
        replace_empty="",
        header={},
    ):
        
        """
        Initialize a Table object with specified parameters

        Args:
        - content: content of the table in a list_in_list, list_in_dict, dict_in_list or dict_in_dict structure
        - space_left: int: space from the content of a cell to its border on the left side
        - space_right: int: space from the content of a cell to its border on the right side
        - orientation: str: "left" or "right" | orientates the content to the left or to the right side of the cell
        - min_width: int: minimum width of a cell. spaces will be added when to short
        - max_width: int: maximum width of a cell. content will be shortened when to long
        - same_sized_cols: bool: toggles same width for each column
        - fill_with_empty_rows: bool: toggles filling empty rows for every not specified row in content
        - fill_with_empty_columns: bool: toggles filling empty columns for every not specified column in content
        - empty_cells: list: specifies what is considered as an empty cell
        - empty_lists: specifies what is considered as an empty list
        - empty_dicts: specifies what is considered as an empty dict
        - replace_empty: str: replaces empty cells and the content of empty lists and dicts with this str
        - header: dict {header_type:[header]}: header_type: str: "row" or "col", "header": list or dict: content of the header
        """

        self.content = content 
        self.space_left = space_left 
        self.space_right = space_right 
        self.orientation = orientation 
        self.min_width = min_width 
        self.max_width = max_width 
        self.same_sized_cols = same_sized_cols 
        self.empty_cells = empty_cells 
        self.empty_lists = empty_lists 
        self.replace_empty = replace_empty 
        self.default_header = []
        self.header = header
    
    def clean_data(self):
        for index, row in enumerate(self.content):
            if row in self.empty_lists:
                self.content[index] = [self.replace_empty]
            else:
                for index2, cell in enumerate(row):
                    if cell in self.empty_cells:
                        self.content[index][index2] = self.replace_empty
            while len(row) < max([len(i) for i in self.content]):
                self.content[index].append(self.replace_empty)


    def get_content(self):
        return self.content
    
    def get_row(self, row):
        return self.content[row]
    
    def get_column(self, column):
        return [i[column] for i in self.content]
    
    def get_cell(self, row, column):
        return self.content[row][column]
    
    def replace_content(self, content):
        self.content = content
            
    def replace_column(self, index, content):
        for row_index, i in enumerate(content):
            self.content[row_index][index] = i

    def replace_row(self, index, content):
        self.content[index] = content

    def replace_cell(self, col, row, content):
        self.content[row][col] = content

    def add_row(self, row, content):
        if str(row) == "-1":
            row = "end"
        elif row < 0:
            row += 1
        
        if row == "end":
            self.content.append(content)
        else:
            self.content.insert(row, content)

    def add_column(self, column, content):
        if str(column) == "-1":
            column = "end"
        elif column < 0:
            column += 1
        for index, i in enumerate(content):
            if column == "end":
                self.content[index] = i
            else:
                self.content[index].insert(column, i)

    def remove_row(self, row):
        self.content.pop(row)

    def remove_column(self, column):
        for i in self.content:
            i.pop(column)

    def sort_col(self, col, reverse=False):
        column = [i[col] for i in self.content]
        column = sorted(column, reverse=reverse)
        for index, i in enumerate(column):
            self.content[index] = i
    
    def sort_row(self, row, reverse=False):
        self.content[row] = sorted(self.content[row], reverse=reverse)
    
    def sort_on_col(self, column, reverse=False):
        self.content = sorted(self.content, key=lambda x: x[column], reverse=reverse)

    def sort_on_row(self, row, reverse=False):
        to_be_sorted_row = self.get_content()[row]
        other_rows = [sublist for i, sublist in enumerate(self.get_content()) if i != row]

        sorted_indices = sorted(range(len(to_be_sorted_row)), key=lambda k: to_be_sorted_row[k], reverse=reverse)

        sorted_row = [to_be_sorted_row[i] for i in sorted_indices]
        sorted_other_rows = [[lst[i] for i in sorted_indices] for lst in other_rows]

        sorted_other_rows.insert(row, sorted_row)

        self.content = sorted_other_rows

    def swap_cols_rows(self):
        self.content = list(map(list, zip(*self.content)))

    def add_header(self, header_type, header_content):
        self.header[header_type] = header_content

    def replace_header(self, header_type, header_content):
        self.add_header(header_type, header_content)

    def remove_header(self, header_type):
        if header_type in self.header:
            del self.header[header_type]

    def use_row_as_header(self, row):
        self.replace_header("row", self.get_row(row))
        self.remove_row(row)
    
    def use_column_as_header(self, column):
        self.replace_header("col", self.get_column(column))
        self.remove_column(column)
    
    def display(self):
        
        self.rows = len(self.content)
        self.columns = 0
        for row in self.content:
            if len(row) > self.columns: 
                self.columns = len(row)

        for header, content in self.header.items():
            if content == ["#default"]:
                if header not in self.default_header:
                    self.default_header.append(header)

        for header in self.header.keys():
            if header in self.default_header:
                if header == "row":
                    self.header["row"] = [f"{i+1}." for i in range(self.columns)]
                if header == "col":
                    self.header["col"] = [f"{i+1}." for i in range(self.rows)]
        display_content = self.content
        if "col" in self.header and "row" in self.header:
            display_content = [[i] + self.content[index] for index, i in enumerate(self.header["col"])]
            display_content = [[""] + self.header["row"]] + display_content
            self.rows += 1
            self.columns += 1
        elif "col" in self.header:
            for index, i in enumerate(self.header["col"]):
                display_content[index].insert(0, i)
            self.columns += 1
        elif "row" in self.header:
            display_content.insert(0, self.header["row"])
            self.rows += 1
        
        
        self.max_chars = []
        for cell in range(self.columns): 
            self.max_chars.append(0)
        for row in display_content: 
            active_column = 0
            for cell in row:
                if len(str(cell)) > self.max_chars[active_column]: 
                    self.max_chars[active_column] = len(str(cell))
                active_column += 1

        if self.min_width != None:
            for index, i in enumerate(self.max_chars):
                if self.min_width > int(i):
                    self.max_chars[index] = self.min_width
        
        if self.max_width != None:
            for index, i in enumerate(self.max_chars):
                if self.max_width < int(i):
                    self.max_chars[index] = self.max_width

        if self.same_sized_cols:
            self.max_chars = [max(self.max_chars) for i in self.max_chars]

        column_index = 0  
        print("╔", end="")
        for column in self.max_chars:
            print("═" * self.space_left, end="")  
            print("═" * column, end="")  
            print("═" * self.space_right, end="")  
            
            if column_index == len(self.max_chars) - 1:  
                print("╗")
            
            else:
            
                if "col" in self.header and column_index == 0:
                    print("╦", end="")
            
                else:
                    print("╤", end="")  
            
            column_index += 1  
        row_index = 0
        for row in range(self.rows): 
            print("║", end="") 
            column_index = 0

            for column in range(self.columns):

                spacebar_counter = self.max_chars[column] - len(str(display_content[row][column])) 
                text = str(display_content[row][column])

                if len(text) > self.max_chars[column_index]:

                    if self.max_chars[column_index] == 2:
                        text = ".."
                    elif int(self.max_chars[column_index]) == 3:
                        text = [i for i in text]
                        text = text[0]
                        text += ("..")
                    
                    elif int(self.max_chars[column_index]) >= 3:
                        text = [i for i in text]
                        text = text[:int(self.max_chars[column_index])-2]
                        text.append("..")
                        textstr = ""
                        for i in text:
                            textstr += i
                        text = textstr
                    spacebar_counter = 0
                
                if self.orientation == "left": 
                    content = text + str(spacebar_counter * " ")  
                
                elif self.orientation == "right":
                    content = str(spacebar_counter * " ") + text 

                print(" " * self.space_left, end="")
                print(content, end="")
                print(" " * self.space_right, end="")
                
                if column_index == self.columns - 1: 
                    print("║") 
                else:
                    if "col" in self.header and column_index == 0:
                        line = "║"
                    else:
                        line = "│" 
                    print(line, end="")
                column_index += 1  
            
            if row_index == 0 and "row" in self.header: 
                left_border = "╠"
                connection = "═"
                right_border = "╣"
                cross_connection = "╪"

            elif row_index == self.rows - 1:
                left_border = "╚"
                connection = "═"
                right_border = "╝"
                cross_connection = "╧"

            else:
                left_border = "╟"
                connection = "─"
                right_border = "╢"
                cross_connection = "┼"

            print(left_border, end="") 
            column_index = 0
        
            for column in self.max_chars: 
                print(connection * self.space_left, end="")
                print(column * connection, end="") 
                print(connection * self.space_right, end="") 
                
                if column_index == len(self.max_chars) - 1: 
                    print(right_border)
                
                else:
                
                    if "col" in self.header and column_index == 0:
                
                        if row_index == self.rows - 1:
                            print("╩", end="")
                
                        elif "row" in self.header and row_index == 0:
                            print("╬", end="")
                
                        else:
                            print("╫", end="")
                
                    else:
                        print(cross_connection, end="") 

                column_index += 1

            row_index += 1

table = Table([[1], [1, 2, 3], [1, 2]])
table.clean_data()
table.use_row_as_header(0)
table.display()