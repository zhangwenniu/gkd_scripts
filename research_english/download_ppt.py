'''
作者zhangwenniu@163.com
需要安装好python3+（本人用的是python3.7.0）在命令行中安装如下依赖包，即可使用。
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests fitz
特别注意，需要保证pdf
pip install PyMuPDF==1.16.14
另外特别注意，一定要先下载安装fitz，再安装PyMuPDF，否则会出现no module named frontend。
'''

import requests
import re

import glob
import fitz
import os


# 根据一个单元、某个章节的一个png的url，下载对应章节的所有url文件，并将其拼合为一个pdf文件。
def download_one_url(url, unit, section):
	print(f'start to download unit{unit} section{section} pdf')
	start = 1
	# 暂时看了一下，没有超过100页的ppt。
	stop = 99
	# 由于后面需要sorted文件名，所以需要让数字前面补零。
	if isinstance(unit, int):
		unit = str(unit).zfill(2)
	elif isinstance(unit, str):
		unit = str(int(unit)).zfill(2)
	if isinstance(section, int):
		section = str(section).zfill(2)
	elif isinstance(section, str):
		section = str(int(section)).zfill(2)

	# 存储png文件的文件夹路径，改为自己的即可。
	pic_folder = rf'C:\File\english\unit{unit}\{section}'
	# 存储pdf文件的文件夹路径，改为自己的即可。
	pdf_path = rf'C:\File\english\unit{unit}'
	# 如果这两个文件夹还没有建好，就自动建立这两个文件夹。
	if not os.path.exists(pdf_path):
		os.makedirs(pdf_path)
	if not os.path.exists(pic_folder):
		os.makedirs(pic_folder)

	# 对于所有的png文件，都下载到png_folder中。
	for i in range (start, stop+1):
		num = str(i).zfill(2)
		# 文件名
		file = os.path.join(pic_folder, f'{num}.png')
		print(file)
		# 修改url中的图片索引。
		url = re.sub('\d{1,2}.png', f'{i}.png', url)
		# 下载的时候，时而服务器会卡顿。
		# 等待五秒钟之后重新下载。如果连续五次都无法下载，只能重新检查哪里出了问题。
		for retryTime in range(5):
			try:
				respond = requests.get(url)
				break
			except:
				import time
				time.sleep(5)
		# 如果只有15张png图片，前几张respond都为200，下载到16.png的时候，respond就会变为404。
		# 根据respond是否ok，判断是否已经结束了所有的下载。
		if not respond.ok:
			break
		# 将png图片保存到本地。
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
	pdf_name = rf'unit{unit}_{section}.pdf'
	pic2pdf(pic_folder, pdf_path, pdf_name)	




unit1_urllist = [ 
			'https://s3.ananas.chaoxing.com/doc/63/f3/9f/efff63ba11ed4beebce2db811602c463/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/59/df/03/e765128996fb3cdd74fa2bb78770da8a/thumb/1.png', 
			'https://s3.ananas.chaoxing.com/doc/bd/32/e6/b8f9b35bf308481f7776af308fb278d3/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/15/21/42/7bf89ba52421e7ec3662fa1f0cb4cca8/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/49/40/f9/4a43527af926ac04c494fe4758bdce03/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/ff/5b/8c/b6d0a229c18a805ead08d0ac969393e8/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/2b/b6/a1/aa86b3d5f5d36ba4bd18c97c1e4a875e/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/c9/23/07/ef7dc55d750df00947bb69c26dc16256/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/9c/5a/3b/359030b0e0c4e771da30870aa2d4325c/thumb/1.png', 
			'https://s3.ananas.chaoxing.com/doc/91/32/f2/6149ef280e533fb965c7141a11cb0da2/thumb/1.png',]

# for i in range(len(unit1_urllist)):
# 	url = unit1_urllist[i]
# 	section = i + 1
# 	unit = 1
# 	download_one_url(url, unit, section)

unit2_urllist = [
			'https://s3.ananas.chaoxing.com/doc/fa/8c/0d/be3af69b7ace3ad549276bc7a6696e80/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/41/b0/2b/c51e38167a8bdba1b86766cd4f7dfe40/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/8d/55/a5/93a71f8f6ce804c12905a57dc9cb28df/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/fd/50/24/f6a8c2a19b48a71b354e98a99d346a88/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/22/55/f5/16ba2e69fc63d52306ee81407e0a12d5/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/5c/82/3c/ca30191ca77509bf33f7ef6320b75830/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/8a/88/ad/650236215d404f309707987d81268697/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/80/bb/83/9af3dd21f3ac0cc8ade38fd608f6c1f6/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/72/16/28/8f9463f1a62b620f9c6584f52bf44b10/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/ae/f3/08/821f4aa4d9c3ec03e1b3d3e4e52a21a9/thumb/1.png',			
]

# for i in range(len(unit2_urllist)):
# 	url = unit2_urllist[i]
# 	section = i + 1
# 	unit = 2
# 	download_one_url(url, unit, section)


unit3_urllist = [
			'https://s3.ananas.chaoxing.com/doc/4b/7f/ba/24f5eba9e8d1c57e97dff6be37a14f81/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/2d/f1/19/69c58772d9c04f8b812e4dc1513b1f70/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/12/e1/91/57b0431bfbc2355b8deaf004a1b65511/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/81/c2/74/9eb6417a160382f395c900969e216745/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/31/4c/f2/259604b9e5f1f213db915b5713e6c44c/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/05/64/55/09355e23600975bfe1e8c013cfa3c1ca/thumb/1.png',	
			'https://s3.ananas.chaoxing.com/doc/34/c3/83/39111d0bf0d68cec0178474327a96d5b/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/a5/77/29/b5d9a0dee020a8db66e25191e622a2a1/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/33/e8/26/a684f71661e7053970329a9d3fceffd1/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/5b/16/cf/a7d76dc7b20e20a41eb0d8d1137f1335/thumb/1.png',			
]


# for i in range(len(unit3_urllist)):
# 	url = unit3_urllist[i]
# 	section = i + 1
# 	unit = 3
# 	download_one_url(url, unit, section)

unit4_urllist = [
			'https://s3.ananas.chaoxing.com/doc/c1/e5/b7/5f20e67d81ebbec3289b6687c8867058/thumb/1.png', 
			'https://s3.ananas.chaoxing.com/doc/52/44/25/1df16ef742e51c03499762d6a5666484/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/d3/06/3a/f2d6e9ea73a74fa831780e120d7c9dea/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/f8/11/a2/8e81d56e02ec56c684a547ae574458f5/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/bb/c7/0b/819136fd519611af2240cdff81fafe21/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/39/76/98/ebcd593e4f6df3a7e04702d31810ee6e/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/f0/b1/9d/3efded4d1d4bcf9a226a069ab51a72b8/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/a0/ef/4d/57fbc813e8df9697c18283433b5842fe/thumb/1.png',
]


# for i in range(len(unit4_urllist)):
# 	url = unit4_urllist[i]
# 	section = i + 1
# 	unit = 4
# 	download_one_url(url, unit, section)

unit5_urllist = [
			'https://s3.ananas.chaoxing.com/doc/05/94/a9/f0357bf9f1fec28b31739cb9800c0508/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/00/b0/d3/8d4d741e809fdeb246720e8dc980ee4c/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/c3/9a/fc/713352f56b0332ebd925a2bcc5efc973/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/97/a6/47/5554661999a60019645436811fce2862/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/cf/9d/73/8aa683778c6e9519aeaff5df5d5d8c13/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/a3/01/03/633e5c44b60df57aaf8976fb1f935cd3/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/92/45/08/5f41968b5fed3e85d2971f4dbcb2da25/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/f3/34/81/1df5b4f9c06133278dae86c83cbe7eef/thumb/1.png',
			'https://s3.ananas.chaoxing.com/doc/2f/bb/d2/4cb34c67b5d6c0bd9026e6fbd2b29b7c/thumb/1.png',
]


urls_list = [unit1_urllist, unit2_urllist, unit3_urllist, unit4_urllist, unit5_urllist]
# urls_list = [[], [], [], [], unit5_urllist]

for unit_idx in range(0, len(urls_list)):
	for section_idx in range(len(urls_list[unit_idx])):
		url = urls_list[unit_idx][section_idx]
		section = section_idx + 1
		unit = unit_idx + 1
		download_one_url(url, unit, section)

