%data = load('abalone.data','-ascii')
addpath(genpath('D:\grade3\VisulizationTechnology\visualization-technology\exp\exp3\drtoolbox.tar\drtoolbox\drtoolbox'))
data_origin = importdata('abalone.data')

[mappeddata_PCA,mapping_PCA] = compute_mapping(data_origin.data,'PCA')

[mappeddata_Isomap,mapping_Isomap] = compute_mapping(data_origin.data,'Isomap')

[mappeddata_SNEp,mapping_SNE] = compute_mapping(data_origin.data,'SNE')