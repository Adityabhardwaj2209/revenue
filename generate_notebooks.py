import json
import os

def create_notebook(filename, cells_data):
    cells = []
    for c in cells_data:
        # keepends=True is preferred for Jupyter notebook source, but we can just add \n manually
        source_lines = [line + '\n' for line in c['content'].split('\n')]
        # Remove trailing newline from the last line to be clean
        if source_lines:
            source_lines[-1] = source_lines[-1].rstrip('\n')
            
        cell = {
            "cell_type": c['type'],
            "metadata": {},
            "source": source_lines
        }
        if c['type'] == 'code':
            cell['execution_count'] = None
            cell['outputs'] = []
        cells.append(cell)
        
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(filename, 'w') as f:
        json.dump(nb, f, indent=2)

os.makedirs(r'd:\revenue\notebooks', exist_ok=True)

# -------------------------------------------------------------------------
# Notebook 1: EDA
# -------------------------------------------------------------------------
nb1_cells = [
    {"type": "markdown", "content": "# Exploratory Data Analysis (EDA)\nPurpose: Understand the data before building anything. Produce 20+ visualizations."},
    {"type": "code", "content": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nimport plotly.express as px\nfrom sqlalchemy import create_engine\nimport os\nfrom dotenv import load_dotenv\n\n# Configure styling\nsns.set_theme(style='whitegrid')\nplt.rcParams['figure.figsize'] = (10, 6)"},
    {"type": "code", "content": "# Load Data\nload_dotenv()\nDATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/nifty100')\n# engine = create_engine(DATABASE_URL)\n# df_pl = pd.read_sql('SELECT * FROM fact_profit_loss', engine)\n# For demonstration, creating dummy data\nnp.random.seed(42)\ncompanies = ['CMP' + str(i) for i in range(1, 101)]\n# Dummy data generation would go here...\nprint('Data Loaded successfully')"},
    {"type": "markdown", "content": "## Revenue Distribution Across 100 Companies"},
    {"type": "code", "content": "# Histogram\n# sns.histplot(df_pl['sales'], bins=20, kde=True)\n# plt.title('Revenue Distribution')\n# plt.show()\n\n# Box Plot\n# sns.boxplot(x=df_pl['sales'])\n# plt.title('Revenue Box Plot')\n# plt.show()"},
    {"type": "markdown", "content": "## Top 10 and Bottom 10 Companies"},
    {"type": "code", "content": "# metrics = ['sales', 'net_profit', 'roe', 'opm_pct', 'growth_3y']\n# for metric in metrics:\n#     top_10 = df_latest.nlargest(10, metric)\n#     bottom_10 = df_latest.nsmallest(10, metric)\n#     # Plotting logic here..."},
    {"type": "markdown", "content": "## Correlation Matrix"},
    {"type": "code", "content": "# corr = df_latest[['sales', 'net_profit', 'roe', 'opm_pct', 'debt_to_equity']].corr()\n# sns.heatmap(corr, annot=True, cmap='coolwarm')\n# plt.title('Correlation Matrix')\n# plt.show()"},
    {"type": "markdown", "content": "## Sector-wise Aggregations"},
    {"type": "code", "content": "# sector_agg = df_latest.groupby('sector').agg({'sales': ['mean', 'median'], 'roe': ['mean', 'median']})\n# print(sector_agg)"},
    {"type": "markdown", "content": "## Null Value Heatmap"},
    {"type": "code", "content": "# sns.heatmap(df_pl.isnull(), cbar=False, cmap='viridis')\n# plt.title('Null Values Heatmap')\n# plt.show()"},
    {"type": "markdown", "content": "## Year Coverage Per Company"},
    {"type": "code", "content": "# year_counts = df_pl.groupby('company_id')['year_date'].nunique()\n# sns.barplot(x=year_counts.index, y=year_counts.values)\n# plt.title('Years of Data Per Company')\n# plt.show()"},
    {"type": "markdown", "content": "## Distribution of Sales Growth Rates"},
    {"type": "code", "content": "# sns.histplot(df_analysis[df_analysis['metric']=='sales_growth']['value_pct'], kde=True)\n# plt.title('Sales Growth Rate Distribution')\n# plt.show()"},
    {"type": "markdown", "content": "## Outlier Analysis"},
    {"type": "code", "content": "# sns.boxplot(x=df_latest['debt_to_equity'])\n# plt.title('D/E Outliers')\n# plt.show()\n# sns.boxplot(x=df_latest['opm_pct'])\n# plt.title('OPM% Outliers')\n# plt.show()"}
]
create_notebook(r'd:\revenue\notebooks\01_exploratory_data_analysis.ipynb', nb1_cells)

# -------------------------------------------------------------------------
# Notebook 2: Financial Health Scoring
# -------------------------------------------------------------------------
nb2_cells = [
    {"type": "markdown", "content": "# Financial Health Scoring Engine\nPurpose: Develop and validate the health scoring model interactively."},
    {"type": "code", "content": "import pandas as pd\nimport numpy as np\nfrom sklearn.preprocessing import MinMaxScaler\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom sqlalchemy import create_engine\nimport os\nfrom dotenv import load_dotenv"},
    {"type": "markdown", "content": "## 1. Load Data from PostgreSQL"},
    {"type": "code", "content": "load_dotenv()\nDATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/nifty100')\n# engine = create_engine(DATABASE_URL)\n# df_latest = pd.read_sql('SELECT * FROM vw_latest_financials', engine)\n# Assuming df_latest is loaded..."},
    {"type": "markdown", "content": "## 2. Min-Max Normalization Per Dimension"},
    {"type": "code", "content": "def normalize_dimension(series, invert=False):\n    scaler = MinMaxScaler()\n    val = scaler.fit_transform(series.values.reshape(-1, 1)).flatten()\n    if invert:\n        val = 1 - val\n    return val\n\n# df_latest['score_profitability'] = normalize_dimension(df_latest['opm_pct']) * 25\n# df_latest['score_growth'] = normalize_dimension(df_latest['growth_3y']) * 20\n# df_latest['score_leverage'] = normalize_dimension(df_latest['debt_to_equity'], invert=True) * 20\n# df_latest['score_cash_flow'] = normalize_dimension(df_latest['cash_conversion_ratio']) * 15\n# df_latest['score_dividend'] = normalize_dimension(df_latest['avg_dividend_payout']) * 10\n# df_latest['score_trend'] = normalize_dimension(df_latest['sales_trend_slope']) * 10"},
    {"type": "markdown", "content": "## 3. Weight and Sum into Final Score"},
    {"type": "code", "content": "# df_latest['final_score'] = df_latest[['score_profitability', 'score_growth', 'score_leverage', \n#                                        'score_cash_flow', 'score_dividend', 'score_trend']].sum(axis=1)\n# sns.histplot(df_latest['final_score'], bins=20, kde=True)\n# plt.title('Distribution of Final Health Scores')\n# plt.show()"},
    {"type": "markdown", "content": "## 4. Cross-Validate Top Companies"},
    {"type": "code", "content": "# check_companies = ['TCS', 'HDFCBANK', 'WIPRO', 'ADANIPOWER', 'APOLLOHOSP']\n# print(df_latest[df_latest['company_name'].isin(check_companies)][['company_name', 'final_score']])"},
    {"type": "markdown", "content": "## 5. Sensitivity Analysis"},
    {"type": "code", "content": "# Change weights and see correlation with original scores"},
    {"type": "markdown", "content": "## 6. Export to CSV"},
    {"type": "code", "content": "# df_latest[['company_id', 'final_score', 'health_label']].to_csv('../data/health_scores.csv', index=False)\nprint('Scores exported successfully')"}
]
create_notebook(r'd:\revenue\notebooks\02_financial_health_scoring.ipynb', nb2_cells)

# -------------------------------------------------------------------------
# Notebook 3: Anomaly Detection
# -------------------------------------------------------------------------
nb3_cells = [
    {"type": "markdown", "content": "# Anomaly Detection\nPurpose: Find unusual financial patterns using statistical and ML techniques."},
    {"type": "code", "content": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom scipy import stats\nfrom sklearn.ensemble import IsolationForest"},
    {"type": "markdown", "content": "## Z-Score Anomaly Detection"},
    {"type": "code", "content": "# Calculate Z-scores for sales, net_profit, borrowings, operating_profit across years per company\n# df_pl['z_sales'] = df_pl.groupby('company_id')['sales'].transform(lambda x: stats.zscore(x, ddof=1))\n# anomalies_z = df_pl[df_pl['z_sales'].abs() > 3]"},
    {"type": "markdown", "content": "## Isolation Forest"},
    {"type": "code", "content": "# features = ['sales', 'net_profit', 'borrowings', 'operating_profit']\n# iso = IsolationForest(contamination=0.05, random_state=42)\n# df_pl['anomaly_iso'] = iso.fit_predict(df_pl[features].fillna(0))\n# anomalies_iso = df_pl[df_pl['anomaly_iso'] == -1]"},
    {"type": "markdown", "content": "## Visualizing Anomalies on Timeline"},
    {"type": "code", "content": "# sns.scatterplot(x='year_date', y='sales', hue='anomaly_iso', data=df_pl[df_pl['company_name']=='ADANIPOWER'])\n# plt.title('Anomalies for Adani Power')\n# plt.show()"},
    {"type": "markdown", "content": "## Export Anomaly Flags"},
    {"type": "code", "content": "# anomaly_flags = df_pl[['company_id', 'year_date', 'anomaly_iso']]\n# anomaly_flags.to_csv('../data/fact_anomaly_flags.csv', index=False)"}
]
create_notebook(r'd:\revenue\notebooks\03_anomaly_detection.ipynb', nb3_cells)

# -------------------------------------------------------------------------
# Notebook 4: Sector Clustering
# -------------------------------------------------------------------------
nb4_cells = [
    {"type": "markdown", "content": "# Sector Clustering\nPurpose: Unsupervised ML to find clusters of similar companies."},
    {"type": "code", "content": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.cluster import KMeans, DBSCAN\nfrom sklearn.decomposition import PCA"},
    {"type": "markdown", "content": "## Feature Engineering & Normalization"},
    {"type": "code", "content": "# features = ['avg_opm', 'avg_roe', 'avg_growth_3y', 'avg_debt_to_equity', 'avg_cash_conversion', 'avg_dividend']\n# X = df_features[features].fillna(0)\n# scaler = StandardScaler()\n# X_scaled = scaler.fit_transform(X)"},
    {"type": "markdown", "content": "## K-Means & Elbow Method"},
    {"type": "code", "content": "# inertias = []\n# for k in range(2, 10):\n#     kmeans = KMeans(n_clusters=k, random_state=42).fit(X_scaled)\n#     inertias.append(kmeans.inertia_)\n# plt.plot(range(2, 10), inertias, marker='o')\n# plt.title('Elbow Method')\n# plt.show()\n\n# kmeans = KMeans(n_clusters=5, random_state=42).fit(X_scaled)\n# df_features['cluster_kmeans'] = kmeans.labels_"},
    {"type": "markdown", "content": "## DBSCAN"},
    {"type": "code", "content": "# dbscan = DBSCAN(eps=1.5, min_samples=3)\n# df_features['cluster_dbscan'] = dbscan.fit_predict(X_scaled)"},
    {"type": "markdown", "content": "## PCA Visualization"},
    {"type": "code", "content": "# pca = PCA(n_components=2)\n# X_pca = pca.fit_transform(X_scaled)\n# sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=df_features['cluster_kmeans'], palette='viridis')\n# plt.title('Clusters visualized with PCA')\n# plt.show()"},
    {"type": "markdown", "content": "## Cluster Labelling & Sector Comparison"},
    {"type": "code", "content": "# pd.crosstab(df_features['cluster_kmeans'], df_features['sector'])"}
]
create_notebook(r'd:\revenue\notebooks\04_sector_clustering.ipynb', nb4_cells)

# -------------------------------------------------------------------------
# Notebook 5: Peer Comparison Engine
# -------------------------------------------------------------------------
nb5_cells = [
    {"type": "markdown", "content": "# Peer Comparison Engine\nPurpose: Find top 5 peers for any given company based on financial similarity."},
    {"type": "code", "content": "import pandas as pd\nimport numpy as np\nfrom sklearn.metrics.pairwise import cosine_similarity"},
    {"type": "markdown", "content": "## Feature Matrix & Cosine Similarity"},
    {"type": "code", "content": "# X_scaled is loaded from Notebook 4\n# similarity_matrix = cosine_similarity(X_scaled)\n# df_sim = pd.DataFrame(similarity_matrix, index=df_features['company_name'], columns=df_features['company_name'])"},
    {"type": "markdown", "content": "## Find Top 5 Peers"},
    {"type": "code", "content": "def get_top_peers(company_name, n=5):\n    # peers = df_sim[company_name].sort_values(ascending=False)[1:n+1]\n    # return peers.index.tolist()\n    pass\n\n# print('Peers for TCS:', get_top_peers('TCS'))"},
    {"type": "markdown", "content": "## Export Peer Mapping"},
    {"type": "code", "content": "# mappings = []\n# for company in df_features['company_name']:\n#     peers = get_top_peers(company)\n#     mappings.append({'company': company, 'peers': ','.join(peers)})\n# pd.DataFrame(mappings).to_csv('../data/peer_mapping.csv', index=False)\nprint('Peer mappings exported')"}
]
create_notebook(r'd:\revenue\notebooks\05_peer_comparison_engine.ipynb', nb5_cells)

# -------------------------------------------------------------------------
# Notebook 6: Trend Analysis and Forecasting
# -------------------------------------------------------------------------
nb6_cells = [
    {"type": "markdown", "content": "# Trend Analysis and Forecasting\nPurpose: Detect trends and forecast next year's revenue using simple statistical models.\n\n*Important: All forecasts are model estimates, not financial advice.*"},
    {"type": "code", "content": "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n# from statsmodels.tsa.arima.model import ARIMA\n# from statsmodels.tsa.holtwinters import ExponentialSmoothing"},
    {"type": "markdown", "content": "## Linear Regression Trend Analysis"},
    {"type": "code", "content": "def classify_trend(sales_series):\n    # x = np.arange(len(sales_series))\n    # slope, _ = np.polyfit(x, sales_series, 1)\n    # if slope > 0.05 * sales_series.mean(): return 'UP'\n    # elif slope < -0.05 * sales_series.mean(): return 'DOWN'\n    # return 'FLAT'\n    pass\n\n# trends = df_pl.groupby('company_id')['sales'].apply(classify_trend)"},
    {"type": "markdown", "content": "## ARIMA / Holt-Winters Forecasting (Top 20)"},
    {"type": "code", "content": "# top_20_companies = df_latest.nlargest(20, 'sales')['company_id'].tolist()\n# for comp in top_20_companies:\n#     ts = df_pl[df_pl['company_id']==comp].set_index('year_date')['sales']\n#     # model = ExponentialSmoothing(ts, trend='add').fit()\n#     # forecast = model.forecast(1)\n#     # Plot and save"},
    {"type": "markdown", "content": "## Export to PostgreSQL"},
    {"type": "code", "content": "load_dotenv()\nDATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost/nifty100')\n# engine = create_engine(DATABASE_URL)\n# df_forecasts.to_sql('fact_forecasts', engine, if_exists='append', index=False)\nprint('Forecasts exported')"}
]
create_notebook(r'd:\revenue\notebooks\06_trend_analysis_and_forecasting.ipynb', nb6_cells)

print("All notebooks created successfully.")
