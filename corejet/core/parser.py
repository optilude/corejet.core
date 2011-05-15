import re

from corejet.core.model import Scenario, Step

scenario_regex = re.compile(r'^\s*Scenario(?: \d+)?: (.+)', re.I)
given_regex = re.compile(r'^\s*Given (.+)', re.I)
when_regex = re.compile(r'^\s*When (.+)', re.I)
then_regex = re.compile(r'^\s*Then (.+)', re.I)
and_regex = re.compile(r'^\s*And (.+)', re.I)

def appendScenarios(story, text):
    """Parse the acceptance criteria in the string 'text' and append the
    relevant scenarios to the given IStory.
    """
    
    scenarios = []
    scenario = None
    previousStep = None
    
    for line in text.splitlines():
        
        scenarioMatch = scenario_regex.match(line)
        if scenarioMatch:
            scenario = Scenario(scenarioMatch.group(1), story=story)
            previousStep = None
            scenarios.append(scenario)
            continue
        
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
        
        andMatch = and_regex.match(line)
        if andMatch:
            if scenario is None:
                raise ValueError("Found %s outside a scenario" % line)
            if previousStep is None:
                raise ValueError("Found %s, but no previous step found" % line)
            
            if previousStep == "given":
                scenario.givens.append(Step(andMatch.group(1), previousStep))
            elif previousStep == "given":
                scenario.whens.append(Step(andMatch.group(1), previousStep))
            elif previousStep == "then":
                scenario.thens.append(Step(andMatch.group(1), previousStep))
            
            continue
    
    story.scenarios.extend(scenarios)