# Environment Setup : Kubernetes 1.10.0-1 on Bare Metal

In this article we will `install and setup Kubernetes` on machines manually. We will install Kubernetes to just make it work for a quick testing and hands on. If you wish to install Kubernetes on production environment then refer this guide: [Kubernetes for Production Setup][]

Since this article is about Linux environment which is the defacto for most of the production environments, the steps that we would be performing for the installation should be same on all the flavours of Linux apart from the OS specific commands and configuration if any.

## Prerequisites
 A bit of OS Administration knowledge is desirable although not mandatory for this setup.

+ `Two Linux machines`. Could be even VM's `able to communicate directly even without NAT`.
+ Internet connectivity (internet connectivity is required for installation of softwares directly)
+ `CentOs 7` or later installed on both the machines
+ `Root` Access to both the machines
+ A bit of linux administration knowledge for a specific flavor of linux that you are using.

All commands are performed with `root` user, unless specified explicitly.

## Initial Setup on both the machines  

1. Disable firewall as it conflicts with the kubernetes rules
    ```
    $ systemctl disable firewalld
    $ systemctl stop firewalld
    ```

2. Setup the repository to download Kubernetes binaries
    ```
    $ echo "[kubernetes]" > /etc/yum.repos.d/kubernetes.repo
    $ echo "name=kubernetes" >> /etc/yum.repos.d/kubernetes.repo
    $ echo "baseurl=http://cbs.centos.org/repos/virt7-kubernetes-110-release/x86_64/os/" >> /etc/yum.repos.d/kubernetes.repo
    $ echo "gpgcheck=0" >> /etc/yum.repos.d/kubernetes.repo
    ```

3. Do a quick update and upgrade
    ```
    $ yum clean all
    $ rm -rf /var/cache/yum
    $ yum -y update && yum -y upgrade
    ```

4. Incase if you are not able to connect to the repository or not able to download the softwares, check if a proxy has been set
    ```
    $ env | grep proxy
    ```
   If there is one for the time being disable it by using the command
    ```
    $ unset http_proxy https_proxy
    ```
   Try the step 3 again

5. Optional step: For helping with the command completion install 
    ```
    $ yum -y install bash-completion
    ```

## Kubernetes Setup 

We would be using the below configuration values for the cluster setup  
+ **Pod Network subnet** : `100.64.0.0/16`
+ **Cluster Name** : `k8s.virtual.local`
+ **Cluster IP Range** :`100.65.0.0/24`
+ **Cluster CIDR** : `100.64.0.0/15`, this is always one less than the `Pod Network subnet`

Edit the Hosts file to add the Hostnames and IP's of all the Nodes that would be participating in the Kubernetes cluster  
> File: `/etc/hosts`  
```
127.0.0.1       localhost
10.126.100.243  k8s01
10.126.100.244  k8s02
```

## Master Node Setup  

1. Change the host name to `K8s01`
    ```
     $ hostnamectl set-hostname k8s01
    ```

2. Install the Kubernetes libraries, Installing flannel is optional but we would install it for the sake of symmetry  
    ```
    $ yum -y install kubernetes-master etcd flannel
    ```

3. Create a Kube-Configuration which would be used in the next steps  
    ```
    $ kubectl config set-cluster k8s.virtual.local --server=http://k8s01:8080 
    $ kubectl config set-context k8s.virtual.local --cluster=k8s.virtual.local
    $ kubectl config use-context k8s.virtual.local
    ```
    This should create a Config file under `~/.kube/config` (`/root/.kube/config`) with the contents as below  
    ```
    apiVersion: v1
    clusters:
    - cluster:
        server: http://k8s01:8080
    name: k8s.virtual.local
    contexts:
    - context:
        cluster: k8s.virtual.local
        user: ""
    name: k8s.virtual.local
    current-context: k8s.virtual.local
    kind: Config
    preferences: {}
    users: []
    ```

4. Lets setup `etcd` next by adding the values for the parameters mentioned below  
    > File: `/etc/etcd/etcd.conf`
    ```
    ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379"
    ETCD_NAME="etcd@K8s01"
    ETCD_ADVERTISE_CLIENT_URLS="http://0.0.0.0:2379"
    ```

    Enable and start the service  
    ```
    $ systemctl enable etcd
    $ systemctl start etcd
    $ systemctl status -l etcd
    ```
    Make sure the service has started correctly using the command `journalctl -xeu etcd`  

    Incase if `etcd` is being configured in a clustered mode the check the health of other members with `etcdctl member list` & `etcdctl cluster-health`

5. Configure `Flannel`  
    Flannel uses the **Pod Network subnet** configuration set in the `etcd` to configure a virtual network.  
    Provide the subnet details by issuing the below command   
    ```
    $ etcdctl set /k8s.cluster/network/config '{ "Network": "100.64.0.0/16", "SubnetLen": 24, "Backend": {"Type": "vxlan"} }'
    ```
    Proceed to configuration of `flanneld` by adding the values for the parameters mentioned below
    >File: `/etc/sysconfig/flanneld`
    ```
    FLANNEL_ETCD_ENDPOINTS="http://k8s01:2379"
    FLANNEL_ETCD_PREFIX="/k8s.cluster/network"
    ```

    Enable and start the service  
    ```
    $ systemctl enable flanneld
    $ systemctl start flanneld
    $ systemctl status -l flanneld
    ```
    Make sure the service has started correctly using the command `journalctl -xeu flanneld`
    check if the adapter is set correctly  
    ```
    $ ip -4 -d link show flannel.1
    ```
    This should give an output as below  
    ```
    3: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/ether 4a:8e:3f:c2:7d:0a brd ff:ff:ff:ff:ff:ff promiscuity 0
    vxlan id 1 local 10.126.100.243 dev ens32 srcport 0 0 dstport 8472 nolearning ageing 300 noudpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
    ```  
    Note the `vxlan` and port `8472` in the output  

    A Successful run will also create a file as below  
    > File: `cat /var/run/flannel/subnet.env`  
    ```
    FLANNEL_NETWORK=100.64.0.0/16
    FLANNEL_SUBNET=100.64.33.1/24
    FLANNEL_MTU=1450
    FLANNEL_IPMASQ=false
    ```  

6. Lets configure the Kubernetes services by adding the values for the parameters mentioned below
    >File: `/etc/kubernetes/config` 
    ```
    KUBE_ALLOW_PRIV="--allow-privileged=true"
    KUBE_MASTER="--master=http://k8s01:8080"
    ```

    Configure  `apiServer` by adding the values for the parameters mentioned below
    >File: `/etc/kubernetes/apiserver`
    ```
    KUBE_API_ADDRESS="--insecure-bind-address=0.0.0.0"
    KUBE_API_PORT="--insecure-port=8080"
    KUBELET_PORT="--kubelet-port=10250"
    KUBE_ETCD_SERVERS="--etcd-servers=http://k8s01:2379"
    KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=100.65.0.0/24"
    KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota"
    KUBE_API_ARGS=""
    ```

    Enable and start the service  
    ```
    $ systemctl enable kube-apiserver
    $ systemctl start kube-apiserver
    $ systemctl status -l kube-apiserver
    ```
    Make sure the service has started correctly using the command `journalctl -xeu kube-apiserver`

    Configure of `controller-manager` by adding the values for the parameters mentioned below
    >File: `/etc/kubernetes/controller-manager`
    ```
    KUBE_CONTROLLER_MANAGER_ARGS="--allocate-node-cidrs=true --attach-detach-reconcile-sync-period=1m0s --cluster-cidr=100.64.0.0/16 --cluster-name=k8s.virtual.local --leader-elect=true --kubeconfig=/root/.kube/config --service-cluster-ip-range=100.65.0.0/24"
    ```

    Enable and start the service  
    ```
    $ systemctl enable kube-controller-manager
    $ systemctl start kube-controller-manager
    $ systemctl status -l kube-controller-manager
    ```
    Make sure the service has started correctly using the command `journalctl -xeu kube-controller-manager`

    Configure  `kube-scheduler` by adding the values for the parameters mentioned below
    >File: `/etc/kubernetes/scheduler`
    ```
    KUBE_SCHEDULER_ARGS="--kubeconfig=/root/.kube/config"
    ```

    Enable and start the service  
    ```
    $ systemctl enable kube-scheduler
    $ systemctl start kube-scheduler
    $ systemctl status -l kube-scheduler
    ```
    Make sure the service has started correctly using the command `journalctl -xeu kube-scheduler`

## Minion / Slave Node Setup  

1. Change the host name to `K8s02`
    ```
    $ hostnamectl set-hostname k8s02
    ```
2. Install the Kubernetes libraries  
    ```
    $ yum -y install kubernetes-node flannel
    ```

3. Repeat the steps mentioned in the [Master Node Setup][] Step no 3 on this machine  

4. `Flannel` configuration
    Proceed to configuration of `flanneld` by adding the values for the parameters mentioned below
    >File: `/etc/sysconfig/flanneld`
    ```
    FLANNEL_ETCD_ENDPOINTS="http://k8s01:2379"
    FLANNEL_ETCD_PREFIX="/k8s.cluster/network"
    ```

    Enable and start the service  
    ```
    $ systemctl enable flanneld
    $ systemctl start flanneld
    $ systemctl status -l flanneld
    ```
    Make sure the service has started correctly using the command `journalctl -xeu flanneld`
    check if the adapter is set correctly  
    ```
    $ ip -4 -d link show flannel.1
    ```
    This should give an output as below  
    ```
    3: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default
    link/ether 4a:8e:3f:c2:7d:0a brd ff:ff:ff:ff:ff:ff promiscuity 0
    vxlan id 1 local 10.126.100.243 dev ens32 srcport 0 0 dstport 8472 nolearning ageing 300 noudpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
    ```  
    Note the `vxlan` and port `8472` in the output  

    A Successful run will also create a file as below  
    > File: `cat /var/run/flannel/subnet.env`  
    ```
    FLANNEL_NETWORK=100.64.0.0/16
    FLANNEL_SUBNET=100.64.15.1/24
    FLANNEL_MTU=1450
    FLANNEL_IPMASQ=false
    ```  
    One important point to note here is Flannel creates a Separate subnet `FLANNEL_SUBNET` locally for each node.

5. `Docker` Setup, Proceed to configuration of `docker` by adding the values for the parameters mentioned below
    >File: `/usr/lib/systemd/system/docker.service`
    ```
    EnvironmentFile=/var/lib/flanneld/subnet.env
    ```

    One more additional step that needs to be performed is to create a group for docker and assign users to it as shown below  
    ```
    $ groupadd docker
    $ usermod -aG docker dockerroot
    ```
    Enable and start the service  
    ```
    $ systemctl stop docker
    $ iptables -t nat -F
    $ ip link set docker0 down
    $ systemctl start docker
    $ systemctl is-enabled docker || systemctl enable docker
    ```
    Make sure the service has started correctly using the command `journalctl -xeu docker`
    check if the adapter is set correctly  
    ```
    $ ip -4 addr show
    ```
    This should give an output as below  
    ```
    3: flannel.1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN group default
    inet 100.64.15.0/32 scope global flannel.1
       valid_lft forever preferred_lft forever
    4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
    inet 100.64.15.1/24 scope global docker0
       valid_lft forever preferred_lft forever
    ```  
    Note the `inet 100.64.15.0/32` for `flannel` and `inet 100.64.15.1/24` for `docker` in the output  

6. Lets configure the Kubernetes services by adding the values for the parameters mentioned below
    >File: `/etc/kubernetes/config` 
    ```
    KUBE_ALLOW_PRIV="--allow-privileged=true"
    KUBE_MASTER="--master=http://k8s01:8080"
    ```

    Configure  `kubelet` by adding the values for the parameters mentioned below
    >File: `/etc/kubernetes/kubelet`
    ```
    KUBELET_ADDRESS="--address=0.0.0.0"
    KUBELET_PORT="--port=10250"
    KUBELET_ARGS="--cgroup-driver=systemd --fail-swap-on=false --kubeconfig=/root/.kube/config --container-runtime=docker --docker=unix:///var/run/docker.sock"
    ```

    Enable and start the service  
    ```
    $ systemctl enable kubelet
    $ systemctl start kubelet
    $ systemctl status -l kubelet
    ```
    Make sure the service has started correctly using the command `journalctl -xeu kubelet`

    Configure `kube-proxy` by adding the values for the parameters mentioned below
    >File: `/etc/kubernetes/proxy`
    ```
    KUBE_PROXY_ARGS="--kubeconfig=/var/lib/kubelet/kubeconfig --cluster-cidr=100.64.0.0/16 --proxy-mode=iptables"
    ```

    Enable and start the service  
    ```
    $ systemctl enable kube-proxy
    $ systemctl start kube-proxy
    $ systemctl status -l kube-proxy
    ```
    Make sure the service has started correctly using the command `journalctl -xeu kube-proxy`


## Caveat
Sometimes you may observe that the services failing with the below exception
```
error: Error loading config file "/root/.kube/config": open /root/.kube/config: permission denied
```
In such cases copy the file from `~/.kube/config` to `/etc/kubernetes/kubeconfig' and correct the location of this file in all the services.

## Testing
Logon to the master server and fire the below commands
```
$ kubectl get nodes
```
> Output  
```
NAME      STATUS    ROLES     AGE       VERSION
k8s02     Ready     <none>    17h       v1.10.0
```

```
$ kubectl get all
```
> Output  
```
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   100.65.0.1   <none>        443/TCP   19h
```

```
$ etcdctl member list
```
> Output  
```
8e9e05c52164694d: name=etcd01 peerURLs=http://localhost:2380 clientURLs=http://0.0.0.0:2379 isLeader=true
```

```
$ etcdctl cluster-health
```
> Output  
```
member 8e9e05c52164694d is healthy: got healthy result from http://0.0.0.0:2379
cluster is healthy
```

At this point we are done with the basic setup for Kubernetes Cluster  

[Kubernetes for Production Setup]:#
[Master Node Setup]:##%20Master%20Node%20Setup 