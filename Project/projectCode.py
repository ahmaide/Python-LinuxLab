import matplotlib.pyplot as plt
# ============ Class: Courses =============================================================
class Course:
    # This class will have the course with its grade and credits
    def __init__(self, name, credit):
        self.__name = name
        self.__credit = credit
        self.__grade = 0    # grade 0 means that the student didn't take this course yet

    def getName(self):
        return self.__name

    def getGrade(self):
        return self.__grade

    def getCredit(self):
        return self.__credit

    def setGrade(self, grade):
        self.__grade = grade


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Initializing all Courses & semester list ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
try:
    couFile = open("courses.txt", "r")      # The system will check if the file exists
    courseList = couFile.readlines()        # Then it saves all the available courses in
    for i in range(0, len(courseList)):     # a list called "courseList" with all grades = 0
        courseInfo = courseList[i].split(" ")
        courseObj = Course(courseInfo[0], int(courseInfo[1]))
        courseList[i] = courseObj
    couFile.close()
    coursesExist = True
except FileNotFoundError:       # If the file doesn't exist the system will ask the user to make the file
    print("The courses file doesn't exist Please give in the file!")
    courseList = []
    coursesExist = False
semesterList = []


#------------- Function: New Courses List --------------------------------------------------------
def MakeCoursesList():
    newlist=[]                  # This function will make a copied courses list with different objects
    for course in courseList:   # Of each course for each student, with initial grade = 0
        CopiedCourse = Course(course.getName(), course.getCredit())
        newlist.append(CopiedCourse)
    return newlist

#------------------ Function: Add to Semester List ------------------------------------------------
def addToSemesterList(semester):
    notThere = True             # This function is to save all the semesters of all students
    for sem in semesterList:    # and it also checks that the semester already exists
        if semester == sem:
            notThere = False
    if notThere:
        semesterList.append(semester)


#^^^^^^^^^^^^^ Initializing Previous Students List Part 1 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
try:
    stuFile = open("students.txt", "r+")    # This function makes a list of all the students from the file
    studentList = stuFile.readlines()       # and makes sure that the students file exists
    stuFile.close()                         # It also gives the option to add a file if it doesn't exist
    PrevStudExist = True
except FileNotFoundError:
    print("No students file, so a new one will be created")
    with open("students.txt", 'a+') as fi:
        fi.write("")
        fi.close()
    PrevStudExist = False
    studentList = []


#============= Class: Student ================================================================
class Student:
    # the student attributes are the id, file name, semesters list, all courses list, and course per semester list
    def __init__(self, id, FileExist):
        # File exists is a boolean to determin the condition of weather the student is new or already has a file
        self.__id = id                      # The id of the student is an integer 
        self.__file = (str(id) + ".txt")    # The name of the student file ( ID + .txt )
        self.semesters = []                 # A list of all the semesters the student taken
        self.subjPerSem = []                # A list of the lists of courses of each semester
        self.allCourses = MakeCoursesList() # A list of all the courses that the student must take
        if FileExist:   # The case of a previous student who already has a file
            try:        # the exception in case it was said that the student has a file but actually don't
                f = open(self.__file, "r+") # Storing students data after they are redden from his file
                fileLines = f.readlines()   # Split the file in a list for each line
                if len(fileLines) > 1:      # Start from the second line because the first is to describe the columns
                    for i in range(1, len(fileLines)):
                        j = i - 1   # the line number is a head of the index by 1
                        lineSplit = fileLines[i].split(" ; ")   # To split the semester from the courses
                        self.semesters.append(lineSplit[0])     # Add the semester to the semesters of the student
                        addToSemesterList(lineSplit[0])
                        self.subjPerSem.append([])              # add a new list of courses to the subject per semester
                        if (len(fileLines[i]) > 13):            # To check that there are courses at this semester
                            subjSplit = lineSplit[1].split(", ")    # Courses split
                            for subjStr in subjSplit:
                                subjInfo = subjStr.split(" ")       # Split course ID from it's grade
                                for course in self.allCourses:
                                    if course.getName() == subjInfo[0]: # Add the grade if its greater than previous
                                        gra = int(subjInfo[1])
                                        if gra > course.getGrade():
                                            course.setGrade(int(subjInfo[1]))
                                            self.subjPerSem[j].append(course)
                f.close()
            except FileNotFoundError:   # In case there is no file, the system gives the user option to add file
                print("The student with the ID: ", self.__id, ", doesn't have a file!")
                choose = input("Enter 1 to add a new file: ")
                if len(choose)>0:
                    if choose[0]=='1':
                        with open(self.__file, 'a+') as fi:
                            fi.write("Year/Semester ; Courses with Grades")
                            fi.close()
                    else:
                        print("student won't be added!")
                else:
                    print("student won't be added!")
        else:   # The case of the student is new and doesn't have a file so it can be added
            with open(self.__file, 'a+') as fi:
                fi.write("Year/Semester ; Courses with Grades")
                fi.close()

    def getId(self):
        return self.__id

    def getFile(self):
        return self.__file

    def checkNewSemester(self, year, sem):  # Checking if this student has the semester in term of (119,120...)
        semester = (str(year+1900) + "-" + str(year+1901) + "/" + str(sem))
        s = True
        for se in self.semesters:
            if semester == se:
                s = False
        return s, semester

    def semesterIndex(self, semester):  # Checks that the semester exists and gets its index
        s = False
        index = len(self.semesters)
        for se in self.semesters:
            if semester == se:
                s = True
                index = self.semesters.index(se)
        return s, index

    def addGrade(self, course, semester, grade):    # Add a new grade for the student
        ind = len(self.semesters)                   # and checks if the course exists to be added
        courseP = 0
        courseFound = False
        semesterFound = False
        for s in self.semesters:
            if semester == s:
                ind = self.semesters.index(s)
                semesterFound = True
        for c in self.allCourses:
            if course[0:8] == c.getName():
                courseP = c
                courseFound = True
        if semesterFound and courseFound:
            if grade > courseP.getGrade():
                courseP.setGrade(grade)
            self.subjPerSem[ind].append(courseP)
        return (courseFound), courseP

    def changeGrade(self, index, newGrade):     # Changes the grade by its index
        cour = self.allCourses[index]
        cour.setGrade(newGrade)

    def searchForSemesterOfCourse(self, cou):   # Get the semester that the student took that course in
        index = 0
        index2 = 0
        for sem in self.subjPerSem:
            for subj in sem:
                if cou.getName == subj.getName:
                    index = self.subjPerSem.index(sem)
                    index2 = sem.index(subj)
        return index, index2

    def getAvg(self):   # Calculates the total average of the student
        sum=0
        cred=0
        for cou in self.allCourses:
            if cou.getGrade()>=55:
                sum+=(cou.getGrade() * cou.getCredit())
                cred+=cou.getCredit()
        if(cred!=0):
            average = float(sum)/float(cred)
            return average
        else:
            return 0

    def getCredPass(self):  #Gets the total passed credits of the student
        cred = 0
        for cou in self.allCourses:
            if cou.getGrade()>=60:
                cred+=cou.getCredit()
        return cred

    def getCredTaken(self): #Gets the total registered credits for the student
        cred = 0
        for cou in self.allCourses:
            if cou.getGrade()>=55:
                cred+=cou.getCredit()
        return cred

    def avgPerSem(self):    # Prints the student's average in some certain semester
        print("\nSemester / Average ")
        for numSem in self.semesters:
            index = self.semesters.index(numSem)
            s = numSem + " / "
            graSum = 0
            credSum = 0
            for matNum in self.subjPerSem[index]:
                graSum+=(matNum.getGrade()*matNum.getCredit())
                credSum+= matNum.getCredit()
            i = 0
            if (credSum != 0):
                i = float(graSum)/float(credSum)
            s = s + str(i)
            print(s)

    def avgAndCredForSem(self, semName):    # Gets both average and credits for a semester
        check, index = self.semesterIndex(semName)
        avg =0
        cr = 0
        if check:
            sum=0
            for cou in self.subjPerSem[index]:
                sum+= (cou.getGrade() * cou.getCredit())
                cr+= cou.getCredit()
            if cr != 0:
                avg = float(sum) / float(cr)
        return check, avg, cr

    def remainingCourses(self):     # Prints the remaining courses for the student
        print("Remaining courses: ")
        counter = 0
        for c in self.allCourses:
            if c.getGrade()<60:
                #print(c.getName(),",", end=" ")
                if(counter %4 == 3):
                    print(c.getName(),", ")
                else:
                    print(c.getName(), ",", end=" ")
                counter += 1
        remInt = 69 - self.getCredPass()
        print("\n\nRemaining Credits: ", str(remInt))


#^^^^^^^^^^^^^^^^^^^^^^^ Initializing Previous Students List Part 2 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if PrevStudExist:
    counter = 0     # Giving the students ID's in the file objects with all their info in their file
    for student in studentList:
        fName = (studentList[counter] + ".txt")
        intId = int(studentList[counter])
        stud = Student(intId, True)
        studentList[counter] = stud
        counter = counter + 1


#---------------- Function: ID Check -----------------------------------------------------------
def CheckId(id):
    s = False       # This function is to make the user enter a student id and check if it is exists
    choose = 0      # And it keeps giving the user chances in option if they entered wrong data
    while (not s) and (choose==0):
        if  id.isdecimal() and len(id) == 7:
            s = True
        else:
            choise = input("The id isn't current,\nenter 1 if you want to change it: ")
            if choise[0] == '1':
                choose = 0
                id = input("Enter ID: ")
            else:
                choose =1
    return s, id


#--------------- Function: New ID and Check If it is unique ---------------------------------------------
def EnterIDAndCheckIFItAlreadyExists():
    lock = True           # This function checks if the id is unique
    check = False         # And it keeps giving the user chances in option if they entered an existing data
    IDstr = ""
    while lock:
        IDstr = input("Enter the ID of the New Student: ")
        check, IDstr = CheckId(IDstr)
        if check:
            # check = checkAlreadyExists(IDstr, studentList)
            check = True
            for i in studentList:
                if i.getId() == int(IDstr):
                    check = False
            if check:
                lock = False
            else:
                print("That ID already exist!")
                choice2 = input("Enter 1 if you want to try again: ")
                if choice2[0] != '1':
                    print("No new record will be added!")
                    lock = False
        else:
            print("No new record will be added!")
            lock = False
    return IDstr, check


#------------------------------------ Function: Check Semester --------------------------------------------------
def checkSemesterInfo(student):         # This function is to add a new semester for a student
    lock = True                         # And checks if this student already has this semester
    check = False
    semester="-"
    while lock:
        year = input("Enter the year in form of(118, 119, 120...): ")
        sem = input("Enter semester (1: for fall, 2: for spring, 3: for summer): ")
        if ( (sem[0]).isdigit() and len(year)>=3 ):
            seme = int(sem[0])
            if seme >= 1 and seme <=3 and (year[0:3]).isdecimal():
                check, semester = student.checkNewSemester(int(year[0:3]), int(sem[0]))
                lock = False
                if not check:
                    print("This student already has this semester!")
            else:
                print("The data you entered is wrong!")
                ch = input("Enter 1 if you want to try again: ")
                if ch[0]!='1':
                    print("No new semester will be added!")
                    lock = False
        else:
            print("The data you entered is wrong!")
            ch = input("Enter 1 if you want to try again: ")
            if ch[0] != '1':
                print("No new semester will be added!")
                lock = False
    return semester, check


#------------------------------ Function: Find Student and check ID ------------------------------------------
def findIndexAndCheck():
    lock = True             # This function checks if the student exists
    check = False           # and gives his index in the student list
    IDstr = ""
    index = len(studentList)
    while lock:
        IDstr = input("Enter the ID of the Student: ")
        check, IDstr = CheckId(IDstr)
        if check:
            ID = int(IDstr)
            check = False
            for stu in studentList:
                if stu.getId() == ID:
                    check = True
                    index = studentList.index(stu)
            if check:
                lock = False
            else:
                print("That student doesn't exist!")
                choice2 = input("Enter 1 if you want to try again: ")
                if choice2[0] != '1':
                    print("This operation won't work!")
                    lock = False
        else:
            print("This operation won't work!")
            lock = False
    return index,check


#-------------------- Function: Check if course Exists ---------------------------------------------
def checkAndFindCourse():
    index= len(courseList)          # This function checks if the course exists
    lock = True                     # and returns its index in the courses list
    check = False
    while lock:
        name = input("Enter Course ID: ")
        name = name.upper()
        for course in courseList:
            if course.getName() == name:
                index = courseList.index(course)
                check = True
        if check:
            lock = False
        else:
            print("This course ID isn't available!")
            cho = input("Enter 1 if you want to try again: ")
            if cho[0] !='1':
                print("No grade will be changed")
                lock = False
    return index, check


#------------- Function: Replace Grade in File -------------------------------------------------
def replaceinFile(student, indexSem, indexCou, newGrade):
    file1 = open(student.getFile(), "r")                    # This function searches for a grade
    lines = file1.readlines()                               # for a student and in his file
    file1.close()                                           # then changes it
    column= (13*(indexCou+1)) + 10
    lineList = list(lines[indexSem + 1])
    lineList[column] = newGrade[0]
    lineList[column+1] = newGrade[1]
    lines[indexSem + 1] = "".join(lineList)
    file2 = open(student.getFile(), "w")
    for line in lines:
        file2.write(line)


#----------------------- Function: Sort Semester List ---------------------------------------------
def semesterSort():
    for i in range(0, len(semesterList)):               # This function sorts
        for j in range(i+1, len(semesterList)):         # the semester list by oldest to newest
            i0 = int(semesterList[i][0:4])
            j0 = int(semesterList[j][0:4])
            iS = int(semesterList[i][10])
            jS = int(semesterList[j][10])
            if ( i0 > j0 )  or ( i0==j0 and iS>jS):
                s = semesterList[i]
                semesterList[i] = semesterList[j]
                semesterList[j] = s


#================================== The Main =======================================================
if coursesExist:
    print("\n     Welcome to Student Record System\n"
          "******************************************\n")
    user = input("Are you an Admin or a Student: ")     # The letters can be either capital
    user = user.lower()                                 # or small
    if user == "admin":
        again = True
        while again:
            print("\n     THE MENU  \n"                 # the first index is considered
                  "******************\n"                # as the menu's choice
                  "1- Add a New Record\n"
                  "2- Add a New Semester for Student\n"
                  "3- Update Grade\n"
                  "4- Get Student Statistics\n"
                  "5- Get Global Statistics\n"
                  "6- Search Based on Credits or Grades\n"
                  "others - Exit\n"
                  "------------------------------------")
            choice = "" # This loop is to make sure that the user enters at least something
            while len(choice) == 0:
                choice = input("Enter your choice here: ")
            # --------------------------------------------------------------------------------------
            if choice[0] == '1':        # To add a new student
                IDstr, check = EnterIDAndCheckIFItAlreadyExists()   # Enter id and check if it is
                if check:                                           # unique
                    ID = int(IDstr)
                    newStud = Student(ID, False)                    # false as new and has no file
                    stuFile = open("students.txt", "a")
                    stuFile.write("\n" + IDstr)                     # add student to students file
                    stuFile.close()
                    studentList.append(newStud)                     # add student to students list
            # --------------------------------------------------------------------------------------
            elif choice[0] == '2':
                index, check = findIndexAndCheck()  # get student index and check if he exists
                if check:
                    student = studentList[index]
                    semester, check = checkSemesterInfo(student)    # check if this student
                    if check:                                       # already has this semester
                        student.semesters.append(semester) # add this new semester to student semesters
                        student.subjPerSem.append([])     # add a new list of courses for this semester
                        info = semester + " ;"            # info is the string to be added to file
                        courseName = ""
                        courseName = input("Enter a new course name or type exit to leave: ")
                        courseName = courseName.upper()
                        counter = 0     # Now a loop will go on as the user enters courses
                        while courseName != "EXIT":     # The loop will end when the user types exit
                            lock = True
                            C = 0
                            while lock:
                                gradeStr = input("Enter the Grade: ")# the grade should be a decimal
                                if gradeStr[0:2].isdecimal() and len(gradeStr) >= 2:
                                    grade = int(gradeStr[0:2])
                                    if grade < 55:
                                        grade = 55
                                    check, C = student.addGrade(courseName, semester, grade)
                                    lock = False
                                else:   # case of the user didn't enter a number
                                    print("That's not a valid grade!")
                            if check:
                                if counter != 0:
                                    info = info + ","   # add the course grade to the string for the file
                                info = info + " " + C.getName() + " " + str(C.getGrade())
                                counter += 1
                            else:   # if the user entered something unvalid
                                print("The course isn't available!")
                            courseName = input("Enter a new course name or type exit to leave: ")
                            courseName = courseName.upper() # course name should be in uppercase
                        f = open(student.getFile(), "a")    # write all the info in the file
                        f.write("\n" + info)
                        f.close()
            # --------------------------------------------------------------------------------------
            elif choice[0] == '3':
                index, check = findIndexAndCheck()  # check if the student exists
                if check:
                    student = studentList[index]
                    index2, check = checkAndFindCourse()
                    if check:
                        course = student.allCourses[index2]  # gets and checks the course for the student
                        if course.getGrade() != 0:  # check that the student took this course
                            newGradeStr = input("Enter new Grade: ")
                            if newGradeStr[0:2].isdecimal():    # check that the user entered a number
                                newGrade = int(newGradeStr)
                                if newGrade < 55:   # grades should be 55 or more
                                    newGrade = 55
                                # Check for the semester to be edited in it's line in the file
                                semIndex, courInSemIndex = student.searchForSemesterOfCourse(course)
                                replaceinFile(student, semIndex, courInSemIndex, newGradeStr[0:2])
                            else:   # case grade wasn't right
                                print("That's not a valid grade!")
                        else:       # case the course grade =0, which means the student didn.t take it
                            print("This student didn't take this course!")
            # --------------------------------------------------------------------------------------
            elif choice[0] == '4':
                index, check = findIndexAndCheck()  #checks for the student
                if check:
                    student = studentList[index]
                    print("Taken credits: ", student.getCredTaken())    # prints taken credit
                    print("Passed credits: ", student.getCredPass(), "\n\n")# prints passed credit
                    student.remainingCourses()  #Prints student's all remaining courses
                    student.avgPerSem()     # Prints student's average per all semesters
                    print("\nOverall Average: ", student.getAvg())  # Prints student's overall average
                else:
                    print("Not valid")
            # --------------------------------------------------------------------------------------
            elif choice[0] == '5':
                print("\nOverall students average :", end=" ")# Prints the overall average
                cred = 0                                      # For all students
                gra = 0
                for student in studentList:     # loop on all available students
                    gra += (student.getAvg() * float(student.getCredTaken()))
                    cred += student.getCredTaken()
                if (cred == 0):
                    print("0")
                else:
                    avg = float(gra) / float(cred)
                    print(avg)
                if len(semesterList) > 0:
                    semesterSort()
                    print("\nSemester, overall average, average credit")
                    for sem in semesterList:    # a loop to print the overall average
                        stri = sem + ": "       # for all students in each semester
                        avgs = 0
                        cre = 0
                        studPerSem = 0
                        for s in studentList: # A loop for all students how have this semester
                            check, a, c = s.avgAndCredForSem(sem)
                            if check:
                                avgs += (a * c)
                                cre += c
                                studPerSem += 1
                        overAllAvg = 0
                        avgCred = 0
                        if cre != 0:    # printing the overall average credits per semester
                            overAllAvg = float(avgs) / float(cre)
                            avgCred = float(cre) / float(studPerSem)
                        stri += str(overAllAvg) + ", " + str(avgCred)
                        print(stri)
                else:
                    print("\nNothing Is available!")
                print("\nThe histogram of the averages should be displayed!")
                avGList = []        # Ploting the averages histogram
                for st in studentList:
                    avGList.append(st.getAvg())
                plt.hist(avGList, bins=[50, 60, 70, 80, 90, 100], rwidth=0.95)
                plt.show()
            # --------------------------------------------------------------------------------------
            elif choice[0] == '6':  # this choice to print all students who satisfy given criteria
                choice2 = ""
                while len(choice2) == 0:
                    choice2 = input("enter 1 to search by credits, 2 to search by average: ")
                if choice2[0] == '1':
                    cred = input("Enter Number of Credits to search for: ")
                    if cred[0:2].isdecimal():
                        credit = int(cred[0:2])
                        choice3 = ""
                        while len(choice3) == 0:
                            choice3 = input("Enter 1 to searched by more, 2 to search by less than: ")
                        if (choice3[0] == '1' or choice3[0] == '2') and credit >= 0 and credit <= 69:
                            print("Student ID, Number of Passed Credits")
                            for student in studentList:
                                if choice3[0] == '1' and student.getCredPass() >= credit:
                                    print(student.getId(), "   , ", student.getCredPass())
                                if choice3[0] == '2' and student.getCredPass() < credit:
                                    print(student.getId(), "   , ", student.getCredPass())
                        else:
                            print("That operation isn't avilable!")
                    else:
                        print("that's not a valid number of credits!")
                elif choice2[0] == '2':
                    av = input("Enter the average to search for: ")
                    avs = av.replace(".", "")
                    if avs.isdecimal() and av.count('.') < 2:
                        average = float(av)
                        choice3 = ""
                        while len(choice3) == 0:
                            choice3 = input("Enter 1 to searched by more, 2 to search by less than: ")
                        if (choice3[0] == '1' or choice3[0] == '2') and average >= 55 and average <= 99:
                            print("Student ID, Average")
                            for student in studentList:
                                if choice3[0] == '1' and student.getAvg() >= average:
                                    print(student.getId(), "   , ", student.getAvg())
                                if choice3[0] == '2' and student.getAvg() < average:
                                    print(student.getId(), "   , ", student.getAvg())
                        else:
                            if choice3[0] != '1' and choice3[0] != '2':
                                print("That operation isn't avilable!")
                            else:
                                print("that's not a valid average (range issue)!")
                    else:
                        print("that's not a valid average!")
                else:
                    print("you entered an invalid data!")
            # --------------------------------------------------------------------------------------
            else:
                again = False
                print("Program is Exiting..........")
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    elif user == "student":
        student = 0     # Here it must be proven that you are a student
        index, again = findIndexAndCheck()  # checking if the student exisists
        if again:
            student = studentList[index]
        while again:
            print("\n     THE MENU  \n"
                  "******************\n"
                  "1- Get Student Statistics\n"
                  "2- Get Global Statistics\n"
                  "others - Exit\n"
                  "------------------------------------")
            choice = ""
            while len(choice) == 0:     # a loop until the user enters something
                choice = input("Enter your choice here: ")
            # --------------------------------------------------------------------------------------
            if choice[0] == '1':
                print("Taken credits: ", student.getCredTaken())  # prints taken credit
                print("Passed credits: ", student.getCredPass(), "\n\n")  # prints passed credit
                student.remainingCourses()  # Prints student's all remaining courses
                student.avgPerSem()  # Prints student's average per all semesters
                print("\nOverall Average: ", student.getAvg())  # Prints student's overall average
            # --------------------------------------------------------------------------------------
            elif choice[0] == '2':
                print("\nOverall students average :", end=" ")  # Prints the overall average
                cred = 0  # For all students
                gra = 0
                for student in studentList:  # loop on all available students
                    gra += (student.getAvg() * float(student.getCredTaken()))
                    cred += student.getCredTaken()
                if (cred == 0):
                    print("0")
                else:
                    avg = float(gra) / float(cred)
                    print(avg)
                if len(semesterList) > 0:
                    semesterSort()
                    print("\nSemester, overall average, average credit")
                    for sem in semesterList:  # a loop to print the overall average
                        stri = sem + ": "  # for all students in each semester
                        avgs = 0
                        cre = 0
                        studPerSem = 0
                        for s in studentList:  # A loop for all students how have this semester
                            check, a, c = s.avgAndCredForSem(sem)
                            if check:
                                avgs += (a * c)
                                cre += c
                                studPerSem += 1
                        overAllAvg = 0
                        avgCred = 0
                        if cre != 0:  # printing the overall average credits per semester
                            overAllAvg = float(avgs) / float(cre)
                            avgCred = float(cre) / float(studPerSem)
                        stri += str(overAllAvg) + ", " + str(avgCred)
                        print(stri)
                else:
                    print("\nNothing Is available!")
                print("\nThe histogram of the averages should be displayed!")
                avGList = []  # Ploting the averages histogram
                for st in studentList:
                    avGList.append(st.getAvg())
                plt.hist(avGList, bins=[50, 60, 70, 80, 90, 100], rwidth=0.95)
                plt.show()
            # --------------------------------------------------------------------------------------
            else:
                again = False
                print("\nProgram is Exiting..........")
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    else:
        print("\nThat's not a valid option, exiting.........")