#!/bin/bash
commit_msg=$1
if [[ -z $commit_msg ]];then
    echo "please input commit message"
    exit 1
fi
git log > /dev/null
if [[ $? -ne 0 ]];then
    echo "Current path is not a repo path"
    exit 1
fi
find . -name "*.pyc"  | xargs rm -f
find . -name ".idea" | xargs rm -rf
git_host=`git config remote.origin.url | awk -F '/' '{print $3}'`
branch=`git symbolic-ref HEAD 2>/dev/null | cut -d"/" -f 3`
git diff
echo "***********************"
echo -n "git push? (yes/no):"
read confirm
echo "***********************"
if [[ $confirm  != "yes" ]];then
    echo "quit"
    exit 2
fi
echo "pushed"
if [[ $git_host == "github.com" ]];then
    git config user.name taomercy
    git config user.email taomercy@qq.com
    git add -A
    git commit -m "$commit_msg"
    git push
else
    git add -A
    git commit -m "$commit_msg"
    git push origin HEAD:refs/for/$branch
fi
