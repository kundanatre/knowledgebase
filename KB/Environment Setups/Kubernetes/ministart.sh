#To start minion services
systemctl start kubelet
systemctl status kubelet
systemctl start docker
systemctl status docker
systemctl start flanneld
systemctl status flanneld
systemctl start kube-proxy
systemctl status kube-proxy
