import PIL.Image
import PIL.ImageTk
import tkFileDialog
from Tkinter import *
from tkColorChooser import askcolor
from tkFileDialog import askopenfilename
from PIL import ImageTk



def addScreen(Img):
    render = ImageTk.PhotoImage(Img)
    img = Label(root, image=render)
    img.image = render
    img.place(x=img_height, y=img_width)
    img.bind("<Button-1>", print_cordinates)


def print_cordinates(event):
    print(event.x, event.y)
    paintBlob(event.x, event.y)


def paintBlob(x, y):
    global select_color
    for i in range(1, col_size - 1):
        for j in range(1, raw_size - 1):
            if labels[i][j] == labels[x][y]:
                pixel[i, j] = select_color
                draw_img.putpixel((i, j), select_color)
    render = ImageTk.PhotoImage(draw_img)
    img = Label(root, image=render)
    img.image = render
    img.place(x=img_height, y=img_width)
    img.bind("<Button-1>", print_cordinates)
    print("paintBlob is over")


def getColor():
    global select_color
    color = askcolor()
    color = str(color)
    start = color.index("((")
    stop = color.index("),")
    color = color[start:stop]
    color = color[2:len(color)]
    r, g, b = color.split(",")
    select_color = int(float(r)), int(float(g)), int(float(b))
    print("Select Color is :", select_color)
    return select_color


def main():
    select_color = (0, 0, 0)
    draw_img = None

    global root
    global img_height
    global img_width
    global startxSize
    global startySize
    global pixbase
    global firstbar


    img_height = 50
    img_width = 50

    root = Tk()
    root.title("Fill Coloring")
    root.geometry("800x600")
    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open", command=openFile)
    file_menu.add_command(label="Exit", command=root.destroy)
    root.config(menu=menu_bar)

    pickColor = Button(root, text='Pick Color', command=getColor)
    pickColor.grid(row=0, column=0)
    pickColor = Button(root, text='Save', command=saveImage)
    pickColor.grid(row=0, column=20)
    pickColor = Button(root, text='Clear', command=clearImage)
    pickColor.grid(row=0, column=40)

    root.mainloop()


def clearImage():
    file_p = open(file_path_string, "rb")
    draw_img = PIL.Image.open(file_p)
    pixel = draw_img.load()
    col_size, raw_size = draw_img.size
    addScreen(draw_img)


def saveImage():
    fname = tkFileDialog.asksaveasfilename(defaultextension=".png")
    if not fname:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    draw_img.save(fname)


def openFile():
    global draw_img
    global pixel
    global raw_size
    global col_size
    global  file_path_string
    file_path_string = askopenfilename(parent=root)

    file_p = open(file_path_string, "rb")
    draw_img = PIL.Image.open(file_p)
    pixel = draw_img.load()
    col_size, raw_size = draw_img.size
    addScreen(draw_img)

    for i in range(col_size):
        for j in range(raw_size):
            pixel[i, j] = vanishNoisesFromPixel(pixel[i, j])

    pixel_matrix = [[0 for x in range(raw_size)] for y in range(col_size)]
    for i in range(col_size):
        for j in range(raw_size):
            pixel_matrix[i][j] = converToBinaryValue(pixel[i, j])


    for i in range(col_size):
        for j in range(raw_size):
            if i == 0 or j == 0 or i == col_size - 1 or j == raw_size - 1:
                pixel_matrix[i][j] = 0


    print("\nBefore labeling pixel_matrix matrix look like")
    for i in range(col_size):
        print()
        for j in range(raw_size):
            print(pixel_matrix[i][j])
    print("\n")


    global labels
    labels = [[0 for i in range(raw_size)] for j in range(col_size)]
    for i in range(col_size):
        for j in range(raw_size):
            labels[i][j] = 0

    label_count = 2
    for i in range(1, col_size - 1):
        for j in range(1, raw_size - 1):
            if pixel_matrix[i][j] == 1:
                if pixel_matrix[i - 1][j] == 1 and pixel_matrix[i][j - 1] == 1:
                    if labels[i - 1][j] == labels[i][j - 1]:
                        labels[i][j] = labels[i][j - 1]
                    else:
                        labels[i][j] = labels[i - 1][j]
                        for p in range(0, i + 1):
                            for q in range(0, j + 1):
                                if labels[p][q] == labels[i][j - 1]:
                                    labels[p][q] = labels[i - 1][j]
                elif pixel_matrix[i - 1][j] == 1 or pixel_matrix[i][j - 1] == 1:
                    if pixel_matrix[i - 1][j] == 1:
                        labels[i][j] = labels[i - 1][j]
                    else:
                        labels[i][j] = labels[i][j - 1]
                else:
                    labels[i][j] = label_count
                    label_count += 1
            else:
                labels[i][j] = 1


def converToBinaryValue(rgbValues):
    if len(rgbValues) == 4:
        r, g, b, f = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average == 255:
        return 1
    return 0


def vanishNoisesFromPixel(rgbValues):

    if len(rgbValues) == 4:
        r, g, b, f = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average > 200:
        return 255, 255, 255
    return 0, 0, 0


if __name__ == '__main__':
    main()
