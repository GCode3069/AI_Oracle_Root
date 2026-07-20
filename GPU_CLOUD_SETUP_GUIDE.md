# GPU Cloud Setup Guide

Complete guide for setting up GPU cloud providers with the Ultimate Viral Roast Factory.

## Overview

The system supports three GPU provider tiers:

| Priority | Provider | Cost | Speed | Use Case |
|----------|----------|------|-------|----------|
| **HIGH** | HAMi Local | FREE | Fastest | You have local GPU access |
| **MEDIUM** | SkyPilot | ~$0.10/min | Fast | Auto-route to cheapest cloud |
| **LOW** | Akash | ~$0.05/min | Good | Decentralized P2P marketplace |

---

## Option 1: HAMi Local (FREE - Recommended if you have GPU)

**What is HAMi?**
HAMi (Heterogeneous AI Computing Virtualization Middleware) allows sharing a single GPU across multiple Kubernetes pods.

### Prerequisites
- Local GPU (NVIDIA recommended)
- Kubernetes cluster (can be local with minikube/kind)
- NVIDIA drivers installed

### Installation

#### Step 1: Install kubectl
```bash
# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# macOS
brew install kubectl

# Windows (PowerShell as admin)
choco install kubernetes-cli
```

#### Step 2: Set up local Kubernetes
```bash
# Option A: Using minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --driver=docker --gpus all

# Option B: Using kind
kind create cluster --config=- <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraMounts:
  - hostPath: /dev/nvidia0
    containerPath: /dev/nvidia0
  - hostPath: /dev/nvidiactl
    containerPath: /dev/nvidiactl
  - hostPath: /dev/nvidia-uvm
    containerPath: /dev/nvidia-uvm
EOF
```

#### Step 3: Install HAMi
```bash
# Install HAMi operator
kubectl apply -f https://raw.githubusercontent.com/Project-HAMi/HAMi/master/deployment/operator.yaml

# Verify installation
kubectl get pods -n hami-system
```

#### Step 4: Verify GPU access
```bash
kubectl get nodes
kubectl describe node <node-name> | grep -i nvidia
```

### Usage with Viral Roast Factory
```powershell
# In launcher, choose option 4
# Or directly:
python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(use_gpu_cloud=True); f.generate_viral_roast(priority='high')"
```

**Pros:**
- ✅ FREE (uses your own hardware)
- ✅ Fastest (no network latency)
- ✅ Full control
- ✅ No cloud costs

**Cons:**
- ❌ Requires local GPU
- ❌ Initial setup complexity
- ❌ Limited to your hardware

---

## Option 2: SkyPilot (EASIEST - Recommended for beginners)

**What is SkyPilot?**
SkyPilot automatically finds the cheapest GPU across AWS, GCP, Azure, Lambda Labs, and more.

### Installation

#### Step 1: Install SkyPilot
```bash
pip install "skypilot[all]"

# Or for specific clouds:
pip install "skypilot[aws]"  # AWS only
pip install "skypilot[gcp]"  # Google Cloud only
pip install "skypilot[azure]"  # Azure only
```

#### Step 2: Configure cloud credentials

**For AWS:**
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter default region (e.g., us-east-1)
```

**For GCP:**
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

**For Azure:**
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login
```

#### Step 3: Verify setup
```bash
# Check which clouds are configured
sky check

# Should show green checkmarks for configured clouds
```

#### Step 4: Test with a simple task
```bash
# Launch a test GPU instance
sky launch --gpus V100:1 --cloud aws

# SkyPilot will automatically find the cheapest option
```

### Usage with Viral Roast Factory
```powershell
# In launcher, choose option 5
# Or directly:
python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(use_gpu_cloud=True); f.generate_viral_roast(priority='medium')"
```

**Pros:**
- ✅ Automatically finds cheapest GPU
- ✅ Multi-cloud support
- ✅ Easy to use
- ✅ Good documentation

**Cons:**
- ❌ Requires cloud account
- ❌ Costs money (but optimized)
- ❌ Network latency

**Pricing Examples:**
- V100 GPU: $0.74 - $2.48/hour (SkyPilot finds cheapest)
- T4 GPU: $0.35 - $0.95/hour
- A100 GPU: $1.10 - $4.13/hour

---

## Option 3: Akash Network (CHEAPEST - Decentralized)

**What is Akash?**
Akash is a decentralized cloud marketplace where providers compete on price. Often 3-5x cheaper than AWS/GCP.

### Installation

#### Step 1: Install Akash CLI
```bash
# Linux/macOS
curl -sSfL https://raw.githubusercontent.com/akash-network/node/master/install.sh | sh

# Verify installation
akash version
```

#### Step 2: Create Akash wallet
```bash
# Create new wallet
akash keys add default

# IMPORTANT: Save your mnemonic phrase!
# You'll need it to recover your wallet
```

#### Step 3: Fund your wallet
```bash
# Get your wallet address
akash keys show default -a

# Buy AKT tokens from an exchange (e.g., Kraken, Gate.io)
# Send AKT to your wallet address
# Minimum: ~10 AKT to get started

# Check balance
akash query bank balances $(akash keys show default -a)
```

#### Step 4: Create deployment certificate
```bash
# Generate certificate (needed for secure deployments)
akash tx cert generate client --from default

# Publish certificate
akash tx cert publish client --from default
```

#### Step 5: Create SDL (deployment config)

Create `deploy.yaml`:
```yaml
---
version: "2.0"

services:
  roast-factory:
    image: nvidia/cuda:11.8.0-runtime-ubuntu22.04
    expose:
      - port: 8080
        as: 80
        to:
          - global: true
    env:
      - NVIDIA_VISIBLE_DEVICES=all

profiles:
  compute:
    roast-factory:
      resources:
        cpu:
          units: 4
        memory:
          size: 16Gi
        gpu:
          units: 1
          attributes:
            vendor:
              nvidia:
        storage:
          size: 100Gi
  placement:
    akash:
      pricing:
        roast-factory:
          denom: uakt
          amount: 100

deployment:
  roast-factory:
    akash:
      profile: roast-factory
      count: 1
```

#### Step 6: Deploy
```bash
# Create deployment
akash tx deployment create deploy.yaml --from default

# Get deployment ID
akash query deployment list --owner $(akash keys show default -a)

# View bids
akash query market bid list --owner $(akash keys show default -a)

# Accept a bid
akash tx market lease create --dseq <DEPLOYMENT_SEQ> --from default
```

### Usage with Viral Roast Factory
```powershell
# In launcher, choose option 6
# Or directly:
python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(use_gpu_cloud=True); f.generate_viral_roast(priority='low')"
```

**Pros:**
- ✅ CHEAPEST option (often 70% cheaper)
- ✅ Decentralized (no single point of control)
- ✅ Pay with crypto (AKT)
- ✅ Censorship-resistant

**Cons:**
- ❌ More complex setup
- ❌ Requires crypto wallet
- ❌ Smaller provider network
- ❌ Less mature ecosystem

**Pricing Examples:**
- GPU instances: $0.02 - $0.10/hour
- Often 3-5x cheaper than AWS/GCP
- Paid in AKT tokens

---

## Quick Comparison

### Choose HAMi if:
- ✅ You have a local GPU
- ✅ You want FREE processing
- ✅ You're comfortable with Kubernetes
- ✅ You want the fastest performance

### Choose SkyPilot if:
- ✅ You're new to cloud GPUs
- ✅ You want automatic cost optimization
- ✅ You need multi-cloud flexibility
- ✅ You have cloud credits to use

### Choose Akash if:
- ✅ You want the absolute cheapest option
- ✅ You're comfortable with blockchain/crypto
- ✅ You value decentralization
- ✅ You're willing to learn a new platform

---

## Testing Your Setup

Run the system check to verify everything:

```powershell
# Launch the main menu
.\ULTIMATE_VIRAL_ROAST_FACTORY_LAUNCHER.ps1

# Choose option 8: Check system status + GPU providers
```

This will show:
- ✅ Green = Installed and working
- ⚠️ Yellow = Installed but needs configuration
- ❌ Red = Not installed
- ⚙️ Gray = Optional

---

## Troubleshooting

### HAMi Issues

**Problem: kubectl not found**
```bash
# Verify installation
which kubectl

# Add to PATH
export PATH=$PATH:/usr/local/bin
```

**Problem: No GPU nodes**
```bash
# Check GPU drivers
nvidia-smi

# Verify Kubernetes can see GPU
kubectl describe nodes | grep -i gpu
```

### SkyPilot Issues

**Problem: "No cloud credentials found"**
```bash
# Run cloud-specific setup
sky check

# Follow prompts to configure missing clouds
```

**Problem: "No GPU instances available"**
```bash
# Try different regions
sky launch --gpus V100:1 --cloud aws --region us-west-2

# Or different GPU types
sky launch --gpus T4:1 --cloud gcp
```

### Akash Issues

**Problem: "Insufficient funds"**
```bash
# Check balance
akash query bank balances $(akash keys show default -a)

# You need AKT tokens - buy from exchange
```

**Problem: "No bids received"**
```bash
# Your pricing might be too low
# Edit deploy.yaml and increase the amount
# Then redeploy
```

---

## Cost Optimization Tips

1. **Use spot/preemptible instances** (SkyPilot does this automatically)
2. **Choose appropriate GPU types** - don't overpay for more power than needed
3. **Batch process** multiple videos to amortize startup costs
4. **Use local GPU** for development/testing
5. **Monitor spending** with cloud billing alerts

---

## Next Steps

1. **Choose your provider** based on needs and budget
2. **Follow setup instructions** for your chosen provider
3. **Run system check** (`option 8` in launcher)
4. **Generate test video** to verify everything works
5. **Scale up** once you've validated the setup

---

## Support Resources

### HAMi
- Documentation: https://github.com/Project-HAMi/HAMi
- Issues: https://github.com/Project-HAMi/HAMi/issues

### SkyPilot
- Documentation: https://skypilot.readthedocs.io/
- Slack: https://slack.skypilot.co/
- GitHub: https://github.com/skypilot-org/skypilot

### Akash
- Documentation: https://docs.akash.network/
- Discord: https://discord.akash.network/
- Forum: https://forum.akash.network/

---

## Security Best Practices

1. **Never commit credentials** to git
2. **Use environment variables** for API keys
3. **Enable MFA** on cloud accounts
4. **Rotate keys regularly**
5. **Monitor usage** for unexpected activity
6. **Set spending limits** on cloud accounts
7. **Use separate accounts** for production vs. testing

---

**Ready to generate viral roasts? Launch the factory!**

```powershell
.\ULTIMATE_VIRAL_ROAST_FACTORY_LAUNCHER.ps1
```
