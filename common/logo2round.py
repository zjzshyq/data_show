from PIL import Image, ImageDraw
import numpy as np

def make_circle_image(image_path, output_path, opacity=128):
    # 打开图片
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    # 创建一个新的透明图像
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # 绘制圆形
    draw.ellipse((0, 0, width, height), fill=255)

    # 将原图与圆形蒙版结合
    circular_img = Image.new("RGBA", (width, height))
    circular_img.paste(img, (0, 0), mask)

    # 获取 alpha 通道并转换为 NumPy 数组
    alpha = np.array(circular_img.split()[3])
    alpha = (alpha > 0) * opacity  # 将非透明部分的 alpha 值设置为 opacity

    # 将 NumPy 数组转换回 Image 对象
    alpha_img = Image.fromarray(alpha.astype('uint8'), mode='L')

    # 将新的 alpha 通道应用到图像
    circular_img.putalpha(alpha_img)

    # 保存结果
    circular_img.save(output_path)

# 使用示例
make_circle_image("../data/logo.png", "logo2.png", opacity=128)