from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

defaultCover = 'https://firebasestorage.googleapis.com/v0/b/teaching-6b309.appspot.com/o/Physics%2FRotational%20Mechanics%2F0NGIMFPU254QUVDPFA5C%2Fquestion_0.jpeg?alt=media&token=92673968-7ce0-44d6-af1c-8d370494512c'

imagePath = 'Rotational Mechanics/001 : Angular Acceleration of Pulley/6.jpeg'

photo = Image.open(imagePath)

w, h = photo.size

drawing = ImageDraw.Draw(photo)
font = ImageFont.truetype('fonts/Nunito-SemiBold.ttf', 14)

text = '© IIT-JEE by Ayush P Gupta'
text_w, text_h = drawing.textsize(text, font)

pos = (w - text_w)/2, (h - text_h) - 10
print(pos)

drawing.text(pos, text, fill="#263238", font=font)

photo.save(imagePath)
