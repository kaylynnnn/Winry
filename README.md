## Winry

A fork of [R. Danny](https://github.com/Rapptz/RoboDanny) tailored to myself.

## Running

I would prefer if you don't run an instance of my bot. Just call the join command with an invite URL to have it on your server. The source here is provided for educational purposes for discord.py.

Nevertheless, the installation steps are as follows:

1. **Make sure to get Python 3.10 or higher**

This is required to actually run the bot.

2. **Set up venv**

Just do `python3.10 -m venv venv`

3. **Activate the environment**
Windows `.\venv\Scripts\activate`
*nix `source venv/bin/activate`

4. **Install dependencies**

This is `pip install -U -r requirements.txt`

5. **Create the database in PostgreSQL**

You will need PostgreSQL 9.5 or higher and type the following
in the `psql` tool:

```sql
CREATE ROLE winry WITH LOGIN PASSWORD 'yourpw';
CREATE DATABASE winry OWNER winry;
CREATE EXTENSION pg_trgm;
```

5. **Setup configuration**

The next step is just to create a `config.py` file in the root directory where
the bot is with the following template:

```py
client_id   = '' # your bot's client ID
token = '' # your bot's token
postgresql = 'postgresql://user:password@host/database' # your postgresql info from above
stat_webhook = ('<webhook_id>','<webhook_token>') # a webhook to a channel for bot stats.
# when you generate your webhook, take the token and ID from the URL like so:
# https://discord.com/api/webhooks/<id>/<token>
```

6. **Configuration of database**

To configure the PostgreSQL database for use by the bot, go to the directory where `launcher.py` is located, and run the script by doing `python3.10 launcher.py db init`
