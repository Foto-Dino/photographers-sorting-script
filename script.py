import os,sys
import shutil
import time

import qrcode
import cv2
import webbrowser

from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from PyQt5.QtWidgets import QMessageBox



def createqr(data, name):
	# output file name
	filename = f"{name}.JPG"
	# generate qr code
	img = qrcode.make(data)
	# save img to a file
	img.save(filename)

def readqr(fname):
	# preprocessing using opencv
	im = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
	blur = cv2.GaussianBlur(im, (5, 5), 0)
	ret, bw_im = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# scanning the image using pyzbar
	qrscan = decode(bw_im, symbols=[ZBarSymbol.QRCODE])

	if(len(qrscan)>0):
		return qrscan[0].data.decode()
	else:
		return False	

def isManuallySorted(dName):
	if any([os.path.isdir(os.path.join(dName,dir)) for dir in os.listdir(dName)]):
		return True
	return

def organiseFolders(self, dName, savingD):
	# parent_dir = os.path.dirname(dName)
	name_dir = os.path.basename(dName) #The name of the source folder
	newpath = os.path.join(savingD,name_dir+"_organized") #Destination folder + the name of the source folder_organized

	if not os.path.exists(newpath):
		os.makedirs(newpath)

	directories = [os.path.join(dName, directory) for directory in os.listdir(dName) if not directory.endswith("DS_Store")] #Prevents counting DS_Store file as a directory

	for directory in directories:

		event_dir = ''
		event_dir_lis = []
		image_dir_lis = []
		no_of_images = 0
		created = ''
		count= 0

		new_folder_dir = os.path.join(newpath, os.path.basename(directory)) #Destination folder path
		old_folder_dir = os.path.join(dName, os.path.basename(new_folder_dir)) #Source folder path
		#Parsing pictures only
		files = [f for f in [fileName.lower() for fileName in sorted(os.listdir(old_folder_dir))] 
				if all([os.path.isfile(os.path.join(old_folder_dir, f)),
					any([f.endswith("jpg"),f.endswith("png"),f.endswith("jpeg"), f.endswith('JPG')])])] 
		
		"""GUI change"""
		self.countChanged.emit([0,''])
		if not len(files):
			eMsg1 = QMessageBox()
			eMsg1.setIcon(QMessageBox.Critical)
			eMsg1.setWindowTitle('Error')
			eMsg1.setText("No images are present!")
			eMsg1.exec()
			print('no images are present')
			exit()
		""""""
		for file in files:
			scan = readqr(os.path.join(old_folder_dir,file))
			if scan: #If valid qr scan
				created = scan
				if(scan[:-2] != event_dir):
					# creating directory for the event
					event_dir = created[:-2]

				image_dir = os.path.join(newpath,scan)
				os.mkdir(image_dir)
				os.mkdir(os.path.join(image_dir,'Preview Sets'))
				os.mkdir(os.path.join(image_dir,'Raw Pics of Photographer'))
				os.mkdir(os.path.join(image_dir,'Final Sets'))
				qrname = f"{created}{os.path.splitext(file)[1]}"
				shutil.copy(os.path.join(old_folder_dir, file), os.path.join(image_dir, "Raw Pics of Photographer"))
				os.rename(os.path.join(image_dir, "Raw Pics of Photographer", file), os.path.join(image_dir, "Raw Pics of Photographer", qrname))
				# initializing image count to be placed in that client folder 
				no_of_images = 0
			else:
				no_of_images += 1
				if created:
					new_path = shutil.copy(os.path.join(old_folder_dir, file), os.path.join(image_dir, "Raw Pics of Photographer"))####
					os.rename(os.path.join(image_dir, "Raw Pics of Photographer", file), new_path)####
				else:
					eMsg = QMessageBox()
					eMsg.setIcon(QMessageBox.Critical)
					eMsg.setWindowTitle('Error')
					eMsg.setText("No Qr Code Found!")
					eMsg.exec()

		else:
			count += 1
			perc = int(count/len(files)*100)
			self.countChanged.emit([perc,file])
			image_dir_lis.append(image_dir)
			event_dir_lis.append(event_dir)
			image_dir_lis = list(set(image_dir_lis))
			event_dir_lis = list(set(event_dir_lis))
			for items in image_dir_lis:
				os.mkdir(os.path.join(items,'Preview Sets','Basic watermarked'))
				os.mkdir(os.path.join(items,'Preview Sets','Basic watermarked','8 Best edited & watermarked'))

				os.mkdir(os.path.join(items,'Preview Sets','Standard watermarked'))
				os.mkdir(os.path.join(items,'Preview Sets','Standard watermarked','16 Best edited & watermarked'))
				os.mkdir(os.path.join(items,'Preview Sets','Standard watermarked','All raw watermarked'))


				os.mkdir(os.path.join(items,'Preview Sets','Premium watermarked'))
				os.mkdir(os.path.join(items,'Preview Sets','Premium watermarked','16 Best edited & watermarked'))
				os.mkdir(os.path.join(items,'Preview Sets','Premium watermarked','All raw watermarked'))
				os.mkdir(os.path.join(items,'Preview Sets','Premium watermarked','Video watermarked'))

				os.mkdir(os.path.join(items,'Final Sets','Basic'))
				os.mkdir(os.path.join(items,'Final Sets','Basic','8 Best edited'))


				os.mkdir(os.path.join(items,'Final Sets','Standard'))
				os.mkdir(os.path.join(items,'Final Sets','Standard','16 Best edited'))
				os.mkdir(os.path.join(items,'Final Sets','Standard','All raw pics'))


				os.mkdir(os.path.join(items,'Final Sets','Premium'))
				os.mkdir(os.path.join(items,'Final Sets','Premium','16 Best edited'))
				os.mkdir(os.path.join(items,'Final Sets','Premium','All raw'))
				os.mkdir(os.path.join(items,'Final Sets','Premium','Video'))
	else:
		#Rename the main folder to the event number
		os.rename(newpath, os.path.join(os.path.dirname(newpath), created[:-2]))
		sys.exit()

def organiseFiles(self, dName, savingD):
	parent_dir = os.path.dirname(dName)
	name_dir = os.path.basename(dName)
	newpath = parent_dir+'\\'+ name_dir+"_organized"
	if not os.path.exists(newpath):
		os.makedirs(newpath)

	os.chdir(dName)
	dir_files = os.listdir(dName)

	for f in dir_files:
		shutil.copy(f,newpath)

	os.chdir(newpath)

	files = [f for f in sorted(os.listdir(dName)) if os.path.isfile(f) and (f.endswith("jpg") or f.endswith("png") or f.endswith("jpeg") or f.endswith('JPG'))]
	self.countChanged.emit([0,''])
	if(len (files)==0):
		eMsg1 = QMessageBox()
		eMsg1.setIcon(QMessageBox.Critical)
		eMsg1.setWindowTitle('Error')
		eMsg1.setText("No images are present!")
		eMsg1.exec()
		print('no images are present')
		exit()
	else:
		pass	

	event_dir = ''
	event_dir_lis = []
	image_dir_lis = []
	no_of_images = 0
	empty_str = ''
	created = ''
	count= 0
	for f in files:
		# scanning the files 
		scan = readqr(f)
		if (scan!=False):
			created = scan

			if(created[:-2] != event_dir):
				event_dir = created[:-2]
				# creating directory for the event
				os.mkdir(event_dir)


			try:
				# creating new directory with the client id 
				os.mkdir(scan)
				# moving the client dir to event dir 


				image_dir = shutil.move(scan, event_dir)
				os.mkdir(os.path.join(image_dir+'/','Preview Sets'))
				os.mkdir(os.path.join(image_dir+'/','Raw Pics of Photographer'))
				os.mkdir(os.path.join(image_dir+'/','Final Sets'))


				# renaming the qr code file after folder creating
				qrname = f"{created}{'{:03}'.format(0)}.JPG"
				os.rename(f, qrname)
				# moving qrcode file to client dir
				shutil.move(qrname, image_dir+"/Raw Pics of Photographer")
				# initializing image count to be placed in that client folder 
				no_of_images = 0

			except Exception as e:
				print(e)
				exit()
			
		else:
			no_of_images += 1
			if(created != empty_str):
				file_rename = f"{created}{'{:03}'.format(no_of_images)}.JPG"
				os.rename(f, file_rename)
				new_path = shutil.move(file_rename, image_dir+"/Raw Pics of Photographer")
			else:
				eMsg = QMessageBox()
				eMsg.setIcon(QMessageBox.Critical)
				eMsg.setWindowTitle('Error')
				eMsg.setText("No Qr Code Found!")
				eMsg.exec()

		count += 1
		perc = int(count/len(files)*100)
		self.countChanged.emit([perc,f])
		image_dir_lis.append(image_dir)
		event_dir_lis.append(event_dir)

	image_dir_lis = list(set(image_dir_lis))
	event_dir_lis = list(set(event_dir_lis))
	for items in image_dir_lis:

		os.mkdir(os.path.join(items+'/Preview Sets','Basic watermarked'))
		os.mkdir(os.path.join(items+'/Preview Sets/Basic watermarked','8 Best edited & watermarked'))

		os.mkdir(os.path.join(items+'/Preview Sets','Standard watermarked'))
		os.mkdir(os.path.join(items+'/Preview Sets/Standard watermarked','16 Best edited & watermarked'))
		os.mkdir(os.path.join(items+'/Preview Sets/Standard watermarked','All raw watermarked'))


		os.mkdir(os.path.join(items+'/Preview Sets','Premium watermarked'))
		os.mkdir(os.path.join(items+'/Preview Sets/Premium watermarked','16 Best edited & watermarked'))
		os.mkdir(os.path.join(items+'/Preview Sets/Premium watermarked','All raw watermarked'))
		os.mkdir(os.path.join(items+'/Preview Sets/Premium watermarked','Video watermarked'))

		os.mkdir(os.path.join(items+'/Final Sets','Basic'))
		os.mkdir(os.path.join(items+'/Final Sets/Basic','8 Best edited'))


		os.mkdir(os.path.join(items+'/Final Sets','Standard'))
		os.mkdir(os.path.join(items+'/Final Sets/Standard','16 Best edited'))
		os.mkdir(os.path.join(items+'/Final Sets/Standard','All raw pics'))


		os.mkdir(os.path.join(items+'/Final Sets','Premium'))
		os.mkdir(os.path.join(items+'/Final Sets/Premium','16 Best edited'))
		os.mkdir(os.path.join(items+'/Final Sets/Premium','All raw'))
		os.mkdir(os.path.join(items+'/Final Sets/Premium','Video'))
		return event_dir_lis, event_dir,newpath

def mainFunc(self,dName, savingD):
	try:
		#Removing the final slash to not ruin the dirname and basename functions
		if dName[-1] == "/" or dName[-1] == "\\": 
			dName = dName[:-1]

		#Refixing the path slashes depending on the OS since It's forward slash by default
		dName = dName.replace("/", os.path.join("_","_").split("_")[1])

		#Checks if the Source Folder(The folder which needs to be organized) contains folders(Manually organized) or files
		#dName: source folder   savingD: destination folder
		if isManuallySorted(dName):
			organiseFolders(self, dName, savingD)
		else:
			organiseFiles(self, dName, savingD)

	except Exception as e:
		print(e)
		eMsg = QMessageBox()
		eMsg.setIcon(QMessageBox.Critical)
		eMsg.setWindowTitle('Error')
		eMsg.setText('Error' + str(sys.exc_info()[0]) + 'Occured')
		eMsg.exec()
		return False

