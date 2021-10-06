from PIL import Image, ImageTk


def create_image(imgPath):
    mImage = Image.open(imgPath)
    render = ImageTk.PhotoImage(mImage)
    return render

