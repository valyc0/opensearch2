docker run -d \
  --name=filebeat \
  --network=mynet \
  --user=root \
  --volume="$(pwd)/filebeat.docker.yml:/usr/share/filebeat/filebeat.yml:ro" \
  --volume="/var/lib/docker/containers:/var/lib/docker/containers:ro" \
  --volume="/var/run/docker.sock:/var/run/docker.sock:ro" \
  --volume="$(pwd)/test:/usr/share/filebeat/test" \
  --name filebeat \
  docker.elastic.co/beats/filebeat:7.10.2 filebeat -e -strict.perms=false \
  -E output.logstash.hosts=["logstash:5044"]

