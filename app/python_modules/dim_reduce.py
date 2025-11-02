
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np


class DimensionReducer:
    def __init__(self, output_dim:int):
        self.output_dim = output_dim
    
    def pca(self, data: list):
        # Convert to NumPy array
        X = np.array(data)

        # Standardize (mean=0, variance=1)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply PCA
        pca = PCA(n_components=self.output_dim)
        X_pca = pca.fit_transform(X_scaled)

        return X_pca