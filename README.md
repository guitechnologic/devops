# DevOps Local Lab – Kubernetes & Observability

Este repositório documenta um **laboratório DevOps completo**, executado em **cluster Kubernetes local (Docker Desktop)**, com foco em **boas práticas reais de mercado**, automação e observabilidade.

## 🎯 Objetivo
Demonstrar domínio prático de:
- Kubernetes
- CI/CD com GitLab
- Observabilidade (Prometheus, Grafana, Loki)
- Infraestrutura como Código (Terraform e Ansible)
- GitOps e automação

Tudo organizado, versionado e reproduzível.

---

## 🧱 Arquitetura

- **Cluster:** Kubernetes local (Docker Desktop)
- **Namespaces separados por responsabilidade**
- **CI/CD:** GitHub (código) + GitLab (pipelines)
- **Deploy:** Kubernetes manifests / Helm
- **Observabilidade:** Prometheus, Grafana, Loki

---

## 📦 Estrutura do Repositório

```text
devops/
├── kubernetes/
│   ├── namespaces/
│   │   └── observability.yaml
│   ├── observability/
│   │   ├── prometheus/
│   │   ├── grafana/
│   │   └── loki/
│   └── apps/
├── ci/
├── docker/
├── terraform/
├── ansible/
└── README.md
