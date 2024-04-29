import itertools

class Option:
    def __init__(self, o_prompt, o_effect, o_type, o_requirement):
        self.text = o_prompt
        self.effect = float(o_effect)
        self.type = o_type
        self.requirements = o_requirement

    #effect of options
    def change(self, game):
        amount = self.effect
        for item in game.tree.skills:
            curr = game.tree.skills[item] 
            if curr.present == False:
                continue
            if curr.option_type == "ALL":
                if curr.effect_type == "BONUS":
                    amount += int(curr.effect_size)
                elif curr.effect_type == "MULT":
                    amount = amount * float(curr.effect_size)


        game.believers = round(game.believers + amount)
        


class Event:
    #TODO change variable name of item to something more descriptive
    #item type [q_prompt, o_prompts, o_effects, o_types, o_requirements]
    #o_types is array of length o_prompts that describes the type of event it is
    #o_requirements is
    def __init__(self, q_prompt, o_prompts, o_effects, o_types, o_requirements):

        self.prompt = q_prompt
        
        self.x = 50
        self.y = 75
        self.width = 650
        self.height = 600

        #copy array
        self.options = []
        for (a, b, c, d) in zip(o_prompts, o_effects, o_types, o_requirements):
            self.options.append(Option(a, b, c, d))
    
    def print(self):
        print(self.prompt)
        for option in self.options:
            print(option.prompt, option.effect, option.type)
            print("end of event")

    
