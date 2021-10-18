%data = load('abalone.data','-ascii')
addpath(genpath('G:\grade3\up\visualization technology\visualization-technology\exp\exp3\drtoolbox.tar\drtoolbox\drtoolbox'))
data_origin = importdata('abalone.data')

[mappeddata_PCA,mapping_PCA] = compute_mapping(data_origin.data,'PCA',3)
%gscatter(mappeddata_PCA(:,1),mappeddata_PCA(:,2),data_origin.textdata)


%[mappeddata_Isomap,mapping_Isomap] = compute_mapping(data_origin.data,'Isomap')
%gscatter(mappeddata_Isomap(:,1),mappeddata_Isomap(:,2))


%[mappeddata_SNEp,mapping_SNE] = compute_mapping(data_origin.data,'SNE')
%gscatter(mappeddata_SNEp(:,1),mappeddata_SNEp(:,2),data_origin.textdata)