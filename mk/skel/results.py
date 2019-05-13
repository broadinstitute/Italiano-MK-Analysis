import os

import pandas as pd
from matplotlib import pyplot as plt
import networkx as nx
from sklearn.manifold import TSNE

from utils import tools
from utils.folder import Folder
from utils.results import ResultsDF, ResultsImage, ResultsObject

class SkelImage(ResultsImage):
    def __init__(self, path, csv, time):
        super(SkelImage, self).__init__(path, csv, time)

    def analyze(self):
        x = self.cols(self._df, ['Metadata_Well','Metadata_Site','Metadata_Time','ImageNumber',
        'FileName_phase','AreaOccupied_AreaOccupied_protrusion_mask','Count_protrusion_mask','Count_pplt_obj'])
        x = self.sort_df(x)
        x.to_csv(self.path + os.sep + 'ImageResults.csv')
        return x

class ProtrusionMask(ResultsObject):
    def __init__(self, path, csv, time, object_name):
        super(ProtrusionMask, self).__init__(path, csv, time, object_name)

    def analyze(self):
        x = self.cols(self._df, ['Metadata_Well','Metadata_Site','Metadata_Time','ImageNumber',
        'ObjectNumber','Parent_pplt_obj','Parent_protrusion','Location_Center_X','Location_Center_Y'])
        x = self.sort_df(x)
        x.to_csv(self.path + os.sep + self.object_name + 'Results.csv')

        return x

class ProtrusionSeed(ResultsObject):
    def __init__(self, path, csv, time, object_name):
        super(ProtrusionSeed, self).__init__(path, csv, time, object_name)

    def analyze(self):
        x = self.cols(self._df, ['Metadata_Well','Metadata_Site','Metadata_Time','ImageNumber',
        'ObjectNumber','Location_Center_X','Location_Center_Y',
        'ObjectSkeleton_NumberBranchEnds_protrusion_mask_image',
        'ObjectSkeleton_NumberNonTrunkBranches_protrusion_mask_image',
        'ObjectSkeleton_NumberTrunks_protrusion_mask_image',
        'ObjectSkeleton_TotalObjectSkeletonLength_protrusion_mask_image'])

        x = x[x['ObjectSkeleton_TotalObjectSkeletonLength_protrusion_mask_image'] > 0]
        x = self.sort_df(x)
        x.to_csv(self.path + os.sep + self.object_name + 'Results.csv')

        return x

class PpltObj(ResultsObject):
    def __init__(self, path, csv, time, object_name):
        super(PpltObj, self).__init__(path, csv, time, object_name)

    def analyze(self):
        x = self.cols(self._df, ['Metadata_Well','Metadata_Site','Metadata_Time','ImageNumber',
        'ObjectNumber','Location_Center_X','Location_Center_Y','Mean_protrusion_mask_Location_Center_X',
        'Mean_protrusion_mask_Location_Center_Y','Children_protrusion_mask_Count'])

        x = self.sort_df(x)
        x.to_csv(self.path + os.sep + self.object_name + 'Results.csv')

        return x

class Edges(ResultsObject):
    def __init__(self, path, csv, time, object_name):
        super(Edges, self).__init__(path, csv, time, object_name)
    
    def analyze(self):
        edges = self._df
        edges = edges.drop(['total_intensity'],axis=1)
        edges.columns = ['ImageNumber', 'Node_1', 'Node_2', 'Distance']
        edges_df = edges[['Node_1','Node_2','Distance','ImageNumber']]

        edges_df = edges_df.set_index('ImageNumber')
        edges_df.to_csv(self.path + os.sep + self.object_name + 'Results.csv')

        return edges_df

class Vertices(ResultsObject):
    def __init__(self, path, csv, time, object_name):
        super(Vertices, self).__init__(path, csv, time, object_name)

    def analyze(self):
        vertices = self._df
        # Rename i,j to y,x
        vertices.columns = ['image_number', 'vertex_number','y','x','labels','kind']
        # Swap y,x to x,y
        vertices_df = vertices[['vertex_number', 'x','y','labels', 'kind','image_number']]
        # Rename csv columns
        vertices_df.columns = ['Node','x','y','Labels','Kind','ImageNumber']

        vertices_df = vertices_df.set_index('ImageNumber')
        vertices_df.to_csv(self.path + os.sep + self.object_name + 'Results.csv')

        return vertices_df

# class AnalyzeSkel(ResultsDF):
#     def __init__(self, path, csv, time):
#         super(AnalyzeSkel, self).__init__(path, csv, time)
#         self.edges_df = pd.DataFrame()
#         self.vertices_df = pd.DataFrame()
 
#     def analyze(self, output_folder):
#         # self.embed_skel(edges_df, vertices_df)

#     # slice edgelist/nodelist via df by column title, ImageNumber
#     @staticmethod
#     def slice_by_image(dataframe,timepoint): 
#         df = dataframe[dataframe["ImageNumber"] == timepoint]

#         return df
        
#     # plot tsne using edgelist & nodelist
#     @staticmethod
#     def embed_skel(edges_df, vertices_df, graph_folder, single_list, timepoints): 
#         n = 1
#         for n in range(timepoints + 1):
#             edge = self.slice_by_image(edges_df, n)
#             # Drop nodes connected to themselves - usually a branch point #
#             edge.drop(edge.loc[edge["Node_1"] == edge["Node_2"]].index.tolist(), inplace=True)

#             node = self.slice_by_image(vertices_df, n)

#             G = nx.Graph()
#             # Add edge attributes #
#             for i, edge_row in edge.iterrows():
#                     G.add_edge(edge_row[0], edge_row[1], attr_dict=edge_row[2:].to_dict())

#             # Add node attributes #
#             for i, node_row in node.iterrows():
#                 try:
#                     G.node[node_row['Node']].update(node_row[1:].to_dict())
#                 except KeyError:
#                     pass
            
#             array = nx.to_numpy_array(G)
#             node_num, embedding_dimension = array.shape
#             if(embedding_dimension > 2):
#                 print("|Embedding skeleton via tSNE: Image {0}..".format(n))
#                 model = TSNE(n_components=2)
#                 node_pos = model.fit_transform(array)

#                 pos = {}
#                 for i in range(node_num):
#                     pos[i] = node_pos[i, :]

#                 plt.figure(figsize=(8, 12))
#                 plt.scatter(node_pos[:, 0], node_pos[:, 1])

#                 single_list_noext = tools.drop_extensions(single_list)
#                 plt.title(single_list_noext[n-1], size=15)
        
#                 plt.savefig(graph_folder + os.sep + single_list_noext[n-1] + '.png', bbox_inches='tight')
#                 plt.close()
#                 n += 1
