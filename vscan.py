# THIS IS THE SIXTH VERSION OF THE SCRIPT AND IS A COMPLETED, RUNNING VERSION. IT NEEDS TO BE ONLY TESTED NOW FOR CONFIGRMING ITS FUNCTIONALITY.
# THIS SCRIPT CAN STRAIGHT AWAY DETECT THE VERSION OF THE SPECIFIED MODULE (IN THIS CASE THE VIEW MODULE) ON A SPECIFIED TARGET DRUPAL SITE (IN THIS CASE 
# LOCALHOST HOSTING THE OLD AND THE NEW VERSION OF THE VIEW MODULE).
# NOW ONLY USER INPUT PART NEEDS TO BE ADDED TO IT AND AN INTERFACE SO THAT ALL THE OTHER MODULES CAN ALSO BE INTEGRATED WITHOUT MAKING ANY MAJOR CHANGES TO THE 
# SCRIPT ITSELF. ALSO A THE DATABASE TABLE CAN HAVE AN ID COLUMN THAT WILL ACT AS A FOREIGN KEY TO THE TABLE, SAY MODULE_DETAILS, THAT WILL HOLD ALL THE NAME ETC.
# DETAILS OF THE MODULE WITH AN ASSOCIATED ID AS IT'S PRIMARY KEY.
# ANOTHER IMPORTANT FACT TO CONSIDER HERE IS THAT THIS IS THE COMPLETE SCRIPT. THE ACTUAL SCANNER MAKES USE OF ONLY 2 FUNCTIONS, VIZ:- liveVersionScan() and 
# requestor(). USING JUST THESE TWO FUNCTIONS A LIVE SCAN CAN BE PERFORMED. THE REST OF THE FUNCTIONS HERE ARE SUPPORTING FUNCTIONS THAT ARE NOT REALLY NEEDED FOR
# DOING A LIVE SCAN. ALTHOUGH IN THIS CASE THE DATABASE IS BEING CREATED BY THE SUPPORTING FUNCTIONS AND HENCE THEY MIGHT BE NEEDED AS OF HERE, BUT THIS FUNCTIONALITY
# CAN EASILY BE ISOLATED SO THAT IT NO LONGER DEPENDS ON THE SUPPORTING FUNCTIONS.
# SUMMARY OF THE CRAP... AN XML NEEDS TO BE CREATED FROM THE VALUES IN THE DATABASE AND THIS XML MUST BE THE ONLY ENTITY USED BY liveVersionScan() TO DETERMINE THE 
# VERSION.


'''
Created on May 23, 2013

@author: admin
'''
# overall logic of the code :-
# this function takes as an argument the directory to be looked in and hash the
# contents of all the files in the directory and take this and store it in a temp
# file. This task is done on both the versions (vul and fixed). The temp file
# produced as the output undergo a diff and the results are stored in a separate file.
# This files contents are then sent to another function as an argument.
# Specification of this function is described later.

from System.IO import *;
import clr
clr.AddReference("System")
clr.AddReference("System.Data")
clr.AddReference("System.Data.SQLite")

import System
from System.Data.SQLite import *

# fileLookUp is a recursive function. It recursively checks all the folders for any files present in it.
# each of the files are taken and their hash is calucated.
# now each of these hashes along with their corresponding files are stored in a temp file
def fileLookUp(fixedPath, version):
  if version:
    targetFile = "c:\\null\\patchedFile.txt";
  else:
    targetFile = "c:\\null\\vulFile.txt";
  # open file for storing files with their corresponding hashes
  vulFileHandle = open(targetFile, "a+");
  # fixedPath is the user supplied path to the directory.
  # however, it is supplied by the user only during the first call of the
  # function. For all subsequent function calls, fixedPath gets automatically
  # calculated through the recursive calls of fileLookUp.
  # temp is used to retain the path just before the control goes another level
  # deeper in the call. This is required to later list out the files in this
  # (i.e. the current) level of the directory. If this is not there then the
  # recursive call will finally reach the level where in there is no further
  # directory in the structure and will print only the files present (if any)
  # at this final level ONLY. Hence in order to also get the files in the
  # directories that we left behind while diving in the recursive calls, the
  # temp variable and it's associated logic is needed.
  temp = fixedPath;
  # checking if the current directory in question has any inner directory.
  if not Directory.GetDirectories(fixedPath):
    # concluded that this is the innermost final directory.
    files = Directory.GetFiles(fixedPath);
    for eachFile in files:
      # file retrieved in the innermost directory.
      print eachFile;  # this prints the path of the file along with the file name
      # opening each of the above files to read its contents
      fileHandle = open(eachFile, "r");
      # reading the contents.
      contents = fileHandle.read();
      # hashing the file contents.
      hashing = Tools.MD5(contents);
      print hashing;
      # closing the file.
      fileHandle.close();
      # writing out into the file, the file name (with the entire path) and the hashing of the contents
      vulFileHandle.write((eachFile[24:]) + '\t' + hashing + '\n');
  else:
    # further inner directory(ies) found.
    directory = Directory.GetDirectories(fixedPath);
    for folder in directory:
      if vulFileHandle.closed:
        vulFileHandle = open(targetFile, "a+");
      # reading each directory one by one to frame the next look-up path.
      fixedPath = "";
      fixedPath += folder;
      fixedPath += "\\";
      # next look-up path framed.
      # sending the new look-up path for a recursive search again.
      # the file needs to be closed before every recursive function call 
      # because every time the function gets called the file is opened.
      # So opening a file that's already open does not make sense and 
      # also gives erroneous file output. Hence it needs to be closed 
      # before every recursive function call.
      vulFileHandle.close();
      fileLookUp(fixedPath, version);
    # after the files in the innner most directories at a particular level is
    # processed, the recursive calls start reverting back and the control now
    # reached here. Now doing the processing of the 'temp' .
    filess = Directory.GetFiles(temp);
    for eachFilee in filess:
      if vulFileHandle.closed:
        vulFileHandle = open(targetFile, "a+");
      print eachFilee;
      # opening each of the above files to read its contents
      fileHandlee = open(eachFilee, "r");
      # readingo the contents.
      contentss = fileHandlee.read();
      # hashing the file contents.
      hashh = Tools.MD5(contentss);
      print hashh;
      # closing the file.
      fileHandlee.close();
      # writing out into the file, the file name (with the entire path) and the hash of the contents
      vulFileHandle.write((eachFilee[24:]) + '\t' + hashh + '\n');
  if not vulFileHandle.closed:
    vulFileHandle.close();


def passDirPath(oldVer, newVer):
  # calling the fileLookup() to process the vulnerable version of the directory
  fileLookUp(oldVer, 0)

  # calling the fileLookup() to process the pathched version of the directory
  fileLookUp(newVer, 1)

  # opening both the files to read
  vulFile = "c:\\null\\vulFile.txt"
  vulFileHand = open(vulFile, "r")
  patFile = "c:\\null\\patchedFile.txt"
  patFileHand = open(patFile, "r")

  # in the following section i have used my logic to compare the two files (vulFIle.txt and pathchedFile.txt).
  # the comparison logic depends on the assumption that the contents of the above 2 files are written out in 
  # a recursive fashion (which is what i have done in the function above where the folders are read for getting
  # all the files in them). However if someone changes this logic (recursive writing out of files) to some other
  # logic, then the contents of the vulFile.txt and patchedFile.txt will also vary. In which case my comparison
  # logic would fail (as it depends on the assumption that the contents of these 2 files are written in a recursive
  # fashion. So to avoid this there's another function that has been called, named dictComp. dictComp accepts
  # the 2 files, vulFile.txt and patchedFile.txt, as parameters and creates 2 dictionaries out of the contents of 
  # vulFile.txt and patchedFile.txt. Please refer to the doc. present in the dictComp function for more details.   
  
  # this function call is just an alternative to my comparison logic.
  dictComp("c:\\null\\vulFile.txt", "c:\\null\\patchedFile.txt") 
  
  # calculating the diff between the two files generated and storing it in a 
  # file for being processed later 
  # calculating the size of the file
  diffFile = "c:\\null\diff.txt"
  diffFileHandle = open(diffFile, "a+");
  
  # move the cursor to the end of the file
  vulFileHand.seek(0, 2) 
  vulFileSize = vulFileHand.tell()
  vulFileHand.seek(0, 0)
  # move the cursor to the end of the file
  patFileHand.seek(0, 2) 
  patFileSize = patFileHand.tell()
  patFileHand.seek(0, 0)
  print vulFileSize
  print patFileSize
  if (vulFileSize > patFileSize):
    biggerFile = vulFileHand
    smallerFile = patFileHand
    diffFileString1 = "In Vulnerable Version\n"
    diffFileString2 = "In Pathched Version\n"
  else:
    biggerFile = patFileHand
    smallerFile = vulFileHand
    diffFileString1 = "In Pathched Version\n"
    diffFileString2 = "In Vulnerable Version\n"
  # iterating through the bigger file and comparing each line read with a corresponding line read in the smaller file.
  # if they are unequal, check if the path is equal, which would mean that the hash is actually causing the inequality.
  # if the path is unequal, that means that this particular file, being read from the bigger file, is a newly introduced
  # file altogether.
  numberOfLinesBF = 0
  numberOfLinesSF = 0
  
  # counting the number of lines in the bigger file so that it can be used in the next iteration when we read through
  # the bigger file. counting the number of lines in the smaller file is not really required. Its done just for the 
  # sake of debugging.
  while(len(biggerFile.readline())):
    numberOfLinesBF += 1
  while(len(smallerFile.readline())):
    numberOfLinesSF += 1
  print numberOfLinesBF
  print numberOfLinesSF

  # starting the loop to read through the contents of the bigger file.
  biggerFile.seek(0, 0)
  smallerFile.seek(0, 0)
  flag = 0
  # purpose of flag-->to pause reading the smaller file further in case the 2 strings read don't match and their paths also do not match
  # indicating that actually the file line being read from the bigger file is a new file all together, in which case the smaller 
  # files iteration should be paused
  iteratorVar = 0  # to iterate through the loop
  while(iteratorVar <= numberOfLinesBF):
    lineReadBF = biggerFile.readline()
    print ("reading the line BF " + lineReadBF)
    if(flag == 0):
      lineReadSF = smallerFile.readline()
      print ("reading the line SF " + lineReadSF)
    if(lineReadBF == lineReadSF):
      print "lines were equal"
      flag = 0
      iteratorVar += 1
      continue
    else:
      print "splitting things"
      if((lineReadBF.split('\t')[0]) == (lineReadSF.split('\t')[0])):  # indicating that diff was due to the hash
        print "paths were equal, only hashes differ"
        flag = 0
        # write out the strings in the diffrences file
        diffFileHandle.write(diffFileString1 + lineReadBF + "\n" + diffFileString2 + lineReadSF + "\n")
      else:  # indicating that actually the file line being read from the bigger file is a new file alltogether
        print "paths were different, new file introduced"
        flag = 1
        diffFileHandle.write(diffFileString1 + lineReadBF + "\n")
        iteratorVar += 1
        continue
    iteratorVar += 1
  
  # there could be a situation where while reading the smaller file we pause at a certain line. Now we keep reading
  # lines from the bigger file to find a match to the line in the smaller file where we are paused. But it may so 
  # happen that we don't find any match at all and also all the lines in the bigger file get read. This indicates that,
  # the line we paused at in the smaller file is actually not present at all in the bigger file. (If we are suspectiong 
  # that in such a situation what if the line being read from the bigger file does not match the line paused at in the 
  # smaller file, but does match a line somewhere after the paused line. So this won't be detected 'coz the further 
  # reading of the smaller file has been paused. BUT, such a situation would never arise, becuase of the way the bigger 
  # and the smaller file contents have been written, ie. in a recursive directory file listing manner.) So in such 
  # situation we need to read and write out the rest of the smaller file on the diffFile indicating that these files
  # were not present in the newer version.
  iteratorVar = 0
  if(flag == 1):
    while(True):
      lineReadSF = smallerFile.readline()
      if(len(lineReadSF) == 0):
        break
      diffFileHandle.write("Extra files present  " + diffFileString2 + "\n")
      
  vulFileHand.close()
  patFileHand.close()
  diffFileHandle.close()



def dictComp(forOldDic, forNewDic):
  # this function takes 2 text files as input. These 2 text files contain the list of all the files present in the 2 
  # versions of the folder. IT DOES NOT MATTER WHAT ORDER IS THE CONTENT OF THESE TWO FILES IN, (as was the restriction 
  # in case of my comparison logic, that the contents of these 2 files should actually be a recursive listing). As long 
  # as the contents of these 2 text files is in the format "file_path/file_name \t hash_key", it does not matter in which 
  # order is the contents being listed in the 2 text files.
  oldDic = {}
  newDic = {}
  oldDic.update(createDic(forOldDic, 1))
  newDic.update(createDic(forNewDic, 1))
  oldDicLength = len(oldDic)
  newDicLength = len(newDic)
  print oldDicLength
  print newDicLength
  oldKeys = oldDic.keys()
  print "the old dictionary keys are "
  print oldKeys
  newKeys = newDic.keys()
  print "the new dictionary keys are "
  print newKeys
  dicDifference = "c:\\null\dicDiff.txt"
  dicHandle = open(dicDifference, "a+");
  dicIterator = 0
  
  # checking if each of the keys in the old dictionary is present in the new dictionary?
  while(dicIterator < oldDicLength):
    # appending single quotes to pass in order to retrieve the value
    temp = oldKeys[dicIterator]
    print "the temp string is "+temp
    if(newDic.has_key(temp)):
      # i.e yes the key was found in the new dictionary as well so now checking for the equality of the 
      # corresponding hash.
      print"some random"
      print newDic[temp]
      if(newDic[temp] != oldDic[temp]):
        # i.e the hashes are not equal so write it out on the diff file
        print "going to write in the dicdiff"
        dicHandle.write("In Patched Version\n" + oldKeys[dicIterator] + "\t" + newDic[temp] + "In Vulnerable Version\n" + oldKeys[dicIterator] + "\t" + oldDic[temp]) 
    else:
      # it is a new file in old dictionary. write it out on the diff file
      dicHandle.write("In Vulnerable Version\n" + oldKeys[dicIterator] + "\t" + oldDic[temp]) 
    dicIterator += 1
  dicHandle.close()
  dicIterator = 0
  # getting a list of things from the dicDiff 
  alreadyWritten=createDic("c:\\null\\dicDiff.txt", 0)
  print "things already written out in dicDiff are" 
  print alreadyWritten
  # checking if each of the keys in the new dictionary is present in the old dictionary?
  dicHandle = open(dicDifference, "a+");
  #dicHandle.write("getting into the reverse logic now")
  while(dicIterator < newDicLength):
    # appending single quotes to pass in order to retrieve the value
    temp = newKeys[dicIterator]
    print "this is the tempoooo " +temp
    if (temp in alreadyWritten):
      dicIterator+=1
      continue
    if(oldDic.has_key(temp)):
      # i.e yes the key was found in the old dictionary as well so now checking for the equality of the 
      # corresponding hash.
      if(oldDic[temp] != newDic[temp]):
        # i.e the hashes are not equal so write it out on the diff file
        dicHandle.write("In Patched Version\n" + newKeys[dicIterator] + "\t" + oldDic[temp] + "In Vulnerable Version\n" + newKeys[dicIterator] + "\t" + newDic[temp]) 
    else:
      # it is a new file in new dictionary. write it out on the diff file
      dicHandle.write("In Patched Version\n" + newKeys[dicIterator] + "\t" + newDic[temp]) 
    dicIterator += 1
  dicHandle.close()
    
# this function simply creates a dictionary or list and returns the same.
def createDic(makeDicFromThis, switcher):
  if(switcher == 1):
    returnThisDic={}
  else:
    returnThisDic=list()
  fileHandle = open(makeDicFromThis, "r")
  # iterating file contents and populating the dictionary
  while(True):
    nextLine = fileHandle.readline()
    if(len(nextLine) == 0):
        break
    if(switcher == 1):
      key = nextLine.split('\t')[0]
      print "the key is "+key
      value = nextLine.split('\t')[1]
      print "the value is "+value
      returnThisDic.update({key:value})
    else:
      if('\t' in nextLine):
        returnThisDic.append(nextLine.split('\t')[0])
        returnThisDic.append(nextLine.split('\t')[1])
  print "the dictionary being returned  is "
  print returnThisDic
  fileHandle.close()
  return returnThisDic
  

def publicAccessFiles():
#{
  # after we have a list of all the files that have changed (even a bit) between the two versions of the module, we now
  # need to find of these files which are the ones that are publicly accessible on a live site. To do this we send requests
  # for these files to both the copies, containing the 2 versions of the module, of our demo installations of Drupal.
  # Depending on the response code we decide if a particular file is publicly accessible or not. And we populate the 
  # PUBLIC_ACCESS database table with the respective details. Later we make use of this table to determine what version of 
  # the module is the live site running.
  print "entering public access"
  # instantiating the sqlite DB
  # open database connection
  log = SQLiteConnection("data source=c:\\null\\drupalReq.db")
  log.Open()
  cmd = SQLiteCommand(log)
  # dropping the table if already exists
  print "removing the table if it exists"
  cmd.CommandText="DROP TABLE IF EXISTS PUBLIC_ACCESS"
  cmd.ExecuteNonQuery()
  # create the table 
  cmd.CommandText = "CREATE TABLE IF NOT EXISTS PUBLIC_ACCESS (FILE_DETAILS varchar(500) NOT NULL, VUL_HASH varchar(100), PAT_HASH varchar(100), PRIMARY KEY (FILE_DETAILS))"
  cmd.ExecuteNonQuery()
  dicDifferenceFile="c:\\null\\dicDiff.txt"
  dicDiffHandle=open(dicDifferenceFile,"r")
  while(True):
   #{
    pat=0
    vul=0
    # read the string that determines if it is a patched or a vulnerable version
    lineInFile=dicDiffHandle.readline()
    if(len(lineInFile) == 0):
      break
    if("In Patched Version" in lineInFile):
      pat=1
    if("In Vulnerable Version" in lineInFile):
      vul=1
    # read the file and the hash itself
    lineInFile=dicDiffHandle.readline()
    # split the line read into path\file and hash and put it in 2 separate variables
    pathFile=lineInFile.split('\t')[0]
    fileHash=lineInFile.split('\t')[1]
    # change the slashes to make it appropriate to send the request
    parsablePathFile=pathFile.replace('\\','/')
    print "\n"+parsablePathFile
    # send the requests for the old and the new versions
    oldFileStaticReq="http://localhost/drupal-7old/"
    newFileStaticReq="http://localhost/drupal-7new/"
    # get the response from both the requests and store it in 2 additional variables 
    oldFileRes=requestor(oldFileStaticReq, parsablePathFile)
    newFileRes=requestor(newFileStaticReq, parsablePathFile)
    print "\nresponse received for old file "+ parsablePathFile + " is "+(str)(oldFileRes)
    print "\nresponse received for new file "+ parsablePathFile + " is "+(str)(newFileRes)
    # check if either of the responses actually returns status code as 2xx, indicating that the file is publicly accessible
    # if not continue back with the loop, if yes skip the 'continue' part and go for the database actions. 
    if((((str)(oldFileRes))[0] != '2') and (((str)(newFileRes))[0] != '2')):
      continue
    try:
        print "\ninserting into table "+pathFile
        cmd.CommandText = "INSERT INTO PUBLIC_ACCESS (FILE_DETAILS,VUL_HASH,PAT_HASH) VALUES (@url, @vulSig, @patSig)"
        cmd.Parameters.AddWithValue("@url",pathFile)
        if(pat == 1):
            print "\ninserting patched hash "+fileHash
            cmd.Parameters.AddWithValue("@patSig",fileHash)
            cmd.Parameters.AddWithValue("@vulSig",None)
        else:
            print "\ninserting vulnerable hash "+fileHash
            if(vul == 1):
                cmd.Parameters.AddWithValue("@vulSig",fileHash)
                cmd.Parameters.AddWithValue("@patSig",None)
        cmd.ExecuteNonQuery()
    except:
        print "\nexception: primary key found at "+pathFile+" no duplicate possible"
        cmd.Parameters.AddWithValue("@url",pathFile)
        if(pat == 1):
            print "\nupdating pathched hash"
            cmd.CommandText="UPDATE PUBLIC_ACCESS SET PAT_HASH=@patSig WHERE FILE_DETAILS=@url"
            cmd.Parameters.AddWithValue("@patSig",fileHash)
        else:
            print "\ninserting vulnerable hash"
            if(vul == 1):
                cmd.CommandText="UPDATE PUBLIC_ACCESS SET VUL_HASH=@vulSig WHERE FILE_DETAILS=@url"
                cmd.Parameters.AddWithValue("@vulSig",fileHash)
        cmd.ExecuteNonQuery()
  #}
  log.Close()
  dicDiffHandle.close()
#}


# this function simply frames and sends the required requests and returns the response code
# in case the requestor method is called with a third parameter as "True", it would indicate that the body of the reponse also needs 
# to be saved in the temp location c:\null\temp
def requestor(requestedFile, dynamicContent, getBodyAlso="False"):
  print "\nsending request as "+(requestedFile+dynamicContent)
  dynamicReq=requestedFile+dynamicContent
  print "\n finally the dynamic request generated is "+dynamicReq
  req = Request(dynamicReq)
  res= req.Send()
  if(getBodyAlso == "True"):
	# delete the file if it already exists, this part needs to be taken care of... not done yet.
	res.SaveBody("c:\\null\\temp\\tempBody")
  return res.Code



# this function now makes use of the database of the publicly accessible files, cereated 
# by the publicAccessFiles(), and sends a request for same to the live site that needs to
# be scanned for its version. 
def liveVersionScan():
	# before sending the request for any of the files in the database, we will actually 
	# check to see if there are any new files present in the database. New as in the ones
	# that are new (unique) to either the old version or the new version. For these files
	# we won't even need to check for the hashes of the files, becuae just knowing that it
	# is present on the live site, would confirm the version.
	# so we create a list of the files in the database that have vul_hash field as null.
	# this signifies that this list will contain files that are present only in the patched
	# version. simillarly we create a list for all the files in the database where pat_hash
	# field i equal to null. this signifies that this list will contain files that are present
	# only in the vulnerable version. 
	# now first we send the request for all the files in these two lists. In case a positive
	# response is received for any one of these files, then that's it. Our job is done and 
	# the version is determined.
	# in case a positive response is not received, then we start checking for the rest of the
	# files in the database. In case if a positive response is still not received then the site
	# is not a drupal site at all. 
	print "entering the live version scanner"
	# defining the live site  url
	liveSite="http://localhost/drupal-7new/"
	# temporary file path where recived files will be stored
	tempFilePath="c:\\null\\temp\\tempBody"
	# lists to store files exclusively in vulnerable version
	xclusiveVulFiles=list()
	# lists to store files exclusively in patched version
	xclusivePatFiles=list()
	# temporary list for processing whenever needed
	tempList=list()
	tempPatHashList=list()
	tempVulHashList=list()
	# xFoundFlag is true when at least one record is returned as a result for the query :-
	# SELECT * FROM PUBLIC_ACCESS WHERE VUL_HASH IS NULL OR PAT_HASH IS NULL
	xFoundFlag=False
	# reportedFlag is true when finally the version has been determined any how 
	reportedFlag="Default"
	# instantiating the sqlite DB
	# open database connection
	print "\nall initializations done successfully"
	log = SQLiteConnection("data source=c:\\null\\drupalReq.db")
	log.Open()
	print "\nconnection opened successfully"
	cmd = SQLiteCommand(log)
	print "\nsqlite command intitalized"
	cmd.CommandText="SELECT * FROM PUBLIC_ACCESS WHERE VUL_HASH IS NULL"
	print "\nsetting the command text was successful"
	queryResult=cmd.ExecuteReader()
	if(queryResult):
		while(queryResult.Read()):
			xclusivePatFiles.append(queryResult["FILE_DETAILS"])
		if((len(xclusivePatFiles)) > 0):
			print "\nvul # is null value(s) found"
			xFoundFlag=True
			print "\nexclusive pat values are \n"
			print xclusivePatFiles
	queryResult.Close()
	print "\ndata reader closed successfully"
	cmd.CommandText="SELECT * FROM PUBLIC_ACCESS WHERE PAT_HASH IS NULL"
	print "\nsetting the command text was successful"
	queryResult=cmd.ExecuteReader()
	if(queryResult):
		while(queryResult.Read()):
			xclusiveVulFiles.append(queryResult["FILE_DETAILS"])
		if((len(xclusiveVulFiles)) > 0):
			print "\npat # is null value(s) found"
			xFoundFlag=True
			print "\nexclusive vul values are \n"
			print xclusiveVulFiles
	queryResult.Close()
	print "\ndata reader closed successfully"
	if(xFoundFlag == True):
		print "\nnull value list found"
		if((len(xclusivePatFiles)) >= (len(xclusiveVulFiles))):
			temp=(len(xclusivePatFiles))
		else:
			temp= (len(xclusiveVulFiles))
		xListIterator=0
		# here the staticRequest is the live site that we want to test for.
		# it actually has to be taken as an input from the user.
		while(True):
			if(xListIterator >= temp):
				break
			if(((len(xclusivePatFiles))>0) and (xListIterator < (len(xclusivePatFiles)))):
				testFile=(xclusivePatFiles[xListIterator]).replace('\\','/')
				print "\nsending request for "+(liveSite+testFile)
				fileFound=requestor(liveSite,testFile)
				if(((str)(fileFound))[0] == '2'):
					reportedFlag="True"
					print "\n given site is patched for the view module"
					break
			if(((len(xclusiveVulFiles))>0) and (xListIterator < (len(xclusiveVulFiles)))):
				testFile=(xclusiveVulFiles[xListIterator]).replace('\\','/')
				print "\nsending request for "+(liveSite+testFile)
				fileFound=requestor(liveSite,testFile)
				if(((str)(fileFound))[0] == '2'):
					reportedFlag="True"
					print "\n given site is vulnerable for the view module"
					break
			xListIterator+=1
		if(reportedFlag == "Default"):
			reportedFlag="False"
	xListIterator=0
	if(reportedFlag == "False" or xFoundFlag == False):
		if(reportedFlag == "False"):
			print "\nstatus not reported yet"
		# that means the null value files existed. So the lists were created, but the files in these lists could not be fetched. 
		# so in this case, resend the request for all the files in the set :- {all files in the table} - {(list1)U(list2)}
		# although this case is almost impossible to happen, because if the list is made, then defintely for at least one 
		# of the values in the list will be positively fetched from the live site, but still just in case) The above assertion 
		# is made because, the lists are prepared only when db contains one such field (the null thing). And the db contains such 
		# a field only when such a file was returned from the test drupal site. It is the same argument as the last few lines of 
		# the comments in the beggining of this function
			cmd.CommandText="SELECT * FROM PUBLIC_ACCESS WHERE FILE_DETAILS NOT IN (SELECT FILE_DETAILS FROM PUBLIC_ACCESS WHERE VUL_HASH IS NULL OR PAT_HASH IS NULL)"
		else:
			if(xFoundFlag == False):
				print "\nnull value list not found"
			# meaning the only vulnerable or the only patched files list itself was not 
			# generated. So in this case a all the files in the table need to be requested.  
				cmd.CommandText="SELECT * FROM PUBLIC_ACCESS"
		queryResult=cmd.ExecuteReader()
		if(queryResult):
			while(queryResult.Read()):
				tempList.append(queryResult["FILE_DETAILS"])
				tempPatHashList.append(queryResult["PAT_HASH"])
				tempVulHashList.append(queryResult["VUL_HASH"])
			print "\nthe lists created are\n"
			print tempList
			print "\n"
			print tempPatHashList
			print "\n"
			print tempVulHashList
			while(True):
				if(xListIterator >= (len(tempList))):
					break
				testFile=(tempList[xListIterator]).replace('\\','/')
				print "sending request for "+(liveSite+testFile)
				fileFound=requestor(liveSite,testFile,"True")
				if(((str)(fileFound))[0] == '2'):
					print "\nfound the file, file was also saved in temp"
					# calculating the hash of the file received
					fileHandle = open(tempFilePath, "r");
					# reading the contents.
					contents = fileHandle.read();
					# hashing the file contents.
					hashOfFileRecvd = Tools.MD5(contents);
					print "hash of the file received is "+ hashOfFileRecvd
					hashOfFileRecvd+='\n'
					# closing the file.
					fileHandle.close();
					# comparing the hash of the recieved file with the database to see where it matches
					if(hashOfFileRecvd in tempVulHashList):
						print"\nthe given site runs the vulnerable version of the mentioned module"
					else:
						if(hashOfFileRecvd in tempPatHashList):
							print"\nthe given site runs the patched version of the mentioned module"
					reportedFlag="True"
					break
				xListIterator+=1
		else:
			print"\nthe target site is either not a drupal site or does not have the module itself"
	xListIterator=0
	queryResult.Close()
	log.Close()
   
def runAsMain():
  passDirPath("C:\\wamp\\www\\drupal-7old\\sites\\all\\modules\\views\\", "C:\\wamp\\www\\drupal-7new\\sites\\all\\modules\\views\\")
  publicAccessFiles()
  liveVersionScan()

