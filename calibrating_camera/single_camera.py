from glob import glob

import cv2 as cv
import numpy as np

# Chessboard dimensions (inner corners)
pattern_size = (9, 6)
square_size = 25.0  # millimeters

# Prepare object points (0,0,0), (1,0,0), (2,0,0), ..., (8,5,0)
pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
pattern_points *= square_size

# Arrays to store object points and image points
obj_points = []  # 3D points in real world
img_points = []  # 2D points in image plane

# Load calibration images
images = glob("calibration_photos/*.jpg")

print(f"Found {len(images)} images")

for fname in images:
    print(f"Processing {fname}...")

    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find chessboard corners
    found, corners = cv.findChessboardCorners(gray, pattern_size, None)

    if found:
        print(f"  Corners found")

        # Refine corner locations
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners_refined = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Store points
        obj_points.append(pattern_points)
        img_points.append(corners_refined)

        # Draw and display corners
        cv.drawChessboardCorners(img, pattern_size, corners_refined, found)
        cv.imshow("Chessboard", img)
        cv.waitKey(100)
    else:
        print(f"  Pattern not found")

cv.destroyAllWindows()

# Calibrate camera
print("\nCalibrating camera...")
h, w = gray.shape[:2]
ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv.calibrateCamera(
    obj_points, img_points, (w, h), None, None
)

# Print results
print(f"\nCalibration successful!")
print(f"RMS re-projection error: {ret:.4f}")
print(f"\nCamera matrix:\n{camera_matrix}")
print(f"\nDistortion coefficients:\n{dist_coeffs.ravel()}")

# Save calibration
np.savez(
    "calibration.npz",
    camera_matrix=camera_matrix,
    dist_coeffs=dist_coeffs,
    rvecs=rvecs,
    tvecs=tvecs,
)

print("\nCalibration saved to calibration.npz")
