"""
Markdown 转 DOCX 工具
将 Markdown 文件转换为 Word 文档
"""
import re
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn


def markdown_to_docx(md_file: str, docx_file: str):
    """
    将 Markdown 文件转换为 DOCX 文件

    Args:
        md_file: Markdown 文件路径
        docx_file: 输出的 DOCX 文件路径
    """
    # 读取 Markdown 文件
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 创建 Word 文档
    doc = Document()

    # 设置默认字体
    doc.styles['Normal'].font.name = '微软雅黑'
    doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    doc.styles['Normal'].font.size = Pt(10.5)

    # 解析 Markdown 内容
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # 跳过空行
        if not line:
            i += 1
            continue

        # 处理标题
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            if level <= 6:
                text = line.lstrip('#').strip()
                heading = doc.add_heading(text, level=min(level, 3))
                heading.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

                # 设置标题字体
                run = heading.runs[0]
                run.font.name = '微软雅黑'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
                run.font.bold = True
                run.font.size = Pt(16 - level * 2)

        # 处理代码块
        elif line.startswith('```'):
            lang = line[3:].strip() if len(line) > 3 else ''
            i += 1
            code_lines = []

            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1

            code_text = '\n'.join(code_lines)
            p = doc.add_paragraph()
            p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT

            # 添加代码块背景（使用灰色文本）
            run = p.add_run(code_text)
            run.font.name = 'Consolas'
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0, 0, 0)

            # 添加边框效果（简化版）
            p.space_after = Pt(6)

        # 处理无序列表
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:]
            p = doc.add_paragraph(text, style='List Bullet')

        # 处理有序列表
        elif re.match(r'^\d+\. ', line):
            text = re.sub(r'^\d+\. ', '', line)
            p = doc.add_paragraph(text, style='List Number')

        # 处理表格
        elif line.startswith('|') and '|' in line[1:]:
            # 读取整个表格
            table_lines = []
            while i < len(lines) and lines[i].startswith('|'):
                if lines[i].strip() != '|':  # 跳过分隔行
                    table_lines.append(lines[i])
                i += 1
            i -= 1  # 回退一行

            # 解析表格
            if table_lines:
                # 提取单元格
                rows = []
                for table_line in table_lines:
                    cells = [cell.strip() for cell in table_line.split('|')[1:-1]]
                    rows.append(cells)

                # 创建表格
                if rows:
                    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
                    table.style = 'Light Grid Accent 1'

                    # 填充表格
                    for row_idx, row_data in enumerate(rows):
                        row = table.rows[row_idx]
                        for col_idx, cell_text in enumerate(row_data):
                            cell = row.cells[col_idx]
                            cell.text = cell_text

                            # 设置表头样式
                            if row_idx == 0:
                                cell.paragraphs[0].runs[0].font.bold = True

        # 处理引用
        elif line.startswith('>'):
            text = line[1:].strip()
            p = doc.add_paragraph(text)
            p.style = 'Intense Quote'
            p.paragraph_format.left_indent = Inches(0.5)

        # 处理分隔线
        elif line.startswith('---') or line.startswith('***'):
            p = doc.add_paragraph('_' * 50)
            p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # 处理普通段落
        else:
            # 处理行内格式
            # 粗体 **text**
            line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
            # 斜体 *text*
            line = re.sub(r'\*(.+?)\*', r'\1', line)
            # 代码 `text`
            line = re.sub(r'`(.+?)`', r'\1', line)

            # 链接 [text](url)
            def replace_link(match):
                text = match.group(1)
                url = match.group(2)
                # Word 文档中暂时只显示文本
                return text

            line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, line)

            if line:
                p = doc.add_paragraph(line)
                p.paragraph_format.line_spacing = 1.5

        i += 1

    # 保存文档
    doc.save(docx_file)
    print(f"✅ 成功转换: {md_file} -> {docx_file}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("用法: python md_to_docx.py <输入.md> <输出.docx>")
        print("示例: python md_to_docx.py DEVELOPMENT.md 安天投标文件智能分析系统-开发文档.docx")
        sys.exit(1)

    md_file = sys.argv[1]
    docx_file = sys.argv[2]

    markdown_to_docx(md_file, docx_file)
