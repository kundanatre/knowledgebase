#To know status of all required services at minion
systemctl status docker && systemctl status kubelet && systemctl status flanneld && systemctl status kube-proxy
