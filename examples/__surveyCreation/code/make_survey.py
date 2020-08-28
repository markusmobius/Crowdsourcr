import pandas as pd
import random

config = __import__("config")
Table = __import__("DocTable")
Q = __import__("Question")
XML = __import__("XMLdoc")
text = __import__("survey_text_config")
consent = __import__("consent_text")

#####  Set Questions and Modules   #############
#################################################

### Questions ####
q_welcome = Q.Question(varname="welcome",
                   questiontext="Before presenting the task, we will provide you"
                                " with some brief instructions.",
                   valuetype="categorical",
                   categories=["I would like to continue to the instructions and then complete the task."])

q_payment = Q.Question(varname="payment",
                   questiontext="Please take time to read the payment scheme carefully before you proceed.",
                   valuetype="categorical",
                   categories=["I understand that the majority of my payment can be earned through "
                               "the accuracy of my responses."])
q_consent = Q.Question(varname = "consent",
		            questiontext = "Please carefully read the consent form provided before proceeding with this task.",
		            valuetype = "categorical",
		            categories = ["I agree to participate in this study."])

q_instructions = Q.Question(varname="instructions",
                   questiontext="Please take time to read the instructions carefully before you proceed.",
                   valuetype="categorical",
                   categories=["I have read and understood the task instructions."])

q_google_site = Q.Question(varname = "google_site",
					questiontext = "Does the Google Scholar site for this researcher exist?",
					valuetype = "categorical",
					categories = ["Yes", "No"],
					bonus = ["threshold:49", 1])

q_google_url = Q.Question(varname = "google_url",
					questiontext = "Please provide the URL of the researcher's Google Scholar site homepage.",
					valuetype = "url",
                    condition = "google_site==Yes")

q_feedback = Q.Question(varname = "feedback",
					questiontext = "Please describe any comments or feedback you have about this task.",
					valuetype = "text",
					helptext = '''Please provide any comments you have about the tasks you have completed.''')

### Modules ##
module_welcome = XML.Module(name="welcome", header=text.welcome_header, questions=[q_welcome])
module_consent = XML.Module(name = "consent", header = "Consent Form", questions = [q_consent])
module_payment = XML.Module(name="payment", header=text.payment_header, questions=[q_payment])
module_instructions = XML.Module(name="instructions", header=text.instructions_header, questions=[q_instructions])
module_researcher = XML.Module(name="researcher_site", header=text.researcher_header, questions=[q_google_site, q_google_url])
module_feedback = XML.Module(name="feedback", header=text.feedback_header, questions=[q_feedback])

modules = [module_welcome, module_consent, module_payment, module_instructions, module_researcher, module_feedback]

#####  Make Tasks and Docs  #########
###############################################
welcome_doc = XML.Document(name="welcome", content=text.welcome_text)
welcome_task = XML.Task(doc_name = "welcome",
						  doc_content =text.welcome_text, taskid = -5, modules = module_welcome)

consent_doc = XML.Document(name="consent", content=consent.consent_form)
consent_task = XML.Task(doc_name = "consent", doc_content=consent.consent_form, taskid = -4, modules = module_consent)

payment_doc = XML.Document(name="payment", content=text.payment_text)
payment_task = XML.Task(doc_name = "payment",
						  doc_content =text.payment_text, taskid = -3, modules = module_payment)
instructions_doc = XML.Document(name="instructions", content=text.instructions_text)
instructions_task = XML.Task(doc_name = "instructions",
						  doc_content =text.instructions_text, taskid = -2, modules = module_instructions)

intro_tasks = [welcome_task, consent_task, payment_task, instructions_task]
intro_docs = [welcome_doc, consent_doc, payment_doc, instructions_doc]

feedback_task = XML.Task(taskid = -100, modules = module_feedback, doc_name="feedback", doc_content="")
feedback_doc = XML.Document(name="feedback", content="")

# read in data to create researcher tasks
researcher_df = pd.read_csv(config.infile_path,sep='\t')

researcher_tasks = []
researcher_docs = []
researcher_task_ids = []
for i, row in researcher_df.iterrows():
    name = str(row[config.name_col])
    areas = str(row[config.researcher_area_col])
    username =  str(row[config.researcher_username])
    
    doc_table = XML.DocTable(name, areas)
    doc_table_str = doc_table.write_table()

    doc_name = username

    doc = XML.Document(name=doc_name, content=doc_table_str)
    task = XML.Task(doc_name=doc_name, doc_content=doc_table_str, taskid=username, modules=module_researcher)

    researcher_task_ids.append(username)
    researcher_tasks.append(task)
    researcher_docs.append(doc)


####    Assign Tasks to HITS     ##########
###########################################
hits = []

random.seed(config.seed)
for i in range(0,2):  # assign each task to two HITs for double data entry

    random.shuffle(researcher_task_ids)
    for j in range(0, len(researcher_task_ids), config.tasks_per_hit):  # assign tasks to each HIT --  NOTE the final HIT will be short if total tasks is not a multiple of tasks_per_HIT

        tasks = ["-5", "-4", "-3", "-2"] # add intro tasks
        tasks += [str(id) for id in researcher_task_ids[j:j + config.tasks_per_hit]]  # add researcher tasks
        tasks += ["-100"]  # add feedback
        hitid = str(j) + "_" + str(i)
        hit = XML.HIT(hitid=hitid, task_ids=" ".join(tasks))
        hits.append(hit)

####   Assign objects to XMLdoc and write output ###
####################################################
xmlDoc_test = XML.XMLdoc(modules = modules, tasks = intro_tasks + researcher_tasks + [feedback_task],
					 hits = hits, documents = intro_docs + researcher_docs + [feedback_doc])

xmlDoc_test.write_xml(config.outfile_path)