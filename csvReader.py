import csv
import world_events
import tree

def read_events(filename):

    events = []
    #file_name
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            #event format in CSV
            #(event_type, Q_prompt, Option_prompts..., "REQ", requirements..., "EFFECTS", effects)
            o_cat = row[0]
            if o_cat == "END":
                break
            q_prompt = row[1]
            o_prompts = []
            o_requirements = []
            o_effects = []
            index = 2
            num_options = 0
            while index < 100:
                if row[index] == "REQ":
                    index += 1
                    break
                o_prompts.append(row[index])
                num_options += 1
                index += 1
            
            #TODO add types at somepoint if I want
            o_types = [0 for _ in range(num_options)]

            for i in range(index, index + num_options):
                o_requirements.append(row[i])
                index += 1

            #Error check to make sure my reader is working well
            if row[index] != "EFFECTS":
                print("Something went horribly wrong: csvReader.py ln33")

                #these print statements were for error checking
                #print(row[index - 1])
                #print(row[index + 1])
            index += 1
            for i in range(index, index + num_options):
                o_effects.append(row[i])
            
            events.append(world_events.Event(q_prompt, o_prompts, o_effects, o_types, o_requirements))
    return events

def read_upgrades(filename):
    skills = []
    #file_name
    with open(filename, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            #event format in CSV
            #(event_type, Q_prompt, Option_prompts..., "REQ", requirements..., "EFFECTS", effects)
            if row[0] == "END":
                break
            skills.append(tree.Upgrade(row))
    return skills

def CSV_test():
    filename = "database/events.csv"

    events = read_events(filename)

    for event in events:
        event.print()

#CSV_test()