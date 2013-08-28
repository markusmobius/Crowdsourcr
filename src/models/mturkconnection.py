import os
import boto.mturk.connection
import boto.mturk.question 
#QuestionContent,Question,QuestionForm,Overview,AnswerSpecification,SelectionAnswer,FormattedContent,FreeTextAnswer

class MTurkConnection(object):
    def __init__(self, access_key=None, secret_key=None, email=None, hitpayment=1.0, running=False, hitid=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.email = email
        self.running = running
        self.hitpayment = hitpayment
        self.mturk_conn = boto.mturk.connection.MTurkConnection(self.access_key,
                                                                self.secret_key)
        self.hitid = hitid
    def try_auth(self, access_key=None, secret_key=None):
        return True if self.get_balance() else False

    def get_balance(self):
        try:
            return self.mturk_conn.get_account_balance()
        except:
            raise

    def get_all_hits(self):
        return [hit.HITId for hit in self.mturk_conn.get_all_hits()]
    
    def serialize(self):
        return { 'access_key' : self.access_key,
                 'secret_key' : self.secret_key,
                 'email' : self.email,
                 'running' : self.running,
                 'hitpayment' : self.hitpayment,
                 'hitid' : self.hitid }
    @classmethod
    def deserialize(cls, d):
        return MTurkConnection(access_key=d['access_key'],
                               secret_key=d['secret_key'],
                               email=d['email'],
                               hitpayment=d['hitpayment'],
                               running=d['running'],
                               hitid=d['hitid'])
    def begin_run(self, max_assignments):
        overview = boto.mturk.question.Overview()
        overview.append_field('Title', 'News Classification Task')
        overview.append(boto.mturk.question.FormattedContent('<p> You will be reading news articles and answering questions about them. To begin, navigate to the following url: <a href="http://localhost:8000/HIT/">localhost:8000/HIT/</a> .</p>'))
        
        
        qc1 = boto.mturk.question.QuestionContent()
        qc1.append_field('Title','Secret Code')
        qc1.append_field('Text', 'Enter the 16 character secret code that you will receive after you complete this task.')
        fta1 = boto.mturk.question.FreeTextAnswer()
        q1 = boto.mturk.question.Question(identifier='secretcode',
                      content=qc1,
                      answer_spec=boto.mturk.question.AnswerSpecification(fta1),
                      is_required=True)

        question_form = boto.mturk.question.QuestionForm()
        question_form.append(overview)
        question_form.append(q1)

        hitinfo = self.mturk_conn.create_hit(questions=question_form,
                                   max_assignments=max_assignments,
                                   title="News article classification.", 
                                   description="Classify a set of news articles as part of an academic research study.", 
                                   keywords="news, classification, research, academic",
                                   reward=self.hitpayment)
        self.running = True
        self.hitid = hitinfo[0].HITId
        return True
    def end_run(self):
        self.mturk_conn.expire_hit(self.hitid)
        self.running = False
        self.hitid = None
    def get_payments_to_make(self):
        if not self.hitid or not self.running:
            return []
        else:
            all_assignments = self.mturk_conn.get_assignments(self.hitid)
            return [[a.AssignmentId, a.WorkerId, a.answers[0][0].fields[0]] for a in all_assignments if a.AssignmentStatus == 'Submitted']

    def make_payments(self, assignment_ids=[]) :
        for assignmentid in assignment_ids:
            try:
                self.mturk_conn.approve_assignment(assignmentid)
            except:
                continue




def _assignment_scratchpad():
    """
    # can only call this on status==Submitted
    #        self.mturk_conn.approve_assignment(all_assignments[0].AssignmentId)
    print all_assignments[0].AssignmentStatus
    print all_assignments[0].AssignmentId
    print all_assignments[0].AutoApprovalTime
    print all_assignments[0].HITId
    print all_assignments[0].WorkerId
    print all_assignments[0].answers[0][0].fields[0]
    print dir(all_assignments[0].answers[0][0].fields)
    
    
    all_assignments = self.mturk_conn.get_assignments(self.hitid) returns
    
    list of ['AcceptTime', 'Assignment', 'AssignmentId', 'AssignmentStatus', 'AutoApprovalTime', 'HITId', 'SubmitTime', 'WorkerId']
    print all_assignments[0].AssignmentStatus
    print all_assignments[0].AssignmentId
    print all_assignments[0].AutoApprovalTime
    print all_assignments[0].HITId
    print all_assignments[0].WorkerId
    
    outputs
    
    Submitted
    2OQ5COW0LGRZ3MSYTQ365NUZ2G8Y75
    2013-09-05T17:19:19Z
    22ESBRI8IUB2Y8PFXMJTVB3L22CG4T
    A1C3R0EZ6HI9OX
    
    and we can fetch the answer (we only have one field, the secret code...) with:
    all_assignments[0].answers[0][0].fields[0]
    
    """
    
