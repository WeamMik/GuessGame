import random
import argparse
import functools

class GuessNumber(object):
    def __init__(self):
        self._parse_args()
        self.number_of_tries = 1
        if not self.random_number:
            self.random_number = random.choice(range(self.minmum_num, self.max_num+1)) #, random_number)[random_number is not None]
        self.game_dsc = """
                            Try to guess that number between %s and %s, we will hint  you along the way.
                        """ % (self.minmum_num, self.max_num)

    def _parse_args(self):
        def add_arguments():
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

        args = add_arguments()
        self.minmum_num = args.min_val
        self.max_num = args.max_val
        if self.minmum_num >= self.max_num:
            raise Exception("min value [%s] shoud be less than max value [%s]." % (self.minmum_num, self.max_num))
        self.random_number = args.number_to_guess
        if self.random_number and self.random_number < self.minmum_num or self.random_number > self.max_num:
            raise Exception("The Number to be gussed, should be in the range [%s, %s], %s is not"
                                        % (self.minmum_num, self.max_num, self.random_number))
        self.max_number_of_tries = args.max_number_of_tries
        if self.max_number_of_tries is not None and self.max_number_of_tries < 1:
            raise Exception("Number of Tries at least should be 1")
        return args

    def _congrats(self):
        print("\n%sYou got it right with [%s] guesses, Congratulations B|" % 
                                (("", "FINALYY ")[self.number_of_tries > self.max_num/3], self.number_of_tries))

    def _hint(self):
        print("This number %s is -%s- than the correct value\nTry Again.." % 
                                (self.guess_value, ("lower", "higher")[self.guess_value > self.random_number]))

    def _game_over(self):
        print("\nGame Over, Hard Luck! No more lives :|\nAnswer: %s" % self.random_number)

    def play(self):
        print(self.game_dsc)
        self.guess_value = int(self._guess())
        while self.guess_value != self.random_number and (not self.max_number_of_tries or (self.number_of_tries < self.max_number_of_tries)):
            self._hint()
            if self.max_number_of_tries:
                print("This is your %s guess, You have %s left." % (self.number_of_tries, self.max_number_of_tries - self.number_of_tries))
            self.guess_value = int(self._guess())
            self.number_of_tries += 1
        (self._congrats, self._game_over)[self.guess_value != self.random_number]()

    def _validate(func):
        @functools.wraps(func)
        def guess_wrapper(self):
            guess_value = func(self)
            while not self._is_valid(guess_value):
                guess_value = func(self)
            return guess_value
        return guess_wrapper

    @_validate
    def _guess(self):
        guess_value = raw_input("Please Enter Integer Value between %s and %s: " % (self.minmum_num, self.max_num))
        """while not self.is_valid(guess_value):
            guess_value = raw_input("Please Enter Integer Value between %s and %s: " % (self.minmum_num, self.max_num))
        """
        return guess_value

    def _is_valid(self, value):
        """
        Function will check  if the value entered is valid:
        1- integer type
        2- within  the range
        """
        valid = True
        try:
            value = int(value)
            if (self.minmum_num > value or  value > self.max_num):
                print("[%s] Not Valid, range should be between %s and %s: " % (value, self.minmum_num, self.max_num))
                valid = False
        except ValueError:          
            print("[%s] Not Valid, only enter integer value" % value)
            valid = False
        return valid

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
