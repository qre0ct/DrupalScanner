# THIS IS THE THIRD VERSION OF THE SCRIPT WHERE IN IT INCLUDES THE FUNCITONALITY OF THE FIRST TWO VERSIONS. ADDITIONALLY IT ALSO PRODUCES TWO DICTIONARIES, ONE FOR
# EACH OF THE VULNERABLE AND THE PATCHED FILE, PRODUCED BY THE RECURSIVE FUNCTION, AND THEN USES THESE TWO DICTIONARIES FOR THE COPARISON (USING THE dictComp(), THAT
# IMPLICITLY CALLS THE createDic()). THE RESULT IS WRITTEN OUT ON THE FILE NAMED dicDiff.TXT. EVEN HERE THE COMPARISON LOGIC IS NOTHING BUT SIMPLE SEQUENTIAL DICTIONARY
# LOOK-UP AND COMPARISON. THE ONLY DIFFERNCE BETWEEN THIS VERSION AND THE SECOND VERSION IS THAT THIS VERSION MAKES USE OF A DICTIONARY TO DO THE COMPARISON, WHILE THE
# SECONOD VERSION DOES A SIMPLE COMPARISON WITHOUT MAKING USE OF ANY EXPLICIT DATA STRUCTURE AS A DICTIONARY.

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
from IronWASP import *;

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
            # readingo the contents.
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
    # indicating that actually the file line being read from the bigger file is a new file alltogether, in which case the smaller
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
    oldDic = createDic(forOldDic)
    newDic = createDic(forNewDic)
    oldDicLength = len(oldDic)
    newDicLength = len(newDic)
    print oldDicLength
    print newDicLength
    oldKeys = oldDic.keys()
    newKeys = newDic.keys()
    dicDifference = "c:\\null\dicDiff.txt"
    dicHandle = open(dicDifference, "a+");
    dicIterator = 0
    # checking if each of the keys in the old dictionary is present in the new dictionary?
    while(dicIterator < oldDicLength):
        # appending single quotes to pass in order to retrieve the value
        temp = '\''
        temp += oldKeys[dicIterator]
        temp += '\''
        if(newDic.has_key(oldKeys[dicIterator])):
            # i.e yes the key was found in the new dictionary as well so now checking for the equality of the
            # corresponding hash.
            print("abhinav" + newDic[temp])
            print("mathew" + oldDic[temp])
            if(newDic[temp] != oldDic[temp]):
                # i.e the hashes are not equal so write it out on the diff file
                dicHandle.write("In Patched Version\n" + oldKeys[dicIterator] + "\t" + newDic[temp] + "\n In Vulnerable Version\n" + oldKeys[dicIterator] + "\t" + oldDic[temp])
        else:
            # it is a new file in old dictionary. write it out on the diff file
            dicHandle.write("In Vulnerable Version\n" + oldKeys[dicIterator] + "\t" + oldDic[temp])
        dicIterator += 1
    dicIterator = 0
    # checking if each of the keys in the new dictionary is present in the old dictionary?
    while(dicIterator < newDicLength):
        # appending single quotes to pass in order to retrieve the value
        temp = '\''
        temp += newKeys[dicIterator]
        temp += '\''
        if(oldDic.has_key(newKeys[dicIterator])):
            # i.e yes the key was found in the new dictionary as well so now checking for the equality of the
            # corresponding hash.
            if(oldDic[temp] != newDic[temp]):
                # i.e the hashes are not equal so write it out on the diff file
                dicHandle.write("In Patched Version\n" + newKeys[dicIterator] + "\t" + oldDic[temp] + "\n In Vulnerable Version\n" + newKeys[dicIterator] + "\t" + newDic[temp])
        else:
            # it is a new file in old dictionary. write it out on the diff file
            dicHandle.write("In Patched Version\n" + newKeys[dicIterator] + "\t" + newDic[temp])
        dicIterator += 1
    dicHandle.close()
       
       
       
       
def createDic(makeDicFromThis):
    returnThisDic = {}
    fileHandle = open(makeDicFromThis, "r")
    # iterating file contents and populating the dictionary
    while(True):
        nextLine = fileHandle.readline()
        if(len(nextLine) == 0):
            break
        key = nextLine.split('\t')[0]
        value = nextLine.split('\t')[1]
        returnThisDic.update({key:value})
    fileHandle.close()
    return returnThisDic
   
   
if __name__ == "__main__":
    passDirPath("C:\\wamp\\www\\drupal-7old\\sites\\all\\modules\\views\\", "C:\\wamp\\www\\drupal-7new\\sites\\all\\modules\\views\\") 
