import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## Script for box plots analysing the performance distributions
## on the RALLM-based approach tackling limited context window. 

# Setup data
dataset = ".../Analysis/exp2_analysis_0shot.csv" # path needs to be adapted
df = pd.read_csv(dataset)

# Consider scores for CSP only above 0,
# as it implies none CS were generated.
df_csp = df.query('CSP > 0.0')

# rounds
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df, x="Round", y="F1", ax=axs[0])
sns.boxplot(data=df, x="Round", y="F2", ax=axs[1])
sns.boxplot(data=df, x="Round", y="F3", ax=axs[2])
sns.boxplot(data=df, x="Round", y="CS", ax=axs[3])
sns.boxplot(data=df_csp, x="Round", y="CSP", ax=axs[4])
plt.show()

# rounds aggregated
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df, x="Rounds_Aggregated", y="F1", ax=axs[0])
sns.boxplot(data=df, x="Rounds_Aggregated", y="F2", ax=axs[1])
sns.boxplot(data=df, x="Rounds_Aggregated", y="F3", ax=axs[2])
sns.boxplot(data=df, x="Rounds_Aggregated", y="CS", ax=axs[3])
sns.boxplot(data=df_csp, x="Rounds_Aggregated", y="CSP", ax=axs[4])
plt.show()


# setup chunks
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df, x="Chunks", y="F1", ax=axs[0])
sns.boxplot(data=df, x="Chunks", y="F2", ax=axs[1])
sns.boxplot(data=df, x="Chunks", y="F3", ax=axs[2])
sns.boxplot(data=df, x="Chunks", y="CS", ax=axs[3])
sns.boxplot(data=df_csp, x="Chunks", y="CSP", ax=axs[4])
plt.show()

# chunks differences for compact
df_chunks_compact = df[df["RSP_Mode"]=="compact"]
df_chunks_compact_csp = df_chunks_compact.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_chunks_compact, x="Chunks", y="F1", ax=axs[0])
sns.boxplot(data=df_chunks_compact, x="Chunks", y="F2", ax=axs[1])
sns.boxplot(data=df_chunks_compact, x="Chunks", y="F3", ax=axs[2])
sns.boxplot(data=df_chunks_compact, x="Chunks", y="CS", ax=axs[3])
sns.boxplot(data=df_chunks_compact_csp, x="Chunks", y="CSP", ax=axs[4])
plt.show()

# chunks differences for refine
df_chunks_refine = df[df["RSP_Mode"]=="refine"]
df_chunks_refine_csp = df_chunks_refine.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_chunks_refine, x="Chunks", y="F1", ax=axs[0])
sns.boxplot(data=df_chunks_refine, x="Chunks", y="F2", ax=axs[1])
sns.boxplot(data=df_chunks_refine, x="Chunks", y="F3", ax=axs[2])
sns.boxplot(data=df_chunks_refine, x="Chunks", y="CS", ax=axs[3])
sns.boxplot(data=df_chunks_refine_csp, x="Chunks", y="CSP", ax=axs[4])
plt.show()


# setup response mode
fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df, x="RSP_Mode", y="F1", ax=axs[0])
sns.boxplot(data=df, x="RSP_Mode", y="F2", ax=axs[1])
sns.boxplot(data=df, x="RSP_Mode", y="F3", ax=axs[2])
sns.boxplot(data=df, x="RSP_Mode", y="CS", ax=axs[3])
sns.boxplot(data=df_csp, x="RSP_Mode", y="CSP", ax=axs[4])
plt.show()

# response mode differences for small chunks
df_mode_small = df[df["Chunks"]=="small"]
df_mode_small_csp = df_mode_small.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_mode_small, x="RSP_Mode", y="F1", ax=axs[0])
sns.boxplot(data=df_mode_small, x="RSP_Mode", y="F2", ax=axs[1])
sns.boxplot(data=df_mode_small, x="RSP_Mode", y="F3", ax=axs[2])
sns.boxplot(data=df_mode_small, x="RSP_Mode", y="CS", ax=axs[3])
sns.boxplot(data=df_mode_small_csp, x="RSP_Mode", y="CSP", ax=axs[4])
plt.show()

# response mode differences for large chunks
df_mode_large = df[df["Chunks"]=="large"]
df_mode_large_csp = df_mode_large.query('CSP > 0.0')

fig, axs = plt.subplots(ncols=5)
sns.boxplot(data=df_mode_large, x="RSP_Mode", y="F1", ax=axs[0])
sns.boxplot(data=df_mode_large, x="RSP_Mode", y="F2", ax=axs[1])
sns.boxplot(data=df_mode_large, x="RSP_Mode", y="F3", ax=axs[2])
sns.boxplot(data=df_mode_large, x="RSP_Mode", y="CS", ax=axs[3])
sns.boxplot(data=df_mode_large_csp, x="RSP_Mode", y="CSP", ax=axs[4])
plt.show()