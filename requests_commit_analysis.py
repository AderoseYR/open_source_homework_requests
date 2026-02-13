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

# -------------------------- 模块3：数据可视化（生成分析图，作业成果核心） --------------------------
# 设置中文字体（避免图表中文乱码，适配Windows）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 创建画布，生成3个子图（作者贡献+小时提交+星期提交）
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# 子图1：贡献前5作者柱状图
ax1.bar(top_author.index, top_author.values, color="#1f77b4")
ax1.set_title("requests项目贡献前5作者", fontsize=14, fontweight="bold")
ax1.set_xlabel("作者")
ax1.set_ylabel("提交次数")
ax1.tick_params(axis='x', rotation=45)  # 作者名旋转，避免重叠

# 子图2：一天24小时提交规律折线图
ax2.plot(hour_count.index, hour_count.values, color="#ff7f0e", linewidth=2, marker="o")
ax2.set_title("requests项目小时提交规律", fontsize=14, fontweight="bold")
ax2.set_xlabel("小时（0-23）")
ax2.set_ylabel("提交次数")
ax2.set_xticks(np.arange(0, 24, 2))  # 每2小时显示一个刻度

# 子图3：一周7天提交规律柱状图
week_map = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
week_count.index = week_count.index.map(week_map)
ax3.bar(week_count.index, week_count.values, color="#2ca02c")
ax3.set_title("requests项目星期提交规律", fontsize=14, fontweight="bold")
ax3.set_xlabel("星期")
ax3.set_ylabel("提交次数")

# 调整子图间距，保存图片（高分辨率，作业文档可用）
plt.tight_layout()
plt.savefig("requests提交历史分析图.png", dpi=300, bbox_inches="tight")
plt.close()

print("可视化完成，已生成高清分析图！")
print("==================== 作业代码运行完成 ====================")