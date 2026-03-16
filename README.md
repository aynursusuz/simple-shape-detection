# Simple Shape Detection

Polygon detection and classification using OpenCV contour analysis.

![Output](simple_shape_detection.png)

## How It Works

1. Convert input image to grayscale and apply binary thresholding
2. Find contours with `cv2.findContours`
3. Approximate each contour to a polygon using Douglas-Peucker algorithm (`cv2.approxPolyDP`)
4. Classify by vertex count:
   - **3** → Triangle
   - **4** → Rectangle
   - **5** → Pentagon
   - **6** → Hexagon
   - **Other** → Ellipse

## Usage

```bash
pip install opencv-python numpy
python simple_shape_detection.py
```

Expects a `polygons.png` input image in the same directory. The script draws detected contours and labels each shape on the output window.

## Dependencies

- OpenCV
- NumPy

## License

MIT
