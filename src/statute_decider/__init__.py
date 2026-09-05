"""statute-decider v2: a five-level decision graph (source -> term -> premise -> outcome -> trace).

Three symmetric chains (statute, user, register) meet in ``premise_outcome``;
every node is independently checkable against oracle data. See README.md and
docs/architecture-plan.md.
"""

__version__ = "2.0.0"
