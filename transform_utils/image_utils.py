import PIL, io
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def txt2img(txt, font = ImageFont.load_default()):
	img=Image.new("RGBA", (500,250),(255,255,255))
	draw = ImageDraw.Draw(img)
	draw.text((0, 0), txt, (0,0,0), font=font)
	draw = ImageDraw.Draw(img)
	outbuf = io.BytesIO()
	img.save(outbuf, format="PNG")
	return outbuf.getvalue()