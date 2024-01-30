from rich.console import Console
from rich.table import Table
# from rich.prompt import Prompt


def table(title=None, title_style=None, header=[], header_style='bold blue', rows=[], row_style='bright_green'):

    table = Table()
    if title:
        table.title = title
        table.title_style = title_style
        table.title_justify = 'left'

    longest_row = max([len(row) for row in rows])
    if len(header) < longest_row:
        for i in range(longest_row - len(header)):
            header.append(f'Column_{i}')

    for column in header:
        table.add_column(column, header_style=header_style, width=40)

    for row in rows:
        table.add_row(*row, style=row_style)

    table.show_lines = True

    Console().print(table)

def parser(book, mode):
    
    if isinstance(book, str):
        console = Console()
        console.print(book, style = 'green')
        return

    if isinstance(book, tuple):
        console = Console()
        console.print(book[0], style='red')
        return

    def value_getter(value):

        if isinstance(value, list):
            value = ' '.join([str(i) for i in value])
        elif value:
            value = str(value)
        else:
            value = ''
        return value

    if mode == '1':
        records = []
        rec_per_page = book.rec_per_page
                
        for record in book.data.values():
            row = [
                value_getter(record.name),
                value_getter(record.phones),
                value_getter(record.emails),
                value_getter(record.birthday),
                value_getter(record.address),
                value_getter(record.memos)
                ]
            records.append(row)

        header = ['Name', 'Phones', 'E-mails',
                'Birthday', 'Address', 'Memos']
        title = '...'
        page = []
        for row in enumerate(records, start=1):
            if (row[0] == len(records)): # and (page != []):
                page.append(row[1])  
                table(title=title, header=header, rows=page)
                page.clear()
            elif row[0]%rec_per_page:
                page.append(row[1])
            else:
                page.append(row[1])
                table(title=title, header=header, rows=page)    
                page.clear()
                if input("Continue (n - to break)?").lower() == 'n':
                    break 
    else:
        records = []
        rec_per_page = book.qua_for_iter
        
        for record in book.data.values():
            row = [
                value_getter(record, 'title'),
                value_getter(record, 'text'),
                value_getter(record, 'tags'),
                ]
            records.append(row)

        header = ['Title', 'Text', 'Tags']
        title = '...'
        page = []
        for row in enumerate(records, start=1):
            if (row[0] == len(records)):
                page.append(row[1])  
                table(title=title, header=header, rows=page)
                page.clear()
            elif row[0]%rec_per_page:
                page.append(row[1])
            else:
                page.append(row[1])
                table(title=title, header=header, rows=page)    
                page.clear()
                if input("Continue (n - to break)?").lower() == 'n':
                    break 