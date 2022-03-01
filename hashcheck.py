from PIL import Image
import imagehash
import hashlib

cpath = "/Users/aroslav/Downloads/1.jpeg"
h1 = imagehash.average_hash(Image.open(cpath))
h11 = hashlib.md5(Image.open(cpath).tobytes())
cpath = "/Users/aroslav/Downloads/2.jpeg"
h2 = imagehash.average_hash(Image.open(cpath))
h21 = hashlib.md5(Image.open(cpath).tobytes())
print(h1)
print(h2)
print("md5: ", '\n')
print(h11.hexdigest())
print(h21.hexdigest())