# WinkelBudget 1.0
**Finally reached 1.0 release!**  
  
This budget application can help you keep track of your spending on a monthly basis. This application makes use of Python's many other capabilities to provide a unique blend of charts, graphs, and tables to give a cohesive experience.

## How To Get Started
1. Install Python 3.10 or later.
2. Download or clone this repo to your desired location
3. Navigate to the folder named *BudgetTool*
4. Install the dependencies by running: *pip install -r requirements.txt*
5. Run the application with *python Winkelbudget.py*

This application should be rather simple to understand. Simply add what you expect your income and monthly costs are, then add the actual costs via the *Add Expense* functionality. From here, the application will calculate insightful information and generate helpful charts and graphs to have a better insight on your monthly expenses. You will be able to fully customize the expense categories as well as save notes regarding the specific month. Remember to press the *save* button to save your budget!

For a more in-depth breakdown of technical details regarding this project see my project article on my pages site here:

## Inspiration for WinkelBudget
I wanted to make this application to give myself a tool to budget effectively with all the bells and whistles of other applications (that often require a payment). In doing so, I've also been able to grow in my ability to develop complex programs. GUI applications are not my strong suit, and having only been exposed to Tkinter previously, learning to use QT via PyQT has been a unique learning experience. 

## Known Gaps
Since this has mainly been a side project, it has taken awhile to fully take form. This 1.0 release is actually the first fully functioning release of this application, but beta forms have existed for well over a year. Sometime back in May 2026 I decided to completely refactor the way I was structuring this program. This was a mix of multiple things: hating the structure of old code (primary reason, hindsight 20/20), coming back to the project after some time away (new unfamiliarity), and allowing for the code to be better expanded upon in the future. Despite the improvements made that have led to the 1.0 release of this application there are still some noticeable gaps. 

#### GUI is Plain
For the 1.0 release I made the GUI design simple. I actually had more Windows and design elements in the beta version of this application but chose to eliminate those to iron out functionality. Further releases/updates will slowly introduce new UI elements as I learn them. I am also hoping to release a set of *themes* that can be selected via some sort of settings functionality.

#### Presence of Non-Implemented Features
There are some features that are deliberately not implemented and labeled as such. These are ultimately placeholders for future functionality that I chose to show in the GUI to better allow my brain to visualize where the application is going. This is probably not best practice, but I was willing to overlook it to get the 1.0 release how I was envisioning and out the door.

#### Functionality Gaps / Unimpressive Nature
You might see this application and say "this is just a Python GUI for an excel spreadsheet" to which I would honestly agree. I hear this criticism loud and clear, but everything needs to start somewhere. Eventually more in-depth functionality will be added to separate it from just a Python-coated spreadsheet, but for the 1.0 release, that criticism will have to stand. It is far more important to me to get the 1.0 release and bones out the door and build up from there. While this program may not be astonishing or impressive in its functionality, it *works* and that is good enough for me.

#### Generic Code Structure Improvements
As I said, I am still fairly new to GUI programming, so it is not a *skill* of mine. With that being said, I am sure that the generic structure and coding practices within this application are not of the highest quality. Marked improvements can be made for sure, and I am open to any and all feedback on the application's code and structure.

## The Future
There are more features that will be added as time goes on, as this is more of a side project, things will take some time.  
Some features that are planned for future releases are:  
- UI improvements
- Savings tracking
- Charts and graphs over selected timeframe
- Different themes
- Removal of cmd line launch, main menu
- Communication with some kind of webserver to pull stored expenses from
    - Planning to pair this with another project of mine to make adding expenses throughout the month easier. Stay tuned.

## Reporting Bugs
Please report any bugs using the "Issues" feature on Github, and I will try my darndest to fix them in a timely manner.

*Thank you for stopping by this Installation!*