import argparse
import cv2


# Color map for each shape type (BGR format)
SHAPE_COLORS = {
    "Triangle":  (0, 255, 0),     # green
    "Square":    (255, 0, 0),     # blue
    "Rectangle": (0, 165, 255),   # orange
    "Pentagon":  (0, 255, 255),   # yellow
    "Hexagon":   (255, 0, 255),   # magenta
    "Circle":    (255, 255, 0),   # cyan
}

# Minimum contour area to filter out noise
MIN_CONTOUR_AREA = 500


def classify_shape(approx):
    """Classify a contour by its vertex count and aspect ratio."""
    n = len(approx)

    if n == 3:
        return "Triangle"

    if n == 4:
        # Use aspect ratio to distinguish square from rectangle
        x, y, w, h = cv2.boundingRect(approx)
        ratio = float(w) / h
        return "Square" if 0.85 <= ratio <= 1.15 else "Rectangle"

    if n == 5:
        return "Pentagon"

    if n == 6:
        return "Hexagon"

    return "Circle"


def detect_shapes(image_path):
    """Load an image, detect and label shapes with colored contours."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    font = cv2.FONT_HERSHEY_SIMPLEX

    for cnt in contours:
        # Skip small contours that are likely noise
        if cv2.contourArea(cnt) < MIN_CONTOUR_AREA:
            continue

        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        shape = classify_shape(approx)
        color = SHAPE_COLORS.get(shape, (0, 0, 0))

        cv2.drawContours(img, [approx], 0, color, 3)

        # Place the label near the top-left corner of the contour
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 10
        cv2.putText(img, shape, (x, y), font, 0.7, color, 2)

    cv2.imshow("Shape Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description="Detect and classify shapes in an image.")
    parser.add_argument("image", nargs="?", default="polygons.png", help="Path to input image")
    args = parser.parse_args()

    detect_shapes(args.image)


if __name__ == "__main__":
    main()
