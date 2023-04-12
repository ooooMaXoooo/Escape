from PIL import Image, ImageDraw

img = Image.open("tile0.png")
img = img.convert("RGBA")

width, height = img.size
draw = ImageDraw.Draw(img)

imgFinal = Image.new('RGBA', (32,32), (0,0,0))


for i in range(21):
    img = Image.open("tile" +  str(i) + ".png")
    imga = img.convert("RGBA")

    datas = imga.getdata()

    newData = list()
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append([255, 255, 255, 0])
        else:
            newData.append(item)

    imgb = Image.frombuffer("RGBA", imga.size, newData, "raw", "RGBA", 0, 1)
    imgb.save("test/tile" + str(i) + ".png", "PNG")

    """
    for x in range(32):
        for y in range(32):
            imgFinal.putpixel((x,y), img.getpixel((x,y)))


    name = "test/tile" + str(i)+ ".png"
    imgFinal.save(name, "png")
    """


