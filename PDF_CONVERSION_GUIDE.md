# How to Convert SYSTEM_DOCUMENTATION.md to PDF

## Option 1: Using Pandoc (Recommended)

1. **Install Pandoc:**
   - Download from: https://pandoc.org/installing.html
   - Or use Chocolatey: `choco install pandoc`
   - Or use winget: `winget install --id JohnMacFarlane.Pandoc`

2. **Install LaTeX (for PDF generation):**
   - Download MiKTeX: https://miktex.org/download
   - Or use Chocolatey: `choco install miktex`

3. **Convert to PDF:**
   ```bash
   pandoc SYSTEM_DOCUMENTATION.md -o SYSTEM_DOCUMENTATION.pdf --pdf-engine=xelatex -V geometry:margin=1in
   ```

## Option 2: Using Online Converters

1. **Markdown to PDF Online:**
   - https://www.markdowntopdf.com/
   - https://dillinger.io/ (has export to PDF)
   - https://stackedit.io/ (has export to PDF)

2. **Steps:**
   - Open SYSTEM_DOCUMENTATION.md
   - Copy the content
   - Paste into the online converter
   - Export as PDF

## Option 3: Using VS Code Extension

1. **Install Markdown PDF Extension:**
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Markdown PDF"
   - Install the extension by yzane

2. **Convert:**
   - Open SYSTEM_DOCUMENTATION.md in VS Code
   - Right-click in the editor
   - Select "Markdown PDF: Export (pdf)"

## Option 4: Using Chrome/Edge Browser

1. **Install Markdown Viewer Extension:**
   - Install "Markdown Viewer" extension for Chrome/Edge
   - Or use "Markdown Preview Plus"

2. **Convert:**
   - Open SYSTEM_DOCUMENTATION.md in the browser
   - Use browser's Print function (Ctrl+P)
   - Select "Save as PDF" as destination
   - Adjust settings and save

## Option 5: Using Python (if you have Python installed)

1. **Install markdown and weasyprint:**
   ```bash
   pip install markdown weasyprint
   ```

2. **Create a conversion script:**
   ```python
   import markdown
   from weasyprint import HTML
   
   with open('SYSTEM_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
       md_content = f.read()
   
   html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
   HTML(string=html).write_pdf('SYSTEM_DOCUMENTATION.pdf')
   ```

3. **Run the script:**
   ```bash
   python convert_to_pdf.py
   ```

## Recommended: Option 1 (Pandoc)

Pandoc produces the best quality PDFs with proper formatting, table of contents, and styling.

