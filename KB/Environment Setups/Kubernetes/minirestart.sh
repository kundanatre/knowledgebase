#To restart minion services
systemctl restart kubelet
systemctl status kubelet
systemctl restart docker
systemctl status docker
systemctl restart flanneld
systemctl status flanneld
systemctl restart kube-proxy
systemctl status kube-proxy
