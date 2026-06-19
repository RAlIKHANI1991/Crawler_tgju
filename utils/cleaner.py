import re


def clean_rows(page_rows):

    cleaned = []
    for row in page_rows:
        new_row = []
        for cell in row:

            if isinstance(cell, str):
                cell = re.sub(r"<[^>]+>", "", cell)
                cell = cell.replace(",", "").strip()
                stripped = cell.strip()

                if stripped in ('','-','–','−','—','+','±'):
                    cell = "0"

                elif ("%" in stripped 
                      or "±" in stripped 
                      or stripped.lstrip("+-").replace(".", "", 1).isdigit()):

                    cell = (stripped.replace("%", "").replace("±", "").replace("–", "-"))

                    if cell in ("", "+", "-"):
                        cell = "0"

            new_row.append(cell)

        cleaned.append(new_row)

    return cleaned