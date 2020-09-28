"""
Script to generate certificates from a Tex file and send them via email
Dependencies rquired:
1. yagmail(python package)
2. pdflatex
Created by Debadutta Patra for CCMB open week 2020
"""

import os
import yagmail
from tqdm import tqdm

msg = '''Dear {nam},

Your Message!
    
CCMB Virtual Open Week Organizing Team'''


name = ["Enter list of name"]
mails = ["Enter list of emails"]
inst = ["Enter list for institutes"]


file = open("certificate.tex", 'r')
tex = file.readlines()
file.close()


yag = yagmail.SMTP(user="Your email id", password="Your password")
for i in tqdm(range(len(name))):
    new_tex = []
    for line in tex:
        if line.startswith("We are pleased"):
            new_tex.append(line + name[i] + '}')
        elif line.startswith(" from"):
            new_tex.append(line + inst[i] + "}")
        else:
            new_tex.append(line)

    file1 = open(f"{name[i]}.tex", 'w')
    for line in new_tex:
        file1.write(line)
    file1.close()
    name_parts = name[i].split()
    tex_name = "\ ".join(name_parts)
    os.system(f"pdflatex {tex_name}.tex")
    yag.send(
        to=mails[i],
        subject="Certificates for Open Week",
        contents=msg.format(nam=name[i]),
        attachments=f"{name[i]}.pdf"
    )

yag.close()
