# Stop all services at minion
systemctl stop kubelet
systemctl status kubelet
systemctl stop docker
systemctl status docker
systemctl stop flanneld
systemctl status flanneld
systemctl stop kube-proxy
systemctl status kube-proxy
