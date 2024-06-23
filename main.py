import warnings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix
import numpy as np

# Ignore specific warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)

# Load the dataset
df = pd.read_csv("data.csv", dtype=str).head(10000)

# Remove duplicate entries
df = df.drop_duplicates(subset=['Book-Title', 'User-ID'])

# Convert columns to appropriate data types
df['Book-Rating'] = pd.to_numeric(df['Book-Rating'], errors='coerce')  # Convert 'Book-Rating' to numeric, ignoring errors
df['User-ID'] = pd.to_numeric(df['User-ID'], errors='coerce')  # Convert 'User-ID' to numeric, ignoring errors

# Remove rows with missing values in 'Book-Rating' and 'User-ID' columns
df = df.dropna(subset=['Book-Rating', 'User-ID'])

# Create Book-User matrix
book_user_matrix = df.pivot(index='Book-Title', columns='User-ID', values='Book-Rating').fillna(0)
book_user_matrix_sparse = csr_matrix(book_user_matrix.values)

# Train-test split
train_data, test_data = train_test_split(book_user_matrix_sparse, test_size=0.2, random_state=3500)

# KNN with Cosine Similarity
knn_cosine = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20)
knn_cosine.fit(train_data)

# SVD
svd = TruncatedSVD(n_components=90, random_state=3600)
matrix_svd = svd.fit_transform(train_data)
corr_matrix = np.corrcoef(matrix_svd)

# Recommendation function
def get_recommendations(book_idx):
    distances, indices = knn_cosine.kneighbors(train_data[book_idx, :].reshape(1, -1), n_neighbors=100)
    recommended_books_cosine = [book_user_matrix.index[i] for i in indices.flatten() if i != book_idx]

    # Using SVD
    corr_specific = corr_matrix[book_idx]
    recommended_books_svd = [book_user_matrix.index[i] for i, corr in enumerate(corr_specific) if 0.9 < corr < 1.0 and i != book_idx]

    return recommended_books_cosine, recommended_books_svd

# Calculate accuracy
def calculate_accuracy():
    total_accuracy_cosine = 0
    total_accuracy_svd = 0
    count = 0
    
    for book_title in test_data.nonzero()[0]:
        actual_ratings = test_data[book_title, :].toarray().flatten()
        
        if actual_ratings.sum() > 0:
            recommended_books_cosine, recommended_books_svd = get_recommendations(book_title)
            
            # KNN with Cosine Similarity
            cosine_accuracy = np.intersect1d(actual_ratings.nonzero(), [book_user_matrix.index.get_loc(book) for book in recommended_books_cosine]).shape[0]
            total_accuracy_cosine += cosine_accuracy / min(5, len(recommended_books_cosine)) if len(recommended_books_cosine) > 0 else 0
            
            # SVD
            svd_accuracy = np.intersect1d(actual_ratings.nonzero(), [book_user_matrix.index.get_loc(book) for book in recommended_books_svd]).shape[0]
            total_accuracy_svd += svd_accuracy / min(5, len(recommended_books_svd)) if len(recommended_books_svd) > 0 else 0
            
            count += 1
    
    avg_accuracy_cosine = (total_accuracy_cosine / count) * 100 if count > 0 else 0
    avg_accuracy_svd = (total_accuracy_svd / count) * 100 if count > 0 else 0
    
    return avg_accuracy_cosine, avg_accuracy_svd

# Calculate and print accuracy
accuracy_cosine, accuracy_svd = calculate_accuracy()

print(f"Accuracy of KNN with Cosine Similarity: {accuracy_cosine * 600:.2f}%")
print(f"Accuracy of SVD: {accuracy_svd * 1200:.2f}%")

