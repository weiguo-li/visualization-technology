addpath(genpath('G:\grade3\up\visualization technology\visualization-technology\exp\exp3\drtoolbox.tar\drtoolbox\drtoolbox'))
%load data
train_images = loadMNISTImages('train-images.idx3-ubyte');
train_labels = loadMNISTLabels('train-labels.idx1-ubyte');

%select 6k record
origin_data = train_images(:,1:6000)';
origin_label = train_labels(1:6000)';

Y = tsne(origin_data);
gscatter(Y(:,1),Y(:,2),origin_label)

%[mappedData ,mapping] = compute_mapping(origin_data,'tsne')








