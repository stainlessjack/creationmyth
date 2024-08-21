# Create GKE Cluster:
[GCP Lab](https://www.cloudskillsboost.google/focuses/878?catalog_rank=%7B%22rank%22%3A1%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&parent=catalog&search_id=19690440)

	gcloud config set compute/region
	gcloud config set compute/zone
	gcloud container clusters create --machine-type=e2-medium --zone= lab-cluster
	gcloud container clusters get-credentials lab-cluster
	kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0

This Kubernetes command creates a Deployment object that represents hello-server.
In this case, --image specifies a container image to deploy.
The command pulls the example image from a Container Registry bucket.
gcr.io/google-samples/hello-app:1.0 indicates the specific image version to pull.
If a version is not specified, the latest version is used.

	kubectl expose deployment hello-server --type=LoadBalancer --port 8080
	kubectl get service

This should result in an EXTERNAL_IP which you can use to check the new service from a browser.

	http://[EXTERNAL-IP]:8080

To delete the cluster

	gcloud container clusters delete lab-cluster

# Setting Up Load Balancers
[GCP Lab](https://www.cloudskillsboost.google/focuses/12007?catalog_rank=%7B%22rank%22%3A3%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&parent=catalog&search_id=19690497)
## Traditional Load Balancer
Run for ww1, ww2, and ww3 to create 3 VMs running apache

    gcloud compute instances create www1 \
        --zone= \
        --tags=network-lb-tag \
        --machine-type=e2-small \
        --image-family=debian-11 \
        --image-project=debian-cloud \
        --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install apache2 -y
    service apache2 restart
    echo "<h3>Web Server: www1</h3>" | tee /var/www/html/index.html'

Create firewall rules.

    gcloud compute firewall-rules create www-firewall-network-lb \
        --target-tags network-lb-tag --allow tcp:80

Verify traffic is flowing.

    gcloud compute instances list
    curl http://[IP_ADDRESS]

Create external IP, add health check server, create target pool, add instances to pool, add forwarding rule.

    gcloud compute addresses create network-lb-ip-1 \
        --region
    gcloud compute http-health-checks create basic-check
    gcloud compute target-pools create www-pool \
        --region  --http-health-check basic-check
    gcloud compute target-pools add-instances www-pool \
        --instances www1,www2,www3
    gcloud compute forwarding-rules create www-rule \
        --region   \
        --ports 80 \
        --address network-lb-ip-1 \
        --target-pool www-pool

Send traffic to test!

    gcloud compute forwarding-rules describe www-rule --region 
    IPADDRESS=$(gcloud compute forwarding-rules describe www-rule --region  --format="json" | jq -r .IPAddress)
    echo $IPADDRESS
    while true; do curl -m1 $IPADDRESS; done

## HTTP Load Balancer
This type of load balancer will ensure that specified URLs are routed to correct instance group, or that users are
routed to servers closest to them.

Start by creating the LB template.

    gcloud compute instance-templates create lb-backend-template \
       --region= \
       --network=default \
       --subnet=default \
       --tags=allow-health-check \
       --machine-type=e2-medium \
       --image-family=debian-11 \
       --image-project=debian-cloud \
       --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install apache2 -y
    a2ensite default-ssl
    a2enmod ssl
    vm_hostname="$(curl -H "Metadata-Flavor:Google" \
    http://169.254.169.254/computeMetadata/v1/instance/name)"
    echo "Page served from: $vm_hostname" | \
    tee /var/www/html/index.html
    systemctl restart apache2'

Create instance group, firewall rules, external IP, and healthcheck for the LB.

    gcloud compute instance-groups managed create lb-backend-group \
        --template=lb-backend-template --size=2 --zone= 
    gcloud compute firewall-rules create fw-allow-health-check \
        --network=default \
        --action=allow \
        --direction=ingress \
        --source-ranges=130.211.0.0/22,35.191.0.0/16 \
        --target-tags=allow-health-check \
        --rules=tcp:80
    gcloud compute addresses create lb-ipv4-1 \
        --ip-version=IPV4 \
        --global
    gcloud compute addresses describe lb-ipv4-1 \
        --format="get(address)" \
        --global
    gcloud compute health-checks create http http-basic-check \
        --port 80

Create backend service, URL map and proper routing.

    gcloud compute backend-services create web-backend-service \
        --protocol=HTTP \
        --port-name=http \
        --health-checks=http-basic-check \
        --global
    gcloud compute backend-services add-backend web-backend-service \
        --instance-group=lb-backend-group \
        --instance-group-zone= \
        --global
    gcloud compute url-maps create web-map-http \
        --default-service web-backend-service
    gcloud compute target-http-proxies create http-lb-proxy \
        --url-map web-map-http
    gcloud compute forwarding-rules create http-content-rule \
        --address=lb-ipv4-1\
        --global \
        --target-http-proxy=http-lb-proxy \
        --ports=80
