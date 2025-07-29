# Network Configuration Analysis

**Date**: 2025-01-29  
**Analysis Method**: UniFi CLI + Direct Web Interface Access  
**Proxmox Cluster**: hephaestus + hephaestus-2

## Executive Summary

Successfully located and analyzed the network configuration for both Proxmox hosts. The cluster is healthy and operational, but currently uses a flat network configuration that could benefit from VLAN segmentation for improved security and traffic management.

## Proxmox Host Locations

### Physical Switch Connections

Both Proxmox hosts are connected to the **USW Pro 8 PoE** switch (192.168.4.159):

| Host | MAC Address | Switch Port | Current Network | Status |
|------|-------------|-------------|-----------------|---------|
| **hephaestus** | 88:ae:dd:72:cd:56 | **Port 7** | Default (192.168.4.50) | ✅ Active |
| **hephaestus-2** | bc:24:11:8c:a1:b2 | **Port 6** | Default (192.168.4.60) | ✅ Active |

### Access Methods

```bash
# Via Tailscale (Recommended)
ssh root@100.124.87.101  # hephaestus
ssh root@100.70.7.127    # hephaestus-2

# Direct IP (when on management network)
ssh root@192.168.4.50    # hephaestus
ssh root@192.168.4.60    # hephaestus-2
```

## Current Network Configuration

### Switch Port Settings

**Port 6 (hephaestus-2)**:
- **Operation**: Standard Switching
- **Native VLAN**: Default (1) - 192.168.4.0/24
- **Tagged VLAN Management**: Allow All
- **PoE**: PoE+ enabled
- **Speed**: 1 GbE

**Port 7 (hephaestus)**:
- **Operation**: Standard Switching  
- **Native VLAN**: Default (1) - 192.168.4.0/24
- **Tagged VLAN Management**: Allow All
- **PoE**: PoE++ enabled
- **Speed**: 1 GbE

### Network Topology

```
Management Network (192.168.4.0/24)
├── UniFi Controller: 192.168.4.1 (UDM Pro Max)
├── Proxmox Nodes:
│   ├── hephaestus: 192.168.4.50 (Tailscale: 100.124.87.101)
│   └── hephaestus-2: 192.168.4.60 (Tailscale: 100.70.7.127)
└── Switches:
    ├── USW Pro 8 PoE: 192.168.4.159 ← Both Proxmox hosts here
    ├── USW Pro Max 24 PoE: 192.168.4.185
    ├── USW Pro Max 24 PoE: 192.168.4.229
    └── USW Aggregation: 192.168.4.91
```

## Cluster Health Assessment

### Proxmox Cluster Status ✅

```bash
# Cluster is healthy and quorate
pvecm status
# Shows: 2 nodes + qdevice (3 votes total)
# Communication latency: ~1.5ms between nodes
```

### Network Performance
- **Inter-node latency**: ~1.5ms (excellent)
- **Bandwidth**: 1 GbE per host (adequate for current workload)
- **Traffic patterns**: 
  - Port 6: 180 GB TX / 84.3 GB RX
  - Port 7: 348 GB TX / 406 GB RX

## Current Issues & Limitations

### ❌ Flat Network Architecture
- **Issue**: All traffic (management, VM, storage) on single VLAN
- **Risk**: No network segmentation for security or performance
- **Impact**: Harder to implement traffic policies and QoS

### ❌ Missing VLAN Segmentation  
- **Issue**: No separation of cluster vs VM vs storage traffic
- **Risk**: Potential performance bottlenecks and security exposure
- **Impact**: Cannot implement best-practice network isolation

### ❌ No Dedicated Storage Network
- **Issue**: Storage replication uses same network as management
- **Risk**: Storage traffic can impact cluster communication
- **Impact**: Potential performance degradation during backups

## Recommended VLAN Implementation

### Proposed VLAN Structure

| VLAN | Name | Subnet | Purpose | Priority |
|------|------|--------|---------|----------|
| **1** | Management | 192.168.4.0/24 | Current (UniFi, SSH) | Keep |
| **10** | Proxmox-Cluster | 10.0.10.0/24 | Corosync heartbeat | High |
| **20** | VM-Production | 192.168.20.0/24 | Production containers | High | 
| **21** | VM-Development | 192.168.21.0/24 | Development containers | Medium |
| **30** | Storage | 10.0.30.0/24 | NFS/backup traffic | High |

### Implementation Plan

#### Phase 1: Create VLANs in UniFi Controller
```bash
# VLANs to create:
- Proxmox-Cluster (VLAN 10): 10.0.10.0/24
- VM-Production (VLAN 20): 192.168.20.0/24  
- VM-Development (VLAN 21): 192.168.21.0/24
- Storage (VLAN 30): 10.0.30.0/24
```

#### Phase 2: Configure Switch Ports as Trunk
**Ports 6 & 7 Configuration**:
- **Native VLAN**: Management (1) - for initial access
- **Tagged VLANs**: 10, 20, 21, 30
- **Operation**: Trunk mode
- **Port Profile**: Custom trunk profile

#### Phase 3: Update Proxmox Network Configuration
```bash
# Add VLAN interfaces to /etc/network/interfaces on both nodes
auto vmbr0.10
iface vmbr0.10 inet static
    address 10.0.10.X/24  # .50 for hephaestus, .60 for hephaestus-2
    vlan-raw-device vmbr0

auto vmbr0.20  
iface vmbr0.20 inet manual
    vlan-raw-device vmbr0

auto vmbr0.21
iface vmbr0.21 inet manual  
    vlan-raw-device vmbr0

auto vmbr0.30
iface vmbr0.30 inet static
    address 10.0.30.X/24  # Storage network
    vlan-raw-device vmbr0
```

#### Phase 4: Migrate Services Gradually
1. **Test VLAN connectivity** before migrating services
2. **Update corosync** to use VLAN 10 for cluster communication
3. **Migrate VMs** to appropriate production/development VLANs
4. **Configure storage** to use VLAN 30

## Implementation Tools Available

### UniFi API Access
```json
{
  "url": "https://192.168.4.1", 
  "api_key": "PH82gfOQNNNbeSuo4gbmHGe9-VPF8Jub"
}
```

### Automation Scripts
- **VLAN Creation**: `/tmp/unifi_vlan_setup_local_admin.py`
- **API Capabilities**: `/tmp/unifi_api_capabilities.py`
- **Port Configuration**: Available via UniFi API or web interface

## Risk Assessment

### Migration Risks
- **Service Interruption**: Brief downtime during network reconfiguration
- **Cluster Split-brain**: If migration not done carefully
- **VM Connectivity Loss**: If VLAN assignments incorrect

### Mitigation Strategies
- **Staged Migration**: Implement one VLAN at a time
- **Rollback Plan**: Keep original configuration documented
- **Testing**: Verify each VLAN before migrating services
- **Maintenance Window**: Schedule during low-usage periods

## Next Steps

1. **Create VLANs** in UniFi Controller
2. **Configure trunk ports** for Ports 6 & 7
3. **Test VLAN connectivity** from Proxmox hosts
4. **Update Proxmox networking** configuration
5. **Migrate cluster communication** to dedicated VLAN
6. **Move VMs** to appropriate VLANs gradually

## Monitoring & Validation

### Post-Implementation Checks
```bash
# Verify cluster health
pvecm status

# Check VLAN interfaces
ip addr show | grep vmbr0

# Test inter-VLAN routing
ping -I vmbr0.10 10.0.10.60  # From hephaestus to hephaestus-2

# Monitor cluster communication
journalctl -u corosync -f
```

### Performance Monitoring
- **Cluster latency**: Should remain ~1-2ms
- **Network throughput**: Monitor for bottlenecks
- **VLAN traffic isolation**: Verify proper segmentation

---

**Status**: Analysis Complete ✅  
**Next Action**: Implement VLAN configuration in UniFi Controller  
**Documentation**: Complete and current as of 2025-01-29