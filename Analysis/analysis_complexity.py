import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


## Script for scatter plots analysing the capability threshold

# Setup data 
dataset = "..../Analysis/exp1_complexity.csv"
df = pd.read_csv(dataset)

############ 0shot #############

df_0shot = df.query('prompting_strategy == "0shot"')

##### F1 #######
# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='F1', hue='complexity_group', data=df_0shot, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="F1", data=df_0shot, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()

##### F2 #######
# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='F2', hue='complexity_group', data=df_0shot, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="F2", data=df_0shot, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()

##### F3 #######
# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='F3', hue='complexity_group', data=df_0shot, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="F3", data=df_0shot, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()

##### CS #######
# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='CS', hue='complexity_group', data=df_0shot, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="CS", data=df_0shot, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()

##### CSP #######

# Consider scores for CSP only above 0,
# as it implies none CS were generated.
df_0shot_csp = df_0shot.query('CSP > 0.0')

# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='CSP', hue='complexity_group', data=df_0shot_csp, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="CSP", data=df_0shot_csp, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()
############ END 0shot #############


############ 1shot begin #############

df_1shot = df.query('prompting_strategy == "1Shot"')

##### F1 #######
# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='F1', hue='complexity_group', data=df_1shot, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="F1", data=df_1shot, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()

##### F2 #######
# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='F2', hue='complexity_group', data=df_1shot, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="F2", data=df_1shot, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()

##### F3 #######
# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='F3', hue='complexity_group', data=df_1shot, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="F3", data=df_1shot, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()

##### CS #######
# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='CS', hue='complexity_group', data=df_1shot, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="CS", data=df_1shot, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()

##### CSP #######

# Consider scores for CSP only above 0,
# as it implies none CS were generated.
df_1shot_csp = df_1shot.query('CSP > 0.0')

# Use lmplot to plot scatter points
sns.lmplot(x='complexity', y='CSP', hue='complexity_group', data=df_1shot_csp, fit_reg=False, legend=False)
# Use regplot to plot the regression line and use line_kws to set line label for legend
ax = sns.regplot(x="complexity", y="CSP", data=df_1shot_csp, scatter_kws={"zorder":-1})
# plot legend
ax.legend()
plt.show()