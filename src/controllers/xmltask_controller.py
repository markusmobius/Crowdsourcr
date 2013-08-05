import models

class XMLTaskController(object):
    @staticmethod
    def xml_upload(xml_path=None) :
        return  models.XMLTask(xml_path)

"""
        for module in xmltask.get_modules():
            CTypeController.create(module)
        all_tasks = xmltask.get_tasks()
        all_hits = xmltask.get_hits()
        all_modules = xmltask.get_modules()
        print all_tasks
        print all_hits
        print all_modules
        for task in all_tasks:
            print task
        for hit in all_hits:
            print hit
        for module in all_modules:
            print module

"""
