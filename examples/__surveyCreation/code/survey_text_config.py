config = __import__("config")

welcome_text = '''
                <p> </p>
                <p style="margin-left: 10px"> <b> Welcome! </b> </p>
                <p> </p>
			    <p style="margin-left: 10px">We have gathered a list of researchers and their research areas.</p>
			     <p> </p>
			     
			    <p style="margin-left: 10px"><mark> <b> Your job is to find the Google Scholar link associated with 
			    the given researcher (if it exists).</b> </mark></p>			    
			    '''
welcome_header = "Welcome"

payment_text = ''' <p> </p>
                    <p> </p>
                    <p style="margin-left: 10px"> We will provide you with a list of ''' + str(config.tasks_per_hit) + ''' researchers. You must complete the full assignment in
                    order to receive your base payment of $''' \
                    + config.base_payment + '''.</p>
                     <p style="margin-left: 10px"> You will earn the majority of your money through <b> bonus 
                     payments </b> which will be <b>determined by
                     the accuracy of your answers: each time you select the same answers that were 
                     choosen by the majority of other mTurkers answering this question</b> you will receive a 
                     <b>$''' + config.bonus_payment + ''' bonus. </b></p>
                     <p> </p>
                     <p> </p>
                     <p style="margin-left: 10px"> You have the opportunity to earn <b>up to
                      $''' + config.bonus_payment_total + ''' in bonus payments</b>, which is paid in addition to the
                      $''' + config.base_payment + ''' for completing the entire task.</p>
                     <p> </p>
                     <p> </p>
                     <p style="margin-left: 10px"> We expect the task to take''' + config.survey_time +'''. </p>
                     <p> </p>
                     <p> </p>
                <p style="margin-left: 10px"> <b> The next page provides detailed instructions for finding the Google Scholar pages.</b></p>'''

payment_header = "Payment Details"

instructions_text = ''' <p style="margin-left: 10px">For each task you will be shown a description of a researcher. </p>

                <p style="margin-left: 10px"> The reseracher description contains two parts:<ol>
			     <li> "Name": the researcher's full name</li>
			      <li>"Research area": a list of research areas</li>
			       <p> </p>
             <p style="margin-left: 10px">Your task is to do the following:</p>
            <p><ol>
                <li>Search for the Google Scholar page of the given researcher. You can either go to <a target="_blank" href="https://scholar.google.com/">https://scholar.google.com/</a> and search by name. To make 
                your task simpler we will already provide a search link that directly opens a Google Scholar search.<p> </p></li>
                <li> If you are able to find the page check "Yes" and enter the url for the page. <p> </p></li>
                <li>If you are unable to find the page check "No."<p> </p></li>
            </ol></li></p>
            <p> </p>
            <p style="margin-left: 10px"><mark> <b> Remember you will be paid a bonus based on your performance, 
            determined by the degree to which 
            your answers match the answers of other mTurkers. </b> </mark></p> 
            <p> </p>
            '''
instructions_header = "Instructions"

researcher_header = "Find the Google Scholar site for this researcher!"

feedback_header = "We want your feedback!"

