"""
Multi-domain seed dataset for SkillGap Engine.

Domains covered:
  - CSE / Software
  - EEE / Electrical
  - ECE / Embedded
  - Mechanical
  - Civil
  - Statistics / Data Science
  - Management

Cross-domain transitions included:
  - EEE -> Software Development Engineer
  - Mechanical -> Data Analyst
  - ECE -> Embedded Engineer
  - CSE -> Data Analyst
  - Statistics -> Data Scientist
  - PS-aligned: Statistical Officer (MoSPI) for Ministry of Statistics

Competency scale: 0-5
  0 = no evidence, 1 = awareness, 2 = basic, 3 = intermediate,
  4 = advanced, 5 = expert
"""

from __future__ import annotations
from typing import Any

# ---------------------------------------------------------------------------
# COMPETENCIES
# Each dict: id, name, description, category, parent_id, taxonomy_source
# ---------------------------------------------------------------------------

COMPETENCIES: list[dict[str, Any]] = [
    # --- Core Programming ---
    {"id": 1,  "name": "Programming Fundamentals",         "description": "Variables, loops, conditionals, functions in any language",             "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 2,  "name": "Python Programming",               "description": "Python syntax, standard library, OOP",                                  "category": "Technical",    "parent_id": 1,    "taxonomy_source": "NSQF"},
    {"id": 3,  "name": "Data Structures & Algorithms",     "description": "Arrays, trees, graphs, sorting, searching, complexity analysis",        "category": "Technical",    "parent_id": 1,    "taxonomy_source": "NSQF"},
    {"id": 4,  "name": "Object-Oriented Design",           "description": "SOLID principles, design patterns, class hierarchies",                  "category": "Technical",    "parent_id": 1,    "taxonomy_source": "NSQF"},
    {"id": 5,  "name": "Version Control (Git)",            "description": "Git branching, merging, pull requests, GitHub/GitLab",                  "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},

    # --- Web / Backend ---
    {"id": 6,  "name": "REST API Design",                  "description": "HTTP verbs, status codes, OpenAPI, authentication patterns",           "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 7,  "name": "Databases & SQL",                  "description": "Relational schemas, SQL queries, indexing, transactions",               "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 8,  "name": "System Design",                    "description": "Scalability, load balancing, caching, microservices concepts",          "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 9,  "name": "Cloud Computing Basics",           "description": "IaaS/PaaS/SaaS, AWS/GCP/Azure fundamentals, deployment",               "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 10, "name": "Linux & Command Line",             "description": "Shell scripting, file system, process management",                      "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},

    # --- Data / Analytics ---
    {"id": 11, "name": "Statistics & Probability",         "description": "Descriptive stats, distributions, hypothesis testing, confidence intervals", "category": "Analytical", "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 12, "name": "Data Wrangling",                   "description": "Cleaning, transforming, reshaping tabular data with pandas/NumPy",     "category": "Analytical",   "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 13, "name": "Data Visualization",               "description": "Matplotlib, Seaborn, Power BI, Tableau, chart selection principles",   "category": "Analytical",   "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 14, "name": "Machine Learning",                 "description": "Supervised/unsupervised models, evaluation metrics, scikit-learn",      "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 15, "name": "Deep Learning",                    "description": "Neural networks, CNNs, RNNs, PyTorch/TensorFlow",                       "category": "Technical",    "parent_id": 14,   "taxonomy_source": "NSQF"},
    {"id": 16, "name": "Feature Engineering",              "description": "Encoding, scaling, selection, dimensionality reduction",                "category": "Analytical",   "parent_id": 14,   "taxonomy_source": "NSQF"},
    {"id": 17, "name": "Big Data Technologies",            "description": "Hadoop, Spark, Hive, distributed processing concepts",                  "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 18, "name": "Official Statistics",              "description": "Survey methodology, census data, national accounts, index numbers",     "category": "Domain",       "parent_id": None, "taxonomy_source": "MoSPI"},
    {"id": 19, "name": "Sampling Theory",                  "description": "Probability sampling, stratified/cluster sampling, sample size estimation", "category": "Analytical", "parent_id": 11,  "taxonomy_source": "MoSPI"},
    {"id": 20, "name": "Econometrics",                     "description": "Regression analysis, panel data, time series, causal inference",        "category": "Analytical",   "parent_id": 11,   "taxonomy_source": "MoSPI"},

    # --- Electrical / EEE ---
    {"id": 21, "name": "Circuit Analysis",                 "description": "KVL, KCL, Thevenin/Norton, AC/DC circuit analysis",                    "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 22, "name": "Power Systems",                    "description": "Generation, transmission, distribution, load flow, protection relays",  "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 23, "name": "Control Systems",                  "description": "Transfer functions, Bode plots, PID control, state-space representation", "category": "Technical",  "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 24, "name": "Electrical Machines",              "description": "Transformers, induction motors, synchronous machines",                  "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 25, "name": "MATLAB / Simulink",                "description": "Numerical computation, signal processing, and simulation using MATLAB",  "category": "Technical",   "parent_id": None, "taxonomy_source": "NSQF"},

    # --- ECE / Embedded ---
    {"id": 26, "name": "Digital Electronics",              "description": "Logic gates, flip-flops, counters, combinational and sequential circuits", "category": "Technical",  "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 27, "name": "Microcontrollers & Embedded C",    "description": "ARM Cortex-M, Arduino/STM32, peripheral drivers, interrupt handling",   "category": "Technical",   "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 28, "name": "RTOS",                             "description": "FreeRTOS, task scheduling, semaphores, inter-task communication",        "category": "Technical",    "parent_id": 27,   "taxonomy_source": "NSQF"},
    {"id": 29, "name": "PCB Design",                       "description": "Schematic capture, layout, design rule checks using KiCad/Altium",      "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 30, "name": "Signal Processing",                "description": "Fourier transforms, filters, DSP concepts and implementation",           "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},

    # --- Mechanical ---
    {"id": 31, "name": "Engineering Drawing & CAD",        "description": "2D/3D modelling with AutoCAD, SolidWorks, or CATIA",                    "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 32, "name": "Thermodynamics",                   "description": "Laws of thermodynamics, cycles, heat engines, refrigeration",            "category": "Technical",   "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 33, "name": "Manufacturing Processes",          "description": "Casting, machining, welding, additive manufacturing",                   "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 34, "name": "Finite Element Analysis",          "description": "Structural FEA using ANSYS or Abaqus, meshing, boundary conditions",   "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 35, "name": "Fluid Mechanics",                  "description": "Continuity, Bernoulli, pipe flow, turbomachinery",                      "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},

    # --- Civil ---
    {"id": 36, "name": "Structural Analysis",              "description": "Beams, trusses, frames, influence lines, matrix methods",               "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 37, "name": "Geotechnical Engineering",         "description": "Soil mechanics, foundation design, site investigation",                 "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 38, "name": "Construction Project Management",  "description": "Scheduling, cost estimation, Gantt charts, risk management",           "category": "Management",   "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 39, "name": "GIS & Remote Sensing",             "description": "Spatial data, QGIS/ArcGIS, satellite imagery interpretation",          "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 40, "name": "Environmental Engineering",        "description": "Water treatment, air quality, EIA, sustainability",                     "category": "Domain",       "parent_id": None, "taxonomy_source": "NSQF"},

    # --- Management / Soft Skills ---
    {"id": 41, "name": "Project Management",               "description": "Planning, execution, stakeholder management, Agile/Scrum",              "category": "Management",   "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 42, "name": "Communication & Reporting",        "description": "Technical writing, presentations, data storytelling",                   "category": "Soft Skills",  "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 43, "name": "Critical Thinking & Problem Solving", "description": "Root cause analysis, structured thinking, decision frameworks",      "category": "Soft Skills",  "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 44, "name": "Business Domain Knowledge",        "description": "Understanding of business processes, KPIs, and organisational context", "category": "Domain",       "parent_id": None, "taxonomy_source": "NSQF"},

    # --- Cross-cutting ---
    {"id": 45, "name": "Data Ethics & Privacy",            "description": "GDPR concepts, data anonymisation, responsible AI principles",          "category": "Domain",       "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 46, "name": "Research Methodology",             "description": "Literature review, experimental design, academic writing",              "category": "Analytical",   "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 47, "name": "Mathematical Modelling",           "description": "Formulating real-world problems as mathematical equations",             "category": "Analytical",   "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 48, "name": "IoT & Sensor Networks",            "description": "Protocols (MQTT, CoAP), sensor interfacing, edge computing",           "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
    {"id": 49, "name": "C / C++ Programming",              "description": "Pointers, memory management, data structures in C/C++",                "category": "Technical",    "parent_id": 1,    "taxonomy_source": "NSQF"},
    {"id": 50, "name": "DevOps & CI/CD",                   "description": "Docker, GitHub Actions, deployment pipelines, monitoring basics",       "category": "Technical",    "parent_id": None, "taxonomy_source": "NSQF"},
]


# ---------------------------------------------------------------------------
# ROLES
# Each dict: id, name, description, sector
# ---------------------------------------------------------------------------

ROLES: list[dict[str, Any]] = [
    {"id": 1,  "name": "Software Development Engineer",   "description": "Builds and maintains backend services, APIs, and system components",                                "sector": "IT"},
    {"id": 2,  "name": "Data Analyst",                    "description": "Analyses structured datasets, builds dashboards, reports insights to business stakeholders",        "sector": "Analytics"},
    {"id": 3,  "name": "Data Scientist",                  "description": "Develops predictive models, runs experiments, extracts insight from large datasets",               "sector": "Analytics"},
    {"id": 4,  "name": "Embedded Systems Engineer",       "description": "Designs and programs firmware for microcontrollers and real-time systems",                         "sector": "Electronics"},
    {"id": 5,  "name": "Electrical Design Engineer",      "description": "Designs power systems, electrical schematics, and control systems",                                "sector": "Electrical"},
    {"id": 6,  "name": "Mechanical Design Engineer",      "description": "Designs components and assemblies using CAD tools, performs FEA and manufacturing process selection", "sector": "Mechanical"},
    {"id": 7,  "name": "Civil Structural Engineer",       "description": "Analyses and designs structural systems for buildings, bridges, and infrastructure",               "sector": "Civil"},
    {"id": 8,  "name": "Statistical Officer (MoSPI)",     "description": "Collects, analyses, and publishes official government statistics; supports survey design and data quality", "sector": "Government / Statistics"},
    {"id": 9,  "name": "ML Engineer",                     "description": "Productionises ML models, builds training pipelines, manages data infrastructure",                 "sector": "IT"},
    {"id": 10, "name": "IoT Solutions Engineer",          "description": "Designs end-to-end IoT systems: firmware, connectivity, cloud ingestion, and dashboards",           "sector": "Electronics"},
]


# ---------------------------------------------------------------------------
# ROLE -> COMPETENCY REQUIREMENTS
# Each dict: role_id, competency_id, required_level (0-5), importance (0-1)
# ---------------------------------------------------------------------------

ROLE_COMPETENCIES: list[dict[str, Any]] = [

    # Role 1: Software Development Engineer
    {"role_id": 1, "competency_id": 1,  "required_level": 4, "importance": 1.0},   # Programming Fundamentals
    {"role_id": 1, "competency_id": 2,  "required_level": 4, "importance": 0.9},   # Python
    {"role_id": 1, "competency_id": 3,  "required_level": 4, "importance": 1.0},   # DSA
    {"role_id": 1, "competency_id": 4,  "required_level": 3, "importance": 0.8},   # OOP
    {"role_id": 1, "competency_id": 5,  "required_level": 3, "importance": 0.7},   # Git
    {"role_id": 1, "competency_id": 6,  "required_level": 3, "importance": 0.8},   # REST API
    {"role_id": 1, "competency_id": 7,  "required_level": 3, "importance": 0.8},   # SQL
    {"role_id": 1, "competency_id": 8,  "required_level": 3, "importance": 0.7},   # System Design
    {"role_id": 1, "competency_id": 10, "required_level": 2, "importance": 0.6},   # Linux
    {"role_id": 1, "competency_id": 50, "required_level": 2, "importance": 0.5},   # DevOps

    # Role 2: Data Analyst
    {"role_id": 2, "competency_id": 11, "required_level": 3, "importance": 1.0},   # Statistics
    {"role_id": 2, "competency_id": 12, "required_level": 4, "importance": 1.0},   # Data Wrangling
    {"role_id": 2, "competency_id": 13, "required_level": 4, "importance": 0.9},   # Data Viz
    {"role_id": 2, "competency_id": 2,  "required_level": 3, "importance": 0.8},   # Python
    {"role_id": 2, "competency_id": 7,  "required_level": 3, "importance": 0.8},   # SQL
    {"role_id": 2, "competency_id": 42, "required_level": 3, "importance": 0.7},   # Communication
    {"role_id": 2, "competency_id": 44, "required_level": 2, "importance": 0.6},   # Business Domain
    {"role_id": 2, "competency_id": 43, "required_level": 3, "importance": 0.7},   # Critical Thinking

    # Role 3: Data Scientist
    {"role_id": 3, "competency_id": 11, "required_level": 4, "importance": 1.0},   # Statistics
    {"role_id": 3, "competency_id": 12, "required_level": 4, "importance": 0.9},   # Data Wrangling
    {"role_id": 3, "competency_id": 14, "required_level": 4, "importance": 1.0},   # ML
    {"role_id": 3, "competency_id": 15, "required_level": 3, "importance": 0.7},   # Deep Learning
    {"role_id": 3, "competency_id": 16, "required_level": 4, "importance": 0.9},   # Feature Engineering
    {"role_id": 3, "competency_id": 2,  "required_level": 4, "importance": 0.9},   # Python
    {"role_id": 3, "competency_id": 13, "required_level": 3, "importance": 0.7},   # Data Viz
    {"role_id": 3, "competency_id": 47, "required_level": 3, "importance": 0.7},   # Mathematical Modelling
    {"role_id": 3, "competency_id": 46, "required_level": 2, "importance": 0.5},   # Research Methodology

    # Role 4: Embedded Systems Engineer
    {"role_id": 4, "competency_id": 27, "required_level": 4, "importance": 1.0},   # Microcontrollers
    {"role_id": 4, "competency_id": 49, "required_level": 4, "importance": 1.0},   # C/C++
    {"role_id": 4, "competency_id": 26, "required_level": 3, "importance": 0.9},   # Digital Electronics
    {"role_id": 4, "competency_id": 28, "required_level": 3, "importance": 0.8},   # RTOS
    {"role_id": 4, "competency_id": 29, "required_level": 2, "importance": 0.6},   # PCB Design
    {"role_id": 4, "competency_id": 30, "required_level": 2, "importance": 0.6},   # Signal Processing
    {"role_id": 4, "competency_id": 5,  "required_level": 2, "importance": 0.5},   # Git

    # Role 5: Electrical Design Engineer
    {"role_id": 5, "competency_id": 21, "required_level": 4, "importance": 1.0},   # Circuit Analysis
    {"role_id": 5, "competency_id": 22, "required_level": 4, "importance": 1.0},   # Power Systems
    {"role_id": 5, "competency_id": 23, "required_level": 3, "importance": 0.9},   # Control Systems
    {"role_id": 5, "competency_id": 24, "required_level": 3, "importance": 0.8},   # Electrical Machines
    {"role_id": 5, "competency_id": 25, "required_level": 3, "importance": 0.7},   # MATLAB
    {"role_id": 5, "competency_id": 29, "required_level": 2, "importance": 0.5},   # PCB Design

    # Role 6: Mechanical Design Engineer
    {"role_id": 6, "competency_id": 31, "required_level": 4, "importance": 1.0},   # CAD
    {"role_id": 6, "competency_id": 32, "required_level": 3, "importance": 0.8},   # Thermodynamics
    {"role_id": 6, "competency_id": 33, "required_level": 3, "importance": 0.8},   # Manufacturing
    {"role_id": 6, "competency_id": 34, "required_level": 3, "importance": 0.9},   # FEA
    {"role_id": 6, "competency_id": 35, "required_level": 3, "importance": 0.7},   # Fluid Mechanics
    {"role_id": 6, "competency_id": 41, "required_level": 2, "importance": 0.5},   # Project Management

    # Role 7: Civil Structural Engineer
    {"role_id": 7, "competency_id": 36, "required_level": 4, "importance": 1.0},   # Structural Analysis
    {"role_id": 7, "competency_id": 37, "required_level": 3, "importance": 0.8},   # Geotechnical
    {"role_id": 7, "competency_id": 38, "required_level": 3, "importance": 0.7},   # Project Management
    {"role_id": 7, "competency_id": 39, "required_level": 2, "importance": 0.5},   # GIS
    {"role_id": 7, "competency_id": 40, "required_level": 2, "importance": 0.5},   # Environmental

    # Role 8: Statistical Officer (MoSPI) — PS-aligned
    {"role_id": 8, "competency_id": 11, "required_level": 4, "importance": 1.0},   # Statistics
    {"role_id": 8, "competency_id": 18, "required_level": 4, "importance": 1.0},   # Official Statistics
    {"role_id": 8, "competency_id": 19, "required_level": 4, "importance": 0.9},   # Sampling Theory
    {"role_id": 8, "competency_id": 20, "required_level": 3, "importance": 0.8},   # Econometrics
    {"role_id": 8, "competency_id": 12, "required_level": 3, "importance": 0.8},   # Data Wrangling
    {"role_id": 8, "competency_id": 13, "required_level": 3, "importance": 0.7},   # Data Viz
    {"role_id": 8, "competency_id": 2,  "required_level": 2, "importance": 0.6},   # Python
    {"role_id": 8, "competency_id": 42, "required_level": 3, "importance": 0.7},   # Communication
    {"role_id": 8, "competency_id": 46, "required_level": 3, "importance": 0.7},   # Research Methodology
    {"role_id": 8, "competency_id": 45, "required_level": 2, "importance": 0.5},   # Data Ethics

    # Role 9: ML Engineer
    {"role_id": 9, "competency_id": 14, "required_level": 4, "importance": 1.0},   # ML
    {"role_id": 9, "competency_id": 15, "required_level": 3, "importance": 0.8},   # Deep Learning
    {"role_id": 9, "competency_id": 2,  "required_level": 4, "importance": 0.9},   # Python
    {"role_id": 9, "competency_id": 3,  "required_level": 3, "importance": 0.7},   # DSA
    {"role_id": 9, "competency_id": 17, "required_level": 3, "importance": 0.7},   # Big Data
    {"role_id": 9, "competency_id": 50, "required_level": 3, "importance": 0.8},   # DevOps/CI
    {"role_id": 9, "competency_id": 6,  "required_level": 3, "importance": 0.7},   # REST API
    {"role_id": 9, "competency_id": 9,  "required_level": 3, "importance": 0.8},   # Cloud
    {"role_id": 9, "competency_id": 16, "required_level": 4, "importance": 0.9},   # Feature Engineering

    # Role 10: IoT Solutions Engineer
    {"role_id": 10, "competency_id": 48, "required_level": 4, "importance": 1.0},  # IoT & Sensors
    {"role_id": 10, "competency_id": 27, "required_level": 3, "importance": 0.9},  # Microcontrollers
    {"role_id": 10, "competency_id": 49, "required_level": 3, "importance": 0.8},  # C/C++
    {"role_id": 10, "competency_id": 9,  "required_level": 3, "importance": 0.8},  # Cloud
    {"role_id": 10, "competency_id": 2,  "required_level": 2, "importance": 0.6},  # Python
    {"role_id": 10, "competency_id": 6,  "required_level": 2, "importance": 0.5},  # REST API
    {"role_id": 10, "competency_id": 26, "required_level": 2, "importance": 0.6},  # Digital Electronics
]


# ---------------------------------------------------------------------------
# USERS (demo profiles for cross-domain transitions)
# ---------------------------------------------------------------------------

USERS: list[dict[str, Any]] = [
    {"id": 1, "name": "Arjun Verma",    "education": "B.Tech EEE",        "department": "Electrical Engineering",    "experience": 2},
    {"id": 2, "name": "Priya Nair",     "education": "B.Tech Mechanical",  "department": "Mechanical Engineering",    "experience": 1},
    {"id": 3, "name": "Rahul Das",      "education": "B.Tech ECE",         "department": "Electronics & Communication", "experience": 2},
    {"id": 4, "name": "Sneha Kulkarni", "education": "B.Sc Statistics",    "department": "Statistics",                "experience": 0},
    {"id": 5, "name": "Vikram Singh",   "education": "B.Tech CSE",         "department": "Computer Science",          "experience": 3},
]


# ---------------------------------------------------------------------------
# USER COMPETENCIES (what each demo user already knows)
# EEE graduate (Arjun) transitioning to SDE — knows EEE, weak in SDE
# Mechanical (Priya) transitioning to Data Analyst — strong mech, basic data
# ECE (Rahul) targeting Embedded Engineer — close fit
# Stats (Sneha) targeting Data Scientist — strong stats, building ML
# CSE (Vikram) targeting Data Analyst — strong programming, moderate analytics
# ---------------------------------------------------------------------------

USER_COMPETENCIES: list[dict[str, Any]] = [
    # Arjun (EEE -> SDE) — user_id=1
    {"user_id": 1, "competency_id": 21, "current_level": 4, "evidence_source": "B.Tech EEE coursework"},
    {"user_id": 1, "competency_id": 22, "current_level": 3, "evidence_source": "B.Tech EEE coursework"},
    {"user_id": 1, "competency_id": 23, "current_level": 3, "evidence_source": "B.Tech EEE coursework"},
    {"user_id": 1, "competency_id": 24, "current_level": 3, "evidence_source": "B.Tech EEE coursework"},
    {"user_id": 1, "competency_id": 25, "current_level": 2, "evidence_source": "MATLAB lab sessions"},
    {"user_id": 1, "competency_id": 1,  "current_level": 2, "evidence_source": "Self-taught Python basics"},
    {"user_id": 1, "competency_id": 2,  "current_level": 2, "evidence_source": "Online course"},
    {"user_id": 1, "competency_id": 3,  "current_level": 1, "evidence_source": "None"},
    {"user_id": 1, "competency_id": 5,  "current_level": 1, "evidence_source": "Basic git usage"},
    {"user_id": 1, "competency_id": 7,  "current_level": 1, "evidence_source": "Basic SQL course"},

    # Priya (Mechanical -> Data Analyst) — user_id=2
    {"user_id": 2, "competency_id": 31, "current_level": 4, "evidence_source": "B.Tech Mechanical coursework"},
    {"user_id": 2, "competency_id": 32, "current_level": 4, "evidence_source": "B.Tech Mechanical coursework"},
    {"user_id": 2, "competency_id": 33, "current_level": 3, "evidence_source": "B.Tech Mechanical coursework"},
    {"user_id": 2, "competency_id": 34, "current_level": 2, "evidence_source": "ANSYS lab"},
    {"user_id": 2, "competency_id": 35, "current_level": 3, "evidence_source": "B.Tech Mechanical coursework"},
    {"user_id": 2, "competency_id": 11, "current_level": 2, "evidence_source": "Engineering math"},
    {"user_id": 2, "competency_id": 12, "current_level": 1, "evidence_source": "Excel usage"},
    {"user_id": 2, "competency_id": 13, "current_level": 1, "evidence_source": "Excel charts"},
    {"user_id": 2, "competency_id": 2,  "current_level": 1, "evidence_source": "None"},
    {"user_id": 2, "competency_id": 43, "current_level": 3, "evidence_source": "Engineering problem solving"},

    # Rahul (ECE -> Embedded Engineer) — user_id=3
    {"user_id": 3, "competency_id": 26, "current_level": 4, "evidence_source": "B.Tech ECE coursework"},
    {"user_id": 3, "competency_id": 27, "current_level": 3, "evidence_source": "Arduino lab projects"},
    {"user_id": 3, "competency_id": 49, "current_level": 3, "evidence_source": "Programming coursework"},
    {"user_id": 3, "competency_id": 30, "current_level": 3, "evidence_source": "DSP course"},
    {"user_id": 3, "competency_id": 29, "current_level": 2, "evidence_source": "PCB design lab"},
    {"user_id": 3, "competency_id": 28, "current_level": 1, "evidence_source": "Brief RTOS exposure"},
    {"user_id": 3, "competency_id": 5,  "current_level": 2, "evidence_source": "Git for assignments"},

    # Sneha (Statistics -> Data Scientist) — user_id=4
    {"user_id": 4, "competency_id": 11, "current_level": 4, "evidence_source": "B.Sc Statistics degree"},
    {"user_id": 4, "competency_id": 19, "current_level": 4, "evidence_source": "Sampling theory course"},
    {"user_id": 4, "competency_id": 20, "current_level": 3, "evidence_source": "Econometrics coursework"},
    {"user_id": 4, "competency_id": 46, "current_level": 3, "evidence_source": "Research project"},
    {"user_id": 4, "competency_id": 47, "current_level": 3, "evidence_source": "Mathematical modelling coursework"},
    {"user_id": 4, "competency_id": 2,  "current_level": 2, "evidence_source": "Python for Statistics NPTEL"},
    {"user_id": 4, "competency_id": 12, "current_level": 2, "evidence_source": "Pandas basics"},
    {"user_id": 4, "competency_id": 14, "current_level": 1, "evidence_source": "Intro ML MOOC"},
    {"user_id": 4, "competency_id": 13, "current_level": 2, "evidence_source": "R ggplot experience"},
    {"user_id": 4, "competency_id": 16, "current_level": 1, "evidence_source": "None"},

    # Vikram (CSE -> Data Analyst) — user_id=5
    {"user_id": 5, "competency_id": 1,  "current_level": 4, "evidence_source": "B.Tech CSE"},
    {"user_id": 5, "competency_id": 2,  "current_level": 4, "evidence_source": "B.Tech CSE + projects"},
    {"user_id": 5, "competency_id": 3,  "current_level": 4, "evidence_source": "Competitive programming"},
    {"user_id": 5, "competency_id": 4,  "current_level": 3, "evidence_source": "B.Tech CSE"},
    {"user_id": 5, "competency_id": 5,  "current_level": 3, "evidence_source": "GitHub projects"},
    {"user_id": 5, "competency_id": 7,  "current_level": 3, "evidence_source": "DBMS coursework"},
    {"user_id": 5, "competency_id": 11, "current_level": 2, "evidence_source": "Probability & Stats course"},
    {"user_id": 5, "competency_id": 12, "current_level": 2, "evidence_source": "Data science workshop"},
    {"user_id": 5, "competency_id": 13, "current_level": 2, "evidence_source": "Data science workshop"},
    {"user_id": 5, "competency_id": 42, "current_level": 2, "evidence_source": "Presentations"},
]


# ---------------------------------------------------------------------------
# COURSES
# ---------------------------------------------------------------------------

COURSES: list[dict[str, Any]] = [
    # SDE-oriented
    {"id": 1,  "title": "Data Structures and Algorithms in Python",    "description": "Arrays, trees, graphs, dynamic programming with Python implementations",     "provider": "NPTEL",    "duration": "12 weeks", "level": "intermediate", "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 2,  "title": "System Design for Engineers",                  "description": "Scalability, load balancing, databases, caching, microservices architecture","provider": "Educative","duration": "8 weeks",  "level": "advanced",     "source": "Educative", "source_url": "https://educative.io"},
    {"id": 3,  "title": "REST APIs with FastAPI and Python",            "description": "Building production-grade REST APIs with FastAPI, Pydantic and SQLAlchemy",  "provider": "Udemy",    "duration": "6 weeks",  "level": "intermediate", "source": "Udemy",    "source_url": "https://udemy.com"},
    {"id": 4,  "title": "Git & GitHub for Developers",                  "description": "Branching, rebasing, pull requests, CI/CD integration",                      "provider": "GitHub",   "duration": "2 weeks",  "level": "beginner",     "source": "GitHub",   "source_url": "https://github.com"},
    {"id": 5,  "title": "Linux Fundamentals and Shell Scripting",       "description": "File system, permissions, shell scripting, process management",               "provider": "Swayam",   "duration": "4 weeks",  "level": "beginner",     "source": "Swayam",   "source_url": "https://swayam.gov.in"},
    {"id": 6,  "title": "Databases and SQL for Developers",             "description": "Relational modelling, advanced SQL, indexing, query optimisation",            "provider": "NPTEL",    "duration": "8 weeks",  "level": "intermediate", "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 7,  "title": "Python OOP and Design Patterns",               "description": "SOLID principles, design patterns in Python, clean architecture",            "provider": "Udemy",    "duration": "5 weeks",  "level": "intermediate", "source": "Udemy",    "source_url": "https://udemy.com"},
    {"id": 8,  "title": "Docker & CI/CD Fundamentals",                  "description": "Containerisation, Docker Compose, GitHub Actions pipelines",                 "provider": "Coursera", "duration": "4 weeks",  "level": "intermediate", "source": "Coursera", "source_url": "https://coursera.org"},
    {"id": 9,  "title": "Cloud Computing with AWS",                     "description": "EC2, S3, RDS, Lambda, IAM — AWS core services",                             "provider": "Coursera", "duration": "8 weeks",  "level": "intermediate", "source": "Coursera", "source_url": "https://coursera.org"},

    # Data / Analytics
    {"id": 10, "title": "Statistics for Data Science",                  "description": "Probability, distributions, hypothesis testing, regression fundamentals",     "provider": "NPTEL",    "duration": "12 weeks", "level": "intermediate", "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 11, "title": "Data Wrangling with Pandas",                   "description": "DataFrame operations, merging, groupby, time series, missing data",          "provider": "Kaggle",   "duration": "3 weeks",  "level": "beginner",     "source": "Kaggle",   "source_url": "https://kaggle.com/learn"},
    {"id": 12, "title": "Data Visualisation with Python",               "description": "Matplotlib, Seaborn, Plotly — choosing the right chart, storytelling",       "provider": "Kaggle",   "duration": "3 weeks",  "level": "beginner",     "source": "Kaggle",   "source_url": "https://kaggle.com/learn"},
    {"id": 13, "title": "Machine Learning Specialisation",              "description": "Supervised learning, neural networks, decision trees, model evaluation",       "provider": "Coursera", "duration": "16 weeks", "level": "intermediate", "source": "Coursera", "source_url": "https://coursera.org"},
    {"id": 14, "title": "Feature Engineering for ML",                   "description": "Encoding, scaling, selection, creating new features, pipelines",              "provider": "Kaggle",   "duration": "4 weeks",  "level": "intermediate", "source": "Kaggle",   "source_url": "https://kaggle.com/learn"},
    {"id": 15, "title": "Deep Learning with PyTorch",                   "description": "Tensors, CNNs, RNNs, training loops, transfer learning",                     "provider": "NPTEL",    "duration": "12 weeks", "level": "advanced",     "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 16, "title": "Big Data Analytics with Spark",                "description": "RDDs, DataFrames, Spark SQL, streaming basics",                              "provider": "Coursera", "duration": "8 weeks",  "level": "advanced",     "source": "Coursera", "source_url": "https://coursera.org"},

    # Official Statistics / MoSPI
    {"id": 17, "title": "Sampling Techniques for Surveys",              "description": "SRSWOR, stratified, cluster, systematic sampling; estimation and inference",   "provider": "IASRI",    "duration": "6 weeks",  "level": "advanced",     "source": "Swayam",   "source_url": "https://swayam.gov.in"},
    {"id": 18, "title": "Official Statistics and National Accounts",    "description": "GDP computation, CPI, IIP, census methodology, MOSPI data sources",          "provider": "IASRI",    "duration": "8 weeks",  "level": "intermediate", "source": "Swayam",   "source_url": "https://swayam.gov.in"},
    {"id": 19, "title": "Econometrics with R",                          "description": "OLS, IV estimation, panel data, time series, R programming",                  "provider": "NPTEL",    "duration": "10 weeks", "level": "advanced",     "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 20, "title": "Research Methods in Social Science",           "description": "Experimental design, questionnaire design, qualitative and quantitative methods","provider": "Swayam","duration": "8 weeks",  "level": "intermediate", "source": "Swayam",   "source_url": "https://swayam.gov.in"},

    # Embedded / ECE
    {"id": 21, "title": "Embedded Systems with ARM Cortex-M",           "description": "ARM architecture, bare-metal programming, peripherals, interrupts",           "provider": "NPTEL",    "duration": "12 weeks", "level": "advanced",     "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 22, "title": "RTOS Fundamentals with FreeRTOS",              "description": "Task creation, scheduling, queues, semaphores on embedded platforms",         "provider": "Udemy",    "duration": "6 weeks",  "level": "advanced",     "source": "Udemy",    "source_url": "https://udemy.com"},
    {"id": 23, "title": "Digital Electronics and VLSI",                 "description": "Logic design, FSMs, FPGA introduction, Verilog basics",                       "provider": "NPTEL",    "duration": "12 weeks", "level": "intermediate", "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 24, "title": "PCB Design with KiCad",                        "description": "Schematic capture, layout, DRC, manufacturing files",                         "provider": "Udemy",    "duration": "4 weeks",  "level": "intermediate", "source": "Udemy",    "source_url": "https://udemy.com"},
    {"id": 25, "title": "IoT with Raspberry Pi and MQTT",               "description": "Sensor interfacing, MQTT protocol, cloud integration, edge processing",       "provider": "Coursera", "duration": "6 weeks",  "level": "intermediate", "source": "Coursera", "source_url": "https://coursera.org"},

    # Electrical
    {"id": 26, "title": "Power Systems Analysis",                       "description": "Load flow, fault analysis, stability, protection systems",                    "provider": "NPTEL",    "duration": "12 weeks", "level": "advanced",     "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 27, "title": "Control Systems Engineering",                  "description": "Transfer functions, Bode plots, root locus, state-space, PID",               "provider": "NPTEL",    "duration": "12 weeks", "level": "advanced",     "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 28, "title": "MATLAB and Simulink for Engineers",            "description": "Matrix operations, Simulink modelling, control and signal processing toolboxes","provider": "MathWorks","duration": "6 weeks", "level": "intermediate", "source": "Coursera", "source_url": "https://coursera.org"},

    # Mechanical
    {"id": 29, "title": "SolidWorks for Mechanical Design",             "description": "Part modelling, assemblies, drawing creation, design intent",                 "provider": "Udemy",    "duration": "6 weeks",  "level": "intermediate", "source": "Udemy",    "source_url": "https://udemy.com"},
    {"id": 30, "title": "Finite Element Analysis with ANSYS",           "description": "Structural FEA, meshing, static and dynamic analysis, result interpretation", "provider": "NPTEL",    "duration": "8 weeks",  "level": "advanced",     "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 31, "title": "Manufacturing Processes and Materials",        "description": "Casting, forging, machining, welding, material selection",                    "provider": "NPTEL",    "duration": "10 weeks", "level": "intermediate", "source": "NPTEL",    "source_url": "https://nptel.ac.in"},

    # Cross-cutting / soft skills
    {"id": 32, "title": "Python Programming for Beginners",             "description": "Variables, loops, functions, files, basic OOP in Python",                    "provider": "NPTEL",    "duration": "4 weeks",  "level": "beginner",     "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
    {"id": 33, "title": "Technical Communication and Reporting",        "description": "Report writing, presentations, email communication for engineers",            "provider": "Swayam",   "duration": "4 weeks",  "level": "beginner",     "source": "Swayam",   "source_url": "https://swayam.gov.in"},
    {"id": 34, "title": "Project Management Fundamentals",              "description": "Scrum, Agile, Gantt charts, stakeholder management, risk",                   "provider": "Coursera", "duration": "6 weeks",  "level": "beginner",     "source": "Coursera", "source_url": "https://coursera.org"},
    {"id": 35, "title": "Data Ethics and Responsible AI",               "description": "Privacy, fairness, bias, governance, Indian data protection context",        "provider": "Swayam",   "duration": "3 weeks",  "level": "beginner",     "source": "Swayam",   "source_url": "https://swayam.gov.in"},
    {"id": 36, "title": "Mathematical Foundations for Data Science",    "description": "Linear algebra, calculus, probability for ML applications",                   "provider": "NPTEL",    "duration": "8 weeks",  "level": "intermediate", "source": "NPTEL",    "source_url": "https://nptel.ac.in"},
]


# ---------------------------------------------------------------------------
# COURSE -> COMPETENCY COVERAGE
# coverage_level: how strongly this course addresses the competency (1-5)
# ---------------------------------------------------------------------------

COURSE_COMPETENCIES: list[dict[str, Any]] = [
    # Course 1: DSA in Python
    {"course_id": 1, "competency_id": 3,  "coverage_level": 5},  # DSA
    {"course_id": 1, "competency_id": 2,  "coverage_level": 3},  # Python
    {"course_id": 1, "competency_id": 1,  "coverage_level": 2},  # Programming Fundamentals

    # Course 2: System Design
    {"course_id": 2, "competency_id": 8,  "coverage_level": 5},  # System Design
    {"course_id": 2, "competency_id": 6,  "coverage_level": 3},  # REST API
    {"course_id": 2, "competency_id": 7,  "coverage_level": 2},  # SQL

    # Course 3: FastAPI
    {"course_id": 3, "competency_id": 6,  "coverage_level": 5},  # REST API
    {"course_id": 3, "competency_id": 2,  "coverage_level": 3},  # Python
    {"course_id": 3, "competency_id": 7,  "coverage_level": 2},  # SQL

    # Course 4: Git
    {"course_id": 4, "competency_id": 5,  "coverage_level": 5},  # Git
    {"course_id": 4, "competency_id": 50, "coverage_level": 2},  # DevOps

    # Course 5: Linux
    {"course_id": 5, "competency_id": 10, "coverage_level": 5},  # Linux
    {"course_id": 5, "competency_id": 5,  "coverage_level": 2},  # Git

    # Course 6: SQL
    {"course_id": 6, "competency_id": 7,  "coverage_level": 5},  # SQL
    {"course_id": 6, "competency_id": 8,  "coverage_level": 2},  # System Design

    # Course 7: Python OOP
    {"course_id": 7, "competency_id": 4,  "coverage_level": 5},  # OOP
    {"course_id": 7, "competency_id": 2,  "coverage_level": 3},  # Python
    {"course_id": 7, "competency_id": 1,  "coverage_level": 2},  # Programming Fundamentals

    # Course 8: Docker/CI-CD
    {"course_id": 8, "competency_id": 50, "coverage_level": 5},  # DevOps
    {"course_id": 8, "competency_id": 10, "coverage_level": 2},  # Linux

    # Course 9: AWS
    {"course_id": 9, "competency_id": 9,  "coverage_level": 5},  # Cloud
    {"course_id": 9, "competency_id": 50, "coverage_level": 2},  # DevOps
    {"course_id": 9, "competency_id": 6,  "coverage_level": 2},  # REST API

    # Course 10: Statistics for DS
    {"course_id": 10, "competency_id": 11, "coverage_level": 5},  # Statistics
    {"course_id": 10, "competency_id": 47, "coverage_level": 3},  # Mathematical Modelling
    {"course_id": 10, "competency_id": 20, "coverage_level": 2},  # Econometrics

    # Course 11: Pandas
    {"course_id": 11, "competency_id": 12, "coverage_level": 5},  # Data Wrangling
    {"course_id": 11, "competency_id": 2,  "coverage_level": 2},  # Python

    # Course 12: Data Viz Python
    {"course_id": 12, "competency_id": 13, "coverage_level": 5},  # Data Viz
    {"course_id": 12, "competency_id": 42, "coverage_level": 2},  # Communication

    # Course 13: ML Specialisation
    {"course_id": 13, "competency_id": 14, "coverage_level": 5},  # ML
    {"course_id": 13, "competency_id": 16, "coverage_level": 3},  # Feature Engineering
    {"course_id": 13, "competency_id": 11, "coverage_level": 2},  # Statistics
    {"course_id": 13, "competency_id": 2,  "coverage_level": 2},  # Python

    # Course 14: Feature Engineering
    {"course_id": 14, "competency_id": 16, "coverage_level": 5},  # Feature Engineering
    {"course_id": 14, "competency_id": 14, "coverage_level": 2},  # ML
    {"course_id": 14, "competency_id": 12, "coverage_level": 2},  # Data Wrangling

    # Course 15: Deep Learning PyTorch
    {"course_id": 15, "competency_id": 15, "coverage_level": 5},  # Deep Learning
    {"course_id": 15, "competency_id": 14, "coverage_level": 3},  # ML
    {"course_id": 15, "competency_id": 2,  "coverage_level": 2},  # Python

    # Course 16: Big Data Spark
    {"course_id": 16, "competency_id": 17, "coverage_level": 5},  # Big Data
    {"course_id": 16, "competency_id": 12, "coverage_level": 2},  # Data Wrangling
    {"course_id": 16, "competency_id": 9,  "coverage_level": 2},  # Cloud

    # Course 17: Sampling Techniques
    {"course_id": 17, "competency_id": 19, "coverage_level": 5},  # Sampling Theory
    {"course_id": 17, "competency_id": 11, "coverage_level": 3},  # Statistics
    {"course_id": 17, "competency_id": 46, "coverage_level": 2},  # Research Methodology

    # Course 18: Official Statistics
    {"course_id": 18, "competency_id": 18, "coverage_level": 5},  # Official Statistics
    {"course_id": 18, "competency_id": 19, "coverage_level": 2},  # Sampling Theory
    {"course_id": 18, "competency_id": 11, "coverage_level": 2},  # Statistics

    # Course 19: Econometrics with R
    {"course_id": 19, "competency_id": 20, "coverage_level": 5},  # Econometrics
    {"course_id": 19, "competency_id": 11, "coverage_level": 3},  # Statistics
    {"course_id": 19, "competency_id": 46, "coverage_level": 2},  # Research Methodology

    # Course 20: Research Methods
    {"course_id": 20, "competency_id": 46, "coverage_level": 5},  # Research Methodology
    {"course_id": 20, "competency_id": 42, "coverage_level": 3},  # Communication
    {"course_id": 20, "competency_id": 45, "coverage_level": 2},  # Data Ethics

    # Course 21: Embedded ARM
    {"course_id": 21, "competency_id": 27, "coverage_level": 5},  # Microcontrollers
    {"course_id": 21, "competency_id": 49, "coverage_level": 3},  # C/C++
    {"course_id": 21, "competency_id": 26, "coverage_level": 2},  # Digital Electronics

    # Course 22: RTOS FreeRTOS
    {"course_id": 22, "competency_id": 28, "coverage_level": 5},  # RTOS
    {"course_id": 22, "competency_id": 27, "coverage_level": 2},  # Microcontrollers
    {"course_id": 22, "competency_id": 49, "coverage_level": 2},  # C/C++

    # Course 23: Digital Electronics VLSI
    {"course_id": 23, "competency_id": 26, "coverage_level": 5},  # Digital Electronics
    {"course_id": 23, "competency_id": 30, "coverage_level": 2},  # Signal Processing

    # Course 24: PCB Design
    {"course_id": 24, "competency_id": 29, "coverage_level": 5},  # PCB Design
    {"course_id": 24, "competency_id": 26, "coverage_level": 2},  # Digital Electronics

    # Course 25: IoT MQTT
    {"course_id": 25, "competency_id": 48, "coverage_level": 5},  # IoT
    {"course_id": 25, "competency_id": 27, "coverage_level": 3},  # Microcontrollers
    {"course_id": 25, "competency_id": 9,  "coverage_level": 2},  # Cloud
    {"course_id": 25, "competency_id": 6,  "coverage_level": 2},  # REST API

    # Course 26: Power Systems
    {"course_id": 26, "competency_id": 22, "coverage_level": 5},  # Power Systems
    {"course_id": 26, "competency_id": 21, "coverage_level": 3},  # Circuit Analysis

    # Course 27: Control Systems
    {"course_id": 27, "competency_id": 23, "coverage_level": 5},  # Control Systems
    {"course_id": 27, "competency_id": 25, "coverage_level": 2},  # MATLAB

    # Course 28: MATLAB Simulink
    {"course_id": 28, "competency_id": 25, "coverage_level": 5},  # MATLAB
    {"course_id": 28, "competency_id": 23, "coverage_level": 2},  # Control Systems
    {"course_id": 28, "competency_id": 30, "coverage_level": 2},  # Signal Processing

    # Course 29: SolidWorks
    {"course_id": 29, "competency_id": 31, "coverage_level": 5},  # CAD
    {"course_id": 29, "competency_id": 33, "coverage_level": 2},  # Manufacturing

    # Course 30: FEA ANSYS
    {"course_id": 30, "competency_id": 34, "coverage_level": 5},  # FEA
    {"course_id": 30, "competency_id": 35, "coverage_level": 2},  # Fluid Mechanics
    {"course_id": 30, "competency_id": 31, "coverage_level": 2},  # CAD

    # Course 31: Manufacturing
    {"course_id": 31, "competency_id": 33, "coverage_level": 5},  # Manufacturing
    {"course_id": 31, "competency_id": 32, "coverage_level": 2},  # Thermodynamics

    # Course 32: Python Beginners
    {"course_id": 32, "competency_id": 2,  "coverage_level": 4},  # Python
    {"course_id": 32, "competency_id": 1,  "coverage_level": 3},  # Programming Fundamentals

    # Course 33: Technical Communication
    {"course_id": 33, "competency_id": 42, "coverage_level": 5},  # Communication
    {"course_id": 33, "competency_id": 43, "coverage_level": 2},  # Critical Thinking

    # Course 34: Project Management
    {"course_id": 34, "competency_id": 41, "coverage_level": 5},  # Project Management
    {"course_id": 34, "competency_id": 38, "coverage_level": 3},  # Construction PM
    {"course_id": 34, "competency_id": 42, "coverage_level": 2},  # Communication

    # Course 35: Data Ethics
    {"course_id": 35, "competency_id": 45, "coverage_level": 5},  # Data Ethics
    {"course_id": 35, "competency_id": 42, "coverage_level": 2},  # Communication

    # Course 36: Math Foundations
    {"course_id": 36, "competency_id": 47, "coverage_level": 5},  # Mathematical Modelling
    {"course_id": 36, "competency_id": 11, "coverage_level": 3},  # Statistics
    {"course_id": 36, "competency_id": 14, "coverage_level": 2},  # ML
]
