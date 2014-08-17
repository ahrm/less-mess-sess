less-mess-sess
==============

A less messy sess.

### How to setup less-mess-sess:


1. First clone or download this repository.
2. In the root folder make a file named my_data.py and put two strings in them:
    ```
    my_username = "your_sess_username"
    my_pass = "your_sess_password"
    ```
3. Open database_manager.py and edit dbfilename to the path to your database file. (if the database does not exist it will be created)
4. Run the database_manager.py. This creates the database tables. **WARNING: running this file will remove anything that you had in the database!**
5. Open load_database.py and edit current_department to the department you want to add to the database. (if you want to add multiple departments you must run this file multiple times)
6. Run load_database.py.
7. Now run mainapp.py.
8. go to http://127.0.0.1:5000.


### How to use less-mess-sess
* You can filter the results using filters in the left part of the screens. The included filters are:
  * Department Filter: You can specify from which department to fetch the courses.
  * Course Name Filter: Name of the course. You don't need to specify the full name of the course. You can select multiple names using ','. for example:
    ```
    الگور,داده
    ```
  * Professor Name Filter: Professor name. Other rules are similar to course name.
  * Course Day Filter: Days of the selected courses seperated by ','. For example:
    ```
    0,2,3 #یعنی شنبه و دو شنبه و سه شنبه
    ```
  * Course Time Filter: What time the courses are. You specify time ranges separated by commas in the following syntax:
    ```
    (7:30-9:0),(12:0-14:0)
    ** Note: Even when the minute is 0 you should specify it. So (12-14) is an error.**
    ```
  * Sex Filter: Which sex is allowed in class.
* After you have selected your filters you can press the update button to show the specified courses. You can select the courses by clicking on them. the newly selected courses are marked green.
* You can change the filter after selecting the desires courses and press the update button again. Note that any selected course will be shown again even if they don't satisfy the new filter.
* After selecting all your courses you can press the schedule button which shows a HTML schedule. Hours that are free are colored green. Hours that have courses are colored yellow. If there are more than one course in a cell it is colored red. Note that being red doesn'y necessarily mean that there is a conflict. Because for Example imagine there is a course from 8 to 10. It is shown in the table in both 7:30-9 and 9:10:30 cells. Now if there is another course from 10 to 12 it is shown in 9:30-11 and 11-12:30 cells. So even though there is no overlap the 9-10:30 cell is still coloured red. 
    
