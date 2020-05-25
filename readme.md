 a) To optimize the app for better performance, I would cythonize the script. Offloading most of the heavy lifting to C has the potential to speed up the application by a great margin.

 b) Steps
   ## Step 1
   - Pull repo to a folder of your choice.

   ## Step 2
   - Open app.py and go to lines 137 and 138. Set the paths specified.

   ## Step 3
   ***Assumption is that app is being run on a Windows platform and that python3.+ is installed***
   - Open app.bat and paste the path to your Python installation on the first argument.
   - Paste the path to app.py in the second argument
   - **Be sure to maintain the quotes on the second argument**

   ## Step4
   - If you wish to create a schedule of when and/or the frequency to run the service, open the architecture diagram pdf and follow the instructions to setup a schedule using Windows Task Scheduler

    ***app.bat should look something like this:***
    *C:\Users\User\AppData\Local\Continuum\anaconda3\python.exe "C:\Users\User\Desktop\Whereismytransport\app.py"*

   - You can run the app anytime by simpling double clicking app.bat. All the modules used by the app are built in with Python so no need to install anything else. If you're facing trouble with app.bat, simply open a terminal window, navigate to the directory where app.py is located and then run *python app.py*.
   
 c) It is very important that you setup app.bat and Windows Task Scheduler correctly for it to automate running the service at 4 hour intervals.

 d) If there was more time, I would develop an efficient and reliable C extension that would dramatically speed up the service, especially since it is anticipated to run millions of logs at a time. I also would've built implementations of the same service that run on other platforms such as MacOS and Linux.

 e) Python is a reliable tool that allows me to execute concepts into production within  a very short time frame. It is also very powerful and efficient.
