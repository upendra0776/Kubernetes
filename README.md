# Kubernetes
This is my Kubernetes repository video's 
Kubernetes configs
GitHub stars GitHub forks Codacy Badge Lines of Config License My LinkedIn GitHub Last Commit

CI Builds Overview Repo on Azure DevOps Repo on GitHub Repo on GitLab Repo on BitBucket

Kubevious Kustomize Installs Kustomize Namespace Kustomize Objects Namespaced YAML JSON Validation

Pluto Kustomize Nova Checkov Grype Kics Semgrep Semgrep Cloud Trivy

git.io/k8s-configs

Intro
Advanced Kubernetes YAML configurations & templates, based on my experiences running Kubernetes in production at different companies.

The top-level directory contains standard Kubernetes object templates with many Best Practices, Tips & Tricks learned over time across production environments.

The sub-directories contain ready-to-run real world apps that I've run across environments.

Templates
Start with deployment.yaml / statefulset.yaml, for advanced users see kustomization.yaml.

The service.yaml and ingress.yaml configs contain settings for using static public IP addresses and locking down your cloud load balancer's firewall rules eg. to private IP addresses, and patches for Cloudflare Proxied or VPN IPs. You may need to extend those IP lists to your office / VPN / public addresses if really want to permit direct internet access to your ingresses and aren't proxying them through a WAF in proxied mode etc.

Apps
Real-world app deployments are found in the more specific <app>/ directories.

These follow the standard Kustomize <app>/base/ and <app>/overlay/ layout to make it easy to use as-is by just tweaking a couple settings in the overlay to your specific environment.

CI/CD
Advanced auto-scaling production-grade CI/CD on Kubernetes:

ArgoCD - deployment, configs and optimizations. Start here: argocd/base/kustomization.yaml
Jenkins - jenkins server and dynamically scaling agents on kubernetes. Start here: jenkins/base/kustomization.yaml
see also: Jenkins repo with advanced Jenkinsfile & Jenkins Shared Library
TeamCity - teamcity server and dynamically scaling agents on kubernetes. Start here: teamcity/base/kustomization.yaml
Selenium Grid - simple and distributed auto-scaling deployments. Start here: selenium-grid/base/kustomization.yaml / selenium-grid-distributed/base/kustomization.yaml
Helm + Kustomize integration
See kustomization.yaml for 2 methods provided:

template the Helm chart using a values.yaml to Git and serve from there (see DevOps Bash Tools for the helm_template.sh convenience script)
dynamically load the Helm chart from upstream with a values.yaml
...then patch override anything the chart doesn't directly support using the standard Kustomize patching examples given in the kustomization.yaml.

Production Ready Checklist
Healthchecks - readiness/liveness probes, see deployment.yaml
Horizontal Pod Autoscaler - horizontal-pod-autoscaler.yaml
Pod Disruption Budget - pod-disruption-budget.yaml
Pod Anti-Affinity - stable vs preemptible, HA across AZs, see deployment.yaml
Ingress Controllers - Nginx (config), Kong (config) or Traefik (config)
Ingress SSL - Cert Manager (config) for Automatic Certificate Management using the popular free Let's Encrypt certificate authority
App Lifecycle Management - ArgoCD (config)
App Ingresses - ingress.yaml, */base/ingress.yaml
App Resources - see resources section in deployment.yaml
App Right-Sizing - Goldilocks (config) to generate VPAs and resource recommendations
DNS - External DNS (config) integration to AWS Route53, Cloudflare etc.
Secrets - External Secrets (config) integration to AWS Secrets Manager, GCP Secret Manager etc. or Sealed Secrets (config)
Resource Quotas per Namespace - resource-quota.yaml
Limit Ranges - per object limits within a namespace - limit-range.yaml
Network Policies - network-policy.yaml
Pod Security Policies - pod-security-policy.yaml
Governance, Security & Best Practices - Polaris (config) for recommendations
Find Deprecated API objects to replace - Pluto - see pluto_detect_kustomize_materialize.sh and pluto_detect_kubectl_dump_objects.sh in the DevOps Bash Tools repo
Quickly update any Helm Charts in a kustomization.yaml file using kustomize_update_helm_chart_versions.sh in the DevOps Bash Tools repo
Further Documention
The best documentation links are provided at the top of each yaml for fast referencing (my advanced .vimrc can open these URLs from the current file via a hotkey!)

Extra Docs
Datree Kubernetes ArgoCD best practices

Environment Enhancements
.envrc - use with direnv to auto-load correct Kubernetes context isolated to current shell to avoid race conditions between shells and scripts caused by naively changing the global ~/.kube/config context

Shortcut symlinks are for faster instantiation from these configs using the standard kubernetes shortcuts such as new pvc.yaml - see the Templates repo for more details on the new command to fast create new files from templates.

Diagrams
For more amazing diagrams see HariSekhon/Diagrams-as-Code

Kubernetes Deployment with Horizontal Pod Autoscaler and Ingress
deployment.yaml
horizontal-pod-autoscaler.yaml
ingress.yaml


Kubernetes Stateful Architecture with persistent volumes
statefulset.yaml
persistent-volume-claim.yaml
persistent-volume.yaml


Kubernetes Service External Traffic Policy
service.yaml


Kubernetes on Premise
GitHub repo: HariSekhon/HAProxy-configs


with MetalLB:

metal-lb/base/*.yaml
Is it just me or do MetaLB think they're Starfleet? (compare their logos)



Traefik Ingress on GKE
A Traefik deployment I did for a client using:

traefik/base/*.yaml
traefik-hub-agent/base/*.yaml


alternative diagram:



Kong API Gateway on AWS EKS
A Kong API Gateway deployment I did for a client using:

kong/base/*.yaml
cert-manager/base/*.yaml
argocd/base/*.yaml


Jenkins on Kubernetes
A production Jenkins on Kubernetes I built for a client with auto-spawning agents for horizontal scaling and integration with Docker, SonarQube, Clair, Grype and Trivy for code & container scanning.

jenkins/base/*.yaml - core config that is inherited by all environments
jenkins/overlay/*.yaml - environment specific settings like ingress address, NFS server mount on agents
claire/base/*.yaml
sonarqube/base/*.yaml
trivy/base/*.yaml
GitHub repo: HariSekhon/Jenkins
Advanced Jenkinsfile
Groovy Shared Library with the code & container scanning functions
clair.groovy
grype.groovy
trivy.groovy, trivyFS.groovy, trivyImages
gcrDockerAuth.groovy, garDockerAuth.groovy
among others in vars/ and don't forget about the epic Jenkinsfile


screenshot:



OpenTSDB on Kubernetes and HBase
A high scale production OpenTSDB replatform I did to Kubernetes for a client, ingesting 9 billion data points per day and serving 3 million queries per day.

I also had to do advanced performance tuning of their production HBase cluster which was suffering from frequent outages at this scale due to being set up by a non-SME on the wrong hardware (I had to make do with the existing hardware of course).

This was the second client I did in-depth performance tuning of HBase for - I've published a selection of useful HBase tools - see hbase_*.py and opentsdb_*.py in my DevOps Python tools repo.



History
Forked from the Templates repo.

Related Repositories
DevOps Bash Tools - 1000+ DevOps Bash Scripts, Advanced .bashrc, .vimrc, .screenrc, .tmux.conf, .gitconfig, CI configs & Utility Code Library - AWS, GCP, Kubernetes, Docker, Kafka, Hadoop, SQL, BigQuery, Hive, Impala, PostgreSQL, MySQL, LDAP, DockerHub, Jenkins, Spotify API & MP3 tools, Git tricks, GitHub API, GitLab API, BitBucket API, Code & build linting, package management for Linux / Mac / Python / Perl / Ruby / NodeJS / Golang, and lots more random goodies

Jenkins - Advanced Jenkinsfile & Jenkins Groovy Shared Library

GitHub-Actions - GitHub Actions master template & GitHub Actions Shared Workflows library

Terraform - Terraform templates for AWS / GCP / Azure / GitHub management

Templates - dozens of Code & Config templates - AWS, GCP, Docker, Jenkins, Terraform, Vagrant, Puppet, Python, Bash, Go, Perl, Java, Scala, Groovy, Maven, SBT, Gradle, Make, GitHub Actions Workflows, CircleCI, Jenkinsfile, Makefile, Dockerfile, docker-compose.yml, M4 etc.

SQL Scripts - 100+ SQL Scripts - PostgreSQL, MySQL, AWS Athena, Google BigQuery

DevOps Python Tools - 80+ DevOps CLI tools for AWS, GCP, Hadoop, HBase, Spark, Log Anonymizer, Ambari Blueprints, AWS CloudFormation, Linux, Docker, Spark Data Converters & Validators (Avro / Parquet / JSON / CSV / INI / XML / YAML), Elasticsearch, Solr, Travis CI, Pig, IPython

DevOps Perl Tools - 25+ DevOps CLI tools for Hadoop, HDFS, Hive, Solr/SolrCloud CLI, Log Anonymizer, Nginx stats & HTTP(S) URL watchers for load balanced web farms, Dockerfiles & SQL ReCaser (MySQL, PostgreSQL, AWS Redshift, Snowflake, Apache Drill, Hive, Impala, Cassandra CQL, Microsoft SQL Server, Oracle, Couchbase N1QL, Dockerfiles, Pig Latin, Neo4j, InfluxDB), Ambari FreeIPA Kerberos, Datameer, Linux...

The Advanced Nagios Plugins Collection - 450+ programs for Nagios monitoring your Hadoop & NoSQL clusters. Covers every Hadoop vendor's management API and every major NoSQL technology (HBase, Cassandra, MongoDB, Elasticsearch, Solr, Riak, Redis etc.) as well as message queues (Kafka, RabbitMQ), continuous integration (Jenkins, Travis CI) and traditional infrastructure (SSL, Whois, DNS, Linux)

Nagios Plugin Kafka - Kafka API pub/sub Nagios Plugin written in Scala with Kerberos support

HAProxy Configs - 80+ HAProxy Configs for Hadoop, Big Data, NoSQL, Docker, Elasticsearch, SolrCloud, HBase, Cloudera, Hortonworks, MapR, MySQL, PostgreSQL, Apache Drill, Hive, Presto, Impala, ZooKeeper, OpenTSDB, InfluxDB, Prometheus, Kibana, Graphite, SSH, RabbitMQ, Redis, Riak, Rancher etc.

Dockerfiles - 50+ DockerHub public images for Docker & Kubernetes - Hadoop, Kafka, ZooKeeper, HBase, Cassandra, Solr, SolrCloud, Presto, Apache Drill, Nifi, Spark, Mesos, Consul, Riak, OpenTSDB, Jython, Advanced Nagios Plugins & DevOps Tools repos on Alpine, CentOS, Debian, Fedora, Ubuntu, Superset, H2O, Serf, Alluxio / Tachyon, FakeS3

HashiCorp Packer templates - Linux automated bare-metal installs and portable virtual machines OVA format appliances using HashiCorp Packer, Redhat Kickstart, Debian Preseed and Ubuntu AutoInstaller / Cloud-Init

Diagrams-as-Code - Cloud & Open Source architecture diagrams with Python & D2 source code provided - automatically regenerated via GitHub Actions CI/CD - AWS, GCP, Kubernetes, Jenkins, ArgoCD, Traefik, Kong API Gateway, Nginx, Redis, PostgreSQL, Kafka, Spark, web farms, event processing...

Knowledge-Base - IT Knowledge Base from 20 years in DevOps, Linux, Cloud, Big Data, AWS, GCP etc.

Stargazers over time

git.io/k8s-configs
