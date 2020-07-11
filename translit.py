import re

with open("in","r") as inf: string = inf.read()

special_words = [("तो", "toh")]
all_devanagari = ["्","़","ं","ँ"]

class Vowel ():
	def __init__ (self, string, matra, latin, terminal = None):
		global all_devanagari
		self.string = string
		self.matra = matra
		all_devanagari += [string, matra]
		self.latin = latin
		if terminal is None: self.terminal = self.latin
		else: self.terminal = terminal

	def __str__ (self): return self.string

class Consonant ():
	def __init__ (self, string, latin, asp = None, n="n"):
		global all_devanagari
		self.string = string
		self.asp = asp
		all_devanagari += [string, asp]
		self.latin = latin
		self.n = n

	def __str__ (self): return self.string

class Syllable ():
	def __init__ (self, cons):
		self.cons = cons
		self.vowel = None
		self.asp = False
		self.n = False
		self.caryonn = False
		self.wordlength = 0

		self.start = False
		self.terminal = False
		self.halant = False

		self.previous = None
		self.next = None

	def get_override (self,cons,vow):
		if not self.start and self.cons is not None and self.cons.string == "ह" and self.vowel is None:
			if vow != "": return (None,None,"he")
		if not self.start and self.cons is not None and self.cons.string == "ह" and self.vowel is not None and self.vowel.string == "उ":
			return (None, None, "ho")

		cons_override = None
		vowel_override = None
		if cons == "v" and not self.start and (self.previous.halant or not self.terminal and (vow == "a" or vow == "aa")):
			cons_override = "w"
		if not self.terminal and self.next.cons is not None and self.next.cons.string == "ह" and self.next.vowel is None:
			vowel_override = "e"
		if not self.terminal and self.next.cons is not None and self.next.cons.string == "ह" and self.next.vowel is not None and self.next.vowel == "उ":
			vowel_override = "o"
		if self.terminal and self.n and self.vowel is not None and self.vowel.string == "ए":
			vowel_override = "ein"

		return (cons_override, vowel_override, None)

	def __str__ (self):
		vowelstr = ""
		cons = ""

		# Schwa Dropping
		if self.vowel == None and self.terminal or not (self.start or (self.terminal or self.previous.halant) or self.caryonn or self.next.halant or self.next.vowel is None):
			self.halant = True

		if self.vowel is not None:
			# Starting आs are "a", their terminal ending, in most cases (when words are longer than two letters)
			if (self.start and self.cons is None and self.vowel.string == "आ" and self.wordlength > 2) or (self.terminal and not self.n): vowelstr = self.vowel.terminal
			else: vowelstr = self.vowel.latin

			if self.terminal and self.n: vowelstr += "n"

			if self.cons is None:
				if self.caryonn: vowelstr = "n" + vowelstr
				return vowelstr

		elif not self.halant:
			vowelstr = "a"

		cons = self.cons.latin
		if self.asp: cons += "h"
		if self.caryonn: cons = self.cons.n + cons

		cons_override, vowel_override, all_override = self.get_override(cons, vowelstr)

		if cons_override is not None: return cons_override + vowelstr
		if vowel_override is not None: return cons + vowel_override
		if all_override is not None: return all_override
		return cons + vowelstr

def is_cons(string, index, cons):
	if string[index:index+len(cons.string)] == cons.string: return 1
	if cons.asp is not None and string[index:index+len(cons.asp)] == cons.asp: return 2
	return 0

def is_vowel(string, index, vowel):
	if string[index:index+len(vowel.string)] == vowel.string: return 1
	if string[index:index+len(vowel.matra)] == vowel.matra: return 2
	return 0

class Word():
	def __init__ (self, string):
		print("WORD",string)
		self.override = None

		if len(string) == 0: 
			self.sylls = []
			return

		for word, replacement in special_words:
			if word == string:
				self.override = replacement
				return

		global vowels, consonants, special_consonants

		def set_previous_and_next (syll_list):
			for i in range(1,len(syll_list)):
				syll_list[i].previous = syll_list[i-1]
				syll_list[i].wordlength = len(syll_list)
			for i in range(len(syll_list)-1):
				syll_list[i].next = syll_list[i+1]
			syll_list[0].start = True
			syll_list[0].wordlength = len(syll_list)
			syll_list[-1].terminal = True

			for i in syll_list:
				if(i.start): print("<", end = "")
				print (i, end="")
				if(i.terminal): print (">", end = "")
				print(" ",end="")
			print("\n")

		i = 0
		self.sylls = []
		syll = None
		caryonn = False
		while i < len(string):
			found = False
			for c in special_consonants + consonants:
				if is_cons(string, i, c) > 0:
					print("FOUND CONSONANT",c)
					if syll is not None: self.sylls.append(syll)
					syll = Syllable(c)
					if caryonn:
						syll.caryonn = True
						caryonn = False
					syll.asp = is_cons(string,i,c) == 2
					i += len(c.string)
					found = True
					break

			if found: continue

			if string[i] == "ं" or string[i] == "ँ":
				print("FOUND n")
				syll.n = True
				caryonn = True
				i += 1
				continue

			if string[i] == "्":
				syll.halant = True
				i += 1
				continue

			for v in vowels:
				if is_vowel(string, i, v) > 0:
					print("FOUND VOWEL",v)
					if syll is None or syll.vowel is not None:
						if syll is not None: self.sylls.append(syll)
						syll = Syllable(None)
						syll.vowel = v
					elif syll is not None:
						syll.vowel = v
					i += 1
					found = True
					break

			if not (syll is None or found):
				break
			elif not found:
				self.sylls.append(string[i])
				i += 1

		if syll is not None: 
			self.sylls.append(syll)
		for i in range(i, len(string)): self.sylls.append(string[i])
		set_previous_and_next (self.sylls)

	def __str__ (self):
		if self.override is not None: return self.override
		string = ""
		for i in self.sylls: string += str(i)
		return string

vowels = [
		Vowel("अ","\\","a"), Vowel("आ","ा","aa","a"),
		Vowel("इ","ि","i"), Vowel("ई","ी","ee","i"),
		Vowel("उ","ु","u"), Vowel("ऊ","ू","oo","u"),
		Vowel("ए","े","e"), Vowel("ऐ","ै","ai"),
		Vowel("ओ","ो","o"), Vowel("औ","ौ","au"),
		Vowel("ऋ","ृ","ri")
		]

consonants = [
		Consonant("क","k","ख"), Consonant("ग","g","घ"),
		Consonant("च","ch","छ"), Consonant("ज","j","झ"),
		Consonant("ट","t","ठ"), Consonant("ड","d","ढ"), Consonant("ण","n"),
		Consonant("त","t","थ"), Consonant("द","d","ध"), Consonant("न","n"),
		Consonant("प","p","फ","m"), Consonant("ब","b","भ","m"), Consonant("म","m"),
		Consonant("य","y"), Consonant("र","r"), Consonant("ल","l"), Consonant("व","v"),
		Consonant("श","sh"), Consonant("ष","sh"), Consonant("स","s"), Consonant("ह","h"), 
		]

special_consonants = [
		Consonant("क़","q"), Consonant("ख़","kh"), Consonant("ग़","gh"), Consonant("ज़","z"),
		Consonant("ड़","d","ढ़"), Consonant("फ़","f"), Consonant("ज्ञ","gy")
		]

cooked = ""
tempword = ""
currentlyrandom = False
for c in string + " ": # Space forces last tempword to be 'random'
	if c in all_devanagari and currentlyrandom:
		cooked += tempword
		tempword = c
		currentlyrandom = False
	elif c in all_devanagari: tempword += c
	elif c not in all_devanagari and currentlyrandom: tempword += c
	else:
		cooked += str(Word(tempword))
		tempword = c
		currentlyrandom = True

if len(tempword) > 1: cooked += tempword[:-1] # Drops the space
with open("out","w") as outf: outf.write(cooked)
