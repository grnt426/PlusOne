PlusOne
========

A bot for Slack that tracks a user's +1s, tallies votes for things, and more coming soon!

Using in Slack
===============

Giving a User +1
-----------------

Internet points are meant to be ruthlessly earned, and hoarded to purchase Teslas, ice-cream, and Reddit Gold.
Giving a user a +1 gives them a single Internet point, but without taking away any of yours. Give generously, but with
purpose and no regrets.

To give a user a +1, simply use ++firstname

	++grant
	
Creating Ballots (Votes)
---------------

Ever need to settle an Internet debate, and your whole intelligence can't fit in the text box, use the power
of mob rule^H^H^H^H^H^H^H^HDemocracy to resolve all issues.

To start a vote, you must specify the Title (surrounded by pipes of Democratic freedom), the number of freedom votes
to conclude the vote (quorum), and optionally what options users may vote on (feature not yet supported). By default,
the options are "yea" and "nay".

	callvote |Should more things be decided by the majority| 7
	> Vote for 'Should more things be decided by the majority' has started! 7 votes are needed for quorum. 'makevote 12 [yea | nay]' to vote.
	
To place your vote, simply specify the ballot ID, returned when the ballot is confirmed created, and your option.

	makevote 12 yea
	
The vote will automatically close once quorum is reached, and will prevent users from doubly-casting votes.


Running the Server
-------------------

The tokens.auth file is expected to have a single line, which is the RTM API token for a user, generally the
bot which will listen and respond back to the chat.

	cat tokens.auth > python plusone.py