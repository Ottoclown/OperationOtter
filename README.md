# OperationOtter

code dependencies:

`python3 -m pip install -U pygame --user`

To run this code enter the following commands:

`python ./game.py`

To add events to the event database:

- open /database/events.xlsx in Excel
- add a row corresponding to your event. The Event components should be added in the following order:
    - EVENT TYPE in the first column. This is a code that corresponds to the type of event it is. No type functioning is in place yet, but this can be added to later models to allow for different types of questions.
    - Q_PROMPT in the second column. Add text that corresponds the event prompt i.e. (a war broke out)
    - OPTION PROMPTS are in the following X columns. Each event has the capability to handle a multitude of different answer prompts. Put each of the X prompts answer prompt in its own column, one after another. 
    - REQ or requirements are in the next X columns. After each answer prompt is added, in the next column, add the string "REQ" to signify the change between answer prompts and requirements. Add X columns for the requirements where X is the number of answer prompts. Requirments should either correspond to a skill id like "TECH10", or be the string "0" if there are no requirements for that answer.
    - EFFECTS are in the last X columns. After the requirements, enter the string "EFFECTS" in the following column. Then enter an integer in each of the X following columns associated with effect size of the corresponding answer prompt. Each integer is the number of believers gained from choosing that prompt.
- Finally, save the file. Then Save the file as a CSV with the name events.csv and overwrite the file already existing within Database with that name.

To add or change Skills:
- open /database/(XXX).xlsx in Excel. replace (XXX) with either (HIST_SKILLS, TECH_SKILLS, or WRIT_SKILLS)
- the columns of the Skills correspond to the following:
    - ID in the first column. this is the small code corresponding to the unique skill. This ID must take the form of TECHX, HISTX, or WRITX where x is the number associated with the upgrade in order. ex. TECH1, HIST4, WRIT12.
    - NAME in the second column. This is the name of the skill which the player will see when they hover over the skill in the skill tree.
    - PREREQS are in the third column. This is the number corresponding the the requirement necessary to recieve before the current skill is obtained. This prereq is 0 if the skill has no requirements. If it does require a previous skill to upgrade as in it is the second or third level in the tree, prereq should take the form of the number corresponding to the prereq in the current tree that is required. ex. if "TECH10" is a prereq, then the entry in prereq should be "10". As of now, each skill can only have one prereq, and prereqs can only be items in the same skill tree.
    - COST is in the fourth column. This entry is a integer that represents the number of believers that skill costs to upgrade.
    - OPTION_TYPE is in the fifth column. This entry is a code written in all capitol letters that describes the events this upgrade applies to. (ex. PANDEMIC, WAR)
    - EFFECT_TYPE is in the sixth column. This refers to the type this effect has (PASSIVE, BONUS, or MULT). PASSIVE increases passive increase of believers. BONUS increases the number of believers gained from event responses by a constant amount. MULT increases the number of believers gained from events by a multiplicative amount.
    - EFFECT_SIZE is in the seventh column. This is an integer that corresponds to the size of the effect. For BONUS this is an integer number of believers. for PASSIVE, this number is float that is the multiplicative increase to passive believer gain.  for MULT, this number is a float that describes multiplicative increase to beliver gain from events.
    - HOVER_TEXT is in the eighth column. This is the text that is displayed when hovering over the upgrade.
- Change upgrades by altering these values or names
- To add new upgrades add a row at the end following the upgrade format above.
- Always keep the last row empty with the ID slot containing the string "END".
- Save the file as an .xlsx with the same name as before.
- Export the file to a .csv format with the same name, and replace the other file with this name in the folder.