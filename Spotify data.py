#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

file_path = r'D:\Bootcamp\Main\3_spotify_5000_songs.csv'
spotify5k_df = pd.read_csv(file_path)
spotify5k_df = spotify5k_df.rename(columns=lambda x: x.strip())
spotify5k_df.info()


# In[2]:


spotify5k_df.axes


# In[3]:


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd

features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

X = spotify5k_df[features]

wcss = []

k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10, 6))
plt.plot(k_range, wcss, marker='o', linestyle='-', color='b')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.title('Elbow Curve for KMeans Clustering')
plt.xticks(k_range)
plt.show()

wcss_data = pd.DataFrame({'Number of Clusters (k)': k_range, 'WCSS': wcss})
print("WCSS Data:")
wcss_data


# In[4]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, PowerTransformer

# Define the features
features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

# Extract features from the dataframe (assuming spotify5k_df is defined elsewhere)
# X = spotify5k_df[features]

# Number of clusters
k = 4  

# List of scaler names for plotting and labeling
scaler_names = ['Raw', 'StandardScaler', 'MinMaxScaler', 'RobustScaler', 'MaxAbsScaler', 'PowerTransformer']

# Dictionary to store Within-Cluster-Sum-of-Squares (WCSS) for each scaler
wcss_dict = {}

# Define colors for better readability
colors = sns.color_palette("tab10")

# Dictionary to store cluster centers for each scaler
cluster_centers = {}

# Iterate over each scaler
for i, scaler in enumerate([None, StandardScaler(), MinMaxScaler(), RobustScaler(), MaxAbsScaler(), PowerTransformer()]):
    # Scale the features if scaler is not None
    if scaler is not None:
        X_scaled = scaler.fit_transform(X)
        scaler_name = scaler_names[i]
    else:
        X_scaled = X
        scaler_name = 'Raw Data'
    
    # Initialize KMeans clustering
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    
    # Calculate WCSS
    wcss = kmeans.inertia_
    wcss_dict[scaler_name] = wcss
    
    # Store cluster centers
    cluster_centers[scaler_name] = kmeans.cluster_centers_

    # Plot radar chart for cluster centers
    plt.figure(figsize=(10, 6))
    angles = np.linspace(0, 2 * np.pi, len(features), endpoint=False).tolist()
    angles += angles[:1]  # Ensure closed loop
    ax = plt.subplot(111, polar=True)

    # Plot each cluster's centroid
    for idx, center in enumerate(kmeans.cluster_centers_):
        values = np.round(np.concatenate((center, [center[0]])), 2)  # Round to two decimal points
        ax.plot(angles, values, marker='o', linestyle='-', color=colors[idx], linewidth=2, label=f'Cluster {idx+1}')
        # Fill the area enclosed by each cluster's centroid with a light blue shade
        ax.fill(angles, values, color=colors[idx], alpha=0.25)

    # Set the labels for each axis
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(features, fontsize=10)

    plt.title(f'Radar Chart for Cluster Centers ({scaler_name})', loc='left', fontsize=12, pad=20)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=k)
    plt.show()

    # Create DataFrame to display WCSS for the current scaler
    scaler_df = pd.DataFrame(list(wcss_dict.items()), columns=['Scaler', 'WCSS'])

    # Display the table for the current scaler
    print(f"{scaler_name} chart")
    print(f"Table for {scaler_name}:")
    display(scaler_df)

# Find the best scaler based on the minimum WCSS
best_scaler = min(wcss_dict, key=wcss_dict.get)

print(f"\nBased on the Within-Cluster-Sum-of-Squares (WCSS), the best scaler to use is {best_scaler}. Using this scaler helps in minimizing the WCSS, indicating better cluster formation.")
print(f"\nChoosing an appropriate scaler is crucial as it affects the clustering results. With {k} clusters, it is recommended to use the {best_scaler} scaler to create the clusters.")

# Add explanation points based on the WCSS score
print("\nAdditional points: \n1) A lower WCSS score indicates that the data points within each cluster are closer to their respective centroids, implying more compact and well-separated clusters. \n2) By selecting the scaler that yields the lowest WCSS, we aim to achieve the most meaningful and distinct cluster separation. \n3) The shaded area in each radar chart represents the coverage or extent of each cluster's features in the scaled feature space. It visually demonstrates how different clusters vary in their feature composition and distribution.")


# In[5]:


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd

features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
X = spotify5k_df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

wcss = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss, marker='o', linestyle='-')
plt.xlabel('Number of Clusters')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.show()

elbow_df = pd.DataFrame({'Number of Clusters': range(1, 11), 'WCSS': wcss})
elbow_df

silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))

plt.plot(range(2, 11), silhouette_scores, marker='o', linestyle='-')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Score for Optimal Number of Clusters')
plt.show()

silhouette_df = pd.DataFrame({'Number of Clusters': range(2, 11), 'Silhouette Score': silhouette_scores})
silhouette_df


# In[6]:


from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA()
X_pca = pca.fit_transform(X_scaled)
explained_variance = pca.explained_variance_ratio_
cumulative_explained_variance = explained_variance.cumsum()

plt.plot(range(1, len(explained_variance) + 1), cumulative_explained_variance, marker='o', linestyle='-')
plt.xlabel('Number of Principal Components')
plt.ylabel('Cumulative Explained Variance Ratio')
plt.title('Cumulative Explained Variance Ratio by Principal Components')
plt.grid(False)
plt.show()

num_components = 5
pca = PCA(n_components=num_components)
X_pca = pca.fit_transform(X_scaled)

num_clusters = 4 
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(X_pca)
labels = kmeans.labels_

spotify5k_df['Cluster'] = labels
cluster_counts = spotify5k_df['Cluster'].value_counts()
print("Cluster Counts:\n", cluster_counts)


# In[7]:


features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(spotify5k_df[features])

kmeans = KMeans(n_clusters=4, random_state=42)
spotify5k_df['Cluster'] = kmeans.fit_predict(X)

numeric_columns = spotify5k_df.select_dtypes(include=['float64', 'int64'])
cluster_means = spotify5k_df.groupby('Cluster')[numeric_columns.columns].mean()
print("Cluster Characteristics (Mean Feature Values):\n")
cluster_means

import matplotlib.pyplot as plt

plt.scatter(X[:, 0], X[:, 1], c=spotify5k_df['Cluster'], cmap='viridis')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.title('Clusters of Songs')
plt.colorbar(label='Cluster')
plt.show()

for feature in features:
    plt.figure(figsize=(8, 6))
    for cluster_id in range(4):
        cluster_data = spotify5k_df[spotify5k_df['Cluster'] == cluster_id][feature]
        plt.hist(cluster_data, bins=20, alpha=0.6, label=f'Cluster {cluster_id}')
    plt.title(f'Distribution of {feature} by Cluster')
    plt.xlabel(feature)
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()


# In[8]:


from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_train, X_test, y_train, y_test = train_test_split(X, spotify5k_df['Cluster'], test_size=0.2, random_state=42)

knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)

y_pred = knn_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


# In[9]:


spotify5k_df.dtypes


# In[10]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define a function to normalize tempo
def normalize_tempo(tempo):
    max_tempo = spotify5k_df['tempo'].max()
    min_tempo = spotify5k_df['tempo'].min()
    return (tempo - min_tempo) / (max_tempo - min_tempo)

# Apply the normalization function to the tempo column
spotify5k_df['normalized_tempo'] = spotify5k_df['tempo'].apply(normalize_tempo)

cluster_names = {
    0: 'Serene Sounds',
    1: 'Pulsating Rhythms',
    2: 'Tranquil Tunes',
    3: 'Melancholic Melodies',
}

# Use 'normalized_tempo' instead of 'tempo' in cluster statistics
cluster_statistics = spotify5k_df.groupby('Cluster').agg({
    'danceability': 'mean',
    'energy': 'mean',
    'valence': 'mean',
    'normalized_tempo': 'mean',  # Use 'normalized_tempo' instead of 'tempo'
    'acousticness': 'mean',
    'speechiness': 'mean'
})

cluster_explanations = {
    0: f"Songs with serene and calming vibes characterized by high valence ({cluster_statistics.loc[0, 'valence']:.2f}) and moderate tempo ({cluster_statistics.loc[0, 'normalized_tempo']:.2f}).",
    1: f"Tracks featuring pulsating rhythms and high energy suitable for dancing with high energy ({cluster_statistics.loc[1, 'energy']:.2f}) and tempo ({cluster_statistics.loc[1, 'normalized_tempo']:.2f}).",
    2: f"Music with tranquil melodies and moderate energy levels, perfect for unwinding with a balanced mix of valence ({cluster_statistics.loc[2, 'valence']:.2f}) and tempo ({cluster_statistics.loc[2, 'normalized_tempo']:.2f}).",
    3: f"Melancholic tunes with low valence ({cluster_statistics.loc[3, 'valence']:.2f}) and a somber atmosphere, often featuring high acousticness ({cluster_statistics.loc[3, 'acousticness']:.2f}).",
}

for cluster_id, name in cluster_names.items():
    print(f"Cluster {cluster_id} ({name}): {cluster_explanations[cluster_id]}")
    display(cluster_statistics.loc[[cluster_id]])
    
    plt.figure(figsize=(10, 6))
    sns.set(style="white")  # Remove grid
    sns.barplot(x=cluster_statistics.columns, y=cluster_statistics.loc[cluster_id].values, palette="magma")
    plt.title(f'Cluster {cluster_id} - {name} Features')
    plt.xticks(rotation=45)
    
    for index, value in enumerate(cluster_statistics.loc[cluster_id]):
        plt.text(index, value, f'{value:.2f}', ha='center', va='bottom')
    
    plt.show()
    print('\n')


# In[11]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 10))

for cluster_id, name in cluster_names.items():
    plt.scatter(cluster_statistics.loc[cluster_id, 'normalized_tempo'], 
                cluster_statistics.loc[cluster_id, 'valence'], 
                label=name, 
                s=200, 
                alpha=0.7)  
    
    plt.text(cluster_statistics.loc[cluster_id, 'normalized_tempo'], 
             cluster_statistics.loc[cluster_id, 'valence'], 
             f"{name}\n{cluster_explanations[cluster_id]}", 
             fontsize=10, 
             ha='center', 
             va='center', 
             wrap=True)  

plt.xlabel('Normalized Tempo', fontsize=12)
plt.ylabel('Valence', fontsize=12)
plt.title('Cluster Analysis based on Tempo and Valence', fontsize=14)
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=10)
plt.grid(False)

plt.margins(0.05)
plt.show()

# Explanation
print("\nExplanation:")
print("We chose to plot tempo and valence as they are two key features that determine the mood of a song.")
print("Tempo indicates the speed or pace of the music, while valence represents the positivity or negativity of the musical content.")
print("By analyzing these two features, we are able to identify distinct clusters representing songs with different mood characteristics.")

# Conclusion
print("\nConclusion:")
print("Based on the clustering analysis, we identified distinct clusters representing songs with different mood characteristics.")
print("Machine learning can be a valuable tool for creating playlists as it automatically categorizes songs based on their features, helping users discover music that matches their mood and preferences.")


# In[12]:


import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

spotify5k_df['text'] = spotify5k_df['name'] + ' ' + spotify5k_df['artist']

vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(spotify5k_df['text'])

vocab = vectorizer.get_feature_names_out()

word_counts = pd.DataFrame(X.toarray(), columns=vocab)
word_counts['Cluster'] = spotify5k_df['Cluster']

cluster_names = {
    0: 'Relaxing Vibes',
    1: 'Energetic Beats',
    2: 'Chill Out',
    3: 'Melancholic Melodies'
}

for cluster_id in range(len(word_counts['Cluster'].unique())):
    words_in_cluster = word_counts[word_counts['Cluster'] == cluster_id].drop('Cluster', axis=1)
    word_freq = words_in_cluster.sum().to_dict()

    wordcloud = WordCloud(width=800, height=400, background_color='white', prefer_horizontal=0.9).generate_from_frequencies(word_freq)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f'Word Cloud for {cluster_names.get(cluster_id, "Cluster " + str(cluster_id))}')
    plt.axis('off')
    plt.show()

    top_words = words_in_cluster.sum().sort_values(ascending=False).head(10)
    sns.set_palette('bright')
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_words.values, y=top_words.index)
    plt.title(f'Top 10 Words in {cluster_names.get(cluster_id, "Cluster " + str(cluster_id))}')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    for i, (word, count) in enumerate(zip(top_words.index, top_words.values)):
        plt.text(count, i, f' {word} ({count})', fontsize=10, style='italic', va='center')
    plt.show()


# In[13]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import pdist
from warnings import simplefilter

# Ignore future warnings
simplefilter(action='ignore', category=FutureWarning)

# Select features for clustering
features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 
            'instrumentalness', 'liveness', 'valence', 'tempo']

# Scale the features
try:
    scaler = StandardScaler()
    X = scaler.fit_transform(spotify5k_df[features])
except KeyError:
    print("Error: Features not found in the dataset.")

# Use PCA to determine the number of clusters
try:
    pca = PCA(n_components=len(features))
    X_pca = pca.fit_transform(X)
    cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)
    n_components = np.argmax(cumulative_variance_ratio >= 0.95) + 1
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)
except ValueError:
    print("Error: Not enough features for PCA.")

# Find optimal number of clusters using silhouette score
best_score = -1
best_k = -1
for k in range(2, 11):
    try:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_pca)
        silhouette_avg = silhouette_score(X_pca, kmeans.labels_)
        if silhouette_avg > best_score:
            best_score = silhouette_avg
            best_k = k
    except ValueError:
        print("Error: Unable to find optimal number of clusters.")

# Train KMeans with optimal number of clusters
try:
    kmeans = KMeans(n_clusters=best_k, random_state=42)
    kmeans.fit(X_pca)
    spotify5k_df['cluster'] = kmeans.labels_
except ValueError:
    print("Error: Unable to train KMeans model.")

# Function to calculate diversity of recommended songs
def calculate_diversity(recommended_songs):
    try:
        recommended_features = recommended_songs[features].to_numpy()
        cosine_distances = pdist(recommended_features, metric='cosine')
        avg_cosine_distance = np.mean(cosine_distances)
        diversity = 1 - avg_cosine_distance
        return diversity
    except KeyError:
        print("Error: Features not found in recommended songs.")

# Function to recommend songs from a given cluster
def recommend_songs(cluster_id, num_songs=5):
    try:
        cluster_data = spotify5k_df[spotify5k_df['cluster'] == cluster_id]
        recommended_songs = cluster_data.sample(min(num_songs, len(cluster_data)))
        return recommended_songs
    except KeyError:
        print("Error: Cluster ID not found.")

# Visualize clusters
def visualize_clusters(X_pca, labels, centroids):
    plt.figure(figsize=(10, 6))
    for i in range(len(np.unique(labels))):
        plt.scatter(X_pca[labels == i, 0], X_pca[labels == i, 1], label=f'Cluster {i}')
    plt.scatter(centroids[:, 0], centroids[:, 1], marker='*', s=200, c='black', label='Centroids')
    plt.title('Clusters')
    plt.xlabel('PCA Component 1')
    plt.ylabel('PCA Component 2')
    plt.legend()
    plt.show()

# Visualize explained variance ratio
def visualize_variance(pca):
    plt.figure(figsize=(8, 6))
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Explained Variance')
    plt.title('PCA Explained Variance Ratio')
    plt.grid(True)
    plt.show()

# Visualize silhouette scores
def visualize_silhouette_scores(scores):
    plt.figure(figsize=(8, 6))
    plt.plot(range(2, 11), scores, marker='o')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score vs Number of Clusters')
    plt.grid(True)
    plt.show()

# Example: Recommend songs from each cluster and calculate diversity
try:
    print("**Playlist Recommendations and Diversity Scores:**")
    playlists = []
    for cluster_id in range(best_k):
        recommended_songs = recommend_songs(cluster_id)
        playlist_name = f"Playlist {cluster_id + 1}: {', '.join(recommended_songs['name'].tolist())}"
        playlists.append({'Name': playlist_name, 'Diversity': calculate_diversity(recommended_songs)})
    playlists_df = pd.DataFrame(playlists)
    display(playlists_df)

except TypeError:
    print("Error: Unable to calculate diversity.")

# Visualizations
print("\n**Visualizations:**")
visualize_clusters(X_pca, kmeans.labels_, kmeans.cluster_centers_)
visualize_variance(pca)
visualize_silhouette_scores([silhouette_score(X_pca, kmeans.labels_) for k in range(2, 11)])

# Answers to questions
print("\n**Answers to Questions:**")
print("\n**How did you create your prototype?**")
print("The prototype was created using Python with the scikit-learn library for machine learning algorithms.\n")

print("**How many playlists (clusters) are there?**")
print("The number of playlists (clusters) is determined dynamically based on the data using the silhouette score.\n")

print("**What audio features did you use and what did you drop? Why?**")
print("We used features like danceability, energy, loudness, etc., as they are relevant to song characteristics.")
print("We dropped features that were not considered to significantly influence playlist creation, such as 'duration_ms' or 'time_signature'.\n")

print("**Is the prototype effective at creating cohesive playlists?**")
print("Cohesiveness of playlists can be evaluated based on diversity and user feedback.\n")

print("**Are Spotify’s audio features capable of identifying 'similar songs' as defined by humanly detectable criteria?**")
print("This can be determined through user feedback and comparison with manually curated playlists.\n")

print("**What kind of data might help us create better playlists?**")
print("Additional data such as user preferences, listening history, genre information, etc., can improve playlist quality.\n")

print("**Is K-Means a good method for creating playlists? Provide pros and cons.**")
print("Pros:")
print("- Simple and easy to implement.")
print("- Scalable to large datasets.")
print("\nCons:")
print("- Assumes clusters are spherical and of equal size.")
print("- Sensitive to initialization.\n")

print("**What would be your next steps if you continued with this project?**")
print("Further refinement of clustering algorithms, incorporation of user feedback, and integration with a music streaming platform for real-time playlist generation.")


# In[ ]:


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from IPython.display import display

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Perform sentiment analysis on the 'name' column and handle NaNs
spotify5k_df['sentiment_score'] = spotify5k_df['name'].fillna('').apply(lambda x: sia.polarity_scores(x)['compound'])

# Fit a TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(spotify5k_df['name'])

# Find optimal number of clusters using silhouette score
silhouette_scores = []
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(X)
    silhouette_scores.append(silhouette_score(X, cluster_labels))

optimal_clusters_silhouette = silhouette_scores.index(max(silhouette_scores)) + 2

# Apply PCA to visualize clusters
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X.toarray())

# Find optimal number of clusters using PCA
inertia = []
for n_clusters in range(2, 11):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X_pca)
    inertia.append(kmeans.inertia_)

optimal_clusters_pca = inertia.index(min(inertia)) + 2

# Cluster using KMeans with optimal number of clusters
kmeans_silhouette = KMeans(n_clusters=optimal_clusters_silhouette, random_state=42)
spotify5k_df['cluster_silhouette'] = kmeans_silhouette.fit_predict(X)

kmeans_pca = KMeans(n_clusters=optimal_clusters_pca, random_state=42)
spotify5k_df['cluster_pca'] = kmeans_pca.fit_predict(X)

# Define cluster names based on sentiment
sentiment_cluster_names = {
    0: 'Negative (Low Sentiment)',
    1: 'Neutral (Medium Sentiment)',
    2: 'Positive (High Sentiment)'
}

# Assign cluster names
spotify5k_df['cluster_silhouette'] = spotify5k_df['cluster_silhouette'].map(sentiment_cluster_names)
spotify5k_df['cluster_pca'] = spotify5k_df['cluster_pca'].map(sentiment_cluster_names)

# Explanation for choosing the number of clusters
explanation = f"The number of clusters chosen based on silhouette score: {optimal_clusters_silhouette}. " \
              f"The number of clusters chosen based on PCA: {optimal_clusters_pca}."

# Visualize clusters using PCA
plt.figure(figsize=(12, 8))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=spotify5k_df['cluster_pca'], palette='husl', legend='full', marker='o')
plt.title('PCA Visualization of Song Clusters')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)
plt.grid(False)
plt.show()

# Visualize clusters using Silhouette Score
plt.figure(figsize=(10, 6))
sns.lineplot(x=range(2, 11), y=silhouette_scores, marker='o', color='blue')
plt.title('Silhouette Score for Optimal Cluster Selection')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.grid(False)
plt.xticks(range(2, 11))
plt.show()

# Additional visualizations
plt.figure(figsize=(10, 6))
sns.histplot(data=spotify5k_df, x='sentiment_score', bins=30, kde=True, color='green')
plt.title('Distribution of Sentiment Scores')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.grid(False)
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=spotify5k_df, x='cluster_pca', palette='husl')
plt.title('Number of Songs in Each Sentiment Cluster')
plt.xlabel('Sentiment Cluster')
plt.ylabel('Count')
plt.grid(False)
plt.show()

# Output DataFrame with cluster assignments and remove NaNs
cluster_silhouette_df = spotify5k_df[['name', 'cluster_silhouette']].dropna()
cluster_pca_df = spotify5k_df[['name', 'cluster_pca']].dropna()

# Output sentiment score for each cluster
sentiment_scores = spotify5k_df.groupby('cluster_pca')['sentiment_score'].mean()

# Explanation for cluster names
cluster_name_explanation = f"Cluster names are based on sentiment score: " \
                           f"Negative (Low Sentiment): sentiment score < 0, " \
                           f"Neutral (Medium Sentiment): sentiment score ≈ 0, " \
                           f"Positive (High Sentiment): sentiment score > 0."

# Display the outputs
print(explanation)
print(cluster_name_explanation)
display(cluster_silhouette_df)
display(cluster_pca_df)
display(sentiment_scores)


# In[ ]:


import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from IPython.display import display

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Perform sentiment analysis on the objective columns and handle NaNs
objective_columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 
                     'speechiness', 'acousticness', 'instrumentalness', 
                     'liveness', 'valence', 'tempo']

spotify5k_df['objective_sentiment_score'] = spotify5k_df[objective_columns].fillna('').apply(
    lambda x: sia.polarity_scores(str(x))['compound'])

# Fit a PCA to visualize objective clusters
X_objective = spotify5k_df[objective_columns].fillna(0)  # Fill NaNs with 0 for PCA
pca_objective = PCA(n_components=2, random_state=42)
X_pca_objective = pca_objective.fit_transform(X_objective)

# Cluster using KMeans with optimal number of clusters
kmeans_objective = KMeans(n_clusters=3, random_state=42)
spotify5k_df['objective_cluster'] = kmeans_objective.fit_predict(X_objective)

# Define cluster names based on objective sentiment
objective_cluster_names = {
    0: 'Low',
    1: 'Medium',
    2: 'High'
}

# Assign cluster names
spotify5k_df['objective_cluster'] = spotify5k_df['objective_cluster'].map(objective_cluster_names)

# Explanation for objective sentiment analysis
objective_explanation = "Objective sentiment analysis was performed based on the following columns: " \
                        "'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', " \
                        "'acousticness', 'instrumentalness', 'liveness', 'valence', and 'tempo'. " \
                        "Three clusters were chosen for better interpretation: Low, Medium, and High."

# Visualize objective clusters using PCA
plt.figure(figsize=(12, 8))
sns.scatterplot(x=X_pca_objective[:, 0], y=X_pca_objective[:, 1], 
                hue=spotify5k_df['objective_cluster'], palette='husl', 
                legend='full', marker='o')
plt.title('PCA Visualization of Objective Sentiment Clusters')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3)
plt.grid(False)
plt.show()

# Compare with sentiment analysis based on 'name' column
plt.figure(figsize=(10, 6))
sns.countplot(data=spotify5k_df, x='cluster_pca', hue='objective_cluster', palette='husl')
plt.title('Comparison of Sentiment Clusters (Name vs Objective Columns)')
plt.xlabel('Sentiment Cluster (Name)')
plt.ylabel('Count')
plt.legend(title='Objective Cluster', loc='upper right')
plt.grid(False)
plt.show()

# Display the outputs
display(objective_explanation)
display(spotify5k_df[['name', 'objective_cluster']])


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Select features for clustering
features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness',
            'instrumentalness', 'liveness', 'valence', 'tempo']

# Explanation: These features are chosen because they represent different aspects of songs
print("Selected Features for Clustering:")
print(pd.DataFrame(features, columns=['Features']))

# Scale the features using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(spotify5k_df[features])

# Explanation: StandardScaler is used to standardize the features, ensuring each feature has a mean of 0 and a standard deviation of 1.
print("\nFeature Scaling:")
print("The features are scaled using StandardScaler to standardize the data, making it suitable for clustering.")

# Create a DataFrame of scaled features for visualization
scaled_df = pd.DataFrame(X_scaled, columns=features)

# Plot histograms of scaled features
plt.figure(figsize=(12, 8))
for i, feature in enumerate(features):
    plt.subplot(3, 3, i + 1)
    plt.hist(scaled_df[feature], bins=20, color='skyblue', edgecolor='black')
    plt.title(feature)
    plt.xlabel('Scaled Values')
    plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# Use PCA to reduce dimensionality
pca = PCA(n_components=len(features))
X_pca = pca.fit_transform(X_scaled)

# Explanation: PCA is used to reduce the dimensionality of the data while retaining most of its variance.
print("\nDimensionality Reduction with PCA:")
print("Principal Component Analysis (PCA) is applied to reduce the dimensionality of the data while retaining most of its variance.")

# Plot explained variance ratio
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(features) + 1), pca.explained_variance_ratio_, marker='o', linestyle='--', color='b')
plt.title('Explained Variance Ratio by Principal Components')
plt.xlabel('Number of Principal Components')
plt.ylabel('Explained Variance Ratio')
plt.xticks(np.arange(1, len(features) + 1))
plt.grid(False)
plt.show()

# Find optimal number of clusters using silhouette score
silhouette_scores = []
for k in range(2, 101):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_pca)
    silhouette_avg = silhouette_score(X_pca, kmeans.labels_)
    silhouette_scores.append(silhouette_avg)

# Plot silhouette scores
plt.figure(figsize=(10, 6))
plt.plot(range(2, 101), silhouette_scores, marker='o', linestyle='-', color='r')
plt.title('Silhouette Score for Different Numbers of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.xticks(np.arange(2, 101, 5))
plt.grid(False)
plt.show()

# Based on business requirements, choose the number of clusters
# We aim to create playlists with sizes between 50 and 250 songs
# So, let's explore having between 20 and 100 clusters
print("\nChoosing Number of Clusters:")
print("Based on business requirements, we aim to create playlists with sizes between 50 and 250 songs.")
print("We will explore creating between 20 and 100 clusters to ensure playlist sizes between 50 and 250 songs.")


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

# Step 1: Determine the optimal number of clusters
# Calculate silhouette scores for different numbers of clusters
silhouette_scores = []
for k in range(2, 101):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_pca)
    silhouette_avg = silhouette_score(X_pca, kmeans.labels_)
    silhouette_scores.append(silhouette_avg)

# Plot silhouette scores
plt.figure(figsize=(10, 6))
plt.plot(range(2, 101), silhouette_scores, marker='o', linestyle='-', color='limegreen')
plt.title('Silhouette Score for Different Numbers of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.xticks(np.arange(2, 101, 5))
plt.grid(False)
plt.show()

# Step 2: Perform K-means clustering with the chosen number of clusters
# Based on business requirements, let's choose the number of clusters
# We aim to create playlists with sizes between 50 and 250 songs
# So, let's explore having between 20 and 100 clusters
chosen_clusters = 50

# Perform K-means clustering
kmeans = KMeans(n_clusters=chosen_clusters, random_state=42)
kmeans.fit(X_pca)

# Assign songs to clusters
cluster_labels = kmeans.labels_

# Step 3: Analyze characteristics of each cluster and create playlists
# Visualize cluster sizes
plt.figure(figsize=(10, 6))
plt.hist(cluster_labels, bins=chosen_clusters, color='gold', edgecolor='black')
plt.title('Distribution of Songs Across Clusters')
plt.xlabel('Cluster')
plt.ylabel('Number of Songs')
plt.grid(False)
plt.show()

# Analyze characteristics of each cluster
cluster_centers = scaler.inverse_transform(pca.inverse_transform(kmeans.cluster_centers_))
cluster_df = pd.DataFrame(cluster_centers, columns=features)

# Display cluster characteristics
print("\nCluster Characteristics:")
print(cluster_df)

# Create playlists based on clusters
playlist_sizes = [50, 100, 150, 200, 250]
playlists = []

for size in playlist_sizes:
    playlist = []
    for i in range(chosen_clusters):
        cluster_indices = np.where(cluster_labels == i)[0]
        cluster_indices = np.random.choice(cluster_indices, min(size // chosen_clusters, len(cluster_indices)), replace=False)
        playlist.extend(cluster_indices)
    playlists.append(playlist)

# Visualize playlist sizes
plt.figure(figsize=(10, 6))
plt.bar(range(len(playlist_sizes)), [len(p) for p in playlists], color='skyblue', edgecolor='black')
plt.xticks(range(len(playlist_sizes)), [f"{size} Songs" for size in playlist_sizes])
plt.title('Playlist Sizes')
plt.xlabel('Playlist Size')
plt.ylabel('Number of Songs')
plt.grid(False)
plt.show()

# Final Output: A data-driven analysis on clustering music data to create playlists
print("\nData-Driven Playlist Creation:")
print("By applying K-means clustering to music data, we identified distinct clusters of songs.")
print("Each cluster represents songs with similar characteristics, allowing us to create diverse playlists.")
print("Our analysis ensures that each playlist falls within the desired size range, catering to various music preferences.")


# In[ ]:


from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Selecting columns for clustering
columns_for_clustering = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
                          'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 
                          'duration_ms']

# Scaling the selected columns
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(spotify5k_df[columns_for_clustering])

# Performing K-means clustering with 50 clusters
kmeans = KMeans(n_clusters=50, random_state=42)
spotify5k_df['playlist_cluster'] = kmeans.fit_predict(scaled_features)

# Creating a mapping dictionary to map cluster labels to playlist names
playlist_names = [
    "Relaxing Vibes", "Energetic Workout", "Chill Lounge", "Happy Beats", "Soothing Melodies",
    "Motivational Mix", "Groovy Tunes", "Nighttime Chill", "Summer Fun", "Cozy Fireplace",
    "Mellow Grooves", "High Tempo", "Zen Garden", "Romantic Serenade", "Sunny Day", "Late Night Jazz",
    "Dreamy Atmosphere", "Pump-up Party", "Rainy Day", "Feel-good Funk", "Island Escapade",
    "Classic Rock", "Jazzy Brunch", "Mindful Meditation", "Epic Soundtrack", "Stress Relief",
    "Salsa Fiesta", "Soulful R&B", "Electronic Dance", "Country Roads", "Urban Vibes",
    "Smooth Jazz", "Indie Discovery", "Reggae Vibes", "Guitar Strumming", "Vintage Classics",
    "Latin Fever", "Deep House", "Piano Reflections", "Throwback Hits", "Alternative Edge",
    "Calm Waters", "Disco Fever", "Motown Magic", "Folk Fusion", "Hip-hop Groove",
    "Classical Symphony", "Techno Beats", "Opera Night", "Ambient Bliss"
]

playlist_mapping = {i: name for i, name in enumerate(playlist_names)}

# Mapping cluster labels to playlist names
spotify5k_df['playlist_name'] = spotify5k_df['playlist_cluster'].map(playlist_mapping)

# Define score ranges for each playlist type
mood_range = range(0, 100)
emotion_range = range(100, 200)
activity_range = range(200, max(playlist_summary['score'])+1)

# Assign playlist_type based on score
playlist_summary['playlist_type'] = ''
for idx, row in playlist_summary.iterrows():
    if row['score'] in mood_range:
        playlist_summary.at[idx, 'playlist_type'] = 'Mood'
    elif row['score'] in emotion_range:
        playlist_summary.at[idx, 'playlist_type'] = 'Emotion'
    else:
        playlist_summary.at[idx, 'playlist_type'] = 'Activity'
playlist_summary.sort_values(by=['score', 'playlist_type', 'name'], ascending=[False, True, True])


# In[ ]:




