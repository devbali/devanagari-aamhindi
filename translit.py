import re

with open("in","r") as inf: string = inf.read()

special_words = [("तो", "toh")]

class Vowel ():
	def __init__ (self, string, matra, latin, terminal = None):
		self.string = string
		self.matra = matra
		self.latin = latin
		if terminal is None: self.terminal = self.latin
		else: self.terminal = terminal

	def __str__ (self): return self.string

class Consonant ():
	def __init__ (self, string, latin, asp = None, n="n"):
		self.string = string
		self.asp = asp
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

		self.start = False
		self.terminal = False
		self.halant = False

		self.previous = None
		self.next = None

	def get_override (self,cons,vow):
		if not self.start and self.cons is not None and self.cons.string == "ह" and self.vowel is None:
			if vow == "": return (None,None,None)
			return (None,None,"he")
		if not self.terminal and self.next.cons is not None and self.next.cons.string == "ह" and self.next.vowel is None:
			return (None, "e", None)
		if not self.start and self.cons is not None and self.cons.string == "ह" and self.vowel is not None and self.vowel.string == "उ":
			return (None, None, "ho")
		if not self.terminal and self.next.cons is not None and self.next.cons.string == "ह" and self.next.vowel is not None and self.next.vowel == "उ":
			return (None, "o", None)
		if self.terminal and self.n and self.vowel is not None and self.vowel.string == "ए":
			return (None, "ein", None)

		return (None, None, None)

	def __str__ (self):
		vowelstr = ""
		cons = ""

		if self.vowel is not None:
			if self.terminal and not self.n: vowelstr = self.vowel.terminal
			else: vowelstr = self.vowel.latin

			if self.terminal and self.n: vowelstr += "n"

			if self.cons is None:
				if self.caryonn: vowelstr = "n" + vowelstr
				return vowelstr

		elif not self.halant and not self.terminal and (self.start or self.terminal or self.previous.halant or self.caryonn  or self.next.halant or self.next.vowel is None):
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
			firstset, lastset = (False, False)
			for i in range(0,len(syll_list)-1):
				#print(i,firstset)
				if firstset and type(syll_list[i]) == Syllable:
					syll_list[i].previous = syll_list[i-1]
				elif type(syll_list[i]) == Syllable:
					syll_list[i].start = True
					firstset = True

				if firstset and type(syll_list[i+1]) == Syllable:
					syll_list[i].next = syll_list[i+1]
				elif firstset:
					syll_list[i].terminal = True
					break

			if not firstset and type(syll_list[-1]) == Syllable: syll_list[-1].start = True
			if type(syll_list[-1]) == Syllable: syll_list[-1].terminal = True

			for i in syll_list:
				if type(i) == Syllable:
					if(i.start): print("<", end = "")
					print (i, end="")
					if(i.terminal): print (">", end = "")
					print(" ",end="")
				else: print(i, end = " ")
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
		Consonant("य","y"), Consonant("र","r"), Consonant("ल","l"), Consonant("व","w"),
		Consonant("श","sh"), Consonant("ष","sh"), Consonant("स","s"), Consonant("ह","h"), 
		]

special_consonants = [
		Consonant("क़","q"), Consonant("ख़","kh"), Consonant("ग़","gh"), Consonant("ज़","z"),
		Consonant("ड़","d","ढ़"), Consonant("फ़","f"), Consonant("ज्ञ","gy")
		]

spliters = ["\n"," ","-"]

stringwords = []
i = 0
j = 0
while j < len(string):
	if string[j] in spliters and i != j:
		stringwords.append((string[i:j],string[j]))
		i = j + 1
	j += 1
stringwords.append((string[i:],""))

words = []
cooked = ""
for word, spliter in stringwords: cooked += str(Word(word)) + spliter
with open("out","w") as outf: outf.write(cooked)
