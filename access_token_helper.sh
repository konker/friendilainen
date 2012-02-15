#!/bin/sh

APP_ID=`cat app_id.txt`
APP_SECRET=`cat app_secret.txt`

echo "https://www.facebook.com/dialog/oauth?client_id=$APP_ID&redirect_uri=http://a-z.fi/&scope=offline_access"
echo "Enter the code:"
read CODE

echo "https://graph.facebook.com/oauth/access_token?client_id=$APP_ID&redirect_uri=http://a-z.fi/&client_secret=$APP_SECRET&code=$CODE"

