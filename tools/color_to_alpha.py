import glob
from PIL import Image

def transparent(image, color: (int, int, int)):
    img = Image.open(image)
    img = img.convert("RGBA")

    pixdata = img.load()

    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y][:3] == color:
                pixdata[x, y] = (255, 255, 255, 0)

    img.save(image, "PNG")


def main()
for image in glob.glob("*.png"):
    transparent(image)


if __name__ == "__main__":
    main()