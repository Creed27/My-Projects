#ifndef V4_0_0_GRAPH_H
#define V4_0_0_GRAPH_H

#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

typedef unsigned char uchar;
typedef unsigned int uint;
using ui = unsigned int;

#define INSERTION_SORT(type, arr, arr_len, swap_condition) do { \
		for (int i=1; i<arr_len; i++) {                             \
			for (int j=i; j>=1; j--) {                              \
				if (swap_condition) {                               \
					type tmp = arr[j-1];                            \
					arr[j-1] = arr[j];                              \
					arr[j] = tmp;                                   \
				} else {                                            \
					break;                                          \
				}                                                   \
			}                                                       \
		}                                                           \
} while(0);


struct Graph {
    int n;
    std::vector<std::vector<unsigned int>> adjmat;
    std::vector<unsigned int> label;
    unsigned int *degree;
    unsigned int **adjlist;
    Graph(unsigned int n);
};

Graph induced_subgraph(struct Graph& g, std::vector<int> vv);

Graph readGraph(char* filename, char format, bool directed, bool edge_labelled, bool vertex_labelled);

void set_adjlist(struct Graph & g);

void GetEqClass(Graph & g, ui *&EqClass);


#endif //V4_0_0_GRAPH_H
