$currentBranch = Read-Host 'Enter current branch: '
$mergeBranch = Read-Host 'Enter the branch you want to merge: '
git checkout $mergeBranch
git pull origin $mergeBranch
git checkout $currentBranch
git merge origin $mergeBranch
git checkout $mergeBranch
git merge origin $currentBranch
git push origin $mergeBranch $currentBranch
git checkout $currentBranch
