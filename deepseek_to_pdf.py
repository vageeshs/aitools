from weasyprint import HTML
import re

def deepseek_to_pdf(text, output_file='output.pdf'):
    """
    Converts DeepSeek-style formatted text to a browser-like PDF
    Handles headers, lists, tables, and styled sections automatically
    """
    # CSS styling to match browser appearance
    styles = """
    <style>
        body { 
            font-family: Arial, sans-serif; 
            line-height: 1.6; 
            margin: 2cm; 
            color: #333;
        }
        h1 { 
            color: #2c3e50; 
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.3em;
            margin-top: 1.5em;
        }
        h2 { 
            color: #3498db; 
            margin-top: 1.2em;
        }
        h3 { 
            color: #27ae60;
            margin-top: 1em;
        }
        ul, ol {
            margin: 0.5em 0;
            padding-left: 1.5em;
        }
        li {
            margin: 0.3em 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #3498db;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f5f5f5;
        }
        .special-section {
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            margin: 1em 0;
            padding: 1em;
        }
        .code-block {
            background: #f4f4f4;
            padding: 1em;
            border-radius: 4px;
            font-family: monospace;
            white-space: pre-wrap;
        }
    </style>
    """

    # Convert DeepSeek text to HTML components
    html_content = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect headers
        if line.startswith('###'):
            html_content.append(f'<h3>{line[3:].strip()}</h3>')
        elif line.startswith('##'):
            html_content.append(f'<h2>{line[2:].strip()}</h2>')
        elif line.startswith('#'):
            html_content.append(f'<h1>{line[1:].strip()}</h1>')
            
        # Detect lists
        elif re.match(r'^[\-\*•]\s', line):
            if '<ul>' not in html_content[-1:]:
                html_content.append('<ul>')
            html_content.append(f'<li>{line[1:].strip()}</li>')
        elif re.match(r'^\d+\.\s', line):
            if '<ol>' not in html_content[-1:]:
                html_content.append('<ol>')
            html_content.append(f'<li>{line[2:].strip()}</li>')
            
        # Detect tables
        elif '|' in line and '---' not in line:
            if '<table>' not in html_content[-1:]:
                html_content.append('<table><thead>')
                headers = [h.strip() for h in line.split('|') if h]
                html_content.append('<tr>' + ''.join(f'<th>{h}</th>' for h in headers) + '</tr>')
                html_content.append('</thead><tbody>')
            else:
                cells = [c.strip() for c in line.split('|') if c]
                html_content.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
                
        # Detect code blocks
        elif line.startswith('```'):
            if '<div class="code-block">' not in html_content[-1:]:
                html_content.append('<div class="code-block">')
            else:
                html_content.append('</div>')
                
        # Detect special sections (Pros/Cons/Notes)
        elif re.match(r'^(Pros|Cons|Note|Warning):', line, re.I):
            html_content.append(f'<div class="special-section"><strong>{line.split(":")[0]}</strong>')
            html_content.append(f'<p>{":".join(line.split(":")[1:]).strip()}</p></div>')
            
        # Default paragraph
        else:
            html_content.append(f'<p>{line}</p>')

    # Close any open tags
    for tag in ['ul', 'ol', 'table', 'div']:
        if f'<{tag}>' in html_content and f'</{tag}>' not in html_content:
            html_content.append(f'</{tag}>')

    # Generate final HTML
    final_html = f"""
    <html>
        <head>{styles}</head>
        <body>
            {"".join(html_content)}
        </body>
    </html>
    """

    # Generate PDF
    HTML(string=final_html).write_pdf(output_file)
    return output_file

# Example usage:
if __name__ == "__main__":
    sample_text = """
    # DeepSeek Response Format
    ## Main Section
    ### Subsection
    - List item 1
    - List item 2
    - List item 3

    | Header1 | Header2 |
    |---------|---------|
    | Data1   | Data2   |
    | Data3   | Data4   |

    Pros: This is a positive aspect
    - Benefit 1
    - Benefit 2

    Cons: These are limitations
    - Limitation 1
    - Limitation 2

    ```python
    print("Code block example")
    ```
    """

    deepseek_to_pdf(sample_text, 'output.pdf')
