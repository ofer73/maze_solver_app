import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import queue


class Pixel:
    ds = [6, 5, 4, 3, 2, 1]
    d = 5
    # draw_line_size = {1: 2, 2: 3, 3: 3, 4: 3, 5: 4, 6: 4}
    draw_line_size = {1: 2, 2: 4, 3: 6, 4: 8, 5: 10, 6: 12}

    def __init__(self, X, Y, visited, prev):
        self.X = X
        self.Y = Y
        self.visited = visited
        self.prev = prev


def init_maze(img):
    maze = [[0 for i in range(edges.shape[1])] for j in range(edges.shape[0])]
    for r in range(img.shape[0]):
        for c in range(img.shape[1]):
            maze[r][c] = Pixel(r, c, 0, None)

    return maze


def crop_background(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    th, threshed = cv.threshold(gray, 240, 255, cv.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    morphed = cv.morphologyEx(threshed, cv.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = cv.findContours(morphed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    cnt = sorted(cnts, key=cv.contourArea)[-1]

    ## (4) Crop and save it
    x, y, w, h = cv.boundingRect(cnt)
    dst = img[y:y + h, x:x + w]
    bb = np.array([[x, y],
                   [x + w, y],
                   [x + w, y + h],
                   [x + w, y]])
    # bb = np.array([[1050, 60],
    #                 [1267, 60],
    #                 [1267, 622],
    #                 [1050, 622]])
    return dst, bb


def is_near_wall(pixel, edges, d, dir):
    M, N = edges.shape
    if (dir == 'r'):
        ranges = (-d, d, 0, d)
    elif (dir == 'l'):
        ranges = (-d, d, -d, 0)
    elif (dir == 'd'):
        ranges = (0, d, -d, d)
    else:
        ranges = (-d, 0, -d, d)

    # for r in range(d,2,-2):
    wallSurrounding = False
    for i in range(ranges[0], ranges[1]):
        for j in range(ranges[2], ranges[3]):
            x = pixel.X + i
            y = pixel.Y + j
            if x < M and y < N and edges[x][y] == 255:
                wallSurrounding = True
                break
        if wallSurrounding:
            break
        # if not wallSurrounding:
        #     Pixel.d = r
        #     break

    return wallSurrounding


def is_end(pixel, end):
    return pixel.X == end[0] and pixel.Y == end[1]


def get_dir(curr, neighbor):
    if curr.X > neighbor.X:
        dir = 'u'
    elif curr.X < neighbor.X:
        dir = 'd'
    elif curr.Y < neighbor.Y:
        dir = 'r'
    else:
        dir = 'l'
    return dir


def getNewCoords(x, y, bb, size):
    bbUpperLeftX = bb[0][0]
    bbUpperLeftY = bb[0][1]
    bbLowerRightX = bb[2][0]
    bbLowerRightY = bb[2][1]

    sizeX = bbLowerRightX - bbUpperLeftX
    sizeY = bbLowerRightY - bbUpperLeftY

    sizeMax = max(sizeX, sizeY)

    centerX = (bbLowerRightX + bbUpperLeftX) / 2
    centerY = (bbLowerRightY + bbUpperLeftY) / 2

    offsetX = (centerX - sizeMax / 2) * size / sizeMax
    offsetY = (centerY - sizeMax / 2) * size / sizeMax

    x = x * size / sizeMax - offsetX
    y = y * size / sizeMax - offsetY
    return (round(x), round(y))


def get_resize_relations(size_old, size_new):
    sizeX_new = size_new[0]
    sizeY_new = size_new[1]
    sizeX_old = size_old[0]
    sizeY_old = size_old[1]

    Rx = sizeX_new / sizeX_old
    Ry = sizeY_new / sizeY_old

    return Rx, Ry


# calculate new coordinates of (x,y) after resizing an image
def getNewCoords2(x, y, Rx, Ry):
    return round(Rx * x), round(Ry * y)


def get_new_coords_after_crop(bb, x, y):
    delta_x = bb[0][1]
    delta_y = bb[0][0]
    x_new = x - delta_x
    y_new = y - delta_y

    return x_new, y_new


def is_wall(pixel, edges):
    return edges[pixel.X][pixel.Y] > 200


def checkCloseSideUpDown(curr, edges):
    for i in range(Pixel.d, 2 * Pixel.d):
        down = curr.X + i >= edges.shape[0] or edges[curr.X + i][curr.Y] > 200
        up = curr.X - i < 0 or edges[curr.X - i][curr.Y] > 200
        if down and up:
            return 'e'  # equal
        if down:
            return 'd'
        if up:
            return 'u'
    return 's'


def checkCloseSideLeftRight(curr, edges):
    for i in range(Pixel.d, 2 * Pixel.d):
        right = curr.Y + i >= edges.shape[1] or edges[curr.X][curr.Y + i] > 200
        left = curr.Y - i < 0 or edges[curr.X][curr.Y - i] > 200

        if right and left:
            return 'e'  # equal
        if right:
            return 'r'
        if left:
            return 'l'
    return 's'


def get_solve_size(img):
    new_size_x = img.shape[0]
    new_size_y = img.shape[1]
    image_size = new_size_x * new_size_y
    if image_size > 600 * 600:
        new_size_x = round(new_size_x * 0.4)
        new_size_y = round(new_size_y * 0.4)
    elif image_size > 300 * 300:
        new_size_x = round(new_size_x * 0.75)
        new_size_y = round(new_size_y * 0.75)
    return new_size_x, new_size_y


def restartMaze(seen):
    for pixel in seen:
        pixel.visited = 0
        pixel.prev = None


def solve_maze():
    seen = []
    q = queue.Queue()
    q.put(maze[start_after_resize[0]][start_after_resize[1]])
    seen.append(maze[start_after_resize[0]][start_after_resize[1]])
    while (not q.empty()):
        curr = q.get()
        curr.visited = 2
        x = curr.X
        y = curr.Y
        neighbors = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]

        for r, c in neighbors:
            if (r < N and r >= 0 and c < M and c >= 0):
                if (is_end(maze[r][c], end_after_resize)):
                    maze[r][c].visited = 1
                    maze[r][c].prev = curr
                    return True, seen

                elif (maze[r][c].visited == 0 and not is_near_wall(maze[r][c], edges, Pixel.d,
                                                                   get_dir(curr, maze[r][c]))):
                    seen.append(maze[r][c])
                    q.put(maze[r][c])
                    maze[r][c].visited = 1
                    maze[r][c].prev = curr
    return False, seen


def draw_on_original_image(bb, original_image, resized_image):
    left = bb[0][0]
    up = bb[0][1]
    line_array = np.array([0, 0, 255])
    # original_colored_image[up:down, left:right] = drawed_resized_image
    r, c = resized_image.shape[:-1]
    for i in range(r):
        for j in range(c):
            if np.array_equal(line_array, resized_image[i, j, :]):
                original_image[up + i, left + j, :] = line_array


##############################################


# use solution on the resized cropped image to draw solution line on original image
def draw_solution_on_original_image(original_image, end, edges, bb, Rx, Ry):
    curr = end
    left = bb[0][0]
    up = bb[0][1]
    draw_range = Pixel.draw_line_size[Pixel.d]
    lastUD = 'u'
    lastLR = 'r'

    while (curr.prev != None):
        prev = curr.prev
        dir = get_dir(prev, curr)
        pre_resize_corrds = getNewCoords2(curr.X, curr.Y, Rx, Ry)  # coordinates of cropped image before resizing
        original_image_coords = (pre_resize_corrds[0] + up, pre_resize_corrds[1] + left)  # coords of original image

        if dir == 'u' or dir == 'd':
            draw_range = round(Pixel.draw_line_size[Pixel.d] * Ry)
            closerTo = checkCloseSideLeftRight(curr, edges)
            if (closerTo == 's' and lastLR == 'l') or closerTo == 'l':
                lastLR = 'l'
                for j in range(draw_range):
                    if j + original_image_coords[1] < original_image.shape[1]:
                        original_image[original_image_coords[0], original_image_coords[1] + j, 0:2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] + j, 2] = 255
                    else:
                        break
            elif (closerTo == 's' and lastLR == 'r') or closerTo == 'r':
                lastLR = 'r'
                for j in range(draw_range):
                    if original_image_coords[1] - j >= 0:
                        original_image[original_image_coords[0], original_image_coords[1] - j, 0:2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] - j, 2] = 255
                    else:
                        break
            else:
                lastLR = 'e'
                for j in range(draw_range // 2):
                    if original_image_coords[1] - j >= 0:
                        original_image[original_image_coords[0], curr.Y + left - j, 0:2] = 0
                        original_image[original_image_coords[0], curr.Y + left - j, 2] = 255
                    if original_image_coords[1] + j < original_image.shape[1]:
                        original_image[original_image_coords[0], original_image_coords[1] + j, 0:2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] + j, 2] = 255

        else:
            draw_range = round(Pixel.draw_line_size[Pixel.d] * Rx)
            closerTo = checkCloseSideUpDown(curr, edges)
            if (closerTo == 's' and lastUD == 'u') or closerTo == 'u':
                lastUD = 'u'
                for j in range(draw_range):
                    if original_image_coords[0] + j < original_image.shape[0]:
                        original_image[original_image_coords[0] + j, original_image_coords[1], 0:2] = 0
                        original_image[original_image_coords[0] + j, original_image_coords[1], 2] = 255
                    else:
                        break

            elif (closerTo == 's' and lastUD == 'd') or closerTo == 'd':
                lastUD = 'd'
                for j in range(draw_range):
                    if original_image_coords[0] - j >= 0:
                        original_image[original_image_coords[0] - j, original_image_coords[1], 0:2] = 0
                        original_image[original_image_coords[0] - j, original_image_coords[1], 2] = 255
                    else:
                        break
            else:
                lastUD = 'e'
                for j in range(draw_range // 2):
                    if original_image_coords[0] - j >= 0:
                        original_image[original_image_coords[0] - j, original_image_coords[1], 0:2] = 0
                        original_image[original_image_coords[0] - j, original_image_coords[1], 2] = 255
                    if curr.X + j + up < curr.X + j:
                        original_image[curr.X + j + up, original_image_coords[1], 0:2] = 0
                        original_image[curr.X + j + up, original_image_coords[1], 2] = 255

        curr = curr.prev


##############################################


if __name__ == "__main__":
    original_colored_image = cv.imread("mazes/maze3.jpeg")

    # start_old = (10, 10)  # maze1
    # end_old = (380, 400)
    # end_old = (500, 210)  # maze 1 transposed
    # start_old = (224, 380) #maze 2 (round)
    # end_old = (385, 390)
    start_old = (23, 15)  # maze 3
    end_old = (460, 633)
    # start_old = (100, 100)  # maze pyramid
    # end_old = (450, 600)
    # start_old = (100, 100)  # maze4
    # end_old = (450, 600)

    plt.imshow(original_colored_image)
    plt.show()

    cropped_image, bb = crop_background(original_colored_image)
    start_after_crop = get_new_coords_after_crop(bb, start_old[0], start_old[1])
    end_after_crop = get_new_coords_after_crop(bb, end_old[0], end_old[1])
    size_after_crop = cropped_image.shape[:-1]
    # solve_size = (900, 900)  # TODO: choose default size / dynamic based on input image
    solve_size = get_solve_size(cropped_image)
    resized_cropped_image = cv.resize(cropped_image, solve_size[::-1])
    Rx, Ry = get_resize_relations(size_after_crop, solve_size)
    start_after_resize = getNewCoords2(start_after_crop[0], start_after_crop[1], Rx, Ry)
    end_after_resize = getNewCoords2(end_after_crop[0], end_after_crop[1], Rx, Ry)
    plt.imshow(resized_cropped_image)
    plt.show()
    gray_image = cv.cvtColor(resized_cropped_image, cv.COLOR_BGR2GRAY)
    plt.imshow(resized_cropped_image)
    plt.show()
    edges = cv.Canny(gray_image, 100, 200)
    plt.imshow(edges)
    plt.show()
    maze = init_maze(gray_image)
    N, M = edges.shape
    for d in Pixel.ds:
        Pixel.d = d
        found, seen = solve_maze()
        if found:
            break
        else:
            restartMaze(seen)

    end_pixel = maze[end_after_resize[0]][end_after_resize[1]]

    draw_solution_on_original_image(original_colored_image, end_pixel, edges, bb, 1 / Rx, 1 / Ry)
    plt.imshow(original_colored_image)
    plt.show()
    cv.imshow('image', original_colored_image)
    cv.waitKey(0)
    cv.destroyAllWindows()
