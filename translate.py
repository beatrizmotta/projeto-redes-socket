from googletrans import Translator, LANGUAGES

translator = Translator()

for language in LANGUAGES:
    dest = translator.translate("eu, você nossos", dest=language).text
    print(dest)
# dest = translator.translate("And that's the way i loved you", dest="pt")
# print(LANGUAGES)