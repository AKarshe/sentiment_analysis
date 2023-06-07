# Import necessary packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import nltk
nltk.download('wordnet')

# Load the 'Data_with_topics.csv' file
old_data = pd.read_csv('Data_with_topics.csv')

# Load the new data
new_data = pd.read_csv('NewData.csv')

# Preprocess the verbatims in the new data
new_data['DIS Verbatim'] = new_data['DIS Verbatim'].apply(lambda x: ' '.join(simple_preprocess(str(x), deacc=True)))

# Combine the old and new data
all_data = pd.concat([old_data, new_data])

# Train the LDA model on the verbatims in the combined data
dictionary = gensim.corpora.Dictionary(all_data['DIS Verbatim'].map(simple_preprocess))
bow_corpus = [dictionary.doc2bow(doc) for doc in all_data['DIS Verbatim'].map(simple_preprocess)]
lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=6, id2word=dictionary, passes=2, workers=2)

# Assign each verbatim in the new data to a topic
topics = [lda_model[bow] for bow in bow_corpus[len(old_data):]]
def get_main_topic(topic_list):
    if not topic_list:
        return None
    return max(topic_list, key=lambda x: x[1])[0]
main_topics = [get_main_topic(topic) for topic in topics]
new_data['Main Topic'] = main_topics

# Append the new data with the assigned topics to the old data
updated_data = pd.concat([old_data, new_data])

# Save the updated data to the 'Data_with_topics.csv' file
updated_data.to_csv('Data_with_topics.csv', index=False)

# Convert ratings into sentiment categories
def rating_to_sentiment(rating):
    if rating <= 3:
        return 'Dissatisfied'
    elif rating == 4:
        return 'Neutral'
    else:
        return 'Satisfied'
updated_data['Sentiment'] = updated_data['DIS (5-Point)'].apply(rating_to_sentiment)

# Count the number of each sentiment category
sentiment_counts = updated_data['Sentiment'].value_counts()

# Create a bar plot of sentiment counts
sns.set(style='whitegrid')
plt.figure(figsize=(10, 6))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='viridis')
plt.title('Sentiment Counts')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

# Calculate the sentiment counts in each category
category_sentiment_counts = updated_data.groupby('Category')['Sentiment'].value_counts().unstack().fillna(0)

# Create a stacked bar chart of sentiment counts in each category
category_sentiment_counts.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='viridis')
plt.title('Sentiment Counts in Each Category')
plt.xlabel('Category')
plt.ylabel('Count')
plt.show()

# Create a word cloud
all_verbatims = ' '.join(updated_data['DIS Verbatim'].astype```python
