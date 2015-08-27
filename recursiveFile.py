# THIS IS THE VERY 1ST VERSION OF THE CODE, WHERE IN IT CONSISTS OF ONLY A RECURSIVE FUNCTION TO TRAVERSE A DIRECTORY TREE AND PRINT OUT 
# ALL THE FILES IN IT.


#overall logic of the code :-
#this function takes as an argument the directory to be looked in and hash the
#contents of all the files in the directory and take this and store it in a temp
#file. This task is done on both the versions (vul and fixed). The temp file
#produced as the output undergo a diff and the results are stored in a separate file.
#This files contents are then sent to another function as an argument.
#Specification of this function is described later.

from System.IO import *;
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
            print eachFile;
            #hashing the file contents.
            hash = Tools.MD5(eachFile);
            print hash;
            vulFileHandle.write(eachFile+'\t'+hash+'\n');
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
            hashh = Tools.MD5(eachFilee);
            print hashh;
            vulFileHandle.write(eachFilee+'\t'+hashh+'\n');
    if not vulFileHandle.closed:
        vulFileHandle.close();