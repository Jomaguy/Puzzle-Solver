Puzzle Solver and Evaluator 

This project is an image-processing-based puzzle solver. It reconstructs a shuffled puzzle by comparing individual pieces to the original image and evaluates the correctness of the solved puzzle using Structural Similarity Index (SSIM). The program leverages OpenCV for image manipulation, tqdm for progress tracking, and skimage for image quality comparison.

### Features
Loads an original image and a set of shuffled puzzle pieces.
Place each puzzle piece back in its original position using template matching.
Evaluates the accuracy of the reconstructed puzzle by comparing it with the original image using SSIM.
Implements Factory and Template design patterns for puzzle piece loading and solving.

### How It Works
Load Puzzle Pieces: The puzzle pieces are loaded from a JSON file (puzzle_pieces.json), which contains the metadata of each piece.
Load Original Image: The original image is loaded and split into individual pieces to compare against the shuffled pieces.
Solve Puzzle: Each shuffled puzzle piece is compared with the original image pieces to find its correct location using template matching.
Evaluate Puzzle: The reconstructed puzzle is compared to the original image using the SSIM metric to determine how well the puzzle was solved.
Display Puzzle: The solved puzzle is displayed using OpenCV.

### Usage
1. Clone the repository and navigate to the project directory.

2. Place your original image in the project directory and name it image.jpg. Ensure the shuffled puzzle pieces are stored in a folder called puzzle_pieces/ with image names corresponding to the IDs in puzzle_pieces.json.

3. Run the program:
