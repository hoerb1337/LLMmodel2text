import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## Script for box plots analysing the performance distributions
## on the RALLM-based approach countering sensitivity on in-context examples.

# Setup data
dataset = ".../Analysis/exp2_analysis_1shot.csv" # path needs to be adapted
df = pd.read_csv(dataset)

# Consider scores for CSP only above 0,
# as it implies none CS were generated.
df_csp = df.query('CSP > 0.0')

# box plot for stability? LLM vs. RALLM indepedent of rounds for LLM
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df, x="Approach", y="F1", ax=axs[0])
sns.boxplot(data=df, x="Approach", y="F2", ax=axs[1])
sns.boxplot(data=df, x="Approach", y="F3", ax=axs[2])
sns.boxplot(data=df, x="Approach", y="CS", ax=axs[3])
sns.boxplot(data=df_csp, x="Approach", y="CSP", ax=axs[4])
plt.show()

# box plot for stability? LLM only rounds 3 and 4 vs. RALLM
df_LLM_rounds3_4 = df.query('Approach_Nr_examples != "LLM"')
df_LLM_rounds3_4_csp = df_LLM_rounds3_4.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_LLM_rounds3_4, x="Approach", y="F1", ax=axs[0])
sns.boxplot(data=df_LLM_rounds3_4, x="Approach", y="F2", ax=axs[1])
sns.boxplot(data=df_LLM_rounds3_4, x="Approach", y="F3", ax=axs[2])
sns.boxplot(data=df_LLM_rounds3_4, x="Approach", y="CS", ax=axs[3])
sns.boxplot(data=df_LLM_rounds3_4_csp, x="Approach", y="CSP", ax=axs[4])
plt.show()

# RALLM only variance within rounds
df_RALLM = df[df["Approach"]=="RALLM"]
df_RALLM_csp = df_RALLM.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_RALLM, x="Round", y="F1", ax=axs[0])
sns.boxplot(data=df_RALLM, x="Round", y="F2", ax=axs[1])
sns.boxplot(data=df_RALLM, x="Round", y="F3", ax=axs[2])
sns.boxplot(data=df_RALLM, x="Round", y="CS", ax=axs[3])
sns.boxplot(data=df_RALLM_csp, x="Round", y="CSP", ax=axs[4])
plt.show()

# rounds aggregated
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_RALLM, x="Rounds_Aggregated", y="F1", ax=axs[0])
sns.boxplot(data=df_RALLM, x="Rounds_Aggregated", y="F2", ax=axs[1])
sns.boxplot(data=df_RALLM, x="Rounds_Aggregated", y="F3", ax=axs[2])
sns.boxplot(data=df_RALLM, x="Rounds_Aggregated", y="CS", ax=axs[3])
sns.boxplot(data=df_RALLM_csp, x="Rounds_Aggregated", y="CSP", ax=axs[4])
plt.show()

# box plot complexity for LLM vs. RALLM
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df, x="Approach_Complexity", y="F1", ax=axs[0])
sns.boxplot(data=df, x="Approach_Complexity", y="F2", ax=axs[1])
sns.boxplot(data=df, x="Approach_Complexity", y="F3", ax=axs[2])
sns.boxplot(data=df, x="Approach_Complexity", y="CS", ax=axs[3])
sns.boxplot(data=df_csp, x="Approach_Complexity", y="CSP", ax=axs[4])
plt.show()

# box plot complexity for RALLM
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_RALLM, x="Model_Complexity", y="F1", ax=axs[0])
sns.boxplot(data=df_RALLM, x="Model_Complexity", y="F2", ax=axs[1])
sns.boxplot(data=df_RALLM, x="Model_Complexity", y="F3", ax=axs[2])
sns.boxplot(data=df_RALLM, x="Model_Complexity", y="CS", ax=axs[3])
sns.boxplot(data=df_RALLM_csp, x="Model_Complexity", y="CSP", ax=axs[4])
plt.show()

# box plot medium + high complexity for RALLM vs. LLM
df_diff_complex = df[df["Model_Complexity"]!="low"]
df_diff_complex_csp = df_diff_complex.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_diff_complex, x="Approach", y="F1", ax=axs[0])
sns.boxplot(data=df_diff_complex, x="Approach", y="F2", ax=axs[1])
sns.boxplot(data=df_diff_complex, x="Approach", y="F3", ax=axs[2])
sns.boxplot(data=df_diff_complex, x="Approach", y="CS", ax=axs[3])
sns.boxplot(data=df_diff_complex_csp, x="Approach", y="CSP", ax=axs[4])
plt.show()


# box plot medium + high complexity for RALLM vs. LLM (round3+4)
df_diff_complex4 = df_LLM_rounds3_4.query('Model_Complexity != "low"')
df_diff_complex4_csp = df_diff_complex4.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_diff_complex4, x="Approach", y="F1", ax=axs[0])
sns.boxplot(data=df_diff_complex4, x="Approach", y="F2", ax=axs[1])
sns.boxplot(data=df_diff_complex4, x="Approach", y="F3", ax=axs[2])
sns.boxplot(data=df_diff_complex4, x="Approach", y="CS", ax=axs[3])
sns.boxplot(data=df_diff_complex4_csp, x="Approach", y="CSP", ax=axs[4])
plt.show()

# box plot low complexity for RALLM vs. LLM (round3+4)
df_diff_complex5 = df_LLM_rounds3_4.query('Model_Complexity == "low"')
df_diff_complex5_csp = df_diff_complex5.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_diff_complex5, x="Approach", y="F1", ax=axs[0])
sns.boxplot(data=df_diff_complex5, x="Approach", y="F2", ax=axs[1])
sns.boxplot(data=df_diff_complex5, x="Approach", y="F3", ax=axs[2])
sns.boxplot(data=df_diff_complex5, x="Approach", y="CS", ax=axs[3])
sns.boxplot(data=df_diff_complex5_csp, x="Approach", y="CSP", ax=axs[4])
plt.show()


# box plot for influence number of examples
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_RALLM, x="Nr_Examples", y="F1", ax=axs[0])
sns.boxplot(data=df_RALLM, x="Nr_Examples", y="F2", ax=axs[1])
sns.boxplot(data=df_RALLM, x="Nr_Examples", y="F3", ax=axs[2])
sns.boxplot(data=df_RALLM, x="Nr_Examples", y="CS", ax=axs[3])
sns.boxplot(data=df_RALLM_csp, x="Nr_Examples", y="CSP", ax=axs[4])
plt.show()

# box plot for influence number of examples medium and high complexity RALLM vs. LLM
df_diff_complex2 = df_diff_complex.query('Approach_Nr_examples != "LLM"')
df_diff_complex2_csp = df_diff_complex2.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_diff_complex2, x="Approach_Nr_examples", y="F1", ax=axs[0])
sns.boxplot(data=df_diff_complex2, x="Approach_Nr_examples", y="F2", ax=axs[1])
sns.boxplot(data=df_diff_complex2, x="Approach_Nr_examples", y="F3", ax=axs[2])
sns.boxplot(data=df_diff_complex2, x="Approach_Nr_examples", y="CS", ax=axs[3])
sns.boxplot(data=df_diff_complex2_csp, x="Approach_Nr_examples", y="CSP", ax=axs[4])
plt.show()



