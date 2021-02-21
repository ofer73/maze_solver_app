import numpy as np
import cv2 as cv
import queue
import os
import sys


class Pixel:
    ds = [3, 2, 1]
    distance = 3
    draw_line_size = {1: 2, 2: 4, 3: 4}

    def __init__(self, X, Y, visited, prev):
        self.X = X
        self.Y = Y
        self.visited = visited
        self.prev = prev

# Initialize maze as board of Pixel objects
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


def save_solution_img(img, maze_name):
    curr_dir = os.getcwd()
    os.chdir(f"{curr_dir}\\mazes\\tmp_solved")
    filename = f'{maze_name}_Solved.jpg'
    cv.imwrite(filename, img)

    return filename


# Process input parameters of : start_point , end_point, maze_file_path, maze_size
def proccess_params(args):
    start_param = args[0]
    end_param = args[1]
    image_path = args[2]
    ui_image_size_param = args[3]
    start, end, ui_image_size = parse_params(start_param), parse_params(end_param), parse_params(ui_image_size_param)
    image_name = image_path.split('\\')[-1].split('.')[0]
    return start, end, image_path, ui_image_size, image_name


# Crop background around the main contour of the maze
# in order to avoid "illegal" solutions outside the maze and reduce BFS runtime
def crop_background(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    th, threshed = cv.threshold(gray, 240, 255, cv.THRESH_BINARY_INV)

    ## Morph-op to remove noise
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    morphed = cv.morphologyEx(threshed, cv.MORPH_CLOSE, kernel)

    ## Find the external contour
    cnts = cv.findContours(morphed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    cnts_flat = cnts[0]
    for contour in cnts[1:]:
        cnts_flat = np.append(cnts_flat, contour, axis=0)

    ## (4) Crop the image and keep the bounding Rectangle verticles
    x, y, w, h = cv.boundingRect(cnts_flat)
    cropped_img = img[y:y + h, x:x + w]
    bounding_rectangle_vertices = np.array([[x, y],
                                            [x + w, y],
                                            [x + w, y + h],
                                            [x + w, y]])

    return cropped_img, bounding_rectangle_vertices


# get starting pixel of the up and down bounding lines
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


# get starting pixel of the left and right bounding lines
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
# Using this cross we try to avoid "wrong" solutions passing outside the maze (You shall not pass!)
def draw_boundline_cross(start, end, img):
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


# Check if this pixel is close to a wall , and in which direction it's closest
def is_near_wall(pixel, edges, d, dir):
    M, N = edges.shape

    # Choose range we will look for walls in based on direction of movement
    if dir == 'r':
        ranges = (-d, d, 0, d)
    elif dir == 'l':
        ranges = (-d, d, -d, 0)
    elif dir == 'd':
        ranges = (0, d, -d, d)
    else:
        ranges = (-d, 0, -d, d)

    wallSurrounding = False
    for i in range(ranges[0], ranges[1]):
        for j in range(ranges[2], ranges[3]):
            x = pixel.X + i
            y = pixel.Y + j

            # Check if this is a wall pixel
            if x < M and y < N and edges[x][y] > 200:
                wallSurrounding = True
                break
        if wallSurrounding:
            break

    return wallSurrounding


# Check if pixel is maze end, end is considered any pixel in the close environment of the input end pixel
def is_end(pixel, end, maze_size):
    return (abs(pixel.X - end[0]) < (maze_size[0] * 0.005)) and (abs(pixel.Y - end[1]) < (maze_size[1] * 0.005))


# get direction of solution line movement
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


# get the relation between sizes pre and post resize, in order to calculate new points coordinates
def get_resize_relations(size_old, size_new):
    size_x_new = size_new[0]
    size_y_new = size_new[1]
    size_x_old = size_old[0]
    size_y_old = size_old[1]

    r_x = size_x_new / size_x_old
    r_y = size_y_new / size_y_old

    return r_x, r_y


# calculate new coordinates of (x,y) after resizing an image
def get_new_coords_by_relations(x, y, Rx, Ry):
    return round(Rx * x), round(Ry * y)


# calculate new coordinates of point after cropping the maze image, based on the difference of size
def get_new_coords_after_crop(bound_rect_vertices, x, y):
    delta_x = bound_rect_vertices[0][1]  # row of left upper corner of crop section
    delta_y = bound_rect_vertices[0][0]  # col of left upper corner of crop section
    x_new = x - delta_x
    y_new = y - delta_y

    return x_new, y_new


def is_wall(pixel, edges):
    return edges[pixel.X][pixel.Y] > 200


# Find direction of closest wall for centering the drawing line
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


# Find direction of closest wall for centering the drawing line
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


# Get the range of sizes we try to resize the maze to before solving, based on original size
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


# Get the new size of the maze we are going to solve based on the resize relation
def get_solve_size(img, resize):
    new_size_x = img.shape[0]
    new_size_y = img.shape[1]
    new_size_x = round(new_size_x * resize)
    new_size_y = round(new_size_y * resize)
    return new_size_x, new_size_y


# Prepare maze for next solving attempt by reseting all info of pixels we saw
def restartMaze(seen):
    for pixel in seen:
        pixel.visited = 0
        pixel.prev = None


# Try to solve the maze using BFS
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
                # if a neighbor is the end pixel, we have solved the maze!
                if (is_end(maze[r][c], solving_end, edges.shape)):
                    maze[r][c].visited = 1
                    maze[r][c].prev = curr
                    return True, seen, (maze[r][c].X, maze[r][c].Y)

                # If this neighbor is not a wall, add it to the queue
                elif (maze[r][c].visited == 0 and not is_near_wall(maze[r][c], edges, Pixel.d,
                                                                   get_dir(curr, maze[r][c]))):
                    seen.append(maze[r][c])
                    q.put(maze[r][c])
                    maze[r][c].visited = 1
                    maze[r][c].prev = curr

    return False, seen, None


# use solution on the resized cropped image to draw solution line on original image
def draw_solution_on_original_image(original_image, end, edges, bb, Rx, Ry):
    curr = end
    left = bb[0][0]
    up = bb[0][1]
    last_u_d = 'u'
    last_l_r = 'r'

    while (curr.prev != None):
        prev = curr.prev
        dir = get_dir(prev, curr)
        pre_resize_corrds = get_new_coords_by_relations(curr.X, curr.Y, Rx,
                                                        Ry)  # coordinates of cropped image before resizing
        original_image_coords = (pre_resize_corrds[0] + up, pre_resize_corrds[1] + left)  # coords of original image

        if dir == 'u' or dir == 'd':
            draw_range = round(Pixel.draw_line_size[Pixel.d] * Ry)
            closer_to = checkCloseSideLeftRight(curr, edges)
            if (closer_to == 's' and last_l_r == 'l') or closer_to == 'l':
                last_l_r = 'l'
                for j in range(draw_range):
                    if j + original_image_coords[1] < original_image.shape[1]:
                        original_image[original_image_coords[0], original_image_coords[1] + j, :2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] + j, 2] = 255
                    else:
                        break
            elif (closer_to == 's' and last_l_r == 'r') or closer_to == 'r':
                last_l_r = 'r'
                for j in range(draw_range):
                    if original_image_coords[1] - j >= 0:
                        original_image[original_image_coords[0], original_image_coords[1] - j, :2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] - j, 2] = 255
                    else:
                        break
            else:
                last_l_r = 'e'
                for j in range(draw_range // 2):
                    if original_image_coords[1] - j >= 0:
                        original_image[original_image_coords[0], original_image_coords[1] - j, :2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] - j, 2] = 255
                    if original_image_coords[1] + j < original_image.shape[1]:
                        original_image[original_image_coords[0], original_image_coords[1] + j, :2] = 0
                        original_image[original_image_coords[0], original_image_coords[1] + j, 2] = 255

        else:
            draw_range = round(Pixel.draw_line_size[Pixel.d] * Rx)
            closer_to = checkCloseSideUpDown(curr, edges)
            if (closer_to == 's' and last_u_d == 'u') or closer_to == 'u':
                last_u_d = 'u'
                for j in range(draw_range):
                    if original_image_coords[0] + j < original_image.shape[0]:
                        original_image[original_image_coords[0] + j, original_image_coords[1], :2] = 0
                        original_image[original_image_coords[0] + j, original_image_coords[1], 2] = 255
                    else:
                        break

            elif (closer_to == 's' and last_u_d == 'd') or closer_to == 'd':
                last_u_d = 'd'
                for j in range(draw_range):
                    if original_image_coords[0] - j >= 0:
                        original_image[original_image_coords[0] - j, original_image_coords[1], :2] = 0
                        original_image[original_image_coords[0] - j, original_image_coords[1], 2] = 255
                    else:
                        break
            else:
                last_u_d = 'e'
                for j in range(draw_range // 2):
                    if original_image_coords[0] - j >= 0:
                        original_image[original_image_coords[0] - j, original_image_coords[1], :2] = 0
                        original_image[original_image_coords[0] - j, original_image_coords[1], 2] = 255
                    if original_image_coords[0] + j < original_image.shape[0]:
                        original_image[original_image_coords[0] + j, original_image_coords[1], :2] = 0
                        original_image[original_image_coords[0] + j, original_image_coords[1], 2] = 255

        curr = curr.prev


# Check that input start and end points were in the maze (not cropped)
# If input points are outside the maze we will return a Fail message to the UI program to display to the user
def check_input_points_after_crop(end_after_crop, start_after_crop, size_after_crop):
    for i in range(2):
        if (end_after_crop[i] < 0 or end_after_crop[i] >= size_after_crop[i] or start_after_crop[i] < 0 or
                start_after_crop[i] >= size_after_crop[i]):
            return False
    return True


if __name__ == "__main__":
    # Procces input params
    start_param, end_param, image_path_param, ui_image_size_param, maze_name = proccess_params(sys.argv[1:])

    # Read maze image based on input path
    original_colored_image = cv.imread(image_path_param)
    if original_colored_image is None:
        print("*Failed2*")  # Failed due to invalid image file path
        exit(0)

    # calculate actual start and end coordinates based on relation between the UI maze size and the original size
    Rx_ui, Ry_ui = get_resize_relations(ui_image_size_param, original_colored_image.shape[:-1])
    original_start = get_new_coords_by_relations(start_param[0], start_param[1], Rx_ui, Ry_ui)
    original_end = get_new_coords_by_relations(end_param[0], end_param[1], Rx_ui, Ry_ui)

    # Crop background of image to optimize the solving process and calculate new start and end coordinates
    cropped_image, bounding_rect_vertices = crop_background(original_colored_image)
    start_after_crop = get_new_coords_after_crop(bounding_rect_vertices, original_start[0], original_start[1])
    end_after_crop = get_new_coords_after_crop(bounding_rect_vertices, original_end[0], original_end[1])
    size_after_crop = cropped_image.shape[:-1]

    # Validate that the input start and end points are inside the maze, otherwise send Fail msg
    valid_start_end_points = check_input_points_after_crop(end_after_crop, start_after_crop, size_after_crop)
    if not valid_start_end_points:
        print("*Failed1*")  # points cropped error
        exit(0)

    # Begin solving attemps!
    solve_flag = False
    start_size = get_solve_size_range(cropped_image)
    for i in np.arange(start_size, 1.2, 0.2):
        #  Compress the maze img for quicker solving
        solve_size = get_solve_size(cropped_image, i)
        resized_cropped_image = cv.resize(cropped_image, solve_size[::-1])
        Rx, Ry = get_resize_relations(size_after_crop, solve_size)
        solving_start = get_new_coords_by_relations(start_after_crop[0], start_after_crop[1], Rx, Ry)
        solving_end = get_new_coords_by_relations(end_after_crop[0], end_after_crop[1], Rx, Ry)

        # Perform edge detection with the Canny algorithm for wall detection
        gray_image = cv.cvtColor(resized_cropped_image, cv.COLOR_BGR2GRAY)
        edges = cv.Canny(gray_image, 100, 200)

        # Add bound line cross to avoid "illegal" solutions outside the maze
        draw_boundline_cross(solving_start, solving_end, edges)

        maze = init_maze(gray_image)
        N, M = edges.shape
        # Attempt solving with decreasing distances from walls (For a nicer looking solution not to close to wall)
        for distance in Pixel.ds:
            Pixel.d = distance
            found, seen, solved_end = solve_maze()
            if found:
                # Maze solved, get actual end finish
                solve_flag = True
                solving_end = solved_end
                break
            else:
                # Restart attempt info before next attempt
                restartMaze(seen)

        # Maze was successfully solved
        if solve_flag:
            end_pixel = maze[solving_end[0]][solving_end[1]]
            draw_solution_on_original_image(original_colored_image, end_pixel, edges, bounding_rect_vertices, 1 / Rx, 1 / Ry)
            solution_name = save_solution_img(original_colored_image, maze_name)
            print(f"*{solution_name}*")
            exit(0)

    if not solve_flag:
        print("*Failed to solve maze*")
