#!/bin/bash
#git config --global user.email "${{ steps.import-gpg.outputs.email }}"
#git config --global user.name "${{ steps.import-gpg.outputs.name }}"
git checkout -b $BRANCH_NAME
git push -u origin $BRANCH_NAME
