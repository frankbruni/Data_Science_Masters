# 266 Final Project: Inverse Hierarchical Multi-Document Summarization

## Group Members: Frank Bruni, Brandon Scolieri, Daphne Yang

<hr>

### Abstract

This paper discusses the implementation of an inverse hierarchical text summarizer that creates abstractive summaries from seeded text data. Subsequent to generating a summary from a primary source (e.g. a news article), the process is repeated on a wider corpus of data (e.g. NYT articles for a certain range of time). The summaries are then clustered by content similarity via cosine similarity. Multi-document summarization using the proposed iterative pipeline architecture allows for more coherent and factually accurate contextual summaries.

<hr>

<strong> Project Report </strong>

<i>Inverse_Hierarchical_MultiDocument_Summarization.pdf</i>: PDF File of our final written report.

<hr>

### Repo Layout:

<strong>nyt_data_collection:</strong> Folder containing datasets from <i>New York Times</i> articles with:
<ul>
        <li> Scripts to call NYT API for articles in the dataset </li>
    <li> Datasets with associated metadata from the official API </li>
</ul>
<strong>initial_models:</strong> Folder containing all of our initial models: abstractive and extractive models, cosine similarity, tfidf measures

<strong>pipeline_models:</strong> Folder containing our final project notebook for submission <i>pipeline.ipynb</i> that contains all pipeline outputs for sample test document

<strong>resources: </strong> Folder containing text cleaning script -- specifically for lemming and stemming text

<hr>

### Accessing CSV Files from Our Collected Dataset

Command to pull csvs: 

```
git lfs pull --include="nyt_data_collection/<file_path/name>"
```
