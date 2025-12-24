#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import os

def parse_json_schema(schema, required_fields=None, nested_level=0, show_required=True):
    """
    解析JSON Schema并生成Markdown表格
    :param schema: JSON Schema对象
    :param required_fields: 必需字段列表
    :param nested_level: 嵌套层级
    :param show_required: 是否显示"是否必需"列
    """
    if required_fields is None:
        required_fields = schema.get("required", [])
    
    # 需要跳过的字段列表
    skip_fields = ["streamConf", "origin", "redirect", "forward", "thirdAuth"]
    
    indent = "&nbsp;&nbsp;&nbsp;&nbsp;" * nested_level
    
    # 表头
    if show_required:
        table = "| 参数名称 | 类型 | 说明 |是否必需|\n"
        table += "|:--------------|:------|:------|:------|\n"
    else:
        table = "| 参数名称 | 类型 | 说明 |\n"
        table += "|:--------------|:------|:------|\n"
    
    # 遍历properties中的字段
    properties = schema.get("properties", {})
    for field_name, field_info in properties.items():
        # 跳过指定字段
        if field_name in skip_fields:
            continue
        
        # 字段类型
        field_type = field_info.get("type", "")
        
        # 如果是数组类型，显示为 []type
        if field_type == "array":
            items = field_info.get("items", {})
            items_type = items.get("type", "")
            if items_type:
                field_type = "[]{}".format(items_type)
            else:
                # 如果数组项是对象引用
                ref = items.get("$ref", "")
                if ref:
                    # 提取引用名称
                    ref_name = ref.split("/")[-1]
                    field_type = "[]{}".format(ref_name)
        
        # 如果字段本身是嵌套对象（不是引用）
        nested_props = {}
        if field_type == "object":
            # 检查是否有嵌套的properties
            nested_props = field_info.get("properties", {})
            if nested_props:
                # 这是一个内联对象，保持type为object
                field_type = "object"
        
        # 如果是对象引用
        ref = field_info.get("$ref", "")
        if ref:
            # 提取引用名称
            ref_name = ref.split("/")[-1]
            field_type = ref_name
        
        # 字段说明（将换行符替换为<br>）
        description = field_info.get("description", "").replace("\n", "<br>")
        
        # 是否必需
        is_required = "必需" if field_name in required_fields else "可选"
        
        # 添加到表格
        name = indent + field_name if nested_level > 0 else field_name
        if show_required:
            table += "| {} | {} | {} | {} |\n".format(name, field_type, description, is_required)
        else:
            table += "| {} | {} | {} |\n".format(name, field_type, description)
        
        # 如果是数组类型且数组项是对象，递归处理其属性
        if field_type.startswith("[]") and field_type[2:] == "object":
            items = field_info.get("items", {})
            if "properties" in items:
                nested_required = items.get("required", [])
                # 递归调用处理嵌套对象
                nested_table = parse_json_schema(items, nested_required, nested_level + 1, show_required)
                # 移除表头，只保留内容行
                lines = nested_table.split('\n')
                # 跳过表头行，只保留数据行
                for line in lines:
                    if line.startswith('|') and not line.startswith('|:'):  # 不是表头分隔线
                        if line.strip() != '' and not (line.startswith('| 参数名称') or line.startswith('|:---')):
                            table += line + '\n'
        
        # 如果是内联嵌套对象，递归处理其属性
        if field_type == "object" and nested_props:
            nested_required = field_info.get("required", [])
            # 递归调用处理嵌套对象
            nested_table = parse_json_schema(field_info, nested_required, nested_level + 1, show_required)
            # 移除表头，只保留内容行
            lines = nested_table.split('\n')
            # 跳过表头行，只保留数据行
            for line in lines:
                if line.startswith('|') and not line.startswith('|:'):  # 不是表头分隔线
                    if line.strip() != '' and not (line.startswith('| 参数名称') or line.startswith('|:---')):
                        table += line + '\n'
    
    return table

def process_nested_objects(schema, definitions, show_required=True):
    """
    处理definitions中的嵌套对象
    :param schema: JSON Schema对象
    :param definitions: definitions对象
    :param show_required: 是否显示"是否必需"列
    """
    tables = []
    
    # 遍历definitions中的嵌套对象
    for def_name, def_schema in definitions.items():
        # 生成表格
        table = parse_json_schema(def_schema, def_schema.get("required", []), 1, show_required)
        tables.append({
            "name": def_name,
            "table": table
        })
    
    return tables

def main():
    # 检查命令行参数
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("使用方法: python generate_jsonschema_to_md_table.py <输入json_schema文件.txt> <输出markdown文件.md> [--no-required]")
        print("示例: python generate_jsonschema_to_md_table.py schema.txt output.md")
        print("      python generate_jsonschema_to_md_table.py schema.txt output.md --no-required")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    show_required = True
    
    # 检查是否有--no-required参数
    if len(sys.argv) == 4 and sys.argv[3] == "--no-required":
        show_required = False
    
    # 从文件中读取JSON Schema
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            json_schema_str = f.read()
    except FileNotFoundError:
        print("错误: 找不到文件 {}".format(input_file))
        sys.exit(1)
    except Exception as e:
        print("读取文件时出错: {}".format(e))
        sys.exit(1)
    
    # 解析JSON Schema
    try:
        schema = json.loads(json_schema_str)
    except json.JSONDecodeError as e:
        print("JSON解析错误: {}".format(e))
        sys.exit(1)
    
    # 准备输出内容
    output_content = []
    
    # 生成主表
    output_content.append("## 响应参数")
    output_content.append(parse_json_schema(schema, schema.get("required", []), 0, show_required))
    
    # 处理definitions中的嵌套对象
    definitions = schema.get("definitions", {})
    if definitions:
        nested_tables = process_nested_objects(schema, definitions, show_required)
        
        # 输出嵌套对象表格
        for table_info in nested_tables:
            output_content.append("\n### {} 参数".format(table_info['name']))
            output_content.append(table_info['table'])
    
    # 写入输出文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_content))
        print("成功生成Markdown表格，已保存到: {}".format(output_file))
    except Exception as e:
        print("写入文件时出错: {}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()