
import entity

class Generation:

    def __init__(self, name, member = [entity.Entity()]*3):
        self.member = member
        self.name = name
        self.gen_len = len(member)


    #evaluates fittness of each member and value of each type of action_name
    #returns a list that will be used by next generation when choosing new actions
    def evaluation(self):

        for x in self.member:

    #produce 3 new member for the next generation
    def reproduce(self):

        return Generation()

    #produces addition member based on the action_choice list
    #returns a new member
    def add_member(self):


    def action_choice(self):

    #decided if a action will mutate into a new action
    #returns true if it will false if it won't
    def willMutate(self):
