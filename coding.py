# Importing all the Python modules used in the program	
import cv2
import numpy as np
from tqdm import tqdm
import json
from skimage.metrics import structural_similarity # Import structural_similarity to compare my image to the original image

'''
Overall idea of the program
1. Loads the original image and the puzzle pieces
2. For each puzzle piece it finds its original location in the image and then place it onto the canvas
3. Evaluates my puzzle against the original image
'''

# This class here represents a puzzle piece
# It encapsualtes the image, id and recatangle information for each puzzle piece
class PuzzlePiece:
	def __init__(self, image, id_=None, rect=None):
		self.image = image
		self.id = id_
		self.rect = rect

# Puzzle loader is the abstract class providign the 'load' method
# It implements the Factory design pattern with its two subclasses PuzzlePiecesLoader and OriginalImageLoader
class PuzzleLoader:
	def load(self):
		pass

# This is a subclass of 'PuzzleLoader'
# It overrides the load method to read the JSON and create a PuzzlePiece objects for each piece 
class PuzzlePiecesLoader(PuzzleLoader):
	def __init__(self, pieces_json_path):
		self.pieces_json_path = pieces_json_path

	def load(self):
		puzzle_pieces = []
		with open(self.pieces_json_path) as json_file:
			pieces = json.load(json_file)
			for piece in pieces:
				image = cv2.imread(f"./puzzle_pieces/{piece['id']}.jpg")
				p = PuzzlePiece(image, id_=piece['id'])
				puzzle_pieces.append(p)
		return puzzle_pieces

# This is another subclass of 'PuzzleLoader'
# This class loads the original image and splits it into pieces. 
# It overrides the load method and creates a PuzzlePiece object for each piece
class OriginalImageLoader(PuzzleLoader):
	def __init__(self, image_path):
		self.image_path = image_path

	def load(self):
		image = cv2.imread(self.image_path)
		h, w, _ = image.shape
		h_step = int(h / 40)
		w_step = int(w / 60)
	
		original_pieces = []
		for i in range(0, h, h_step):
			for j in range(0, w, w_step):
				rect = (j, i, w_step, h_step)
				original_pieces.append(PuzzlePiece(image[i:i+h_step, j:j+w_step], rect=rect))

		return image, original_pieces

# This class which solves and evaluates our puzzle implements the Template design pattern
# Here the solve_puzzle method acts as the template method. 
class PuzzleSolver:
	def __init__(self, original_image, shuffled_pieces):
		self.original_image = original_image
		self.shuffled_pieces = shuffled_pieces
		self.completed_puzzle = np.zeros_like(self.original_image)

	# This method solves the puzzles
	def solve_puzzle(self):
		for piece in tqdm(self.shuffled_pieces):
			original_location = self.find_original_location(piece)
			if original_location:
				x, y, _, _ = original_location
				self.completed_puzzle[y:y+piece.image.shape[0], x:x+piece.image.shape[1]] = piece.image
	
	# This method finds the original location of puzzle pieces
	def find_original_location(self, piece):
		for original_piece in self.original_pieces:
			correlation_score = cv2.matchTemplate(original_piece.image, piece.image, cv2.TM_CCOEFF_NORMED)
			max_score = np.max(correlation_score)
			if max_score > 0.9: # Threshold for similarity, tried many different numbers 0.9 turned out to be the most acccurate
				return original_piece.rect
		return None

	# This compares our puzzle to the original image
	def evaluate_puzzle(self):
		original_image_gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
		completed_puzzle_gray = cv2.cvtColor(self.completed_puzzle, cv2.COLOR_BGR2GRAY)

		ssim_score = structural_similarity(original_image_gray, completed_puzzle_gray)
		print(f"SSIM Score: {ssim_score}")

if __name__ == "__main__":
	shuffled_puzzle_loader = PuzzlePiecesLoader("puzzle_pieces.json")
	shuffled_puzzle_pieces = shuffled_puzzle_loader.load()

	original_image_loader = OriginalImageLoader("image.jpg")
	image, original_pieces = original_image_loader.load()

	solver = PuzzleSolver(image, shuffled_puzzle_pieces)
	solver.original_pieces = original_pieces
	solver.solve_puzzle()
	solver.evaluate_puzzle()

	cv2.imshow("Completed Puzzle", solver.completed_puzzle)
	cv2.waitKey(0)

