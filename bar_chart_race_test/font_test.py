import matplotlib.pyplot as plt

# 设置全局字体为支持中文的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows

# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

# 示例绘图
plt.plot([1, 2, 3], [4, 5, 6])
plt.title('中文标题')  # 中文标题
plt.xlabel('X轴标签')  # 中文X轴标签
plt.ylabel('Y轴标签')  # 中文Y轴标签
plt.show()