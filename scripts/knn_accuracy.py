import numpy as np
from scipy import sparse
from sklearn.neighbors import NearestNeighbors
import sys
import run_sklearn

# Usage:
# - From command line: 
#     python knn_accuracy.py path_to_input_data path_to_chens_output k d N
#     example: python knn_accuracy.py ../data/frey.dat ../data/frey.knn 12 560 1965
# - In interpreter: 
#     knn_accuracy.compare_chen(path_to_input_data, path_to_chens_output, k, d, N)
#     example: knn_accuracy.compare_chen('../data/frey.dat', '../data/frey.knn', 12, 560, 1965)

def get_accuracy(data_file, knn_output, alg, k, d, N):
  # Get ground truth
  print "getting ground truth"
  ground_truth = run_sklearn.get_knn_graph(data_file, k, d, N, 'brute')
  print "finished getting ground truth"
  
  if alg == "chen":
    # Get knn graph file in numpy array
    print "creating numpy knn graph from chen's output"
    knn_graph = np.zeros((N,N), dtype=np.int)
    print "created graph; opening file to fill graph"
    with open(knn_output, 'r') as f:
      for line in f:
        line.strip()
        line = line.split()
        j = int(line[0]) - 1
        i = int(line[1]) - 1
        knn_graph[i][j] = 1
    print "finished reading file, converting to sparse matrix"
    knn_sparse = sparse.csr_matrix(knn_graph)
    print "finished converting to sparse matrix"

  elif alg == "sklearn":
    knn_sparse = knn_output

  print "getting n_correct"
  # n_correct = np.where(ground_truth == knn_sparse)[0].size
  # accuracy = n_correct/(N*N+0.0)
  n_incorrect = (ground_truth - knn_sparse).nnz
  accuracy = 1 - n_incorrect/(N*N+0.0)
  return accuracy

def compare_chen(input_data, chen_output, k, d, N):
  # Chen's approach:
  chen_accuracy = get_accuracy(input_data, chen_output, 'chen', k, d, N)
  print "Chen's approach: \taccuracy = ", chen_accuracy

  # Scikit-learn's approach, using kd-tree:
  # g = run_sklearn.get_knn_graph(input_data, k, d, N, 'kd_tree')
  # sklearn_accuracy = get_accuracy(input_data, g, 'sklearn', k, d, N)
  # print "Scikit-learn's kd-tree: accuracy = ", sklearn_accuracy

if __name__ == '__main__':
  compare_chen(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))