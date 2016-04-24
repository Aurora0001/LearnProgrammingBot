# Setup
 To configure LearnProgrammingBot, you'll need to obtain an OAuth access token from reddit. This will allow LearnProgrammingBot to log in to the account that you want to automate. 
## Getting the OAuth Tokens
 To use OAuth (which reddit requires), you need **3 tokens**: the client id, the client secret and the access token.
### Getting the ID and Secret Tokens
 To create these tokens, you'll need to go to [the app preferences](https://www.reddit.com/prefs/apps/) page, while logged in as your bot account. If you don't see something like this, you may need to click 'create another app...':

 Set the **name** box to 'LearnProgrammingBot' (or a custom name, if you prefer - it isn't important).
 Select the **script** app type from the radio buttons below the textbox.
 Leave **description** and **about url** blank, and enter **http://127.0.0.1/callback** in the **redirect uri** box.
 Then, click 'create app', and you should see something like what you see in the image:
 
 ![image](https://camo.githubusercontent.com/d53f92cd85d1279a239444acee25179e8e6d8bb5/687474703a2f2f692e696d6775722e636f6d2f65326b4f5231612e706e67)

The token under '**personal use script**' is your *client ID*. The token underlined in red is your *client secret*.

Open up `settings.py` and change the following lines to your ID and secret:

    CLIENT_ID = 'my_client_id_here'
    CLIENT_SECRET = 'my_client_secret_here'
    
You can ignore any lines preceded by #.

### Getting your Access Token
LearnProgrammingBot can help you generate your access token automatically. This only needs to be done once - after this, it can be done manually.

In a terminal, run:

    ./main.py create-token
    
A web browser should open (if you are logged in as your bot account). Click 'Allow', and wait to be redirected. You will probably get something like this:

![](https://praw.readthedocs.org/en/stable/_images/CodeUrl.png)

Don't worry, this is **correct**. Copy the token after `code=` (circled in the image), and put it in `settings.py` as CLIENT_ACCESSTOKEN. **Do not include the `code=` section - this will not work!**

## Running LearnProgrammingBot

You're now ready to run LearnProgrammingBot (finally!). Use `./main.py` run in the terminal. This will run continuously until killed using `Ctrl+C` or an exception. You might find useful logging information in bot.log if the bot does crash. Feel free to report an issue if you do find a bug!