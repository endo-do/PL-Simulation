def restructure(data, structure, fill_with_empty_columns=None, fill_with_empty_rows=None, empty_dicts=None, empty_lists=None, empty_cells=None, replace_empty=None):
    
    """
    Restructures and cleanes the given data based on the specified structure

    Args:
    - data: The data to be restructured
    - structure: The desired form in which data will be restructured (e.g., 'list' or 'list_in_list')
    - fill_with_empty_columns: If True, adds columns that are not specified in the given data, otherwise skips them during table printing
    - fill_with_empty_rows: If True, adds rows that are not specified in the given data, otherwise skips them during table printing
    - empty_dicts: Specifies how an empty dict looks like
    - empty_lists: Specifies how an empty list looks like
    - empty_cells: Specifies how an empty cell looks like
    - replace_empty: Content to replace when an empty dict/list/cell is specified

    Returns:
    - The restructured and cleaned data.
    """

    # If the data is an empty list return a list with the specified 'replace_empty' var
    if data in empty_lists:
        if structure == "list":
            return [replace_empty]
        elif structure == "list_in_list":
            return [[replace_empty]]
    
    else:
        
        # Get the structure of the data with the 'type()' function
        data_type = type(data) 
        if data_type is list:
            element_type = type(data[0])
        elif data_type is dict:
            element_type = type(next(iter(data.values())))

        # Restructers the data into a list
        if structure == "list":    
            data_structure = data_type.__name__

            # Handle if the data is a structured as a dictionary
            if data_structure == "dict":            

                # Handles 'fill_with_empty_columns' as specified
                if fill_with_empty_columns:
                    columns = list(data.keys())
                    columns = sorted(columns)
                    if len(columns) >= 2:
                        for i in range(columns[0], columns[-1]):
                            if i not in columns:
                                data[i] = replace_empty

                # Sorts the dictionary and restructeres it to a list
                data = dict(sorted(data.items()))
                data = [i for i in list(data.values())]
            
            # Replaces any cell that was specified as empty in the 'empty_cells' list with the given 'replace_empty' var
            for index, i in enumerate(data):
                if i in empty_cells:
                    data[index] = replace_empty

            # Returns the restructured and cleaned data as a list
            return data
        
        # Restructures the data into a list_in_list structure
        if structure == "list_in_list":
            data_structure = f"{element_type.__name__}_in_{data_type.__name__}"

            # Handle if the data is structured as a dict_in_list
            if data_structure == "dict_in_list":

                # Handles 'fill_with_empty_rows' as specified
                if fill_with_empty_rows:
                    rows = [key for d in data for key in d]
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data.append({row:[]})
                
                # Sorts the given data and creates a new list for the cleaned data
                new_content = []
                data = sorted(data, key=lambda d: next(iter(d)))

                # Restructures the given data and replaces any dict that was specified as empty in 'empty_dits' with the given 'replace_empty' var
                for line in data:    
                    if any(str(val) in empty_dicts for val in line.values()):
                        new_content.append([replace_empty])
                    else:
                        new_content.append([char for char in line.values()])
                
                # Replaces the old data with the cleaned and restructured one
                data = new_content

            # Handle if the data is structured as a 'list_in_dict'
            elif data_structure == "list_in_dict":
                
                # Handles 'fill_with_empty_rows' as specified
                if fill_with_empty_rows:
                    input(data)
                    rows = list(data.keys())
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data[row] = []
                
                # Sorts the given data and creates a new list for the cleaned data
                new_content = []
                data = dict(sorted(data.items()))
                
                # Restructures the given data and replaces any list that was specified as empty in 'empty_lists' with the given 'replace_empty' var
                for line in data.values():
                    if line in empty_lists:
                        new_content.append([replace_empty])
                    else:
                        new_content.append(line)
                
                # Replaces the old data with the cleaned and restructured one
                data = new_content

            # Handle if the data is structured as a 'dict_in_dict'
            elif data_structure == "dict_in_dict":
                
                # Handles 'fill_with_empty_rows' as specified
                if fill_with_empty_rows:
                    rows = list(data.keys())
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data[row] = {}
                
                # Handles 'fill_with_empty_columns' as specified
                if fill_with_empty_columns:
                    for key, row in data.items():
                        columns = list(row.keys())
                        if len(columns) >= 2:
                            for col in range(columns[0], columns[-1]):
                                if col not in columns:
                                    data[key][col] = replace_empty
                
                # Sorts the given data and creates a new list for the cleaned data
                new_content = []
                data = {k: dict(sorted(v.items())) if isinstance(v, dict) else v for k, v in sorted(data.items())}

                # Restructures the given data and replaces any list that was specified as empty in 'empty_lists' with the given 'replace_empty' var
                for line in data:
                    if data[line] in empty_dicts:
                        new_line = [replace_empty]
                    else:
                        new_line = []
                        for cell in data[line].values():
                            if str(cell) in empty_cells:
                                cell = replace_empty
                            new_line.append(cell)
                    new_content.append(new_line)
                
                # Replaces the old data with the cleaned and restructured one
                data = new_content
            
            # Replaces any cell that was specified as empty in the 'empty_cells' list with the given 'replace_empty' var
            new_content = []
            for line in data:
                new_content.append([str(char) if str(char) not in empty_cells else replace_empty for char in line])
                data = new_content 
            
            # Returns the restructured and cleaned data as a 'list_in_list'
            return data



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
        fill_with_empty_rows=True,
        fill_with_empty_columns=True,
        empty_cells=["", "#empty"],
        empty_lists=[[], [""], ["#empty"]],
        empty_dicts=[{}, {""}, {"#empty"}],
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
        self.fill_with_empty_rows = fill_with_empty_rows 
        self.fill_with_empty_columns = fill_with_empty_columns 
        self.empty_cells = empty_cells 
        self.empty_lists = empty_lists 
        self.empty_dicts = empty_dicts 
        self.replace_empty = replace_empty 
        self.default_header = []
        self.header = header

        self.content = restructure(self.content, "list_in_list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)

    def replace_content(self, content):
        self.content = restructure(content, "list_in_list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)
            
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
                    self.header["row"] = [f"{i}." for i in range(self.columns)]
                if header == "col":
                    self.header["col"] = [f"{i}." for i in range(self.rows)]
            
        display_content = self.content
        if "col" in self.header and "row" in self.header:
            for index, i in enumerate(self.header["col"]):
                display_content[index].insert(0, i)
            display_content.insert(0, [""] + self.header["row"])
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
        
        # Set a minimum width for each column if specified
        if self.min_width != None:
            for index, i in enumerate(self.max_chars):
                if self.min_width > int(i):
                    self.max_chars[index] = self.min_width
        
        # ... maximum ...
        if self.max_width != None:
            for index, i in enumerate(self.max_chars):
                if self.max_width < int(i):
                    self.max_chars[index] = self.max_width

        # Implement the same size for each column if specified
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

        # Print each row
        for row in range(self.rows): 
            print("║", end="") 
            column_index = 0

            # For each cell in row
            for column in range(self.columns):
                
                # Calculate amount of spaces to add to content to ensure correct sizing of the cell
                spacebar_counter = self.max_chars[column] - len(str(display_content[row][column])) 
                text = str(display_content[row][column])

                # Handle if content is larger than max width
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
                
                # Handle left orientation
                if self.orientation == "left": 
                    content = text + str(spacebar_counter * " ")  
                
                # ... right ...
                elif self.orientation == "right":
                    content = str(spacebar_counter * " ") + text 

                # Print the cell
                print(" " * self.space_left, end="")
                print(content, end="")
                print(" " * self.space_right, end="")
                
                # Handle the vertical separators between cells and the right border
                if column_index == self.columns - 1: 
                    print("║") 
                else:
                    if "col" in self.header and column_index == 0:
                        line = "║"
                    else:
                        line = "│" 
                    print(line, end="")
                column_index += 1  
            
            # Handle the horizontal sperators between rows and the bottom border
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

            # Print the horizontal separators
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


TestTable = Table([[1, 2, 3], [4, 5, 6], [7, 8, 9]], header={"col":["#default"], "row":["#default"]})
# TestTable.display()