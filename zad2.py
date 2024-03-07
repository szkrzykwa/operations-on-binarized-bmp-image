from PIL import Image

def binarization(image: Image):
    for x in range(row):
            for y in range(col):
                if MC[x][y] > 170 : MC[x][y] = 255
                else: MC[x][y] = 0
    for x in range(row):
        for y in range(col):
            image.putpixel((y,x), MC[x][y])
    return image


def dilatation(image: Image):
    image = binarization(image)
    radius = int(input("Radius (min 1 - max 10): "))
    width, height = image.size
    if radius < 1 or radius > 10:
      return image
    else:  
        new_MC = [[0 for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                neighbors = []
                for i in range(max(0, y - radius), min(height, y + radius + 1)):
                    for j in range(max(0, x - radius), min(width, x + radius+  1)):
                        neighbors.append(image.getpixel((j, i)))
                        
                new_MC[y][x] = min(neighbors)

        for y in range(height):
            for x in range(width):
                image.putpixel((x, y), new_MC[y][x])

        image.show()
        return image

def erosion(image: Image):
    image = binarization(image)
    radius = int(input("Radius (min 1 - max 10): "))
    width, height = image.size
    if radius < 1 or radius > 10:
      return image
    else:
        new_MC = [[0 for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                neighbors = []

                for i in range(max(0, y - radius), min(height, y + radius + 1)):
                    for j in range(max(0, x - radius), min(width, x + radius+  1)):
                        neighbors.append(image.getpixel((j, i)))

                new_MC[y][x] = max(neighbors)

        for y in range(height):
            for x in range(width):
                image.putpixel((x, y), new_MC[y][x])

        image.show()
        return image

def morphological_opening(image: Image):
    erosion(image)
    dilatation(image)
    return image

def morphological_closing(image: Image):
    dilatation(image)
    erosion(image)
    return image

def convolution(image: Image):
    name = input("File name (filter): ")
    file = open(name)
    kernel = []
    for i in file.readlines():
        kernel.append(i.split())
    width, height = image.size
    new_MC = [[0 for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            sum = 0
            ky = kx = 0
            for i in range(max(0, y - 1), min(height, y + 2)):
                for j in range(max(0, x - 1), min(width, x + 2)):
                    pixel = image.getpixel((j, i))
                    weight = float(kernel[kx][ky])
                    sum += int(pixel * weight)
                    ky+=1
                kx+=1
                ky = 0
            new_MC[i][j] = sum
    for y in range(height):
        for x in range(width):
            image.putpixel((x, y), new_MC[y][x])        
    
    image.show()

def convolution_radius(image: Image):
    radius = int(input("Radius (min 3 - max 10): "))
    value = 1/((1+2*radius)**2)
    kernel = [[value for _ in range(1+2*radius)]for _ in range(1+2*radius)]
    width, height = image.size
    if radius < 3 or radius > 10:
      return image  
    else:
        new_MC = [[0 for _ in range(width)] for _ in range(height)]
        for y in range(height):
            for x in range(width):
                sum = 0
                kx = ky = 0
                for i in range(max(0, y - radius), min(height, y + radius +1)):
                    for j in range(max(0, x - radius), min(width, x + radius+1)):
                        pixel = image.getpixel((j, i))
                        sum += pixel * float(kernel[kx][ky])
                        ky+=1
                    kx+=1
                    ky = 0
                new_MC[i][j] = int(sum)
        for y in range(height):
            for x in range(width):
                image.putpixel((x, y), new_MC[y][x])        
        
        image.show()
        return image



if __name__ == "__main__":
    img = Image.open("Mapa_MD_no_terrain_low_res_Gray.bmp")
    col, row = img.size
    MC = [[0 for _ in range(col)] for _ in range(row)]
    for xsize in range(row):
        for ysize in range(col):
            MC[xsize][ysize] = img.getpixel((ysize,xsize))
    x = int(input("pick operation: "))
    if x == 0:
        dilatation(img)
    elif x==1:
        erosion(img)
    elif x==2:
        morphological_closing(img)
    elif x==3:
        morphological_opening(img)
    elif x==4:
        convolution(img)
    elif x==5:
        convolution_radius(img)
    else:
        print("wrong input")