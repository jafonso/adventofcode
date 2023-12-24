import aocutils
import numpy as np
from typing import List, Tuple

test_array = [
    "19, 13, 30 @ -2,  1, -2",
    "18, 19, 22 @ -1, -1, -2",
    "20, 25, 34 @ -2, -2, -4",
    "12, 31, 28 @ -1, -2, -1",
    "20, 19, 15 @  1, -5, -3",
]

class NoIntersection(Exception):
    pass

def parse_data(input: List[str]):
    return [((int(x), int(y), int(z)), (int(vx), int(vy), int(vz))) for (x, y, z), (vx, vy, vz) in [(pos.split(","), vel.split(","))for pos, vel in [entry.split("@") for entry in input]]]

def get_intersection_xy(h1: Tuple[Tuple[int,int,int], Tuple[int,int,int]], h2: Tuple[Tuple[int,int,int], Tuple[int,int,int]]):

    # 'z' is ignored here 

    (x1, y1, _), (vx1, vy1, _) = h1
    (x2, y2, _), (vx2, vy2, _) = h2

    P1 = np.array([x1, y1]).reshape(2,1)
    V1 = np.matrix([
        [vx1, 0],
        [vy1, 0],
    ])
    P2 = np.array([x2, y2]).reshape(2,1)
    V2 = np.matrix([
        [0, vx2],
        [0, vy2],
    ])

    # Calculate X = A^(-1)B
    # Where X = [x,y]
    #       A is matrix of velocities
    #       B is based on original positions

    A = np.matrix([
        [vx1, -vx2],
        [vy1, -vy2],
    ])

    B = np.array([x2-x1, y2-y1]).reshape(2,1)

    try:
        A_inv = np.linalg.inv(A)
    except np.linalg.LinAlgError as e:
        # Impossible to invert, do not intersect
        raise NoIntersection() from e

    X = np.dot(A_inv, B)

    R1 = P1 + np.dot(V1, X)
    R2 = P2 + np.dot(V2, X)

    if not np.allclose(R1, R2):
        raise RuntimeError(f"Result R1 and R2 not equal, something is wrong:\n{R1}\n{R2}")
    
    # Return (x, y) and (t1, t2)
    return np.round(R1, 6).reshape(1,2).tolist()[0], np.round(X, 6).reshape(1,2).tolist()[0]

def calculate_intersections_xy(hailstones: Tuple, min_pos: int, max_pos: int):
    count = 0
    for idx, hail_1 in enumerate(hailstones):
        for hail_2 in hailstones[idx+1:]:
            try:
                (x, y), (t1, t2) = get_intersection_xy(hail_1, hail_2)
            except NoIntersection:
                # Do not intersect, ignore
                continue
            if x < min_pos or x > max_pos or y < min_pos or y > max_pos:
                # Intersected outside of boundaries
                continue
            if t1 < 0 or t2 < 0:
                # Intersected in the past
                continue
            count += 1
    return count

if __name__ == "__main__":

    input_data = aocutils.getDataInput(24)
    #input_data = test_array

    hailstones = parse_data(input_data)

    #### Part 1 ####

    aocutils.printResult(1, calculate_intersections_xy(hailstones, 200000000000000, 400000000000000))

    #### Part 2 ####