# Devanagari to Aam Latin Hindi
Algorithm to transliterate Hindi from Devanagari to "Aam Latin Hindi," or Hindi in the Latin script commonly used in texting and online instead of standardized transliterations

## About the Algorithm
Transliteration from Devanagari often takes two forms.
- One is IAST, or various variations of this concept, which use diacritics to preserve all devanagari information into Latin
- Second is something like ITRANS, or systems that eliminate diacritics but use double vowels and lose some information, but maintain most of it

However, Hindi is very often written in the Latin script, and in virtually all non-governmental uses, a different scheme is used. I am calling this "Aam Latin Hindi," and here are the key differences:
- Schwa dropping and the use of "a": The word आवारा is transliterated aawaaraa in ITRANS but awaara in Aam Latin Hindi
- The use of "ee" vs "i" and "oo" vs "u". These are never used in standard transliterations, but are used in Aam Latin Hindi
- Some inconsistencies like the ending एं is transliterated as "ein" instead of the expected "en"
- And many more

## To Use
- Clone this repo and enter devanagari in the `in` file
- Run `translit.py` and the transliterated output will be in `out`. All non-devanagari characters should be escaped
