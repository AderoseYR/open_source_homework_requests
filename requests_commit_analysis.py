# 导入所需开源库
from git import Repo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# -------------------------- 模块1：从本地requests仓库提取提交历史数据 --------------------------
# 配置requests本地仓库路径（替换为你自己的路径！）
repo_path = r"C:\Users\32600\Desktop\open_source_homework\requests"  # 你的实际路径

# 初始化仓库对象
repo = Repo(repo_path)
# 获取所有提交记录（按时间倒序）
commits = list(repo.iter_commits('main'))  # main为requests主分支

# 存储提交数据的列表
commit_data = []
# 遍历所有提交，提取核心信息
for commit in commits:
    commit_info = {
        "提交ID": commit.hexsha[:8],  # 取提交ID前8位，简洁展示
        "作者": commit.author.name,
        "作者邮箱": commit.author.email,
        "提交时间": commit.committed_datetime,  # 带时区的datetime对象
        "提交信息": commit.message.strip(),  # 提交备注信息
        "修改文件数": len(commit.stats.files)  # 本次提交修改的文件数量
    }
    commit_data.append(commit_info)

# -------------------------- 模块2：数据清洗与统计分析 --------------------------
# 将数据转为pandas DataFrame，方便统计
df = pd.DataFrame(commit_data)

# ========== 关键修改：处理带时区的datetime，指定utc=True ==========
# 方式1：转为UTC时区（推荐，保留时间准确性）
df["提交时间"] = pd.to_datetime(df["提交时间"], utc=True)
# 可选方式2：移除时区信息（简单，不影响小时/星期统计）
# df["提交时间"] = df["提交时间"].dt.tz_convert(None)

# 现在可以正常使用.dt访问器提取时间维度（若用方式1，需先转为本地时区，不影响统计）
df["提交小时"] = df["提交时间"].dt.hour
df["提交星期"] = df["提交时间"].dt.weekday  # 0=周一，6=周日
df["提交月份"] = df["提交时间"].dt.month

# 统计核心指标
top_author = df["作者"].value_counts().head(5)  # 贡献前5的作者
hour_count = df["提交小时"].value_counts().sort_index()  # 各小时提交次数
week_count = df["提交星期"].value_counts().sort_index()  # 各星期提交次数

# 将统计结果保存为CSV文件（作业成果之一）
df.to_csv("requests提交历史统计数据.csv", index=False, encoding="utf-8-sig")
top_author.to_csv("贡献前5作者统计.csv", encoding="utf-8-sig")
print("数据统计完成，已生成CSV统计文件！")
