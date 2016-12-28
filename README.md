# pollease
Custom Slack integration for anonymous surveys/polls


## Debugging locally using ngrok
1. Visit https://ngrok.com/download and download/install ngrok
2. Run `sh build.sh`
3. Run `sh run.sh`
4. Run `ngrok http 7000` (or whatever port is currently in run.sh)
5. Note the forwarding URL in the command output in step 4 
6. In the slack slash command integration page for pollease, change the URL to the URL from step 5
7. Incoming HTTP requests will now be displayed in the command window below your ngrok command.