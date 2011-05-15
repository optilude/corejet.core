"""Decorators. You would normally import these from corejet.core directly.
"""

import types

from zope.interface import alsoProvides
from corejet.core.interfaces import IStep, IScenario, IStory

def iter_step_types(cls):
    for name, func in cls.__dict__.items():
        if isinstance(func, types.FunctionType):
            step_type = getattr(func, 'step_type', None)
            step = getattr(func, 'text', None)
            if step_type is not None and step is not None:
                if step_type in ('given', 'when', 'then',):
                    yield step_type, func
                else:
                    raise ValueError("Unkown step type %s" % step_type)

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
        
        for step_type, func in iter_step_types(cls):
            if step_type == 'given':
                global_givens.append(func)
            elif step_type == 'when':
                global_whens.append(func)
            elif step_type == 'then':
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
                
                closure.func_name = 'test_%s' % name
                closure.__module__ = cls.__module__
                
                closure.scenario = scenario
                
                setattr(cls, 'test_%s' % name, closure)
                
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
        
        for step_type, func in iter_step_types(cls):
            if step_type == 'given':
                cls.givens.append(func)
            elif step_type == 'when':
                cls.whens.append(func)
            elif step_type == 'then':
                cls.thens.append(func)
        
        alsoProvides(cls, IScenario)
        
        return cls

class _step(object):
    
    step_type = None
    
    def __init__(self, step):
        self.step = step
    
    def __call__(self, method):
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
