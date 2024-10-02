#!/bin/bash
git config --global user.email 181243999+tna-da-bot@users.noreply.github.com
git config --global user.name tna-da-bot
git checkout -b $BRANCH_NAME
git push -u origin $BRANCH_NAME
