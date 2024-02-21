def restructure(data, structure, integer=False, fill_with_empty_columns=None, fill_with_empty_rows=None, empty_dicts=None, empty_lists=None, empty_cells=None, replace_empty=None):
    
    """
    - Restructures and cleanes the given data based on the specified structure.

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

    if data in empty_lists:
        if structure == "list":
            return [replace_empty]
        elif structure == "list_in_list":
            return [[replace_empty]]
    
    else:
        data_type = type(data) 
        if data_type is list:
            element_type = type(data[0])
        elif data_type is dict:
            element_type = type(next(iter(data.values())))

        if structure == "list" and integer:    
            data_structure = data_type.__name__

            if data_structure == "dict":            

                if fill_with_empty_columns:
                    columns = list(data.keys())
                    columns = sorted(columns)
                    if len(columns) >= 2:
                        for i in range(columns[0], columns[-1]):
                            if i not in columns:
                                data[i] = replace_empty

                data = dict(sorted(data.items()))
                data = [i for i in list(data.values())]
            
            for index, i in enumerate(data):
                if i in empty_cells:
                    data[index] = replace_empty

            return data
        
        if structure == "list_in_list" and integer:
            data_structure = f"{element_type.__name__}_in_{data_type.__name__}"

            if data_structure == "dict_in_list":

                if fill_with_empty_rows:
                    rows = [key for d in data for key in d]
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data.append({row:[]})
                
                new_content = []
                data = sorted(data, key=lambda d: next(iter(d)))

                for line in data:    
                    if any(str(val) in empty_dicts for val in line.values()):
                        new_content.append([replace_empty])
                    else:
                        new_content.append([char for char in line.values()])
                
                data = new_content

            elif data_structure == "list_in_dict":
                
                if fill_with_empty_rows:
                    input(data)
                    rows = list(data.keys())
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data[row] = []
                
                new_content = []
                data = dict(sorted(data.items()))
                
                for line in data.values():
                    if line in empty_lists:
                        new_content.append([replace_empty])
                    else:
                        new_content.append(line)
                
                data = new_content

            elif data_structure == "dict_in_dict":
                
                if fill_with_empty_rows:
                    rows = list(data.keys())
                    rows = sorted(rows)
                    for row in range(rows[0], rows[-1]):
                        if row not in rows:
                            data[row] = {}
                
                if fill_with_empty_columns:
                    for key, row in data.items():
                        columns = list(row.keys())
                        if len(columns) >= 2:
                            for col in range(columns[0], columns[-1]):
                                if col not in columns:
                                    data[key][col] = replace_empty
                
                new_content = []
                data = {k: dict(sorted(v.items())) if isinstance(v, dict) else v for k, v in sorted(data.items())}

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
                
                data = new_content
            
            new_content = []
            for line in data:
                new_content.append([str(char) if str(char) not in empty_cells else replace_empty for char in line])
                data = new_content 
            
            return data



