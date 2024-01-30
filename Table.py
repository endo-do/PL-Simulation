"""
Documentation:
- The term "column" may be abbreviated to 'col' for brevity
- Each function will include a brief introduction explaining its general purpose and detailing each argument
- In the Argument Explanation section of a function, data types may be referenced to prevent potential ValueErrors

Sources:
- Box Drawing Characters: https://en.wikipedia.org/wiki/Box-drawing_character

"""


### General Functions

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
        self.header = header
        
        # Set the header_actions vars to 'insert'
        self.header_action_col = "calculate"
        self.header_action_row = "calculate"

        # Restructure the given content to a 'list_in_list'
        self.content = restructure(self.content, "list_in_list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)
        
    
    def sort_on_col(self, column):
        sorted_content = sorted(self.get_content(), key=lambda x: x[column], reverse=True)
        self.replace_content(sorted_content)

    def sort_on_row(self, row):
        to_be_sorted_row = self.get_content()[row]
        other_rows = [sublist for i, sublist in enumerate(self.get_content()) if i != row]

        sorted_indices = sorted(range(len(to_be_sorted_row)), key=lambda k: to_be_sorted_row[k])

        # Reorder the other lists based on the sorted indices
        sorted_row = [to_be_sorted_row[i] for i in sorted_indices]
        sorted_other_rows = [[lst[i] for i in sorted_indices] for lst in other_rows]

        sorted_other_rows.insert(row, sorted_row)

        self.replace_content(sorted_other_rows)
    
    
    def add_row(self, index, row):
        
        """
        Adds a row at specified index into the content of the tablet

        Args:
        - index: int: specifies at what index the column will be added
        - row: the content of the new row in a dict or list structure
        
        """

        # Manages the index handling addressing the fact that using insert(-1) doesn't insert at the last position
        # Replaces -1 with "end" and subtracts -1 when the index is negative, ensuring accurate placement.
        if index == -1:
            index = "end"
        else:
            if index < 0:
                index += 1
            # Offset the index by 1 when the row header is active to insert the content accurately
            if "row" in self.header:
                index += 1
        
        # Restructure the row's content to a list structure
        row = restructure(row, "list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)
        
        # Add a place holder header if 'col' header is active to prevent errors later on when handling the headers
        if "col" in self.header:
            row.insert(0, "")
        
        # Handle inserting at last place due to insert function as explained above
        if index == "end":
            self.content.append(row)
        else:
            self.content.insert(index , row)
        
        # Set the headers to update later on
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"

        self.update()

   
    def add_column(self, index, column):

        """
        Adds a column at specified index into the content of the table
        
        Args:
        - index: int: specifies at what index the column will be added
        - column: the content of the new row in a dict or list structure
        """

        # ...
        if index == -1:
            index = "end"
        else:
            if index < 0:
                index += 1
            # ... column ...
            if "col" in self.header:
                index += 1
        
        # ...
        column = restructure(column, "list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)
        
        # ...
        if "row" in self.header:
            column.insert(0, "")
        
        # ...
        for i in range(len(column)):
            if index == "end":
                self.content.append(column[i])
            else:
                self.content[i].insert(index, column[i])
        
        # ...
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"

        self.update()


    def remove_row(self, index):
        
        """
        Removes the row at specified index from the table

        Args:
        - index: int: specifies which row will be removed
        """
        
        # Offset the index by one when row header is active to remove the correct row
        if "row" in self.header:
            index += 1

        # Remove the specified row
        self.content.pop(index)
        
        # ...
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"


    def remove_column(self, index):
        
        """
        removes the column at specified index from the table
        
        Args:
        - index: int: specifies which column will be removed
        """

        # ... column ... column
        if "col" in self.header:
            index += 1
        
        # ... column
        for i in self.content:
            i.pop(index)
        
        # ...
        if "col" in self.header:
            self.header_action_col = "update"
        if "row" in self.header:
            self.header_action_row = "update"


    def replace_content(self, content):
        self.content = restructure(content, "list_in_list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)
        
        if "row" in self.header:
            self.header_action_row = "insert"

        if "col" in self.header:
            self.header_action_col = "insert"


    def replace_row(self, index, row=None):
        """
        Replaces the row at specified index with given content

        Args:
        - index: int: specifies which row will be replaced
        - row: content of the new row
        """
    
        # If row var was not specified it will be replaced with standart empty content specified in the table
        if column == None:
            column = [self.replace_empty]

        # Remove the existing row and add the new row at given index
        self.remove_row(index)
        self.add_row(index, row)


    def replace_column(self, index, column=None):
        """
        Replaces the column at specified index with given content

        Args:
        - index: int: specifies which column will be replaced
        - column: content of the new column
        """

        # ... column ...
        if column == None:
            column = [self.replace_empty]

        # ... column ... column ...
        self.remove_column(index)
        self.add_column(index, column)


    def replace_cell(self, row, col, replace=None):
        
        """
        Replaces the content of the specified cell with the specified content
        
        Args:
        - row: int: specifies in which row the cell is in
        - col: int: ... column ...
        - replace: str/int: specifies with what the cell's content will be replaced
        """
        # ... replace ...
        if replace == None:
            replace = self.replace_empty
        
        # Handle index offset due to headers
        if "row" in self.header:
            row += 1
        if "col" in self.header:
            col += 1
        
        # Replace the content
        self.content[row][col] = replace


    def get_content(self):
        """
        Returns the content of the table without the headers in a list_in_list structure

        Returns:
        - content in a list_in_list structure
        """

        content = self.content

        # Remove the 'row' header if active
        if "row" in self.header:
            content.pop(0)

        # Remove the 'col' header if active
        if "col" in self.header:
            for i in content:
                i.pop(0)

        # Return the content of the table
        return content

    
    def get_row(self, index):
        """
        Returns the content of the row at specified index

        Args:
        - index: int: specifies which row will be returned

        Return:
        - content of the specified row in a list
        """

        # Offset the index by 1 if 'row' header is active
        if "row" in self.header:
            index += 1
        
        # Get the content of the row
        row = self.content[index]

        # Return the content
        return row
    

    def get_column(self, index):
        """
        Returns the content of the column at specified index
        
        Args:
        - index: int: specifies which column will be returned

        Return:
        - content of the specified column in a list
        """

        # ... 'col' ...
        if "col" in self.header:
            index += 1

        # ... column
        column = [i[index] for i in self.content]

        # ...
        return column
    

    def get_cell(self, row, col):
        """
        Returns the content of the cell in given row and column
        
        Args:
        - row: int: specifies in which row the cell is
        - col: int: specifies in which col the cell is
        
        Return:
        - content of the specified cell in a string
        """
    
        # Offset the indexes due to active headers
        if "col" in self.header:
            col += 1
        if "row" in self.header:
            row += 1
        
        # ... cell
        cell = self.content[row][col]

        # ...
        return str(cell)
    
    def swap_cols_rows(self):

        """
        Swaps the columns with the rows and vice versa

        """

        # Swap the headers
        if "row" in self.header:
            if "col" in self.header:
                col = self.header["col"][1:]
                self.header["col"] = [""] + self.header["row"]
                self.header["row"] = col
            else:
                self.header["col"] = self.header["row"]
                del self.header["row"]
        elif "col" in self.header:
            self.header["row"] = self.header["col"]
            del self.header["col"]

        # Swap the columns with the rows and vice versa
        self.content = list(map(list, zip(*self.content)))

    
    def get_header(self, header):
        """
        Returns the specified header

        Args:
        - header: str: specifies which active header's content will be returned ('col' or 'row')

        Return:
        - content of the specified header in a list
        """
        
        # If the given header is active
        if header in self.header:
            
            # Get the headers content
            header_content = self.header[header]

            # Return the content
            return header_content
    
    
    def conf_header(self, header, action, content=None, index=None):
        """
        add, remove or edit headers

        Args:
        
        - action: str: 'add', 'remove', 'edit' or fully 'replace' existing header
        - index: int: when editing a specific header specifies the row or column
        """
        
        # Handle removing a header
        if action.lower() == "remove":
            if header in self.header:
                
                # Delete the header and its implemented content from of the table
                del self.header[header]
                if header == "row":
                    self.content.pop(0)
                elif header == "col":
                    for i in self.content:
                        i.pop(0)

        # Handle editing the header of a specific row or column
        elif action.lower() == "edit":
            
            # Handle the 'row' header
            if header == "row" and "row" in self.header:
            
                # Replace the header with given content and set header_action to update
                self.header["row"][index] = content
                self.header_action_row = "update"
            
            # ... col ...
            elif header == "col" and "col" in self.header:
                
                # ...
                self.header["col"][index] = content
                self.header_action_col = "update"
        
        # Handle adding or replacing an existing header
        elif action.lower() == "add" or action.lower() == "replace":
            
            # Handle 'row' header
            if header == "row":
                if header not in self.header:
                    self.header_action_row = "calculate"
                else:
                    self.header_action_row = "update"
            
            # ... 'col' ...
            elif header == "col":
                if header not in self.header:
                    self.header_action_col = "calculate"
                else:
                    self.header_action_col = "update"
        
            # Add the specified header or replace it if it's already active
            self.header[header] = restructure(content, "list", self.fill_with_empty_columns, self.fill_with_empty_rows, self.empty_dicts, self.empty_lists, self.empty_cells, self.replace_empty)

        self.update()

    
    def update(self):

        """
        Updates the headers and other stuff. Recommended to run before 'display' function
        """

        # Handle the 'row' header such as implementing it to the table or update it if necessary
        if "row" in self.header:
            
            # Handle 'update' header action
            if self.header_action_row == "update":
                
                # Remove the implemented header and set action the 'insert' to fully update the header
                self.content.pop(0)
                self.header_action_row = "calculate"

            # Handle 'insert' header action
            if self.header_action_row == "calculate":
                
                # Recalculate the count of columns
                self.columns = 0
                for row in self.content:
                    if len(row) > self.columns: 
                        self.columns = len(row)

                # If header content is not specified implement the default one
                if self.header["row"] == ["#default"]:    
                    self.header["row"] = [f"{index+1}." for index in range(0, self.columns)]

                # If header content is given
                else: 
                    
                    # Add empty headers if header content doesnt cover all rows
                    if len(self.header["row"]) < self.columns -1 if "col" in self.header else self.columns:
                        for i in range(self.columns -1 if "col" in self.header else self.columns - len(self.header["row"])):
                            self.header["row"].append(self.replace_empty)

                self.header_action_row = "insert" 
            
            if self.header_action_row == "insert":
                # Implement the header into the content of the table
                self.content = [self.header["row"]] + self.content

        # ... col ...
        if "col" in self.header:

            # ...
            if self.header_action_col == "update":
            
                # ...
                for i in self.content:
                    i.pop(0)    
                self.header_action_col = "calculate"

            # ...
            if self.header_action_col == "calculate":

                # ...
                if self.header["col"] == ["#default"]:
                    self.header["col"] = [f"{index+1}." for index in range(0, len(self.content))]

                # ...
                else:

                    # ... columns
                    if len(self.header["col"]) < len(self.content):
                        for i in range(len(self.content) - len(self.header["col"])):
                            self.header["col"].append(self.replace_empty)

                # Handle if 'row' and 'col' header are active
                if "row" in self.header:
                    self.header["col"].pop(-1)
                    self.header["col"].insert(0, self.replace_empty)
                
                self.header_action_col = "insert"
            
            if self.header_action_col == "insert":
                for index, i in enumerate(self.header["col"]):
                    self.content[index] = [i] + self.content[index]

        # Reset header actions
        self.header_action_col = "nothing"
        self.header_action_row = "nothing"

        # Recalculate the counts for columns and rows
        self.rows = len(self.content)
        self.columns = 0
        for row in self.content:
            if len(row) > self.columns: 
                self.columns = len(row)

        # Adding empty cells to fill up missing cells
        for row in self.content:
            
            while len(row) < self.columns:
                row.append(self.replace_empty)

        # Calculating the width for each column
        self.max_chars = []
        for cell in range(self.columns): 
            self.max_chars.append(0)
        for row in self.content: 
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

    def display(self):
    
        self.update()

        # Print the headline
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
                spacebar_counter = self.max_chars[column] - len(str(self.content[row][column])) 
                text = str(self.content[row][column])

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