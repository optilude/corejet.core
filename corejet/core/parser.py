import os
import gettext

DOMAIN = 'gherkin'
LOCALEDIR = os.path.dirname(__file__) + '/locales'

gettext.bindtextdomain(DOMAIN, LOCALEDIR)
gettext.textdomain(DOMAIN)
_ = lambda x: x  # dummy func for translatable strings; we translate manually

import re

from corejet.core.model import Scenario, Step

class RegEx(object):

    translations = {
        'en': gettext.translation(DOMAIN, LOCALEDIR, languages=['en']),
        'fi': gettext.translation(DOMAIN, LOCALEDIR, languages=['fi']),
        }

    def __init__(self, pattern, keyword):
        self._expressions = {}
        self._pattern = pattern
        self._keyword = keyword

    def match(self, line, language='en'):
        if language not in self.translations:
            language = 'en'
        if language not in self._expressions:
            keyword = self.translations[language].gettext(self._keyword)
            pattern = self.translations[language].gettext(self._pattern)
            try:
                self._expressions[language] =\
                    re.compile(pattern.format(keyword=keyword), re.I)
            except AttributeError:
                # 'str' object has no attribute 'format' in Python < 2.6
                self._expressions[language] =\
                    re.compile(pattern.replace("{keyword}", keyword), re.I)
        return self._expressions[language].match(line)

language_regex = re.compile(r'^#\s+language:\s+(\w{0,2})\s*', re.I)
scenario_regex = RegEx(_(r'^\s*{keyword}(?: \d+)?: (.+)'), _('Scenario'))
given_regex = RegEx(_(r'^\s*{keyword} (.+)'), _('Given'))
when_regex = RegEx(_(r'^\s*{keyword} (.+)'), _('When'))
then_regex = RegEx(_(r'^\s*{keyword} (.+)'), _('Then'))
and_regex = RegEx(_(r'^\s*{keyword} (.+)'), _('And'))
but_regex = RegEx(_(r'^\s*{keyword} (.+)'), _('But'))

def appendScenarios(story, text, default_language='en'):
    """Parse the acceptance criteria in the string 'text' and append the
    relevant scenarios to the given IStory.
    """
    
    language = default_language
    scenarios = []
    scenario = None
    previousStep = None
    
    for line in text.splitlines():

        languageMatch = language_regex.match(line)
        if languageMatch:
            language = languageMatch.group(1)
        
        scenarioMatch = scenario_regex.match(line, language)
        if scenarioMatch:
            scenario = Scenario(scenarioMatch.group(1), story=story)
            previousStep = None
            scenarios.append(scenario)
            continue
        
        givenMatch = given_regex.match(line, language)
        if givenMatch:
            if previousStep:
                raise ValueError("Found %s, but previous step was %s" % (line, previousStep,))

            if scenario is None:
                story.givens.append(Step(givenMatch.group(1), previousStep))
            else:
                scenario.givens.append(Step(givenMatch.group(1), previousStep))
            previousStep = "given"
            continue
        
        whenMatch = when_regex.match(line, language)
        if whenMatch:
            if previousStep not in ('given', None):
                raise ValueError("Found %s, but previous step was %s" % (line, previousStep,))

            if scenario is None:
                story.whens.append(Step(whenMatch.group(1), previousStep))
            else:
                scenario.whens.append(Step(whenMatch.group(1), previousStep))
            previousStep = "when"
            continue
        
        thenMatch = then_regex.match(line, language)
        if thenMatch:
            if previousStep != 'when':
                raise ValueError("Found %s, but previous step was %s" % (line, previousStep,))
            
            if scenario is None:
                story.thens.append(Step(thenMatch.group(1), previousStep))
            else:
                scenario.thens.append(Step(thenMatch.group(1), previousStep))
            previousStep = "then"
            continue
        
        andMatch = and_regex.match(line, language) or but_regex.match(line, language)
        if andMatch:
            if previousStep is None:
                raise ValueError("Found %s, but no previous step found" % line)
            
            if scenario is None:
                if previousStep == "given":
                    story.givens.append(Step(andMatch.group(1), previousStep))
                elif previousStep == "when":
                    story.whens.append(Step(andMatch.group(1), previousStep))
                elif previousStep == "then":
                    story.thens.append(Step(andMatch.group(1), previousStep))
            else:
                if previousStep == "given":
                    scenario.givens.append(Step(andMatch.group(1), previousStep))
                elif previousStep == "when":
                    scenario.whens.append(Step(andMatch.group(1), previousStep))
                elif previousStep == "then":
                    scenario.thens.append(Step(andMatch.group(1), previousStep))
            continue
    
    story.scenarios.extend(scenarios)
