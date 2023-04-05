from PIL import Image, ImageDraw

img = Image.open("image_128.png")
img = img.convert("RGBA")

width, height = img.size
draw = ImageDraw.Draw(img)

droit1 = Image.new('RGBA', (32,32), (0,0,0))
droit2 = Image.new('RGBA', (32,32), (0,0,0))
droit3 = Image.new('RGBA', (32,32), (0,0,0))
droit4 = Image.new('RGBA', (32,32), (0,0,0))

gauche1 = Image.new('RGBA', (32,32), (0,0,0))
gauche2 = Image.new('RGBA', (32,32), (0,0,0))
gauche3 = Image.new('RGBA', (32,32), (0,0,0))
gauche4 = Image.new('RGBA', (32,32), (0,0,0))


for x in range(32):
    for y in range(32):
        gauche1.putpixel((x,y), img.getpixel((x,y+32)))
        gauche2.putpixel((x,y), img.getpixel((x+32,y+32)))
        gauche3.putpixel((x,y), img.getpixel((x+64,y+32)))
        gauche4.putpixel((x,y), img.getpixel((x+96,y+32)))

        droit1.putpixel((x,y), img.getpixel((x,y+64)))
        droit2.putpixel((x,y), img.getpixel((x+32,y+64)))
        droit3.putpixel((x,y), img.getpixel((x+64,y+64)))
        droit4.putpixel((x,y), img.getpixel((x+96,y+64)))


droit1.save("droit1.png", "png")
droit2.save("droit2.png", "png")
droit3.save("droit3.png", "png")
droit4.save("droit4.png", "png")

gauche1.save("gauche1.png", "png")
gauche2.save("gauche2.png", "png")
gauche3.save("gauche3.png", "png")
gauche4.save("gauche4.png", "png")

print("Images Cleric priest 2 découpées !!!")

