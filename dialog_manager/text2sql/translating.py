class Translating:
    """
        Kelas ini digunakan untuk memetakan hasil
        parsing menjadi query SQL.
    """

    def translate2sql(self, ner, parsing):

        _select = ""
        _from = ""
        _where = ""
        bool_w = False

        # print(ner)
        # jika entitas tipe kosong maka select tipe

        # jika entitas merk dan tipe terpenuhi maka select stok 

        for sql_component in parsing:
            if sql_component[0] == 'SELECT':
                for column, value in ner.items():
                    if 'tipe' in column and value:
                        _select = str(sql_component[1]).replace('*', 'stok ')
                    else:
                        _select = str(sql_component[1]).replace('*', 'tipe ')
            elif sql_component[0] == 'FROM':
                _from += sql_component[1] + ' '
            elif sql_component[0] == 'WHERE':
                bool_w = True
                _where += sql_component[1] + ''.join(' AND ')

        if bool_w:
            sql_query = _select + _from + "WHERE " + _where[:-4]
        else:
            sql_query = _select + _from 

        return sql_query
