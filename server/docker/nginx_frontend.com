upstream server_cluster {
#   server 127.0.0.1:9000;
#   server 127.0.0.1:9001;
    <%Clusters%>
}


server {
    listen 80 default_server;
    access_log /var/log/nginx/localhost.access.log;

    location / {
        proxy_pass http://server_cluster;
        include /etc/nginx/proxy_params;
    }
}
