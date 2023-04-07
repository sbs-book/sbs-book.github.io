import markdown


def convert_markdown_to_html(markdown_file, template_file, output_file):
    # Read the Markdown file
    with open(markdown_file, 'r') as md_file:
        md_text = md_file.read()

    # Extract level 3 headers from the Markdown file
    headers = []
    start_indexes = []
    for i, line in enumerate(md_text.splitlines()):
        
        # HACK: ignore the start of the file
        if i < 50: continue

        if line.startswith('###'):
            headers.append(line.strip().lstrip('#').strip())
            start_indexes.append(i)

    # Convert each section between headers to HTML
    section_htmls = []
    for i, header in enumerate(headers):
        
        start_index = start_indexes[i]
        end_index = start_indexes[i+1] if i+1 < len(start_indexes) else len(md_text.splitlines())
        section_md_text = '\n'.join(md_text.splitlines()[start_index:end_index]).strip()
        section_html = markdown.markdown(section_md_text)
        section_html = section_html.replace(f'<h3>{header}</h3>', '')  # Remove the <h3> tag
        section_htmls.append(section_html)

    # Replace the content of the HTML template file between the delimiters
    with open(template_file, 'r') as tmpl_file:
        tmpl_text = tmpl_file.read()
        start_delimiter = '<!-- CONTENT START -->'
        end_delimiter = '<!-- CONTENT STOP -->'
        start_index = tmpl_text.index(start_delimiter) + len(start_delimiter)
        end_index = tmpl_text.index(end_delimiter)
        tmpl_text0 = tmpl_text
        tmpl_text = tmpl_text[:start_index] + '\n'  # Add a new line after the start delimiter
        
        for header, section_html in zip(headers, section_htmls):
            # Generate the HTML code for the section
            header_slug = header.lower().replace(' ', '-')
            section_html = f'<section id="{header_slug}">\n' \
                           f'    <div class="wrapper">\n' \
                           f'        <div class="title">\n' \
                           f'            <a name="{header_slug}" class="anchor"></a>\n' \
                           f'            <h2>{header}</h2>\n' \
                           f'        </div>\n' \
                           f'        <div>\n' \
                           f'            {section_html}\n' \
                           f'        </div>\n' \
                           f'    </div>\n' \
                           f'</section>\n\n'
            tmpl_text += section_html
        tmpl_text += tmpl_text0[end_index:]  # Add the end delimiter and everything after it

    # Write the output to a file
    with open(output_file, 'w') as out_file:
        out_file.write(tmpl_text)


if __name__ == '__main__':
    convert_markdown_to_html('README.md', 'template.html', 'details.html')
