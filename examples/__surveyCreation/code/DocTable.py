class DocTable:
    table_head = '''<table class="table table-hover">
                    <thead>
                    <tr>
                    <th scope="col"></th>
                    <th scope="col">Researcher</th>
                    </tr>
                    </thead>
                    <tbody> '''
    table_tail = '</tbody></table>'

    def __init__(self, name, areas):
        # All inputs are type string
        self.label = '<tr><th scope="row">Name</th><td>' + name + "</td></tr>"
        self.words = '<tr><th scope="row">Research areas</th><td>' + areas + "</td></tr>"
        self.search = '<tr><th scope="row">Google Scholar search</th><td><a target="_blank" href="https://scholar.google.com/scholar?q='+name.replace(" ","+")+ ">Click here to open Google Scholar search for '+name+' in new tab</a></td></tr>"
        self.table = ""
        self.made = False

    def make_table(self):
        table_parts = [DocTable.table_head, self.label, self.words, self.search, DocTable.table_tail]
        self.table = "".join(table_parts)
        self.made = True

    def write_table(self):
        if not self.made:
            self.make_table()
        return self.table
