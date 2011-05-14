"""Decorators. You would normally import these from corejet.core directly.
"""

import types

class scenario(object):
    """Defines a reference to a scenario with a title, used as a class
    decorator
    """
    
    def __init__(self, title):
        self.title = title
    
    def __call__(self, cls):
        cls.corejet_title = self.title
        cls.corejet_steps = steps = {}
        
        for name, func in cls.__dict__.items():
            if isinstance(func, types.FunctionType):
                step_type = getattr(func, 'corejet_step_type', None)
                step = getattr(func, 'corejet_step', None)
                if step_type is not None and step is not None:
                    steps.setdefault(step_type, []).append(func)
        
        return cls

class story(scenario):
    """Defines a reference to a story with an id and title, used as a class
    decorator
    """
    
    def __init__(self, id, title):
        super(story, self).__init__(title)
        self.id = id
    
    def __call__(self, cls):
        cls.corejet_id = self.id
        cls.corejet_scenarios = []
        
        super(story, self).__call__(cls)
        
        # Go through each scenario and turn it into a test_* method
        
        shared_steps = cls.corejet_steps
        
        for name, scenario in cls.__dict__.items():
            steps = getattr(scenario, 'corejet_steps', None)
            if steps is not None:
                
                test_given = []
                test_when  = []
                test_then  = []
                
                # Copy all shared steps as the first in the lists
                
                for func in shared_steps.get('given', []):
                    test_given.append(func)
                for func in shared_steps.get('when', []):
                    test_when.append(func)
                for func in shared_steps.get('then', []):
                    test_then.append(func)
                
                # Then all scenario-specific steps
                
                for func in steps.get('given', []):
                    test_given.append(func)
                for func in steps.get('when', []):
                    test_when.append(func)
                for func in steps.get('then', []):
                    test_then.append(func)
                
                def closure(self):
                    
                    # Hack! We work out the steps to call outside the closure,
                    # and set them as attributes on the function. We need to
                    # read those back here, so we use the test method name,
                    # which is set up by the test suite, to get back the
                    # function object representing the closure for this test
                    # case.

                    fn = getattr(self, self._testMethodName)
                    
                    # Call each of the step methods. Note ``self`` here is
                    # the *story* class, not the scenario class, which is
                    # really just a grouping mechanism and not used directly.
                    
                    for func in fn.given:
                        func(self)
                    for func in fn.when:
                        func(self)
                    for func in fn.then:
                        func(self)
                
                closure.func_name = 'test_%s' % name
                closure.__module__ = cls.__module__
                
                closure.scenario = scenario.corejet_title
                
                closure.given = test_given
                closure.when  = test_when
                closure.then  = test_then
                
                setattr(cls, 'test_%s' % name, closure)
                
                cls.corejet_scenarios.append(closure)
                
        return cls

class _step(object):
    
    step_type = None
    
    def __init__(self, step):
        self.step = step
    
    def __call__(self, method):
        method.corejet_step_type = self.step_type
        method.corejet_step = self.step
        return method

class given(_step):
    """Defines a reference to a 'given' step with step text, used as a method
    decorator
    """
    
    step_type = "given"

class when(_step):
    """Defines a reference to a 'given' step with step text, used as a method
    decorator
    """
    
    step_type = "when"

class then(_step):
    """Defines a reference to a 'given' step with step text, used as a method
    decorator
    """
    
    step_type = "then"
