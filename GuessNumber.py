import random
import argparse
import functools

class GuessNumber(object):
	def __init__(self):
		self.parseArgs()
		self.numberOfTries = 1
		if not self.randomNumber:
			self.randomNumber = random.choice(range(self.minmumNum, self.maxNum + 1)) #, random_number)[random_number is not None]
		self.gameDsc = """
						Try to guess that number between %s and %s, we will hint  you along the way.
				  	   """ % (self.minmumNum, self.maxNum)

	def parseArgs(self):
		def addArguments():
			parser = argparse.ArgumentParser()
			parser.add_argument("--min", dest="min_val", type=int, default=0,
		                    	help='Minmum value of the range, that user will guess from - default 0')
			parser.add_argument("--max", dest="max_val", type=int, default=100,
		                    	help='Maximum value, of the range that user will guess from - default 100')
			parser.add_argument("-n", "--the_number", dest="number_to_guess", type=int, 
								help="The Number that user will try to guess, or it will be randomized")
			parser.add_argument("-t", "--max_tries", dest="max_number_of_tries", type=int,
								help="Maximum Number of Tries, or there will be no limit.")
			return parser.parse_args()

		args = addArguments()
		self.minmumNum = args.min_val
		self.maxNum = args.max_val
		if self.minmumNum >= self.maxNum:
			raise Exception("min value [%s] shoud be less than max value [%s]." % (self.minmumNum, self.maxNum))
		self.randomNumber = args.number_to_guess
		if self.randomNumber and self.randomNumber < self.minmumNum or self.randomNumber > self.maxNum:
			raise Exception("The Number to be gussed, should be in the range [%s, %s], %s is not"
										% (self.minmumNum, self.maxNum, self.randomNumber))
		self.maxNumberOfTries = args.max_number_of_tries
		if self.maxNumberOfTries is not None and self.maxNumberOfTries < 1:
			raise Exception("Number of Tries at least should be 1")
		return args

	def congrats(self):
		print("\n%sYou got it right with [%s] guesses, Congratulations B|" % 
								(("", "FINALYY ")[self.numberOfTries > self.maxNum/3], self.numberOfTries))

	def hint(self):
		print("This number %s is -%s- than the correct value\nTry Again.." % 
								(self.guessVal, ("lower", "higher")[self.guessVal > self.randomNumber]))

	def gameOver(self):
		print("\nGame Over, Hard Luck! No more lives :|\nAnswer: %s" % self.randomNumber)

	def play(self):
		print(self.gameDsc)
		self.guessVal = int(self.guess())
		while self.guessVal != self.randomNumber and (not self.maxNumberOfTries or (self.numberOfTries < self.maxNumberOfTries)):
			self.hint()
			if self.maxNumberOfTries:
				print("This is your %s guess, You have %s left." % (self.numberOfTries, self.maxNumberOfTries - self.numberOfTries))
			self.guessVal = int(self.guess())
			self.numberOfTries += 1
		(self.congrats, self.gameOver)[self.guessVal != self.randomNumber]()

	def validate(func):
		@functools.wraps(func)
		def guessWrapper(self):
			guessVal = func(self)
			while not self.isValid(guessVal):
				guessVal = func(self)
			return guessVal
		return guessWrapper

	@validate
	def guess(self):
		guessVal = raw_input("Please Enter Integer Value between %s and %s: " % (self.minmumNum, self.maxNum))
		"""while not self.isValid(guessVal):
			guessVal = raw_input("Please Enter Integer Value between %s and %s: " % (self.minmumNum, self.maxNum))
		"""
		return guessVal

	def isValid(self, value):
		"""
		Function will check  if the value entered is valid:
		1- integer type
		2- within  the range
		"""
		valid = True
		try:
			value = int(value)
			if (self.minmumNum > value or  value > self.maxNum):
				print("[%s] Not Valid, range should be between %s and %s: " % (value, self.minmumNum, self.maxNum))
				valid = False
		except ValueError:			
			print("[%s] Not Valid, only enter integer value" % value)
			valid = False
		return valid

def addArguments():
	pass

def main():
	"""
	Play the game
	"""
	try:
		game = GuessNumber()
		game.play()
	except Exception, e:
		print(str(e))

if __name__ == "__main__":
	main()
