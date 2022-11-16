import re


def in_lines(find: str, lines: list) -> bool:
    for line in lines:
        clean_line = ""
        matches = re.findall(r"(\[\/((\w+)(\s(\w+))*?)+\])", line)
        if matches:
            for item in matches:
                style_end = item[0]
                style_begin = f"[{style_end[2:-1]}]"
                clean_line = line.replace(style_end, "")
                clean_line = clean_line.replace(style_begin, "")

        if find in line or find in clean_line:
            return True
    return False
