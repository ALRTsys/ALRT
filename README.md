## What is ALRT?
ALRT is a tailgating and piggybacking detection system that utilizes video analytics to count people 
using line-crossing detection to detect intrusion attempts that might happen in restricted areas containing assets.

## What does ALRT stand for?
ALRT is a contribution to the project developers. The name does not really mean 
anything, but it does sound like the word alert, which is a goal of the project as it alerts the CCTV operator of attempted intrusions.

## ALRT prerequisites
1- Download Python - https://www.python.org/downloads/

2- Download PyCharm Community - https://www.jetbrains.com/pycharm/

3- Download MySQL Workbench - https://dev.mysql.com/downloads/workbench/

4- Download "ALRT-Complete" 

In GitHub, “ALRT-Complete” is the full project that contains the detection code including the interface while “Main_Code” is just the detection code without the interface. In “Main_Code” the alarming messages will only 
be shown in the terminal and no alarm will go off, so to see the full project with its full potential it’s better to work on “ALRT-Complete”.

## ALRT with MySQL Workbench

“ALRT-Complete” requires using a database, so with MySQL Workbench create a new MySQL Connection, keep the name 
as it is, which is ‘root’ and the for the password you can choose your own password. Then create a database named `log_in` and a table named `cctv_operator`.

The table contains:

1-	`Id` (Binary)
2-	`Username` (VARCHAR)
3-	`Password` (VARCHAR)

After adding all three to the table, right-click on `cctv_operator`, copy to clipboard - insert statement 
then write this command:

     INSERT INTO `log_in`.`cctv_operator`
     (`ID`,
     `Username`,
     `Password`)
      VALUES
      (0, 'CCTVop', sha1('Ant17a1l8at1n8#')), 
      (1, 'Admin', sha1('AdminME123#'));
      
      
Lastly, don’t forget to add your MySQL Workbench password in the 10th line of both 
the “LoginForCCTVop.py” and ”LoginForAdmin.py” in the “ALRT-Complete” file.

![2023-02-27](https://user-images.githubusercontent.com/125115519/221488709-fef4ce28-dc68-47dd-be43-b75c6060cabf.png)

## Opening "ALRT-Complete" using PyCharm

When done with the database, open “ALRT-Complete” using PyCharm. Before running it, you need to make sure that you installed all the needed packages
by going to file -> settings -> project: ALRT -> Python interpreter -> + than choose the needed packages:

                1.	flet
                2.	opencv-python
                3.	time
                4.	base64
                5.	threading
                6.	mysql-connector-python

For the mysql-connector-python you need to watch this short video to make sure the connector does work:https://www.youtube.com/watch?v=MhaH7o3lf4E (starts from 4:30 and ends at 12:52).

After installing all the required packages using the terminal in PyCharm write this command and then press return: 
 
                 Python main.py

![2023-02-27 (3)](https://user-images.githubusercontent.com/125115519/221490994-49c0908b-14df-4303-ae00-73ce816d5155.png)


and just like that ALRT should start working well with you just as it did with us :).

![2023-02-27 (4)](https://user-images.githubusercontent.com/125115519/221491165-35a01cb1-865d-4452-9a99-81dae2deab08.png)

## ALRT issues

In the event that the project does not work with you, please do not hesitate to contact us: tailgatingdetectionsys@gmail.com

