import git
repo = git.Repo("C:\\Users\wei.wu\Desktop\CMS_data_backup")
repo.git.add(".")
print(repo.index.diff('HEAD'))
