# /// script
# requires-python = ">=3.10,<3.12"
# dependencies = ["pywin32", "libratom", "numpy==1.23.5"]
# ///

import FindEmailArchives
from libratom.lib.pff import PffArchive

'''
короче там было задание сделать рекурсию, но
archive.folders() уже дает тебе все подпапки
поэтому ничего делать не надо вообщем-то
'''

def print_pst_file(archive):
    for folder in archive.folders(): # итератор на pst архив типо
        if folder.get_number_of_sub_messages() != 0: # количеств сообщений в папке
            for message in folder.sub_messages:
                print("Sender: %s" % message.get_sender_name())
                print("Subject: %s" % message.get_subject())
                print("Message: %s" %message.get_plain_text_body())

files = FindEmailArchives.findFiles()
for f in files:
    try:
        archive = PffArchive(f)
        print_pst_file(archive)
    except Exception as e:
        print("Cannot open file, probably its fake")
        continue