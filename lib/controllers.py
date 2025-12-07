def queryAppend(url,queries):
    queri = ""
    for data in queries:
        queri_data = ""
        if (data[1]):
            queri_data += f"{data[0]}={data[1]}"
            if (queri != ""):
                queri += "&"+queri_data
            else:
                queri += queri_data
    if ("?" in url):
        url = url.split('?')[0]  
    return url + "?" + queri

def get_table_data(table):
    data = []
    for row in range(table.rowCount()):
        row_data = []
        for col in range(table.columnCount()):
            item = table.item(row, col)
            if (col == 0 and not item.text() ):
                break
            row_data.append(item.text() if item else "")
        if (row_data != []):
            data.append(row_data)
    return data