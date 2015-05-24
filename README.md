PlusOne
========

A bot for Slack that tracks a user's +1s, tallies votes for things, and more coming soon!

Using in Slack
---------------

To give a user a +1, simply use ++firstname

	++grant

Running
--------

The tokens.auth file is expected to have a single line, which is the RTM API token for a user.

	cat tokens.auth > python plusone.py