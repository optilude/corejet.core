import re

from corejet.core.model import Scenario, Step

background_regex = re.compile(r'^\s*Background(?: \d+)?:', re.I)
scenario_regex = re.compile(r'^\s*Scenario(?: \d+)?: (.+)', re.I)
given_regex = re.compile(r'^\s*Given (.+)', re.I)
when_regex = re.compile(r'^\s*When (.+)', re.I)
then_regex = re.compile(r'^\s*Then (.+)', re.I)
and_regex = re.compile(r'^\s*And (.+)', re.I)
but_regex = re.compile(r'^\s*But (.+)', re.I)

def setBackground(story, text):
    """Parse the acceptance criteria in the string 'text' and set the
    relevant background to the given IStory.
    """

    backgroundGivens = None
    previousStep = None

    for line in text.splitlines():

        scenarioMatch = scenario_regex.match(line)
        if scenarioMatch:
            # background should be described first,
            # break when the first scenario is found
            break

        backgroundMatch = background_regex.match(line)
        if backgroundMatch:
            backgroundGivens = []
            previousStep = None
            continue

        givenMatch = given_regex.match(line)
        if givenMatch:
            if backgroundGivens is None:
                raise ValueError("Found %s outside a background" % line)
            if previousStep:
                raise ValueError("Found %s, but previous step was %s" % (line, previousStep,))

            previousStep = "given"
            backgroundGivens.append(Step(givenMatch.group(1), previousStep))
            continue

        andMatch = and_regex.match(line) or but_regex.match(line)
        if andMatch:
            if backgroundGivens is None:
                raise ValueError("Found %s outside a background" % line)
            if previousStep is None:
                raise ValueError("Found %s, but no previous step found" % line)

            backgroundGivens.append(Step(andMatch.group(1), previousStep))

    if backgroundGivens:
        story.givens.extend(backgroundGivens)

def appendScenarios(story, text):
    """Parse the acceptance criteria in the string 'text' and append the
    relevant scenarios to the given IStory.
    """
    
    scenarios = []
    scenario = None
    previousStep = None
    withinBackground = True
    
    for line in text.splitlines():
        
        scenarioMatch = scenario_regex.match(line)
        if scenarioMatch:
            scenario = Scenario(scenarioMatch.group(1), story=story)
            previousStep = None
            scenarios.append(scenario)
            continue

        backgroundMatch = background_regex.match(line)
        if backgroundMatch:
            scenario = None
            withinBackground = True
            continue
        elif withinBackground and not scenario:
            continue
        else:
            withinBackground = False
        
        givenMatch = given_regex.match(line)
        if givenMatch:
            if scenario is None:
                raise ValueError("Found %s outside a scenario" % line)
            if previousStep:
                raise ValueError("Found %s, but previous step was %s" % (line, previousStep,))
            
            previousStep = "given"
            scenario.givens.append(Step(givenMatch.group(1), previousStep))
            continue
        
        whenMatch = when_regex.match(line)
        if whenMatch:
            if scenario is None:
                raise ValueError("Found %s outside a scenario" % line)
            if previousStep not in ('given', None):
                raise ValueError("Found %s, but previous step was %s" % (line, previousStep,))
            
            previousStep = "when"
            scenario.whens.append(Step(whenMatch.group(1), previousStep))
            continue
        
        thenMatch = then_regex.match(line)
        if thenMatch:
            if scenario is None:
                raise ValueError("Found %s outside a scenario" % line)
            if previousStep != 'when':
                raise ValueError("Found %s, but previous step was %s" % (line, previousStep,))
            
            previousStep = "then"
            scenario.thens.append(Step(thenMatch.group(1), previousStep))
            continue
        
        andMatch = and_regex.match(line) or but_regex.match(line)
        if andMatch:
            if scenario is None:
                raise ValueError("Found %s outside a scenario" % line)
            if previousStep is None:
                raise ValueError("Found %s, but no previous step found" % line)
            
            if previousStep == "given":
                scenario.givens.append(Step(andMatch.group(1), previousStep))
            elif previousStep == "when":
                scenario.whens.append(Step(andMatch.group(1), previousStep))
            elif previousStep == "then":
                scenario.thens.append(Step(andMatch.group(1), previousStep))
            
            continue
    
    story.scenarios.extend(scenarios)
