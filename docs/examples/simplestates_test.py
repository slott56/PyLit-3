#!/usr/bin/env python
# -*- coding: utf8 -*-

# simplestates_test.py:
# *********************
# Test the simplestates.py generic state machine
# ==============================================
#
# :Status:    draft
# :Date:      2006-12-01
# :Copyright: 2006 Guenter Milde.
#             Released under the terms of the GNU General Public License
#             (v. 2 or later)
#
# .. default-role:: literal
#
# Revised for Python3.
#
# .. contents:: :depth: 2
#
#
# Abstract State Machine Class
# ----------------------------
#
# First version of an abstract state machine
# ::

class SimpleStates1:
    """generic state machine acting on iterable data

    Class attributes
    init_state -- name of the first state_handler method
    """
    init_state = 'start'

# Initialisation
#
# * sets the data object to the `data` argument.
# * remaining keyword arguments are stored as class attributes (or methods, if
#   they are function objects) overwriting class defaults (a neat little trick
#   I found somewhere on the net)
# * the `state_handler` attribute is set to the method named in `init_state`
#
# ::

    def __init__(self, data, **keyw):
        """data   --  iterable data object
                      (list, file, generator, string, ...)
           **keyw --  all remaining keyword arguments are
                      stored as class attributes
        """
        self.data = data
        self.__dict__.update(keyw)

# The special `__iter__` method returns an iterator_. This allows to use
# a  class instance directly in an iteration loop.  We define it as is a
# generator_ method that sets the initial state and then iterates over the
# data calling the state methods::

    def __iter__(self):
        self.state_handler = getattr(self, self.init_state)
        for token in self.data:
            yield self.state_handler(token)

# To use class instances as callable objects, we add a `__call__` method::

    def __call__(self):
        """Run state-machine and return tokens as a list"""
        return [token for token in self]

# Example 1: A two-state machine sorting numbers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Our small example state machine subclasses the `SimpleStates1` class::

class Example1(SimpleStates1):
    """A silly example two-state machine sorting numbers
    in the categories "low" (< 3) and "high" (>= 3).
    """

# It will be completed by two state methods and a `__str__` method.
#
# State Methods
# """""""""""""
#
# State methods are functions that are called to iterate over the data. They
# will typically
#
# * test the data token for a change of state indicator
# * return the data token after some processing
#
# In our example, the `low` method switches to `high` (and calls it with the
# data token), if token is bigger than 3. If not, it returns "l(token)"::

    def low(self, token):
        # print( "low(", token, ")", end=' ' )
        if token > 3:
            self.state_handler = self.high
            # backtracking
            return self.state_handler(token)
        return "l(%d)"%token

# The `high` method switches to `low`, if token is bigger than 3. If not, it
# returns "h(token)"::

    def high(self, token):
        # print( "high(", token, ")", end= ' ' )
        if token <= 3:
            self.state_handler = self.low
            # backtracking
            return self.state_handler(token)
        return "h(%d)"%token

# Conversion of the class instance to a string is done by joining the list
# that is returned by a call to the instance with spaces::

    def __str__(self):
        return " ".join(self())

# Test
# """"
#
# Testing is done with the nose_ test framework. This will collect and
# execute all test functions and methods (basically everything that starts or
# ends with "[Tt]est"). This is similar to the more known "py.test".
#
# .. _nose: http://somethingaboutorange.com/mrl/projects/nose/
#
# We set up some test data::

testdata = [1, 2, 3, 4, 5, 4, 3, 2, 1]

# and define a test function::

def test_Example1():
    statemachine = Example1(testdata, init_state='low')
    for result in statemachine:
        print( result, end=' ' )
    print()

    # Calling an instance should return a list of results
    print( statemachine() )
    assert statemachine() == ['l(1)','l(2)','l(3)',  # low numbers
                             'h(4)','h(5)','h(4)',  # high numbers
                             'l(3)','l(2)','l(1)']  # low again

    # Converting to a string should call the __str__ method::
    print( str(statemachine) )
    assert str(statemachine) == "l(1) l(2) l(3) h(4) h(5) h(4) l(3) l(2) l(1)"

# Discussion
# """"""""""
#
# The sorting works as expected. However, as the state handlers get the data
# token by token, acting on subsequent tokens or tests that combine the
# knowledge of several tokens are hard to achieve.
#
# An example would be a state handler that sums up the data tokens and
# returns the result if it exceeds a threshold.
#
#
#
# Varied State Machine Class Template
# -----------------------------------
#
# The second version of an abstract state machine converts the test data to an
# iterator which is shared by the state methods.
#
# There is no need to pass this on via arguments, as class methods share the
# class instances attributes (class variables).
#
# We subclass our first version and modify to our needs::

class SimpleStates2(SimpleStates1):
    """second version of the abstract state machine class
    """

# We add the initialisation of the data to the `__iter__` method. The data is
# transformed into an iterator_ first. ::

    def __iter__(self):
        self.data_iterator = iter(self.data)
        self.state_handler = getattr(self, self.init_state)
        # do not pass data tokens as argument
        # (state methods should call next(self.data_iterator) instead)
        while True:
            yield self.state_handler()

# Iterators "use up" the data, so the state methods will always get a "new"
# token until the data is fully "used up" and `StopIteration` is raised
# aborting the iteration.
#
# Doing the conversion from iterable to iterator in `__iter__` and not in
# `__init__` allows repeated iteration over the class instance (if the data is
# a list or a file and not already a generator) as the "used up" generator is
# replaced by a new one.
#
# Example 2: Another two-state machine sorting numbers
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Our small example state machine subclasses the `SimpleStates2` class
# and adds 2 methods as state handlers. ::

class Example2(SimpleStates2):
    """An example two-state machine sorting numbers
    in the categories "low" (< 3) and "high" (>= 3).
    """

# State methods
# """""""""""""
#
# This time, the state methods will get the data tokens not as argument but
# take them from the `data_iterator`. Note that *backtracking* is impossible
# with a standard iterator. See below for the problem this causes for our
# sorting algorithm. ::

    def low(self):
        # print( "low(", token, ")", end= ' ' )
        token = next(self.data_iterator)
        if token > 3:
            self.state_handler = self.high
        return "l(%d)"%token
    def high(self):
        # print( "high(", token, ")", end= ' ' )
        token = next(self.data_iterator)
        if token <= 3:
            self.state_handler = self.low
        return "h(%d)"%token

# Test
# """"
#
# Define a second test function::

def test_Example2():
    statemachine = Example2(testdata, init_state='low')

# Calling an instance should return a list of results. However, as
# we cannot backtrack on a normal iterator, the result is not as we expected:
# There is a "hysteresis" the "switch triggering" token is always processed by
# the "old" state::

    print( statemachine() )
    assert statemachine() == ['l(1)', 'l(2)', 'l(3)', # low numbers
                             'l(4)', 'h(5)', 'h(4)', # high numbers
                             'h(3)', 'l(2)', 'l(1)'] # low numbers

# Discussion
# """"""""""
#
# Missing backtracks break our number sorting machine. The remedy
# is the use of an iterator with an appendleft() method (known from the
# dqueue() standard class). We will come to this in `Example 4`__
#
# __ `Example 4: A two-state machine with generators and backtracking`_
#
# OTOH, as the state methods do the fetching of data tokens themself, a state
# handler that sums up the data tokens and returns the result if it exceeds a
# threshold would be easy to implement. We will do this in our next example
# using state handler generators.
#
#
# State Machine class using state_handler generators
# --------------------------------------------------
#
# The variations in `StateMachine2` complicate the StateMachine design. They
# makes sense, however, if we use generated iterators to handle the states.
# No changes are needed to the abstract base class, so that Example 3 can
# build on `StateMachine2`::

class Example3(SimpleStates2):

# Example 3: A two-state machine with state handler generators
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# State Generators
# """"""""""""""""
#
# State Generators generate and return an iterator that will handle the next
# data token(s) if its .__next__() method is called. This is easily achieved with a
# for loop over self.data and the `yield` keyword.
# ::

    def high_handler_generator(self):
        """Return an iterator, whose next() method
        returns "h(token)" and switches to `low`, if token > 3
        """
        for token in self.data_iterator:
            if token <= 3:
                self.state_handler = self.low
            yield "h(%d)"%token
    #
    def low_handler_generator(self):
        """Return an iterator, whose next() method sums up data tokens.
        If the sum exceeds 8, it is returned and the state
        switches to `high`.
        """
        sum = 0
        for token in self.data_iterator:
            sum += token
            if sum > 8:
                self.state_handler = self.high
                yield "s=%d"%sum
                sum = 0 # next iteration continues here
        # no more tokens but sum not reached
        yield "p=%d"%sum # partial sum

# The iterator must instantiate the state-iterators before starting the
# iteration loop::

    def __iter__(self):
        """Generate and return an iterator

        * convert `data` to an iterator
        * convert the state generators into iterators
        * (re) set the state_handler attribute to the init-state
        * pass control to the active states state_handler
          which should call and process next(self.data_iterator)
        """
        self.data_iterator = iter(self.data)
        self.high = self.high_handler_generator().__next__
        self.low = self.low_handler_generator().__next__
        # init state
        self.state_handler = getattr(self, self.init_state)
        # now start the iteration, aborts if data is empty
        while True:
            yield self.state_handler()

# Test
# """"
#
# Again define a test function that gets an instance of the Example3 class ::

def test_Example3():
    statemachine = Example3(testdata, init_state='low')

# Calling statemachine() should iterate over the test data and return the
# processed values as list::

    print( statemachine() )
    assert statemachine() == ['s=10','h(5)','h(4)','h(3)', 'p=3']

# Backtracking
# ------------
#
# the iterqueue module provides an "extensible" iterator with, e.g.,
# an `appendleft` method to push back values::

from iterqueue import XIter

# Thus we can prepend a non-processed data item
# to the data iterator for use by the next state handler
#
# Example 4: A two-state machine with generators and backtracking
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Again we start from the `SimpleStates2` base class::

class Example4(SimpleStates2):
    """two-state machine with generators and backtracking
    """

# Let the iterator wrap the data in an XIter instance with `appendleft`
# method::

    def __iter__(self):
        """Generate and return an iterator

        * convert `data` to an iterator queue
        * convert the state generators into iterators
        * (re) set the state_handler attribute to the init-state
        * pass control to the active states state_handler
          which should call and process next(self.data_iterator)
        """
        self.data_iterator = XIter(self.data) # queue with `appendleft` method
        self.high = self.high_handler_generator().__next__
        self.low = self.low_handler_generator().__next__
        self.state_handler = getattr(self, self.init_state)
        # now start the iteration
        while True:
            yield self.state_handler()

# Add state method generators that use the "backtracking" feature::

    def high_handler_generator(self):
        """Return an iterator, whose next() method
        returns "h(token)" and switches to `low`, if token > 3
        """
        for token in self.data_iterator:
            # print( "high got", token )
            if token <= 3:
                # push back data token
                self.data_iterator.appendleft(token)
                # set the new state
                self.state_handler = self.low
                # return non-value indicating the state switch
                yield None
            else:
                yield "h(%d)"%token
    #
    def low_handler_generator(self):
        """Return an iterator, whose next() method
        returns "l(token)" and switches to `high`, if token <=3
        """
        for token in self.data_iterator:
            # print( "low got", token )
            if token > 3:
                self.data_iterator.appendleft(token) # push back
                # set and run the new state
                self.state_handler = self.high
                # alternatively, return the token processed by the new
                # state handler
                yield self.state_handler()
            else:
                yield "l(%d)"%token

# The `__str__` converter should ignore the switch-indicator::

    def __str__(self):
        tokens = [token for token in self() if token != None]
        return " ".join(tokens)

# Test
# """"
#
# Again define a test function. This time with an instance of the Example4
# class ::

def test_Example4():
    statemachine = Example4(testdata, init_state='low')

# Calling statemachine() should iterate over the test data and return the
# processed values as list. If the state of the machine changes, the special
# "non-value" `None` is returned. ::

    print( statemachine() ) # only printed if something goes wrong
    assert statemachine() == ['l(1)', 'l(2)', 'l(3)',
                             'h(4)', 'h(5)', 'h(4)', None, # switch indicator
                             'l(3)', 'l(2)', 'l(1)']

# Converting to a string should skip the `None` values::

    print( statemachine )
    assert str(statemachine) == "l(1) l(2) l(3) h(4) h(5) h(4) l(3) l(2) l(1)"

# Discussion
# """"""""""
#
# The `XIter` class allows backtracking also in a state machine with state
# handlers acting on a common iterator object. The "high" and "low" handlers
# demonstrate two possible actions for the state-transition with backtrack:
# Either call the new state handler from the current one
# (like the `low_handler_generator`) or return a "non-value" that signifies
# that processing the data token did not produce any output data.
#
# Using generators made the state handlers shorter and (once the concept of a
# generator is clear) easier. Further advantages of the generator concept are
#
# * internal variables are easily saved over subsequent invocations
# * no function-call overhead (not relevant in this example but maybe for a
#   state machine that has to process long data lists.
#
#
# Converting all state method generators with a generic function
# --------------------------------------------------------------
#
# In `Example4`, we had to redefine the `__iter__` method to convert the
# method state generators into iterators. It would be nice if this could be
# done in the base class.
#
# `SimpleStates3` adds a generic function for this task that relies on a
# simple naming convention: functions whose name matches
# `<state>_handler_generator` should be converted to iterators and their
# `.__next__()` method stored as `<state>`.
# ::

class SimpleStates5(SimpleStates2):
    """generic state machine acting on iterable data
    """
    def _initialize_state_generators(self):
        """Generic function to initialise state handlers from generators

        functions whose name matches `[^_]<state>_handler_generator` should
        be converted to iterators and their `.__next__()` method stored as
        `<state>`.
        """
        suffix = "_handler_generator"
        shg_names = [name for name in dir(self)
                      if name.endswith(suffix)
                      and not name.startswith("_")]
        for name in shg_names:
            shg = getattr(self, name)
            print( shg )
            setattr(self, name[:-len(suffix)], shg().__next__)


    def __iter__(self):
        """Generate and return an iterator

        * convert `data` to an iterator queue
        * convert the state generators into iterators
        * (re) set the state_handler attribute to the init-state
        * pass control to the active states state_handler
          which should call and process next(self.data_iterator.next)
        """
        self.data_iterator = XIter(self.data) # queue with `appendleft` method
        self._initialize_state_generators()
        self.state_handler = getattr(self, self.init_state)
        # now start the iteration
        while True:
            yield self.state_handler()

# Example 5
# ~~~~~~~~~
#
# The next example combines the state handlers from Example 4 and the new
# class.::

class Example5(Example4, SimpleStates5):
    """one more example"""
    pass

# Test
# """"
#
# A function that has the generator-suffix but is prefixed with an underscore,
# should be skipped by the `_initialize_state_generators` method::

class Test_SimpleStates5:
    E5 = Example5(testdata)
    E5._bogus_handler_generator = "low"
    def test_initialize_state_generators(self):
        self.E5._initialize_state_generators()

# A test function. This time with an instance of the Example5 class ::

def test_Example5():
    statemachine = Example5(testdata, init_state='low')
    print( statemachine.__dict__ )

# Calling statemachine() should iterate over the test data and return the
# processed values as list. If the state of the machine changes, the special
# "non-value" `None` is returned. ::

    print( statemachine() ) # only printed if something goes wrong
    assert statemachine() == ['l(1)', 'l(2)', 'l(3)',
                             'h(4)', 'h(5)', 'h(4)', None, # switch indicator
                             'l(3)', 'l(2)', 'l(1)']

# Converting to a string should skip the `None` values::

    print( statemachine )
    assert str(statemachine) == "l(1) l(2) l(3) h(4) h(5) h(4) l(3) l(2) l(1)"

# Putting it together
# -------------------
#
# The file `simplestates.py` contains the full definition of the `SimpleStates5`
# class in a self-contained version.
#
# Example 6
# ~~~~~~~~~
#
# The final Example is used to test whether we have put it together well. It
# subclasses SimpleStates and adds state method generators for "high" and
# "low"::

import simplestates
class Example6(simplestates.SimpleStates):
    """two-state machine with generators and backtracking
    """
    def high_handler_generator(self):
        """Return an iterator, whose next() method
        returns "h(token)" and switches to `low`, if token > 3
        """
        for token in self.data_iterator:
            # print( "high got", token )
            if token <= 3:
                # push back data token
                self.data_iterator.appendleft(token)
                # set the new state
                self.state_handler = self.low
                # return the token processed by the new state handler
                yield self.state_handler()
            else:
                yield "h(%d)"%token
    #
    def low_handler_generator(self):
        """Return an iterator, whose next() method
        returns "l(token)" and switches to `high`, if token <=3
        """
        for token in self.data_iterator:
            # print( "low got", token )
            if token > 3:
                self.data_iterator.appendleft(token) # push back
                # set and run the new state
                self.state_handler = self.high
                # return the token processed by the new state handler
                yield self.state_handler()
            else:
                yield "l(%d)"%token

# Test
# """"
#
# In order not to make it dependent on the iterqueue module, the final
# `SimpleStates` does not wrap the data in an XIter instance. This step should
# be done at the instantiation of a state machine. ::

def test_Example5():
    statemachine = Example5(XIter(testdata), init_state='low')
    print( statemachine.__dict__ )

# Calling statemachine() should iterate over the test data and return the
# processed values as list::

    print( statemachine() ) # only printed if something goes wrong
    # reset the data iterator as it is "used up" now
    statemachine.data = XIter(testdata)
    assert statemachine() == ['l(1)', 'l(2)', 'l(3)',
                             'h(4)', 'h(5)', 'h(4)', None,
                             'l(3)', 'l(2)', 'l(1)']

# Index
# -----
#
#
# :_`generator`: A function with a `yield` keyword. Calling this function will
#                return an iterator_
#
# :_`iterator`: An object with a `next()` method. Calling `next(<iterator>)`
#               will (typically) return one data token (list element, line in
#               a file, ...). If there is no more data the `StopIteration`
#               exception is raised.
#
# Command line usage
# ------------------
#
# running this script should explore it in the "nose" test framework::

if __name__ == "__main__":
    import nose, doctest
    # first run any doctests
    doctest.testmod()
    # then run nose on this module
    nose.runmodule() # requires nose 0.9.1
