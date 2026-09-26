"""
data.py
Static data model for the CKA Exam Tracker.

The structure intentionally mirrors the Excel sheet:
5 categories, each with a weight (summing to 100%) and an ordered
list of topics. UI code (app.py) is generated from this structure —
no per-row UI logic is hard-coded anywhere else.
"""

# Default status applied to every topic on first run.
DEFAULT_STATUS = "Yet to Start"

# The three allowed status values, in dropdown order.
STATUS_OPTIONS = ["Yet to Start", "WIP", "Done"]

# Numeric weight used for progress-percentage math.
STATUS_WEIGHT = {
    "Yet to Start": 0,
    "WIP": 50,
    "Done": 100,
}

# Colors used for each status value's text (matches the Excel screenshot).
STATUS_COLOR = {
    "Yet to Start": "#2E86C1",  # cyan / blue
    "WIP": "#E67E22",           # orange
    "Done": "#1E8449",          # green
}

STATUS_BOLD = {
    "Yet to Start": False,
    "WIP": False,
    "Done": True,
}

# Certification-readiness thresholds (configurable).
READINESS_THRESHOLDS = [
    (100, "Ready to get your CKA Cert!"),
    (80, "Nearly Ready"),
    (50, "Almost"),
    (0, "Not Yet"),
]


def _topic(tid, name, exam):
    return {"id": tid, "name": name, "exam": exam, "status": DEFAULT_STATUS}


CATEGORIES = [
    {
        "id": 1,
        "name": "Cluster Architecture, Installation & Configuration",
        "weight": 25,
        "color": "#C55A11",  # orange
        "topics": [
            _topic(1, "Kubernetes Architecture", "CKA & CKAD"),
            _topic(2, "Installing Kubernetes using Kubeadm", "CKA & CKAD"),
            _topic(3, "Pods", "CKA & CKAD"),
            _topic(4, "ReplicaSet", "CKA & CKAD"),
            _topic(5, "Namespaces", "CKA & CKAD"),
            _topic(6, "Upgrading Kubernetes Version", "CKA"),
            _topic(7, "Managing Highly-Available K8s Cluster", "CKA"),
            _topic(8, "ETCD", "CKA"),
            _topic(9, "RBAC", "CKA"),
        ],
    },
    {
        "id": 2,
        "name": "Workloads & Scheduling",
        "weight": 15,
        "color": "#2E75B6",  # blue
        "topics": [
            _topic(10, "Deployments", "CKA & CKAD"),
            _topic(11, "Rolling Update & Rollback", "CKA & CKAD"),
            _topic(12, "Scaling Applications", "CKA"),
            _topic(13, "ConfigMaps", "CKA & CKAD"),
            _topic(14, "Secrets", "CKA & CKAD"),
            _topic(15, "Node-Selectors", "CKA"),
            _topic(16, "Resource Limits", "CKA & CKAD"),
            _topic(17, "Self-Healing", "CKA"),
            _topic(18, "Manifest Managing & Templating Tools", "CKA"),
        ],
    },
    {
        "id": 3,
        "name": "Services & Networking",
        "weight": 20,
        "color": "#1CADE4",  # blue/cyan
        "topics": [
            _topic(19, "Networking Basics", "CKA"),
            _topic(20, "CNI", "CKA"),
            _topic(21, "Connectivity (Pod-To-Pod & More)", "CKA"),
            _topic(22, "Services", "CKA & CKAD"),
            _topic(23, "KubeProxy", "CKA"),
            _topic(24, "DNS in Kubernetes | CoreDNS & KubeDNS", "CKA"),
            _topic(25, "Service Discovery", "CKA"),
            _topic(26, "Endpoints", "CKA"),
            _topic(27, "Ingress", "CKA"),
        ],
    },
    {
        "id": 4,
        "name": "Storage",
        "weight": 10,
        "color": "#17A398",  # teal/cyan
        "topics": [
            _topic(28, "Volumes", "CKA"),
            _topic(29, "HostPath Volume", "CKA & CKAD"),
            _topic(30, "Persistent Storage", "CKA"),
            _topic(31, "Access Modes | Volume Modes | Reclaim Policies", "CKA & CKAD"),
            _topic(32, "GCE Persistent Storage", "CKA"),
            _topic(33, "Persistent Volume (PV)", "CKA & CKAD"),
            _topic(34, "Persistent Volume Claim (PVC)", "CKA & CKAD"),
            _topic(35, "Storage Classes", "CKA"),
        ],
    },
    {
        "id": 5,
        "name": "Troubleshooting",
        "weight": 30,
        "color": "#1F3864",  # dark blue
        "topics": [
            _topic(36, "Logging", "CKA & CKAD"),
            _topic(37, "Monitoring", "CKA & CKAD"),
            _topic(38, "Troubleshooting Cluster Components", "CKA & CKAD"),
            _topic(39, "Troubleshooting Application", "CKA & CKAD"),
            _topic(40, "Troubleshooting Networking", "CKA & CKAD"),
        ],
    },
]

# Which categories render in the left spreadsheet block vs the right one,
# matching the screenshot's layout.
LEFT_CATEGORY_IDS = [1, 2]
RIGHT_CATEGORY_IDS = [3, 4, 5]

TOTAL_TOPICS = sum(len(c["topics"]) for c in CATEGORIES)
TOTAL_WEIGHT = sum(c["weight"] for c in CATEGORIES)


def get_readiness_label(weighted_pct: float) -> str:
    """Map a weighted progress percentage to a readiness label."""
    for threshold, label in READINESS_THRESHOLDS:
        if weighted_pct >= threshold:
            return label
    return "Not Yet"
