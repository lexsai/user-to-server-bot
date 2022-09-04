# Cloner-Bot:
A discordpy rewrite bot that clones messages sent from one server and sends them into the 'nexus server'.

Update:
Four years old. Almost certainly does not work with the modern discord API, especially with discord's recent moves towards limited intents.

# Disclaimer:
This bot uses *selfbots*.

Selfbots **ARE** against discord TOS, and any action taken by the discord staff team towards your account is your responsibility.

https://support.discordapp.com/hc/en-us/articles/115002192352-Automated-user-accounts-self-bots-

# Features:
-also clones typing indicators.

-changes nickname to the member who sends the message.

-a `>show_history` command to display past messages.

-customizable embed colour.

-easy input of config files

-simple setup

------------------------------------------------------------------------------------------------------------------------------------
# Warning:

*Only perform setup in a server you don't care about- the bot will wipe all channels and generate new ones during setup.

------------------------------------------------------------------------------------------------------------------------------------

# Setup:

1) input a valid config file.

2) use `>initialize` to start instantly.

OR

2) use `>restart`, this will wipe all the channels and generate two text channels named `#control-panel` and `#help`, the latter will contain the help message (which is also invokable with `>help` or `>dm_help`)

3) use `>init_channels` to generate the channels of the chosen server into the nexus server.

4) done.
