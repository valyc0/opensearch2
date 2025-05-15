HOME_DIR=$PWD

cd $HOME_DIR/opensearch/ && ./install.sh
cd $HOME_DIR/nginx/ && ./install.sh
cd $HOME_DIR/logstash/ && ./install.sh
cd $HOME_DIR/filebeat/ && ./install.sh