import aocutils
import numpy as np
import functools
import math
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
    
    return R1.reshape(1,2).tolist()[0], X.reshape(1,2).tolist()[0]

def check_same_speed(hailstones: Tuple[Tuple[int,int,int], Tuple[int,int,int]]):
    
    count_vx = dict()
    count_vy = dict()
    count_vz = dict()

    for hail in hailstones:
        (x, y, z), (vx, vy, vz) = hail
        if vx not in count_vx:
            count_vx[vx] = set()
        if vy not in count_vy:
            count_vy[vy] = set()
        if vz not in count_vz:
            count_vz[vz] = set()
        count_vx[vx].add(hail)
        count_vy[vy].add(hail)
        count_vz[vz].add(hail)

    for v, hails in count_vx.items():
        if len(hails) >= 3:
            print(f"Same vx {v} at least trice: ", hails)
    for v, hails in count_vy.items():
        if len(hails) >= 3:
            print(f"Same vy {v} at least trice: ", hails)
    for v, hails in count_vz.items():
        if len(hails) >= 3:
            print(f"Same vz {v} at least trice: ", hails)

def normalize_hail(hailstones: Tuple[Tuple[int,int,int], Tuple[int,int,int]]):
    ref = hailstones[0]
    (x0, y0, z0), (vx0, vy0, vz0) = ref
    return ref, [((x-x0, y-y0, z-z0), (vx-vx0, vy-vy0, vz-vz0)) for (x, y, z), (vx, vy, vz) in hailstones]

def calculate_intersections_xy(hailstones: Tuple[Tuple[int,int,int], Tuple[int,int,int]], min_pos: int, max_pos: int):
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

def print_position_at(hailsone: Tuple[Tuple[int,int,int], Tuple[int,int,int]], t: float, key: str=""):
    print(key, np.array(hailsone[0]) + (t * np.array(hailsone[1])))

def find_gcd(arr):
    return functools.reduce(math.gcd, arr)

def scale_down(v):
    divisor = find_gcd(v)
    return v // divisor

def calculate_rock_trajectory(hailstones: List[Tuple[Tuple[int,int,int], Tuple[int,int,int]]]):

    # Normalize all hails referential to hail #0 (choosed arbitrarily).
    # The hail #0 will end with a starting position and velocity of ((0,0,0), (0,0,0)). This makes following calculations easier.

    (hail_0_ref_p, hail_0_ref_v), norm_hailstones = normalize_hail(hailstones)

    norm_hailstones_0 = norm_hailstones[0]
    norm_hailstones_1 = norm_hailstones[1]
    norm_hailstones_2 = norm_hailstones[2]

    hail_0_pos, hail_0_vel = norm_hailstones_0
    hail_1_pos, hail_1_vel = norm_hailstones_1
    hail_2_pos, hail_2_vel = norm_hailstones_2

    # Use vector of hail #1 and #2, together with hail #0 (a single dot!), to calculate the normal
    # vectors of planes 1 and 2.
    # NOTE: It's important to scale down the result!!!! (we don't care about vector mudule for now, just the direction)

    n_plane_1 = scale_down(np.cross(hail_1_pos, hail_1_vel))
    n_plane_2 = scale_down(np.cross(hail_2_pos, hail_2_vel))

    # Calculate the vector of the intersection between the two planes
    # NOTE: It's important to scale down the result!!!! (we don't care about vector mudule for now, just the direction)

    vel_par = scale_down(np.cross(n_plane_1, n_plane_2))

    # We know that the rock passes by origin (hail #0), and has a direction given by the vector calculated previously
    temp_rock_vect = (hail_0_pos, vel_par)

    # Calculate intersection times between rock, hail #1, hail #2
    # The time of the rock will be wrong but we don't care
    # We will know the time of intersection of hail #1 and hail #2, which will also be the correct time of the rock vector
    _, (t_1, _) = get_intersection_xy(norm_hailstones_1, temp_rock_vect)
    _, (t_2, _) = get_intersection_xy(norm_hailstones_2, temp_rock_vect)

    # Based on the times obtained, calculate the colision coordinates
    colision_coords_1 = np.array(norm_hailstones_1[0], dtype=np.float128) + (t_1 * np.array(norm_hailstones_1[1], dtype=np.float128))
    colision_coords_2 = np.array(norm_hailstones_2[0], dtype=np.float128) + (t_2 * np.array(norm_hailstones_2[1], dtype=np.float128))

    # Calculate the correct coordinates and velocity of the rock
    t_diff = t_2 - t_1
    coord_diff = np.array(colision_coords_2, dtype=np.float128) - np.array(colision_coords_1, dtype=np.float128)
    vel = coord_diff / t_diff
    pos = np.array(colision_coords_1, dtype=np.float128) - (t_1 * vel)

    # Get back the real values!! (reverse the referential transformation)
    vel_real = vel + np.array(hail_0_ref_v, dtype=np.float128)
    pos_real = pos + np.array(hail_0_ref_p, dtype=np.float128)

    return pos_real, vel_real

if __name__ == "__main__":

    input_data = aocutils.getDataInput(24)
    #input_data = test_array

    hailstones = parse_data(input_data)

    #### Part 1 ####

    aocutils.printResult(1, calculate_intersections_xy(hailstones, 200000000000000, 400000000000000))

    #### Part 2 ####

    rock_trajectory = calculate_rock_trajectory(hailstones)
    aocutils.printResult(2, int(np.sum(rock_trajectory[0])))