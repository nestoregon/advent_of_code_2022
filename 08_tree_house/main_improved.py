from typing import List


def read_input_as_lines(input_path: str) -> List[List[int]]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    # cast to int
    map = [[int(i) for i in row] for row in lines]
    return map


def main():
    input = read_input_as_lines('input.txt')
    W = len(input[0])
    H = len(input)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    p1 = 0
    for x in range(W):
        for y in range(H):
            visible = False
            for dx, dy in directions:
                xx = x
                yy = y
                while True:
                    xx += dx
                    yy += dy
                    if 0 <= xx < W and 0 <= yy < W:
                        if input[xx][yy] >= input[x][y]:
                            # it ends when there's a tree that is equal or higher
                            break
                    else:
                        # it ends when the shore is reached += 1!
                        visible = True
                        break
                if visible:
                    break
            if visible:
                p1 += 1

    p2 = 0
    for x in range(W):
        for y in range(H):
            visible = False
            score = 1
            for dx, dy in directions:
                xx = x
                yy = y
                tree_counter = 0
                while True:
                    xx += dx
                    yy += dy
                    if 0 <= xx < W and 0 <= yy < W:
                        tree_counter += 1
                        if input[xx][yy] >= input[x][y]:
                            # it ends when there's a tree that is equal or higher
                            break
                    else:
                        break
                score *= tree_counter
                if score == 0:
                    break  # no point in multiplying by 0
            p2 = max(p2, score)

    print(p1)
    print(p2)


if __name__ == '__main__':
    main()
