import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## Script for box plots analysing the performance distributions
## on the LLM-based approach following both Zero-Shot and One-Shot prompting.

# Setup data
dataset = ".../Analysis/exp1_analysis_0shot_1shot.csv"
df = pd.read_csv(dataset)

# Consider scores for CSP only above 0,
# as it implies none CS were generated.
df_csp = df.query('CSP > 0.0')

## Prepare all relevant data frames:

# Zero-Shot
df_prompt_zero = df[df["Prompting_Strategy"]=="0shot"]
df_prompt_zero_csp = df_prompt_zero.query('CSP > 0.0')

# One-Shot
df_prompt_one = df[df["Prompting_Strategy"]=="1shot"]
df_prompt_one_csp = df_prompt_one.query('CSP > 0.0')

# Complexity for Zero-Shot
df_complexity_zero = df[df["Prompting_Strategy"]=="0shot"]
df_complexity_zero_csp = df_complexity_zero.query('CSP > 0.0')

# Complexity for One-Shot
df_complexity_one = df[df["Prompting_Strategy"]=="1shot"]
df_complexity_one_csp = df_complexity_one.query('CSP > 0.0')


## Construct box plots:

# 0shot vs. 1shot
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df, x="Prompting_Strategy", y="F1", ax=axs[0])
sns.boxplot(data=df, x="Prompting_Strategy", y="F2", ax=axs[1])
sns.boxplot(data=df, x="Prompting_Strategy", y="F3", ax=axs[2])
sns.boxplot(data=df, x="Prompting_Strategy", y="CS", ax=axs[3])
sns.boxplot(data=df_csp, x="Prompting_Strategy", y="CSP", ax=axs[4])
plt.show()

# prompt differences
# 0shot:
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_prompt_zero, x="Prompt_Template", y="F1", ax=axs[0])
sns.boxplot(data=df_prompt_zero, x="Prompt_Template", y="F2", ax=axs[1])
sns.boxplot(data=df_prompt_zero, x="Prompt_Template", y="F3", ax=axs[2])
sns.boxplot(data=df_prompt_zero, x="Prompt_Template", y="CS", ax=axs[3])
sns.boxplot(data=df_prompt_zero_csp, x="Prompt_Template", y="CSP", ax=axs[4])
plt.show()

# 1shot:
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_prompt_one, x="Prompt_Template", y="F1", ax=axs[0])
sns.boxplot(data=df_prompt_one, x="Prompt_Template", y="F2", ax=axs[1])
sns.boxplot(data=df_prompt_one, x="Prompt_Template", y="F3", ax=axs[2])
sns.boxplot(data=df_prompt_one, x="Prompt_Template", y="CS", ax=axs[3])
sns.boxplot(data=df_prompt_one_csp, x="Prompt_Template", y="CSP", ax=axs[4])
plt.show()

# complexity differences
# 0shot:
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_complexity_zero, x="Complexity_Level", y="F1", ax=axs[0])
sns.boxplot(data=df_complexity_zero, x="Complexity_Level", y="F2", ax=axs[1])
sns.boxplot(data=df_complexity_zero, x="Complexity_Level", y="F3", ax=axs[2])
sns.boxplot(data=df_complexity_zero, x="Complexity_Level", y="CS", ax=axs[3])
sns.boxplot(data=df_complexity_zero_csp, x="Complexity_Level", y="CSP", ax=axs[4])
plt.show()

#1shot
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_complexity_one, x="Complexity_Level", y="F1", ax=axs[0])
sns.boxplot(data=df_complexity_one, x="Complexity_Level", y="F2", ax=axs[1])
sns.boxplot(data=df_complexity_one, x="Complexity_Level", y="F3", ax=axs[2])
sns.boxplot(data=df_complexity_one, x="Complexity_Level", y="CS", ax=axs[3])
sns.boxplot(data=df_complexity_one_csp, x="Complexity_Level", y="CSP", ax=axs[4])
plt.show()

