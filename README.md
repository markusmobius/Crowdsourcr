Crowdsourcr is a Python 3 tool to create surveys programmatically and run them in a browser. Amazon Turk integration is inbuilt.

- Surveys are defined in XML format.
- A survey consists of modules and modules consist of questions.
- There is a wide variety of text, numerical and categorial (including nested categorical) questions (all defined through XML).
- A task is some content (such as an image or a piece of text) paired with a sequence of modules/questions.
- A Crowdsourcr HIT (or cHIT) consists of a set of tasks 
- Two cHITs can contain the same tasks. This allows for programmatic definition of double or triple data entry.
- If a task is completed by more than one worker a bonus can be paid depending on agreement and if the question is defined as a bonus question in the XML.
- Conditional flow within the survey is available: this allows for screening questions (where cHITs are retired if a worker scores below a threshold) and conditional flow within a module.

Crowdsourcr was originally developed by Kyle Miller and Sam Grondahl at MSR New England in 2014. Bonus questions were added by Markus Mobius and Tobias Schmidt in 2017. In 2019, Ling Dong and Markus Mobius ported the code to Python 3 and updated the MTurk integration to use boto3.
