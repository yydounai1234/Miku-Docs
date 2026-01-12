#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import defaultdict

# 1. 读取 json 文件
with open("test.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 累计 duration
duration_sum = defaultdict(int)

for item in data:
    values = item.get("values", {})
    for key, detail in values.items():
        duration_sum[key] += detail.get("duration", 0)

# 3. 输出概要 + Top N，避免整屏都是尾部的小数值
sorted_items = sorted(duration_sum.items(), key=lambda kv: kv[1], reverse=True)
top_n = 20

print(f"记录总数: {len(data)}, 设备/键数量: {len(sorted_items)}")
print(f"duration 最大值: {sorted_items[0][1]}, 最小值: {sorted_items[-1][1]}")
print(f"\n前 {top_n} 个（按 duration 倒序）：")
for key, total in sorted_items[:top_n]:
    print(f"{key}: {total}")

# 如需完整排序结果，可打开生成的文件查看
with open("duration_sum_sorted.json", "w", encoding="utf-8") as f:
    json.dump(sorted_items, f, ensure_ascii=False, indent=2)
print("\n完整排序已写入 duration_sum_sorted.json")

