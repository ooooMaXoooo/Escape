from PIL import Image

def splitTiles(image, imageSize, tileSize, destination):
    img = Image.open(image)
    img = img.convert("RGBA")

    iX, iY = imageSize
    tX, tY = tileSize
    count = 0

    print(iY/tY)

    for b in range(iY // tY):
        for a in range(iX // tX): # faire la première ligne
            tile = Image.new('RGBA', tileSize, (0,0,0))

            for x in range(tX):
                for y in range(tY):
                    tile.putpixel((x,y), img.getpixel((x+a*tX, y+b*tY)))

            tile.save(destination + "\\tile" + str(count) + ".png", "png")
            count += 1

splitTiles("tiles-jungle.png",(320, 256),(64,64),"jungle")
splitTiles("tiles-stones.png",(320, 256),(64,64),"stone")
splitTiles("tiles-skulls.png",(320, 256),(64,64),"skull")
splitTiles("tiles-wood.png",(320, 256),(64,64),"wood")

