"""Basic data model
"""

from lxml import etree

from zope.interface import implements

from corejet.core.interfaces import IRequirementsCatalogue
from corejet.core.interfaces import IEpic
from corejet.core.interfaces import IStory
from corejet.core.interfaces import IScenario
from corejet.core.interfaces import IStep

class RequirementsCatalogue(object):
    implements(IRequirementsCatalogue)
    
    def __init__(self,
        extractTime=None,
        testTime=None,
        project=None,
        epics=None,
    ):
        
        self.extractTime = extractTime
        self.testTime = testTime
        self.projcet = project
        self.epics = epics or []
    
    def populate(self, input):
        pass
    
    def write(self, output):
        pass
    
class Epic(object):
    implements(IEpic)
    
    def __init__(self, name, title, stories=None):
        self.name = name
        self.title = title
        self.stories = stories or []

class Story(object):
    implements(IStory)
    
    def __init__(self, name, title, scenarios=None,
        points=None,
        status=None,
        resolution=None,
        priority=None,
        epic=None,
    ):
        self.name = name
        self.title = title
        self.scenarios = scenarios or []
        self.points = points
        self.status = status
        self.resolution = resolution
        self.priority = priority
        self.epic = epic

class Scenario(object):
    implements(IScenario)
    
    def __init__(self, name,
        givens=None,
        whens=None,
        thens=None,
        status=None,
        story=None,
    ):
        self.name = name
        self.givens = givens or []
        self.whens = whens or []
        self.thens = thens or []
        self.status = status
        self.story = story

class Step(object):
    implements(IStep)
    
    def __init__(self, text, step_type):
        self.text = text
        self.step_type = step_type
