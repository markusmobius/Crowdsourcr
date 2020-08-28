config = __import__("config")

consent_form = '''
<h1>Microsoft Research Project Participation Consent Form</h1>
<h2>INTRODUCTION</h2>
Thank you for taking the time to consider volunteering in a Microsoft Corporation research project.  This form explains what would happen if you join this research project. 
Please read it carefully and take as much time as you need. Email the study team to ask about anything that is not clear.  
Participation in this study is voluntary and you may withdraw at any time. 

<h2>TITLE OF RESEARCH PROJECT</h2>
Researcher Labeling Task

<h3>Principal Investigator</h3>
Markus Mobius

<h2>PURPOSE</h2>
The purpose of this project is to find additional publicly available data on a list of researchers.

<h2>PROCEDURES</h2>
<p>During this session, you will be shown a list of researchers.</p>
<p>For each researcher, you will be asked to find additional information through a web search.</p>

<h3>PAYMENT FOR PARTICIPATION</h3>
<p>You will receive $''' + config.base_payment + ''' for completing this session plus an additional bonus payment of up to $'''+ config.bonus_payment_total + ''' contingent on your performance, as measured by the agreement of your responses with those of other raters.</p>

<h2>PERSONAL INFORMATION</h2>
<p>Aside from your WorkerID, we do not collect any personal information in this project. </p>
<p>Your WorkerID and response will be temporarily recorded and used for the purpose of paying out bonuses based on task performance.</p>
<p>Your WorkerID will not be shared outside of Microsoft Research and the confines of this study without your permission, and will be promptly deleted after compensation has been successfully provided (30 days or less). De-identified data may be used for future research or given to another investigator for future use without additional consent. </p>
<p>Responses from all participants will be aggregated and stored for a period of up to 5 years. Once your WorkerID is disassociated from your responses we may not be able to remove your data from the study without re-identifying you.</p>
<p>For additional information on how Microsoft handles your personal information, 
please see the <a href="https://privacy.microsoft.com/en-us/privacystatement">Microsoft Privacy Statement</a>.</p>

<h2>BENEFITS AND RISKS</h2>
<p>Benefits: The research team expects to learn how to group researchers working on similar topics across disciplines. You will receive any public benefit that may come these Research Results being shared with the greater scientific community. </p>
<p>Risks:  During your participation, you should experience no greater risks than in normal daily life. 
<p>You accept the risks described above and whatever consequences may come of those risks, however unlikely, 
unless caused by our negligence or intentional misconduct.  
You hereby release Microsoft and its affiliates from any claim you may have now or in the future arising from such risks or consequences.    
In addition, you agree that Microsoft will not be liable for any loss, damages or injuries 
that may come of improper use of the study prototype, equipment, facilities, or 
any other deviations from the instructions provided by the research team.   
Don’t participate in this study if you feel you may not be able to safely participate in any way 
including due to any physical or mental illness, condition or limitation.    
You agree to immediately notify the research team of any incident or issue or unanticipated risk or incident.</p>

<h2>CONTACT INFORMATION</h3>
<p>Should you have any questions concerning this project, or if you are harmed as a result of being in this study, please contact Markus Mobius at mobius@microsoft.com.</p>
<p>Should you have any questions about your rights as a research subject, please contact Microsoft Research Ethics Program Feedback at MSRStudyfeedback@microsoft.com.</p>
<p>Upon request, a copy of this consent form will be provided to you for your records. On behalf of Microsoft, we thank you for your contribution and look forward to your research session.</p>
'''