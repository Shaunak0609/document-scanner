# Python Document Scanner

This project is a simple document scanner built with Python using OpenCV, NumPy, and Pillow. It detects a document in a photo, applies a perspective transform to get a top-down scan view, and saves the result as a high-contrast black-and-white PDF.

---

## Features

- Edge detection using Canny
- Document detection via contour approximation
- Perspective transformation (like a flatbed scanner)
- Adaptive thresholding for black & white scan effect
- Exports the scanned image as a PDF file