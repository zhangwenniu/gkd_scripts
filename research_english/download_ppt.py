import requests
import re

import glob
import fitz
import os


start = 1
stop = 25
unit = '01'
section = '03'
unit1_urllist = [ 'https://s3.ananas.chaoxing.com/doc/63/f3/9f/efff63ba11ed4beebce2db811602c463/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/59/df/03/e765128996fb3cdd74fa2bb78770da8a/thumb/1.png', 
			'https://s3.ananas.chaoxing.com/doc/bd/32/e6/b8f9b35bf308481f7776af308fb278d3/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/15/21/42/7bf89ba52421e7ec3662fa1f0cb4cca8/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/49/40/f9/4a43527af926ac04c494fe4758bdce03/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/ff/5b/8c/b6d0a229c18a805ead08d0ac969393e8/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/2b/b6/a1/aa86b3d5f5d36ba4bd18c97c1e4a875e/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/c9/23/07/ef7dc55d750df00947bb69c26dc16256/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/9c/5a/3b/359030b0e0c4e771da30870aa2d4325c/thumb/1.png', 
			'https://s3.ananas.chaoxing.com/doc/91/32/f2/6149ef280e533fb965c7141a11cb0da2/thumb/1.png',]


url = 'https://s3.ananas.chaoxing.com/doc/bd/32/e6/b8f9b35bf308481f7776af308fb278d3/thumb/1.png'

pic_folder = rf'C:\Users\TSG\Desktop\english\unit{unit}\{section}'
pdf_path = rf'C:\Users\TSG\Desktop\english\unit{unit}'
if not os.path.exists(pdf_path):
	os.makedirs(pdf_path)
if not os.path.exists(pic_folder):
	os.makedirs(pic_folder)


for i in range (start, stop+1):
	num = str(i).zfill(2)
	file = rf'C:\Users\TSG\Desktop\english\unit{unit}\{section}\{num}.png'
	print(file)
	url = re.sub('\d{1,2}.png', f'{i}.png', url)
	respond = requests.get(url)
	with open(file, 'wb') as f:
		f.write(respond.content)
		
def pic2pdf(pic_folder, pdf_path, pdf_name):
	# 创建一个新的pdf空文档
	doc = fitz.open()
	for img in sorted(glob.glob(os.path.join(pic_folder, '*.png'))):
		print(img)
		# 读取png图像
		imgdoc = fitz.open(img)
		# 将png文件转为pdf流
		pdfbytes = imgdoc.convertToPDF()
		# 用fitz转换为pdf
		imgpdf = fitz.open('pdf', pdfbytes)
		# 将最新png转为的pdf插入文档中
		doc.insertPDF(imgpdf)

	if not pdf_name.endswith('.pdf'):
		pdf_name += '.pdf'

	save_pdf_path = os.path.join(pdf_path, pdf_name)

	if os.path.exists(save_pdf_path):
		os.remove(save_pdf_path)

	doc.save(save_pdf_path)
	doc.close()

print('Converting png to pdf')
pdf_name = rf'{section}.pdf'
pic2pdf(pic_folder, pdf_path, pdf_name)
