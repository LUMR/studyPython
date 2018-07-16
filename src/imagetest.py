from PIL import Image, ImageDraw, ImageFont

if __name__ == '__main__':
    img = Image.open('/Users/lumr/Pictures/表情/278ea501a18b87d6a98e54600f0828381e30fd10.jpg')
    print(img)
    draw = ImageDraw.Draw(img)
    ttfront = ImageFont.truetype('Arial Unicode.ttf',16)
    draw.text((0, 160), "我的内心毫无波动\n甚至还想笑",fill=(0,0,0), font=ttfront)
    img.show()