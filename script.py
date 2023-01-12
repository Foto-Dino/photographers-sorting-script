import os,sys
import shutil
import time

import qrcode
import cv2
import webbrowser

from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from PySide6.QtWidgets import QMessageBox



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
		print("here is qr data", qrscan[0].data.decode())
		return qrscan[0].data.decode()

	else:
		return False

def isManuallySorted(dName):
	"""
	this returns true when the photographer created client folders on cam
	returning False is an edge case
	"""
	if any([os.path.isdir(os.path.join(dName,dir)) for dir in os.listdir(dName)]):
		return True
	return False

def organiseFolders(self, dName, savingD):
	# parent_dir = os.path.dirname(dName)
	name_dir = os.path.basename(dName) #The name of the source folder
	newpath = os.path.join(savingD,name_dir+"_organized") #Destination folder + the name of the source folder_organized

	print("new path is: " + newpath)

	if not os.path.exists(newpath):
		os.makedirs(newpath)

	directories = [os.path.join(dName, directory) for directory in os.listdir(dName) if not directory.endswith("DS_Store")] #Prevents counting DS_Store file as a directory

	for directory in directories:

		event_dir = ''
		event_dir_lis = []
		image_dir_lis = []
		no_of_images = 0
		created = False
		count = 0

		new_folder_dir = os.path.join(newpath, os.path.basename(directory)) #Destination folder path
		old_folder_dir = os.path.join(dName, os.path.basename(new_folder_dir)) #Source folder path
		#Parsing pictures only
		files = [f for f in [fileName.lower() for fileName in sorted(os.listdir(old_folder_dir))] 
				if all([os.path.isfile(os.path.join(old_folder_dir, f)),
					any([f.endswith("jpg"),f.endswith("png"),f.endswith("jpeg"), f.endswith('JPG')])])] 
		
		"""GUI change"""
		self.countChanged.emit([0,''])
		if not len(files):
# 			eMsg1 = QMessageBox()
# 			eMsg1.setIcon(QMessageBox.Critical)
# 			eMsg1.setWindowTitle('Error')
# 			eMsg1.setText("No images are present!")
# 			eMsg1.exec()
# 			print('no images are present')
			exit()
		""""""
		for file in files:
			scan = readqr(os.path.join(old_folder_dir,file))
			count += 1
			perc = int(count/len(files)*100)
			print("count: " + str(count) +  "; percentage done: " + str(perc))
			self.countChanged.emit([perc,file])
			if scan: #If valid qr scan
				created = scan
				if(scan[:-2] != event_dir):
					# creating directory for the event
					event_dir = created[:-2]
				print("newpath before image_dir is")
				print(newpath)
				# image_dir is client_number
				image_dir = os.path.join(newpath,scan)

				os.mkdir(image_dir)
				os.mkdir(os.path.join(image_dir,'preview_sets'))
				os.mkdir(os.path.join(image_dir,'raw_pics_of_photographer'))
				os.mkdir(os.path.join(image_dir,'final_sets'))

				qrname = f"{created}{os.path.splitext(file)[1]}"
				shutil.copy(os.path.join(old_folder_dir, file), os.path.join(image_dir, "raw_pics_of_photographer"))
				#os.rename(os.path.join(image_dir, "raw_pics_of_photographer", file), os.path.join(image_dir, "raw_pics_of_photographer", qrname))

				# initializing image count to be placed in that client folder 
				no_of_images = 0

				image_dir_lis.append(image_dir)
				event_dir_lis.append(event_dir)
				image_dir_lis = list(set(image_dir_lis))
				event_dir_lis = list(set(event_dir_lis))
				for items in image_dir_lis:

					os.mkdir(os.path.join(items,'preview_sets','basic_watermarked'))
					os.mkdir(os.path.join(items,'preview_sets','basic_watermarked','8_best_edited_watermarked'))

					os.mkdir(os.path.join(items,'preview_sets','standard_watermarked'))
					os.mkdir(os.path.join(items,'preview_sets','standard_watermarked','16_best_edited_watermarked'))
					os.mkdir(os.path.join(items,'preview_sets','standard_watermarked','all_raw_watermarked'))


					os.mkdir(os.path.join(items,'preview_sets','premium_watermarked'))
					os.mkdir(os.path.join(items,'preview_sets','premium_watermarked','16_best_edited_watermarked'))
					os.mkdir(os.path.join(items,'preview_sets','premium_watermarked','all_raw_watermarked'))
					os.mkdir(os.path.join(items,'preview_sets','premium_watermarked','video_watermarked'))

					os.mkdir(os.path.join(items,'final_sets','basic'))
					os.mkdir(os.path.join(items,'final_sets','basic','8_best_edited'))


					os.mkdir(os.path.join(items,'final_sets','standard'))
					os.mkdir(os.path.join(items,'final_sets','standard','16_best_edited'))
					os.mkdir(os.path.join(items,'final_sets','standard','all_raw'))


					os.mkdir(os.path.join(items,'final_sets','premium'))
					os.mkdir(os.path.join(items,'final_sets','premium','16_best_edited'))
					os.mkdir(os.path.join(items,'final_sets','premium','all_raw'))
					os.mkdir(os.path.join(items,'final_sets','premium','Video'))

		for file in files:
			no_of_images += 1
			print("number of images increased")

			new_path = shutil.copy(os.path.join(old_folder_dir, file), os.path.join(image_dir, "raw_pics_of_photographer"))####
			print("new_path is now: " + str(new_path))
			os.rename(os.path.join(image_dir, "raw_pics_of_photographer", file), new_path)####
				# eMsg = QMessageBox()
				# eMsg.setIcon(QMessageBox.Critical)
				# eMsg.setWindowTitle('Error')
				# eMsg.setText("No Qr Code Found!")
				# eMsg.exec()
			count += 1
			perc = int(count / len(files) * 100)
			print("count: " + str(count) +  "; percentage done: " + str(perc))
			self.countChanged.emit([perc, file])
	else:
		# Rename the main folder to the event number
		print("new folder is")
		print(newpath)
		os.rename(newpath, os.path.join(os.path.dirname(newpath), created[:-2]))
		return os.path.join(os.path.dirname(newpath), created[:-2])
		# sys.exit()

def organiseFiles(self, dName, savingD):
	# parent_dir = os.path.dirname(dName)
	name_dir = os.path.basename(dName)  # The name of the source folder
	newpath = savingD  # Destination folder + the name of the source folder_organized

	print("new path is" + newpath)

	if not os.path.exists(newpath):
		os.makedirs(newpath)

	# directories = [os.path.join(dName, directory) for directory in os.listdir(dName) if
	# 			   not directory.endswith("DS_Store")]  # Prevents counting DS_Store file as a directory

	directory=dName

	event_dir = ''
	event_dir_lis = []
	image_dir_lis = []
	no_of_images = 0
	created = ''
	count = 0

	new_folder_dir = os.path.join(newpath, os.path.basename(directory))  # Destination folder path
	old_folder_dir = dName # Source folder path
	# Parsing pictures only
	files = [f for f in [fileName.lower() for fileName in sorted(os.listdir(old_folder_dir))]
				if all([os.path.isfile(os.path.join(old_folder_dir, f)),
						any([f.endswith("jpg"), f.endswith("png"), f.endswith("jpeg"), f.endswith('JPG')])])]

	"""GUI change"""
	self.countChanged.emit([0, ''])
	if not len(files):
		# 			eMsg1 = QMessageBox()
		# 			eMsg1.setIcon(QMessageBox.Critical)
		# 			eMsg1.setWindowTitle('Error')
		# 			eMsg1.setText("No images are present!")
		# 			eMsg1.exec()
		# 			print('no images are present')
		exit()
	""""""
	for file in files:
		scan = readqr(os.path.join(old_folder_dir, file))
		if scan:  # If valid qr scan
			print("valid qr scan called")
			created = scan
			if (scan[:-2] != event_dir):
				# creating directory for the event
				event_dir = created[:-2]
			print("newpath before image_dir is")
			print(newpath)
			image_dir = os.path.join(newpath, scan)
			os.mkdir(image_dir)
			os.mkdir(os.path.join(image_dir, 'preview_sets'))
			os.mkdir(os.path.join(image_dir, 'raw_pics_of_photographer'))
			os.mkdir(os.path.join(image_dir, 'final_sets'))
			qrname = f"{created}{os.path.splitext(file)[1]}"
			shutil.copy(os.path.join(old_folder_dir, file), os.path.join(image_dir, "raw_pics_of_photographer"))
			# os.rename(os.path.join(image_dir, "raw_pics_of_photographer", file), os.path.join(image_dir, "raw_pics_of_photographer", qrname))
			# initializing image count to be placed in that client folder
			no_of_images = 0
	for file in files:
	
		no_of_images += 1
		new_path = shutil.copy(os.path.join(old_folder_dir, file), os.path.join(image_dir, "raw_pics_of_photographer"))  ####
		os.rename(os.path.join(image_dir, "raw_pics_of_photographer", file), new_path)  ####
			
		# eMsg = QMessageBox()
		# eMsg.setIcon(QMessageBox.Critical)
		# eMsg.setWindowTitle('Error')
		# eMsg.setText("No Qr Code Found!")
		# eMsg.exec()
		count += 1
		perc = int(count / len(files) * 100)
		print("precne")
		print(perc)
		print(count)
		self.countChanged.emit([perc, file])

	else:
		count += 1
		perc = int(count / len(files) * 100)
		print("precne")
		print(perc)
		print(count)
		self.countChanged.emit([perc, file])
		image_dir_lis.append(image_dir)
		event_dir_lis.append(event_dir)
		image_dir_lis = list(set(image_dir_lis))
		event_dir_lis = list(set(event_dir_lis))
		for items in image_dir_lis:
			os.mkdir(os.path.join(items, 'preview_sets', 'basic_watermarked'))
			os.mkdir(os.path.join(items, 'preview_sets', 'basic_watermarked', '8_best_edited_watermarked'))

			os.mkdir(os.path.join(items, 'preview_sets', 'standard_watermarked'))
			os.mkdir(os.path.join(items, 'preview_sets', 'standard_watermarked', '16_best_edited_watermarked'))
			os.mkdir(os.path.join(items, 'preview_sets', 'standard_watermarked', 'all_raw_watermarked'))

			os.mkdir(os.path.join(items, 'preview_sets', 'premium_watermarked'))
			os.mkdir(os.path.join(items, 'preview_sets', 'premium_watermarked', '16_best_edited_watermarked'))
			os.mkdir(os.path.join(items, 'preview_sets', 'premium_watermarked', 'all_raw_watermarked'))
			os.mkdir(os.path.join(items, 'preview_sets', 'premium_watermarked', 'video_watermarked'))

			os.mkdir(os.path.join(items, 'final_sets', 'basic'))
			os.mkdir(os.path.join(items, 'final_sets', 'basic', '8_best_edited'))

			os.mkdir(os.path.join(items, 'final_sets', 'standard'))
			os.mkdir(os.path.join(items, 'final_sets', 'standard', '16_best_edited'))
			os.mkdir(os.path.join(items, 'final_sets', 'standard', 'all_raw'))

			os.mkdir(os.path.join(items, 'final_sets', 'premium'))
			os.mkdir(os.path.join(items, 'final_sets', 'premium', '16_best_edited'))
			os.mkdir(os.path.join(items, 'final_sets', 'premium', 'all_raw'))
			os.mkdir(os.path.join(items, 'final_sets', 'premium', 'Video'))
	
	#else:
		# Rename the main folder to the event number
		#print("new folder iss")
		#print(newpath)
		#print(os.path.join(os.path.dirname(newpath), created[:-2]))
		#os.rename(newpath, os.path.join(os.path.dirname(newpath), created[:-2]))
		#pass


# sys.exit()


def mainFunc(self,dName, savingD):
	try:
		#Removing the final slash to not ruin the dirname and basename functions
		if dName[-1] == "/" or dName[-1] == "\\": 
			dName = dName[:-1]

		#Refixing the path slashes depending on the OS since It's forward slash by default
		dName = dName.replace("/", os.path.join("_","_").split("_")[1])

		#Checks if the Source Folder(The folder which needs to be organized) contains folders(Manually organized) or files
		#dName: source folder   savingD: destination folder

		# TODO needs refactoring, manually sorted should not be an edge case
		if isManuallySorted(dName):
		# if bulk==True:
			final_path = organiseFolders(self, dName, savingD)
		else:
			directory_list = []
			for root, dirs, files in os.walk(dName, topdown=False):
				for name in dirs:
					directory_list.append(os.path.join(root, name))
			if len(directory_list)==0:
				organiseFiles(self, dName, savingD)
			else:
				for direct in directory_list:
					print(direct)
					organiseFiles(self, direct, savingD)
		# return the path of the now sorted images to the calling function
		return final_path

	except Exception as e:
		print(e)
		return False

