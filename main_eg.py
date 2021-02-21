import numpy as np
import cv2 as cv
import queue
import os
import sys


class Pixel:
    ds = [3, 2, 1]
    d = 3
    draw_line_size = {1: 2, 2: 4, 3: 4}

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


def parse_params(corrds):
    st_x1, st_y1 = corrds.split(',')
    x1, y1 = int(st_x1), int(st_y1)

    return (x1, y1)


def display_image(img, maze_name):
    curr_dir = os.getcwd()
    os.chdir(f"{curr_dir}\\mazes\\tmp_solved")
    filename = f'{maze_name}_Solved.jpg'
    cv.imwrite(filename, img)

    return filename


def proccess_params(args):
    start_param = args[0]
    end_param = args[1]
    image_path = args[2]
    ui_image_size_param = args[3]
    start, end, ui_image_size = parse_params(start_param), parse_params(end_param), parse_params(ui_image_size_param)
    image_name = image_path.split('\\')[-1].split('.')[0]
    return start, end, image_path, ui_image_size, image_name


def crop_background(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    th, threshed = cv.threshold(gray, 240, 255, cv.THRESH_BINARY_INV)

    ## (2) Morph-op to remove noise
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    morphed = cv.morphologyEx(threshed, cv.MORPH_CLOSE, kernel)

    ## (3) Find the max-area contour
    cnts = cv.findContours(morphed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    cnts_flat = cnts[0]
    for contour in cnts[1:]:
        cnts_flat = np.append(cnts_flat, contour, axis=0)
    # cnt = sorted(cnts, key=cv.contourArea)[-1]

    # cv.drawContours(gray, cnts_flat, -1, (0, 0, 255), 10)
    # plt.imshow(gray)
    # plt.show()
    ## (4) Crop and save it
    x, y, w, h = cv.boundingRect(cnts_flat)
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


def get_boundline_start_updown(start, end, img, dir):
    if (dir == 'u'):
        row_range = range(img.shape[0])
    else:
        row_range = range(img.shape[0] - 1, 0, -1)
    y_range_start = min(start[1], end[1])
    y_range_end = max(start[1], end[1])
    for row in row_range:
        for col in range(y_range_start, y_range_end):
            if img[row, col] > 220:
                return row, col
    return 0, 0


def get_boundline_start_leftright(start, end, img, dir):
    if (dir == 'l'):
        col_range = range(img.shape[1])
    else:
        col_range = range(img.shape[1] - 1, 0, -1)
    x_range_start = min(start[0], end[0])
    x_range_end = max(start[0], end[0])
    for col in col_range:
        for row in range(x_range_start, x_range_end):
            if img[row, col] > 220:
                return row, col
    return 0, 0


# Draw bounding edges around creating a cross extending the maze external contour
# Using this cross we avoid "wrong" solutions passing outside the maze (You shall not pass!)
def draw_boundline(start, end, img):
    if abs(start[1] - end[1]) > img.shape[1] * 0.02:
        upper_line_start = get_boundline_start_updown(start, end, img, 'u')
        lower_line_start = get_boundline_start_updown(start, end, img, 'd')
        for row in range(upper_line_start[0]):
            img[row][upper_line_start[1]] = 255
        for row in range(lower_line_start[0], img.shape[0]):
            img[row][lower_line_start[1]] = 255
    if abs(start[0] - end[0]) > img.shape[0] * 0.02:
        left_line_start = get_boundline_start_leftright(start, end, img, 'l')
        right_line_start = get_boundline_start_leftright(start, end, img, 'r')
        for col in range(left_line_start[1]):
            img[left_line_start[0]][col] = 255
        for col in range(right_line_start[1], img.shape[1]):
            img[right_line_start[0]][col] = 255


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
            if x < M and y < N and edges[x][y] > 200:
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


def get_resize_relations(size_old, size_new):
    sizeX_new = size_new[0]
    sizeY_new = size_new[1]
    sizeX_old = size_old[0]
    sizeY_old = size_old[1]

    Rx = sizeX_new / sizeX_old
    Ry = sizeY_new / sizeY_old

    return Rx, Ry


# calculate new coordinates of (x,y) after resizing an image
def get_new_coords_by_relations(x, y, Rx, Ry):
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


def get_solve_size_range(img):
    new_size_x = img.shape[0]
    new_size_y = img.shape[1]
    image_size = new_size_x * new_size_y
    if image_size > 900 * 900:
        return 0.4
    if image_size > 600 * 600:
        return 0.6
    if image_size > 300 * 300:
        return 0.8
    return 1


def get_solve_size(img, resize):
    new_size_x = img.shape[0]
    new_size_y = img.shape[1]
    new_size_x = round(new_size_x * resize)
    new_size_y = round(new_size_y * resize)
    return new_size_x, new_size_y


def restartMaze(seen):
    for pixel in seen:
        pixel.visited = 0
        pixel.prev = None


def solve_maze():
    seen = []
    q = queue.Queue()
    q.put(maze[solving_start[0]][solving_start[1]])
    seen.append(maze[solving_start[0]][solving_start[1]])
    while (not q.empty()):
        curr = q.get()
        curr.visited = 2
        x = curr.X
        y = curr.Y
        neighbors = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]

        for r, c in neighbors:
            if (r < N and r >= 0 and c < M and c >= 0):
                if (is_end(maze[r][c], solving_end)):
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


# use solution on the resized cropped image to draw solution line on original image
def draw_solution_on_original_image(original_image, end, edges, bb, Rx, Ry):
    curr = end
    left = bb[0][0]
    up = bb[0][1]
    lastUD = 'u'
    lastLR = 'r'

    while (curr.prev != None):
        prev = curr.prev
        dir = get_dir(prev, curr)
        pre_resize_corrds = get_new_coords_by_relations(curr.X, curr.Y, Rx,
                                                        Ry)  # coordinates of cropped image before resizing
        original_image_coords = (pre_resize_corrds[0] + up, pre_resize_corrds[1] + left)  # coords of original image

        if dir == 'u' or dir == 'd':
            draw_range = round(Pixel.draw_line_size[Pixel.d] * Ry)
            closerTo = checkCloseSideLeftRight(curr, edges)
            if (closerTo == 's' and lastLR == 'l') or closerTo == 'l':
                lastLR = 'l'
                for j in range(draw_range):
                    if j + original_image_coords[1] < original_image.shape[1]:
                        original_image[original_image_coords[0], original_image_coords[1] + j, :2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] + j, 2] = 255
                    else:
                        break
            elif (closerTo == 's' and lastLR == 'r') or closerTo == 'r':
                lastLR = 'r'
                for j in range(draw_range):
                    if original_image_coords[1] - j >= 0:
                        original_image[original_image_coords[0], original_image_coords[1] - j, :2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] - j, 2] = 255
                    else:
                        break
            else:
                lastLR = 'e'
                for j in range(draw_range // 2):
                    if original_image_coords[1] - j >= 0:
                        original_image[original_image_coords[0], original_image_coords[1] - j, :2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] - j, 2] = 255
                    if original_image_coords[1] + j < original_image.shape[1]:
                        original_image[original_image_coords[0], original_image_coords[1] + j, :2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] + j, 2] = 255

        else:
            draw_range = round(Pixel.draw_line_size[Pixel.d] * Rx)
            closerTo = checkCloseSideUpDown(curr, edges)
            if (closerTo == 's' and lastUD == 'u') or closerTo == 'u':
                lastUD = 'u'
                for j in range(draw_range):
                    if original_image_coords[0] + j < original_image.shape[0]:
                        original_image[original_image_coords[0] + j, original_image_coords[1], :2] = 0
                        original_image[original_image_coords[0] + j, original_image_coords[1], 2] = 255
                    else:
                        break

            elif (closerTo == 's' and lastUD == 'd') or closerTo == 'd':
                lastUD = 'd'
                for j in range(draw_range):
                    if original_image_coords[0] - j >= 0:
                        original_image[original_image_coords[0] - j, original_image_coords[1], :2] = 0
                        original_image[original_image_coords[0] - j, original_image_coords[1], 2] = 255
                    else:
                        break
            else:
                lastUD = 'e'
                for j in range(draw_range // 2):
                    if original_image_coords[0] - j >= 0:
                        original_image[original_image_coords[0] - j, original_image_coords[1], :2] = 0
                        original_image[original_image_coords[0] - j, original_image_coords[1], 2] = 255
                    if original_image_coords[0] + j < original_image.shape[0]:
                        original_image[original_image_coords[0] + j, original_image_coords[1], :2] = 0
                        original_image[original_image_coords[0] + j, original_image_coords[1], 2] = 255

        curr = curr.prev

    ########## main ##########


# Check that input start and end points were not in the background, and lost in the crop process
def check_input_points_after_crop(end_after_crop, start_after_crop, size_after_crop):
    for i in range(2):
        if (end_after_crop[i] < 0 or end_after_crop[i] >= size_after_crop[i] or start_after_crop[i] < 0 or
                start_after_crop[i] >= size_after_crop[i]):
            return False
    return True


if __name__ == "__main__":
    start_param, end_param, image_path_param, ui_image_size_param, maze_name = proccess_params(sys.argv[1:])
    original_colored_image = cv.imread(image_path_param)
    if original_colored_image is None:
        print("*Failed2*")  # Failed due to invalid image file path
        exit(0)
    Rx_ui, Ry_ui = get_resize_relations(ui_image_size_param, original_colored_image.shape[:-1])
    original_start = get_new_coords_by_relations(start_param[0], start_param[1], Rx_ui, Ry_ui)
    original_end = get_new_coords_by_relations(end_param[0], end_param[1], Rx_ui, Ry_ui)
    solve_flag = False

    cropped_image, bb = crop_background(original_colored_image)
    start_after_crop = get_new_coords_after_crop(bb, original_start[0], original_start[1])
    end_after_crop = get_new_coords_after_crop(bb, original_end[0], original_end[1])
    size_after_crop = cropped_image.shape[:-1]
    valid_start_end_points = check_input_points_after_crop(end_after_crop, start_after_crop, size_after_crop)
    if not valid_start_end_points:
        print("*Failed1*")  # points cropped error
        exit(0)
    else:
        start_size = get_solve_size_range(cropped_image)
        for i in np.arange(start_size, 1.2, 0.2):
            solve_size = get_solve_size(cropped_image, i)
            resized_cropped_image = cv.resize(cropped_image, solve_size[::-1])
            Rx, Ry = get_resize_relations(size_after_crop, solve_size)
            solving_start = get_new_coords_by_relations(start_after_crop[0], start_after_crop[1], Rx, Ry)
            solving_end = get_new_coords_by_relations(end_after_crop[0], end_after_crop[1], Rx, Ry)
            gray_image = cv.cvtColor(resized_cropped_image, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray_image, 100, 200)
            draw_boundline(solving_start, solving_end, edges)
            maze = init_maze(gray_image)
            N, M = edges.shape
            for d in Pixel.ds:
                Pixel.d = d
                found, seen = solve_maze()
                if found:
                    solve_flag = True
                    break
                else:
                    restartMaze(seen)
            if solve_flag:
                end_pixel = maze[solving_end[0]][solving_end[1]]
                draw_solution_on_original_image(original_colored_image, end_pixel, edges, bb, 1 / Rx, 1 / Ry)
                solution_name = display_image(original_colored_image, maze_name)
                print(f"*{solution_name}*")
                exit(0)

        if not solve_flag:
            print("*Failed to solve maze*")
