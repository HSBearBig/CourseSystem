from flask import Flask, render_template, request, redirect, flash, session, url_for
import MySQLdb
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = ""
dbhost = ""
dbuser = ""
dbpasswd = ""
db = ""
conn = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpasswd, db=db)

def get_student_course(studentID):
    get_student_course_query = f"""
    select Takes.SectionID, Course.CourseName, Course.CourseCredit, Course.CourseType, Teacher.TeacherName
    from Takes
    inner join Student
    on Takes.StudentID = Student.StudentID 
    inner join Section
    on Takes.SectionID = Section.SectionID
    inner join Course
    on Section.CourseID = Course.CourseID
    inner join Teaches
    on Teaches.SectionID = Section.SectionID
    inner join Teacher
    on Teacher.TeacherID = Teaches.TeacherID
    where Student.studentID = '{studentID}'
    order by Takes.SectionID;
    """  # SQL 指令：撈該學生的課程
    cursor = conn.cursor()
    cursor.execute(get_student_course_query)
    results = {}
    total_credit = 0
    for (SectionID, CourseName, CourseCredit, CourseType, TeacherName) in cursor.fetchall():
        if SectionID not in results:
            TeacherNameList = [TeacherName, ]
            results[SectionID] = [CourseName, CourseCredit, CourseType, TeacherNameList] # 把用 SQL 指令撈出來的資料 加入 results (用 dict 型態)
            total_credit += CourseCredit
        else:
            results[SectionID][3].append(TeacherName)
    return results

def get_student_courseTable(studentID):
    get_student_course_query = f"""
    select Course.CourseName, Time.Day, Time.Session
    from Takes
    inner join Student
    on Takes.StudentID = Student.StudentID 
    inner join Section
    on Takes.SectionID = Section.SectionID
    inner join Course
    on Section.CourseID = Course.CourseID
    inner join Teaches
    on Teaches.SectionID = Section.SectionID
    inner join Teacher
    on Teacher.TeacherID = Teaches.TeacherID
    inner join SectionAt
    on Takes.SectionID = SectionAt.SectionID
    inner join Time
    on SectionAt.TimeID = Time.TimeID
    where Student.studentID = '{studentID}'
    order by Takes.SectionID;
    """  # SQL 指令：撈該學生的課程
    cursor = conn.cursor()
    cursor.execute(get_student_course_query)
    courseTable = [['' for x in range(7)] for y in range(14)]
    for (CourseName, Day, Session) in cursor.fetchall():
        courseTable[Session-1][Day-1] = CourseName
    return courseTable

def get_all_course():
    get_all_course_query = """
        select Section.`SectionID`, Course.`CourseName`, Teacher.TeacherName, count(Takes.SectionID) as choosenNum, Section.SectionCapacity
        from Section
        inner join Course
        on Course.CourseID = Section.CourseID
        inner join Teaches
        on Teaches.SectionID = Section.SectionID
        inner join Teacher
        on Teacher.TeacherID = Teaches.TeacherID
        left join Takes
        on Takes.SectionID = Section.SectionID
        group by Section.SectionID, Teacher.TeacherName;
    """
    cursor = conn.cursor()
    cursor.execute(get_all_course_query)
    results = {}
    for (SectionID, CourseName, TeacherName, choosenNum, SectionCapacity) in cursor.fetchall():
        if SectionID not in results:
            TeacherNameList = [TeacherName, ]
            results[SectionID] = [CourseName, TeacherNameList, choosenNum, SectionCapacity]
        else:
            results[SectionID][1].append(TeacherName)
    return results


@app.route('/')
@app.route("/login/", methods=["GET", "POST"])
def login():
    if 'StudentID' not in session:
        if request.method == 'POST':
            cursor = conn.cursor()
            login_studentID = request.form.get("studentID")
            login_password = request.form.get("password")
            find_user_query = f"""SELECT User.StudentID, User.Password, Student.StudentName FROM User INNER JOIN Student ON User.StudentID = Student.StudentID WHERE User.StudentID = \"{login_studentID}\""""
            cursor.execute(find_user_query)
            login_user = cursor.fetchone()
            if login_user:
                if bcrypt.checkpw(login_password.encode("utf-8"), login_user[1].encode('utf-8')):
                    session['StudentID'] = login_user[0]
                    session['StudentName'] = login_user[2]
                    return redirect(url_for('my_course'))
                else:
                    flash("alert-danger")
                    flash("密碼錯誤")
                    return render_template("index.html")
            else:
                flash("alert-danger")
                flash("無此使用者")
                return render_template("index.html")
        else:
            return render_template("index.html")
    else:
        return redirect(url_for('my_course'))

@app.route('/register/')
def register():
    cursor = conn.cursor()
    hash_password = bcrypt.hashpw("123".encode("utf-8"), bcrypt.gensalt())
    hash_password_str = hash_password.decode("utf-8")
    query = f"INSERT INTO User VALUES (\"D0948079\", \"{hash_password_str}\")"
    cursor.execute(query)
    conn.commit()

@app.route('/logout/', methods=['GET'])
def logout():
    session.clear()
    flash('alert-success')
    flash('登出成功')
    return redirect(url_for('login'))

@app.route('/my_course/', methods=['POST', 'GET']) # 設定瀏覽器在 /my_course/ 的時候要跑這個程式，以及設定方法只能是 POST 跟 GET
def my_course():
    if 'StudentID' in session:
        cursor = conn.cursor()
        get_total_credit_query = f"""
        SELECT cast(coalesce(SUM(CourseCredit), 0) AS UNSIGNED) as CourseCredit
        FROM Takes
        INNER JOIN Section
        ON Takes.SectionID = Section.SectionID
        INNER JOIN Course
        ON Section.CourseID = Course.CourseID
        WHERE StudentID = "{session['StudentID']}"
        """
        cursor.execute(get_total_credit_query)
        total_credit = cursor.fetchone()[0]
        results = get_student_course(session['StudentID'])
        courseTable = get_student_courseTable(session['StudentID'])
        return render_template("course_table_result.html", results=results, courseTable=courseTable, total_credit=total_credit)
    else:
        return redirect(url_for('login'))

@app.route('/add_course/', methods=['POST', 'GET'])
def add_course():
    if 'StudentID' in session:
        ########### 建立選課選單 #############
        results = get_all_course()
        ####################################

        ########### 選課 ####################
        if request.method == 'POST':
            try: # 用例外處理 判斷報錯就跳轉到 404
                course = request.form.get("course")
                cursor = conn.cursor()
                if course == None: # 判斷輸入是否為空
                    flash("alert-danger")
                    flash("未選課程！")
                    return redirect(url_for("add_course"))

                ########## 獲取學生現在的學分 ###########
                get_total_credit_query = f"""
                SELECT cast(coalesce(SUM(CourseCredit), 0) AS UNSIGNED) as CourseCredit
                FROM Takes
                INNER JOIN Section
                ON Takes.SectionID = Section.SectionID
                INNER JOIN Course
                ON Section.CourseID = Course.CourseID
                WHERE StudentID = "{session['StudentID']}"
                """
                ######################################
                ######### 獲取欲選的課的學分 ############
                get_current_credit_query = f"""
                SELECT Course.CourseCredit
                FROM Section
                INNER JOIN Course
                ON Course.CourseID = Section.CourseID
                WHERE SectionID = "{course}"
                """
                ######################################

                # ----------------- #
                cursor.execute(get_total_credit_query)
                total_credit = cursor.fetchone()[0] # 把輸出強制轉成 Int
                cursor.execute(get_current_credit_query)
                total_credit += cursor.fetchone()[0] # 把輸出強制轉成 Int 並加上 total_credit 得出會不會超修
                if total_credit > 30:
                    print("您已超修")
                    flash("alert-danger")
                    flash("您已超修！")
                    return redirect(url_for("add_course"))
                # ------------------ #

                ########### 獲取學生已選的課 ############
                get_total_course_query = f"""
                select Course.CourseName
                from Takes
                inner join Student
                on Takes.StudentID = Student.StudentID
                inner join Section
                on Takes.SectionID = Section.SectionID
                inner join Course
                on Course.CourseID = Section.CourseID
                where Student.studentID = '{session['StudentID']}';
                """
                ######################################

                get_current_course_name_query = f"""
                select Course.CourseName
                from Course
                inner join Section
                on Section.CourseID = Course.CourseID
                where Section.SectionID = {course}
                """
                
                # ----------------- #
                cursor.execute(get_total_course_query)
                total_course = cursor.fetchall() # 把已選課表 (SectionID) 撈出來 (Tuple 型態)
                cursor.execute(get_current_course_name_query)
                current_course_name = cursor.fetchone()[0]
                total_course_list = []
                for section in total_course:
                    total_course_list.append(section[0])
                if current_course_name in total_course_list:
                    print("無法選取重複的課程")
                    flash("alert-danger")
                    flash("無法選取重複的課程！")
                    return redirect(url_for("add_course"))
                # ----------------- #

                ####### 獲取欲選的課的現在人數 ###########
                get_section_sum_query = f"""
                select count(SectionID) as ChoosenCount
                from Takes
                where SectionID = "{course}"
                """
                ######################################
                ######### 獲取欲選的課的最大人數 #########
                get_section_maximum_query = f"""
                select SectionCapacity
                from Section
                where SectionID = "{course}"
                """
                ######################################

                # ----------------- #
                cursor.execute(get_section_sum_query)
                section_sum = cursor.fetchone()[0] # 把已選的人數撈出來強制轉成 Int
                cursor.execute(get_section_maximum_query)
                section_maximum = cursor.fetchone()[0] # 把課程最大人數撈出來強制轉成 Int
                if section_sum >= section_maximum:
                    print("課程人數已滿")
                    flash("alert-danger")
                    flash("課程人數已滿！")
                    return redirect(url_for("add_course"))
                # ----------------- #

                ######### 獲取學生已選的時間 #########
                get_total_time_query = f"""
                SELECT Time.TimeID
                FROM Time
                INNER JOIN SectionAt
                ON SectionAt.TimeID = Time.TimeID
                INNER JOIN Takes
                ON Takes.SectionID = SectionAt.SectionID
                WHERE Takes.StudentID = "{session['StudentID']}"
                ORDER BY `TimeID`;
                """
                ###################################
                ######### 獲取欲選的課的時間 #########
                get_current_time_query = f"""
                SELECT Time.TimeID
                FROM Time
                INNER JOIN SectionAt
                ON SectionAt.TimeID = Time.TimeID
                INNER JOIN Section
                ON Section.SectionID = SectionAt.SectionID
                WHERE Section.SectionID = "{course}";
                """
                ###################################

                # ----------------- #
                cursor.execute(get_total_time_query)
                total_time = cursor.fetchall() # 獲取學生所有課的時間
                total_time_list = []
                for time in total_time:
                    total_time_list.append(time[0]) # 把撈出來的資料轉成 list 型態
                cursor.execute(get_current_time_query)
                current_time = cursor.fetchall()
                for time in current_time:
                    if time[0] in total_time_list: # 如果要選的課有任何一個時段重複，就顯示衝堂
                        print("您已衝堂")
                        flash("alert-danger")
                        flash("您已衝堂！")
                        return redirect(url_for("add_course"))
                # ----------------- #
                if total_credit < 31 and current_course_name not in total_course_list and section_sum < section_maximum:
                    insert_query = f"""
                    INSERT INTO `Takes` (`SectionID`, `StudentID`, `Semester`, `Year`) VALUES ('{course}', '{session['StudentID']}', "2", "110");
                    """ # SQL 指令：把選課資料 insert 進去 takes
                    cursor.execute(insert_query)
                    conn.commit()
                    flash("alert-success")
                    flash("加選成功！")
                    return redirect(url_for("add_course"))
            except Exception as e:
                return render_template("error.html", error_message=str(e))
        else:
            return render_template('add_course.html', results=results)
    else:
        return redirect(url_for('login'))

@app.route("/del_course/", methods=["GET", "POST"])
def del_course():
    if 'StudentID' in session:
        if request.method == "POST":
            try:
                cursor = conn.cursor()
                del_sectionID = request.form.get("del_sectionID")
                ########## 獲取學生現在的學分 ###########
                get_total_credit_query = f"""
                SELECT cast(coalesce(SUM(CourseCredit), 0) AS UNSIGNED) as CourseCredit
                FROM Takes
                INNER JOIN Section
                ON Takes.SectionID = Section.SectionID
                INNER JOIN Course
                ON Section.CourseID = Course.CourseID
                WHERE StudentID = "{session['StudentID']}"
                """
                ######################################
                ######### 獲取欲選的課的學分 ############
                get_current_credit_query = f"""
                SELECT Course.CourseCredit
                FROM Section
                INNER JOIN Course
                ON Course.CourseID = Section.CourseID
                WHERE SectionID = "{del_sectionID}"
                """
                ######################################

                cursor.execute(get_total_credit_query)
                total_credit = cursor.fetchone()[0] # 把輸出強制轉成 Int
                cursor.execute(get_current_credit_query)
                total_credit -= cursor.fetchone()[0] # 把輸出強制轉成 Int 並加上 total_credit 得出會不會超修
                if total_credit < 9:
                    print("無法退選，已到最低學分")
                    flash("alert-danger")
                    flash("無法退選，已到最低學分!")
                    return redirect(url_for("my_course"))
                
                if total_credit > 8:
                    delete_query = f"""DELETE FROM Takes WHERE StudentID = "{session['StudentID']}" AND SectionID = "{del_sectionID}";"""
                    cursor.execute(delete_query)
                    conn.commit()
                    flash("alert-success")
                    flash("退選成功！")
                    return redirect(url_for("my_course"))
            except Exception as e:
                return render_template("error.html", error_message=str(e))
        else:
            return redirect(url_for("my_course"))
    else:
        return redirect(url_for("login"))

