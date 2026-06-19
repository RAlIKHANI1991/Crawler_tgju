# crawler/parser.py
def build_params():

    params = {

        "lang": "fa",

        "order_dir": "asc",

        "search": "",

        "order_col": "",

        "from": "",

        "to": "",

        "convert_to_ad": "1"
    }

    for i in range(8):

        params[f"columns[{i}][data]"] = str(i)
        params[f"columns[{i}][name]"] = ""
        params[f"columns[{i}][searchable]"] = "true"
        params[f"columns[{i}][orderable]"] = "true"
        params[f"columns[{i}][search][value]"] = ""
        params[f"columns[{i}][search][regex]"] = "false"

    return params