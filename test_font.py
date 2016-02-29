from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (192, 64))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Alternatively load a TTF font.
# Some nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('fonts/arial.ttf', 8)
#font = ImageFont.load_default()

# Write some text.
draw.rectangle((0,0,192,64), outline=1, fill=0)
draw.text((0,0), 'Ahoj jak se mas ja se mam dobre', font=font)

data = image.load()
#parse data
d = [""]*1536
for p in range(8):
    for i in range(8):
        for c in range(192):
            d[(i*192)+c] = str(data[(c,p*i)])
#data = [int(i,2) for i in d]
print(d)
exit()



col = 0
cis = 0
data = list(image.getdata())
for r in range(0,8):
    for p in data[r*1536:(r+1)*1536]:
        d[(r * 192) + cis] += str(p)
        col += 1
        if cis == 191:
            cis = 0
        else:
            cis += 1
    cis = 0
    col = 0

data = [hex(int(i,2)) for i in d]


print(len(data))
