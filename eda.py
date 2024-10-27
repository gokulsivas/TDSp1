import pandas as pd
from ydata_profiling import ProfileReport

df_users = pd.read_csv('users.csv')
profile_user = ProfileReport(df_users, title="Users Profiling Report") 
df_repositories = pd.read_csv('repositories.csv')
profile_repositories = ProfileReport(df_repositories, title="Repositories Profiling Report")

profile_user.to_file("report_users.html")
profile_repositories.to_file("report_repositories.html")



