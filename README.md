# pollease
**Custom Slack integration for anonymous surveys/polls**

pollease: _What is my purpose?_

slack: _You create polls_

pollease: _Oh my god_

slack: _Yeah, welcome to the club, pal_

## Adding pollease to slack and debugging locally
1. Visit https://ngrok.com/download and download/install ngrok
2. Run `ngrok http 7000` (or whatever port is currently in run.sh)
3. Note the HTTPS forwarding URL in the command output in step 4 
4. Visit https://api.slack.com/apps?new_app=1
5. Use pollease as the name of the app, and select your team. (leave "I plan to submit this app to the Slack App Directory" unchecked for now.)
6. Under "OAuth & Permissions", paste the url from step 5. Append "/authorize" to the url.
7. Under "Interactive Messages", paste the url from step 5. Append "/interactive" to the url.
8. Under "Slash Commands", add "/pollease". Paste the url from step 5. Append "/create" to the url.
9. Under "Basic Information", note the Client ID and Client Secret. Paste those into the config_local.py configuration file. 
10. Run `sh build.sh`
11. Run `sh run.sh`
12. Open add-to-slack.html in a broswer and click the button. 
13. If everything goes correctly, the app should now be added to your team and the /pollease command should be functional. All HTTP requests will now be tunnelled to your localhost.