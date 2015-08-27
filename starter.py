# THIS IS THE SECOND VERSION OF THE CODE. APART FORM PRINTING OUT THE FILES IN A RECURSIVE FASHION, IT ALSO DOES A COMPARISON ON THE TWO VERSIONS OF THE FILES 
# PRODUCED,(USING THE passDirPath()) AND WRITES OUT THE DIFFERENCES ON THE DIFF.TXT FILE. THE COMPARISON LOGIC IS NOTHING BUT A SEQUENTIAL LOOK-UP AND COMPARISON.



'''
Created on May 23, 2013

@author: admin
'''
#overall logic of the code :-
#this function takes as an argument the directory to be looked in and hash the
#contents of all the files in the directory and take this and store it in a temp
#file. This task is done on both the versions (vul and fixed). The temp file
#produced as the output undergo a diff and the results are stored in a separate file.
#This files contents are then sent to another function as an argument.
#Specification of this function is described later.

from System.IO import *;
from IronWASP import *;

#fileLookUp is a recursive function. It recursively checks all the folders for any files present in it.
#each of the files are taken and their hash is calucated.
#now each of these hashes along with their corresponding files are stored in a temp file
def fileLookUp(fixedPath, version):
    if version:
        targetFile="c:\\null\\patchedFile.txt";
    else:
        targetFile="c:\\null\\vulFile.txt";
    #open file for storing files with their corresponding hashes
    vulFileHandle=open(targetFile,"a+");
    #fixedPath is the user supplied path to the directory.
    #however, it is supplied by the user only during the first call of the
    #function. For all subsequent function calls, fixedPath gets automatically
    #calculated through the recursive calls of fileLookUp.
    #temp is used to retain the path just before the control goes another level
    #deeper in the call. This is required to later list out the files in this
    #(i.e. the current) level of the directory. If this is not there then the
    #recursive call will finally reach the level where in there is no further
    #directory in the structure and will print only the files present (if any)
    # at this final level ONLY. Hence in order to also get the files in the
    #directories that we left behind while diving in the recursive calls, the
    #temp variable and it's associated logic is needed.
    temp=fixedPath;
    #checking if the current directory in question has any inner directory.
    if not Directory.GetDirectories(fixedPath):
        #concluded that this is the innermost final directory.
        files=Directory.GetFiles(fixedPath);
        for eachFile in files:
            #file retrieved in the innermost directory.
            print eachFile; #this prints the path of the file along with the file name
            #opening each of the above files to read its contents
            fileHandle=open(eachFile, "r");
            #readingo the contents.
            contents=fileHandle.read();
            #hashing the file contents.
            hashing = Tools.MD5(contents);
            print hashing;
            #closing the file.
            fileHandle.close();
            #writing out into the file, the file name (with the entire path) and the hashing of the contents
            vulFileHandle.write((eachFile[23:])+'\t'+hashing+'\n');
    else:
        #further inner directory(ies) found.
        directory=Directory.GetDirectories(fixedPath);
        for folder in directory:
            if vulFileHandle.closed:
                vulFileHandle=open(targetFile,"a+");
            #reading each directory one by one to frame the next look-up path.
            fixedPath="";
            fixedPath+=folder;
            fixedPath+="\\";
            #next look-up path framed.
            #sending the new look-up path for a recursive search again.
            #the file needs to be closed before every recursive function call
            #because every time the function gets called the file is opened.
            #So opening a file that's already open does not make sense and
            #also gives erroneous file output. Hence it needs to be closed
            #before every recursive function call.
            vulFileHandle.close();
            fileLookUp(fixedPath, version);
        #after the files in the innner most directories at a particular level is
        #processed, the recursive calls start reverting back and the control now
        #reached here. Now doing the processing of the 'temp' .
        filess=Directory.GetFiles(temp);
        for eachFilee in filess:
            if vulFileHandle.closed:
                vulFileHandle=open(targetFile,"a+");
            print eachFilee;
            #opening each of the above files to read its contents
            fileHandlee=open(eachFilee, "r");
            #readingo the contents.
            contentss=fileHandlee.read();
            #hashing the file contents.
            hashhing = Tools.MD5(contentss);
            print hashhing;
            #closing the file.
            fileHandlee.close();
            #writing out into the file, the file name (with the entire path) and the hash of the contents
            vulFileHandle.write((eachFilee[23:])+'\t'+hashhing+'\n');
    if not vulFileHandle.closed:
        vulFileHandle.close();


def passDirPath(oldVer,newVer):
    #calling the fileLookup() to process the vulnerable version of the directory
    fileLookUp(oldVer,0)

    #calling the fileLookup() to process the pathched version of the directory
    fileLookUp(newVer,1)

    #opening both the files to read
    vulFile="c:\\null\\vulFile.txt"
    vulFileHand=open(vulFile,"r")
    patFile="c:\\null\\patchedFile.txt"
    patFileHand=open(patFile,"r")

    #caluclating the diff between the two files generated and storing it in a
    #file for being processed later calculating the size of the file
    diffFile="c:\\null\diff.txt"
    diffFileHandle=open(diffFile,"a+");
   
    # move the cursor to the end of the file
    vulFileHand.seek(0,2)
    vulFileSize = vulFileHand.tell()
    vulFileHand.seek(0,0)
    # move the cursor to the end of the file
    patFileHand.seek(0,2)
    patFileSize = patFileHand.tell()
    patFileHand.seek(0,0)
    print vulFileSize
    print patFileSize
    if (vulFileSize > patFileSize):
        biggerFile=vulFileHand
        smallerFile=patFileHand
        diffFileString1="In Vulnerable Version\n"
        diffFileString2="In Pathched Version\n"
    else:
        biggerFile=patFileHand
        smallerFile=vulFileHand
        diffFileString1="In Pathched Version\n"
        diffFileString2="In Vulnerable Version\n"
    #iterating through the bigger file and comparing each line read with a corresponding line read in the smaller file.
    #if they are unequal, check if the path is equal, which would mean that the hash is actually causing the inequality.
    #if the path is unequal, that means that this particular file, being read from the bigger file, is a newly introduced
    #file altogether.
    numberOfLinesBF=0
    numberOfLinesSF=0
   
    #counting the number of lines in the bigger file so that it can be used in the next iteration when we read through
    #the bigger file. counting the number of lines in the smaller file is not really required. Its done just for the
    #sake of debugging.
    while(len(biggerFile.readline())):
        numberOfLinesBF+=1
    while(len(smallerFile.readline())):
        numberOfLinesSF+=1
    print numberOfLinesBF
    print numberOfLinesSF

    #starting the loop to read through the contents of the bigger file.
    biggerFile.seek(0,0)
    smallerFile.seek(0,0)
    flag=0
    #purpose of flag-->to pause reading the smaller file further in case the 2 strings read don't match and their paths also do not match
    #indicating that actually the file line being read from the bigger file is a new file alltogether, in which case the smaller
    #files iteration should be paused
    iteratorVar=0 #to iterate through the loop
    while(iteratorVar <= numberOfLinesBF):
        lineReadBF=biggerFile.readline()
        print ("reading the line BF " +lineReadBF)
        if(flag == 0):
            lineReadSF=smallerFile.readline()
            print ("reading the line SF " +lineReadSF)
        if(lineReadBF == lineReadSF):
            print "lines were equal"
            flag=0
            iteratorVar+=1
            continue
        else:
            print "splitting things"
            if((lineReadBF.split('\t')[0]) == (lineReadSF.split('\t')[0])): #indicating that diff was due to the hash
                print "paths were equal, only hashes differ"
                flag=0
                #write out the strings in the diffrences file
                diffFileHandle.write(diffFileString1 + lineReadBF + "\n" + diffFileString2 + lineReadSF + "\n")
            else: #indicating that actually the file line being read from the bigger file is a new file alltogether
                print "paths were different, new file introduced"
                flag=1
                diffFileHandle.write(diffFileString1 + lineReadBF + "\n")
                iteratorVar+=1
                continue
        iteratorVar+=1
   
    #there could be a situation where while reading the smaller file we pause at a certain line. Now we keep reading
    #lines from the bigger file to find a match to the line in the smaller file where we are paused. But it may so
    #happen that we don't find any match at all and also all the lines in the bigger file get read. This indicates that,
    #the line we paused at in the smaller file is actually not present at all in the bigger file. (If we are suspectiong
    #that in such a situation what if the line being read from the bigger file does not match the line paused at in the
    #smaller file, but does match a line somewhere after the paused line. So this won't be detected 'coz the further
    #reading of the smaller file has been paused. BUT, such a situation would never arise, becuase of the way the bigger
    #and the smaller file contents have been written, ie. in a recursive directory file listing manner.) So in such
    #situation we need to read and write out the rest of the smaller file on the diffFile indicating that these files
    #were not present in the newer version.
    iteratorVar=0
    if(flag == 1):
        while(True):
            lineReadSF=smallerFile.readline()
            if(len(lineReadSF) == 0):
                break
            diffFileHandle.write("Extra files present  " + diffFileString2 + "\n")
           
    vulFileHand.close()
    patFileHand.close()
    diffFileHandle.close()
   
if __name__ == "__main__":
    passDirPath("C:\\wamp\\www\\drupal7old\\sites\\all\\modules\\views\\", "C:\\wamp\\www\\drupal7new\\sites\\all\\modules\\views\\")