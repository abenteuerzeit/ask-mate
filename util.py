def remove_html_tag_attributes(file, attributes_list):
    # Remove selected attributes from an HTML tag
    # A new file is generated
    updated_list = [' ' + attribute.lower() + '="' for attribute in attributes_list]
    with open(file) as html_file:
        new_lines = []
        for line in html_file.readlines():
            line = line
            for attribute in updated_list:
                while attribute in line.lower():
                    start = line.find(attribute)
                    if line.find(';'):
                        stop = line.find(';') + 1
                    new_line = line[start:].replace(attribute, "")
                    if new_line.find('"'):
                        stop = new_line.find('"') + 1
                    line = line.replace(new_line[:stop], "")
                    line = line.replace(attribute, "")
            new_lines.append(line)

        file_name = file[:file.find('.html')]
        capitalize = [attribute.upper()[0] + attribute.lower()[1:] for attribute in attributes_list]
        renamed_file = file_name + f"_{'-'.join(capitalize)}" + "-removed" + ".html"
        save_new_file = open(renamed_file, 'w')
        save_new_file.writelines(new_lines)


# def remove(file, tag):
#     with open(file) as html_file:
#         lines = []
#         for line in html_file.readlines():
#             while tag in line.lower():
#                 start = line.find(tag)-1
#                 if line.find('>'):
#                     stop = line.find('>') + 1
#                 new_line = line[start:].replace(tag, "")
#                 line = line.replace(new_line[:stop], "")
#                 line = line.replace(tag, "")
#         lines.append(line)
#         for line in lines:
#             print(line)

# if __name__ == "__main__":
#     # files = ['add-answer.html', 'add-question.html', 'edit-question.html', 'error.html', 'layout.html', 'question.html']
#     # for file in files:
#     #     filepath = f"./templates/{file}"
#     #     remove_html_tag_attributes(filepath, ["style", "class"])
#     remove(add-question.html)
