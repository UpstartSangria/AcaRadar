from transformer_extractor import extract_keywords_for_papers
from dimension_reducer import build_keyword_counts, logratio_positions


papers_A = journalA_papers = [
    ("Deep Learning for Gene Expression Prediction",
     "We apply deep neural networks to predict gene expression levels from promoter sequences using convolutional layers and attention mechanisms."),
    ("Bayesian Inference of Gene Regulatory Networks",
     "A hierarchical Bayesian framework infers regulatory interactions from RNA-seq time series data, integrating prior biological knowledge."),
    ("Dimensionality Reduction of Proteomics Data",
     "Principal component analysis and autoencoders reveal latent factors explaining variability in protein abundance across tissues."),
    ("Simulation of Evolutionary Pathways",
     "Monte Carlo simulations model the evolution of protein domains under selective pressure and mutation rates."),
    ("Graph Neural Networks for Protein Interaction Mapping",
     "Graph convolutional networks are used to predict protein–protein interactions based on known molecular complexes."),
    ("Unsupervised Clustering of Single-Cell Transcriptomes",
     "We use k-means, spectral clustering, and density-based methods to identify rare cell populations in single-cell RNA-seq data."),
    ("Optimization of CRISPR Off-Target Scoring",
     "A stochastic gradient optimization approach improves CRISPR guide RNA design using large-scale off-target data."),
    ("Variational Autoencoders for Genomic Compression",
     "Variational autoencoders are trained to encode high-dimensional genomic data into compact latent representations for visualization."),
    ("Reinforcement Learning for Experimental Design",
     "An agent-based reinforcement learning model optimizes sequencing experiment selection under limited resources."),
    ("Multimodal Data Fusion via Tensor Decomposition",
     "Tensor factorization integrates gene expression, methylation, and proteomic data to extract shared biological components."),
]



papers_B = journalB_papers = [
    ("Deep Learning for Galaxy Morphology Classification",
     "Convolutional neural networks classify galaxies from imaging surveys, achieving high accuracy compared to human experts."),
    ("Bayesian Inference of Cosmological Parameters",
     "We use hierarchical Bayesian methods with MCMC sampling to constrain dark energy and matter density parameters from CMB data."),
    ("Dimensionality Reduction of Spectroscopic Data",
     "Autoencoders and principal component analysis compress galaxy spectra to identify latent features correlated with star formation rate."),
    ("N-body Simulations of Galaxy Clustering",
     "Large-scale cosmological simulations reproduce galaxy clustering statistics and dark matter halo mass functions."),
    ("Graph Neural Networks for Cosmic Structure Detection",
     "We develop a graph-based neural model that identifies filaments and voids in the cosmic web from 3D simulation data."),
    ("Unsupervised Learning of Exoplanet Populations",
     "We use k-means and Gaussian mixture models to cluster exoplanets based on orbital and stellar properties."),
    ("Optimization of Telescope Scheduling via Reinforcement Learning",
     "A reinforcement learning agent schedules telescope observations under time and weather constraints."),
    ("Variational Autoencoders for Spectral Reconstruction",
     "Autoencoders are trained to denoise and reconstruct incomplete spectral data for faint astronomical sources."),
    ("Simulation-Based Calibration of Gravitational Lensing Models",
     "Monte Carlo simulations are used to calibrate mass modeling pipelines for galaxy cluster lensing."),
    ("Tensor Decomposition for Cosmic Microwave Background Analysis",
     "We apply tensor factorization methods to separate cosmological signals from instrumental noise and foregrounds."),
]





def run_pipeline_shared(journalA_papers, journalB_papers, top_k_per_paper=10):
    kwA_per_paper = extract_keywords_for_papers(journalA_papers, top_k_per_paper)
    kwB_per_paper = extract_keywords_for_papers(journalB_papers, top_k_per_paper)

    kwA = set().union(*kwA_per_paper) if kwA_per_paper else set()
    kwB = set().union(*kwB_per_paper) if kwB_per_paper else set()
    shared = kwA & kwB

    if not shared:
        return {
            "shared_keyword_coords": {},
            "basis": None,
            "shared_keywords": set(),
        }

    vocab, counts = build_keyword_counts(kwA_per_paper, kwB_per_paper)

    keep_idx = [i for i, w in enumerate(vocab) if w in shared]
    if not keep_idx:
        return {
            "shared_keyword_coords": {},
            "basis": None,
            "shared_keywords": set(),
        }
    counts_shared = counts[keep_idx, :]
    vocab_shared = [vocab[i] for i in keep_idx]

    coords, basis = logratio_positions(counts, alpha=0.5)

    shared_keyword_coords = {vocab_shared[i]: (float(coords[i, 0]), float(coords[i, 1]))
                             for i in range(len(vocab_shared))}

    return {
        "shared_keyword_coords": shared_keyword_coords,
        "basis": basis,
        "shared_keywords": set(vocab_shared),
    }

if __name__ == "__main__":
    out = run_pipeline_shared(papers_A, papers_B, top_k_per_paper=8)
    print(f"# shared keywords: {len(out['shared_keywords'])}")
    for k, xy in list(out["shared_keyword_coords"].items())[:10]:
        print(f"{k:40s} -> {xy}")

