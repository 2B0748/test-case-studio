#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_xlsx.py — 将 Markdown 测试用例表转换为 Excel(.xlsx) 或 CSV。

用法:
    python md_to_xlsx.py <input.md> [--out output.xlsx] [--csv]

说明:
    - 按 '## ' 二级标题切分章节，每个章节的表格写入一个 sheet
      (openpyxl 可用时) 或一个独立 CSV（--csv 或 openpyxl 缺失时）。
    - 同一章节出现多张表时：表头相同则合并数据行；表头不同则以
      空行 + 新表头顺序追加。
    - 单元格中的 <br> / <br/> / <br /> 会转换为 Excel 单元格内换行，
      数据行自动开启自动换行与顶端对齐。
    - 零依赖也可工作（自动回退到 CSV）；安装 openpyxl 可获得真正的 .xlsx。
      pip install openpyxl
"""
import argparse
import csv
import os
import re
import sys

TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
SEP_CELL = re.compile(r":?-+:?")
BR = re.compile(r"<br\s*/?>", re.IGNORECASE)
BAD_NAME = re.compile(r"[:?*\[\]/\\]")


def split_sections(lines):
    """按 '## ' 标题切分，返回 [(标题, 行列表), ...]"""
    sections = []
    current_title = "用例"
    current_lines = []
    for line in lines:
        m = re.match(r"^##\s+(.*)$", line)
        if m:
            if current_lines:
                sections.append((current_title, current_lines))
            current_title = m.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_title, current_lines))
    return sections


def parse_tables(block_lines):
    """解析一组行中的所有 Markdown 表格，返回 [(header, rows), ...]。
    表格之间以非表格行（空行、说明文字等）分隔。"""
    tables = []
    cur = []

    def flush():
        if cur:
            data = [r for r in cur if not is_sep_row(r)]
            if data:
                tables.append((data[0], data[1:]))
            cur.clear()

    for line in block_lines:
        if TABLE_ROW.match(line):
            cells = [clean_cell(c) for c in line.strip().strip("|").split("|")]
            cur.append(cells)
        else:
            flush()
    flush()
    return tables


def is_sep_row(row):
    return all(SEP_CELL.fullmatch(c) for c in row if c != "")


def clean_cell(text):
    """单元格清洗：<br> 系列标签转换为换行符。"""
    return BR.sub("\n", text.strip())


def safe_sheet(name, taken):
    """Excel sheet 名限制：≤31 字符，禁用 [:?*/\\]；重名时自动追加序号。"""
    base = BAD_NAME.sub("_", name).strip() or "Sheet"
    base = base[:31]
    candidate, i = base, 2
    while candidate in taken:
        suffix = f"_{i}"
        candidate = base[: 31 - len(suffix)] + suffix
        i += 1
    taken.add(candidate)
    return candidate


def safe_filename(name):
    return BAD_NAME.sub("_", name).strip()[:31] or "sheet"


def pad_row(row, width):
    if len(row) < width:
        return row + [""] * (width - len(row))
    return row[:width]


def to_xlsx(sections, out_path):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.utils import get_column_letter
    except ImportError:
        print("[warn] 未检测到 openpyxl，自动回退为 CSV 输出。")
        print("       安装: pip install openpyxl  以获得真正的 .xlsx。")
        base = os.path.splitext(out_path)[0]
        to_csv_fallback(sections, base)
        return

    wb = Workbook()
    wb.remove(wb.active)
    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(bold=True, color="FFFFFF")
    header_align = Alignment(vertical="center", wrap_text=True)
    data_align = Alignment(vertical="top", wrap_text=True)
    taken = set()

    for title, lines in sections:
        tables = parse_tables(lines)
        if not tables:
            continue
        ws = wb.create_sheet(title=safe_sheet(title, taken))
        max_cols = 0
        prev_header = None
        for header, body in tables:
            max_cols = max(max_cols, len(header))
            same = header == prev_header
            if prev_header is not None and not same:
                ws.append([])  # 不同表头之间空一行
            if not same:
                ws.append(header)
                for c in ws[ws.max_row]:
                    c.fill = header_fill
                    c.font = header_font
                    c.alignment = header_align
            for r in body:
                ws.append(pad_row(r, len(header)))
                for c in ws[ws.max_row]:
                    c.alignment = data_align
            prev_header = header
        # 列宽自适应（中文按 2 计，多行单元格按最长一行估算）
        for col_idx in range(1, max_cols + 1):
            char_w = 0
            for row in ws.iter_rows(min_col=col_idx, max_col=col_idx):
                v = row[0].value
                if v is None:
                    continue
                w = max(
                    (sum(2 if ord(ch) > 0x2E80 else 1 for ch in seg)
                     for seg in str(v).split("\n")),
                    default=0,
                )
                char_w = max(char_w, w)
            ws.column_dimensions[get_column_letter(col_idx)].width = min(max(char_w + 2, 10), 60)
        ws.freeze_panes = "A2"

    if not wb.sheetnames:
        print("[warn] 未解析到任何 Markdown 表格，未生成文件。")
        sys.exit(1)
    wb.save(out_path)
    print(f"[ok] 已生成 Excel: {out_path}  (sheet 数: {len(wb.sheetnames)})")


def to_csv_fallback(sections, base):
    made = 0
    for i, (title, lines) in enumerate(sections):
        tables = parse_tables(lines)
        if not tables:
            continue
        fname = f"{base}_{i}_{safe_filename(title)}.csv"
        with open(fname, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            prev_header = None
            for header, body in tables:
                same = header == prev_header
                if prev_header is not None and not same:
                    w.writerow([])
                if not same:
                    w.writerow(header)
                for r in body:
                    w.writerow(pad_row(r, len(header)))
                prev_header = header
        print(f"[ok] 已生成 CSV: {fname}")
        made += 1
    if made == 0:
        print("[warn] 未解析到任何 Markdown 表格。")
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description="Markdown 用例表 → Excel/CSV")
    ap.add_argument("input", help="输入的 Markdown 文件")
    ap.add_argument("--out", default=None, help="输出 .xlsx 路径")
    ap.add_argument("--csv", action="store_true", help="强制输出 CSV")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        print(f"[error] 文件不存在: {args.input}")
        sys.exit(1)

    with open(args.input, encoding="utf-8") as f:
        lines = f.readlines()

    sections = split_sections(lines)
    if args.csv:
        base = args.out or os.path.splitext(args.input)[0]
        to_csv_fallback(sections, base)
    else:
        out = args.out or (os.path.splitext(args.input)[0] + ".xlsx")
        to_xlsx(sections, out)


if __name__ == "__main__":
    main()
