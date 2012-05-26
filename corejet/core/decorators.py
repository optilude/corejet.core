"""Decorators. You would normally import these from corejet.core directly.
"""

import sys
import string
import unicodedata

from zope.interface import alsoProvides
from corejet.core.interfaces import IStep, IScenario, IStory

def iter_step_type(cls, step_type):
    for func in getattr(cls, 'corejet.%s' % step_type, []):
        yield func

def normalize(s):
    """Normalizes non-ascii characters to their closest ascii counterparts
    and replaces spaces with underscores"""
    whitelist = (' ' + string.ascii_letters + string.digits)

    if type(s) == str:
        s = unicode(s, 'utf-8', 'ignore')

    table = {}
    for ch in [ch for ch in s if ch not in whitelist]:
        if ch not in table:
            try:
                replacement = unicodedata.normalize('NFKD', ch)[0]
                if replacement in whitelist:
                    table[ord(ch)] = replacement
                else:
                    table[ord(ch)] = u'_'
            except:
                table[ord(ch)] = u'_'
    return s.translate(table).replace(u'_', u'').replace(u' ', u'_')

class story(object):
    """Defines a reference to a story with an id and title, used as a class
    decorator. The class object will become a valid IStory, with all relevant
    properties set.
    """
    
    def __init__(self, id, title):
        self.id = id
        self.title = title
    
    def __call__(self, cls):
        cls.name = self.id
        cls.title = self.title
        cls.__name__ = str(normalize(self.title))
        cls.scenarios = []
        
        cls.points = None
        cls.status = None
        cls.resolution = None
        cls.priority = None
        cls.epic = None
        
        # Go through each scenario and turn it into a test_* method
        
        global_givens = []
        global_whens = []
        global_thens = []
        
        for func in iter_step_type(cls, 'given'):
            global_givens.append(func)
        for func in iter_step_type(cls, 'when'):
            global_whens.append(func)
        for func in iter_step_type(cls, 'then'):
            global_thens.append(func)
        
        for name, scenario in cls.__dict__.items():
            if IScenario.providedBy(scenario):
                
                # Prepend global given/when steps to the scenario steps
                for func in reversed(global_givens):
                    scenario.givens.insert(0, func)
                for func in reversed(global_whens):
                    scenario.whens.insert(0, func)
                
                # Append global then steps to the scenario steps
                for func in global_thens:
                    scenario.thens.append(func)
                
                scenario.story = cls
                
                def closure(self):
                    
                    # Hack! We work out the steps to call outside the closure,
                    # and set them as attributes on the function. We need to
                    # read those back here, so we use the test method name,
                    # which is set up by the test suite, to get back the
                    # function object representing the closure for this test
                    # case.

                    fn = getattr(self, self._testMethodName)
                    scenario = fn.scenario
                    
                    # Create an instance of the scenario as the 'self'
                    # argument to the function, and set the 'story'
                    # attribute
                    
                    story = self
                    try:
                        scenario = scenario(story)
                    except TypeError:
                        scenario = scenario()
                        scenario.story = story
                    
                    # Call each of the step methods. Note ``self`` here is
                    # the *scenario* class, not the story class
                    
                    for func in scenario.givens:
                        func(scenario)
                    for func in scenario.whens:
                        func(scenario)
                    for func in scenario.thens:
                        func(scenario)
                
                closure.func_name = 'test_%s' %\
                    str(normalize(scenario.name))
                closure.__module__ = cls.__module__
                
                closure.scenario = scenario
                
                setattr(cls, 'test_%s' %\
                    str(normalize(scenario.name)), closure)
                
                cls.scenarios.append(scenario)
        
        alsoProvides(cls, IStory)
        
        return cls

class scenario(object):
    """Defines a reference to a scenario with a title, used as a class
    decorator. The class object will become a valid IScenario, with all
    relevant properties set.
    """
    
    def __init__(self, title):
        self.title = title
    
    def __call__(self, cls):
        cls.name = self.title
        
        cls.givens = []
        cls.whens = []
        cls.thens = []
        
        cls.status = None
        cls.story = None
        
        for func in iter_step_type(cls, 'given'):
            cls.givens.append(func)
        for func in iter_step_type(cls, 'when'):
            cls.whens.append(func)
        for func in iter_step_type(cls, 'then'):
            cls.thens.append(func)
        
        alsoProvides(cls, IScenario)
        
        return cls

class _step(object):
    
    step_type = None
    
    def __init__(self, step):
        self.step = step
    
    def __call__(self, method):
        
        frame = sys._getframe(1)
        frame.f_locals.setdefault('corejet.' + self.step_type, []).append(method)
        
        method.step_type = self.step_type
        method.text = self.step
        
        alsoProvides(method, IStep)
        
        return method

class given(_step):
    """Defines a reference to a 'given' step with step text, used as a method
    decorator. The function object will become a valid IStep, with all
    relevant properties set.
    """
    
    step_type = "given"

class when(_step):
    """Defines a reference to a 'given' step with step text, used as a method
    decorator. The function object will become a valid IStep, with all
    relevant properties set.
    """
    
    step_type = "when"

class then(_step):
    """Defines a reference to a 'given' step with step text, used as a method
    decorator. The function object will become a valid IStep, with all
    relevant properties set.
    """
    
    step_type = "then"
