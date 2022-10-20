!# /bin/bash
mkdir data
cd data
wget https://data.mendeley.com/public-files/datasets/4drtyfjtfy/files/a03e6097-f7fb-4e1a-9c6a-8923c6a0d3e0/file_downloaded -O archive.zip
unzip archive.zip -d .
rm archive.zip
cd ..
ls ./data/dataset2/*.jpg > data/image_list.txt
