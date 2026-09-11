"""
Skillora — Extended Skill-Based Career & Salary Dataset
Full faithful representation of all 3 Excel sheets:
  1. Skill Career Dataset   (105 rows)
  2. Learning Resources     (4 paid + 4 free per skill)
  3. Company Job References (35 rows: 20 Software + 15 Hardware)

Salary: indicative annual CTC in India (INR LPA).
URLs:   taken directly from dataset — not altered.
"""
from __future__ import annotations
from typing import Any

# ============================================================
# SECTION A: CANONICAL COMPETENCY CATALOGUE (50 entries)
# Maps Skillora skill names to internal competency IDs used
# by the gap engine. IDs are referenced in SKILL_CAREER_RECORDS.
# ============================================================

COMPETENCIES: list[dict[str, Any]] = [
    # Software Development
    {"id": 1,  "name": "C Programming",               "description": "Procedural C: pointers, memory management, embedded C",              "category": "Software Development",   "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0001"},
    {"id": 2,  "name": "Java",                         "description": "Java OOP, collections, JVM, Spring basics",                         "category": "Software Development",   "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0004"},
    {"id": 3,  "name": "Python Programming",           "description": "Python syntax, stdlib, OOP, data science libraries",                 "category": "Software Development",   "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0005"},
    {"id": 4,  "name": "Data Structures & Algorithms", "description": "Arrays, trees, graphs, sorting, complexity analysis",               "category": "AI / Data Science",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0010"},
    {"id": 5,  "name": "DBMS & SQL",                   "description": "Relational schemas, SQL queries, indexing, transactions",           "category": "Software Development",   "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0012"},
    {"id": 6,  "name": "SQL",                          "description": "Advanced SQL queries, joins, aggregations, stored procedures",       "category": "Software Development",   "parent_id": 5,    "taxonomy_source": "Skillora", "taxonomy_id": "SKL0035"},
    {"id": 7,  "name": "Web Development",              "description": "HTML, CSS, JS, React/Next.js, REST APIs, full-stack fundamentals",  "category": "Software Development",   "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0015"},
    {"id": 8,  "name": "Operating Systems",            "description": "Process management, memory, file systems, Linux/Unix fundamentals", "category": "Software Development",   "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0016"},
    {"id": 9,  "name": "Computer Networks",            "description": "TCP/IP, OSI model, subnetting, protocols, network security",        "category": "IT Infrastructure",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0018"},
    {"id": 10, "name": "Cloud Computing",              "description": "IaaS/PaaS/SaaS, AWS/GCP/Azure fundamentals, deployment",           "category": "IT Infrastructure",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0020"},
    {"id": 11, "name": "Cybersecurity",                "description": "Threat modelling, secure coding, cryptography fundamentals",        "category": "IT Infrastructure",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0023"},
    # AI / Data Science
    {"id": 12, "name": "Statistics",                   "description": "Descriptive & inferential stats, probability, hypothesis testing",  "category": "AI / Data Science",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0029"},
    {"id": 13, "name": "Data Analysis",                "description": "EDA, pattern recognition, insight generation from data",            "category": "AI / Data Science",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0032"},
    {"id": 14, "name": "Data Visualization",           "description": "Matplotlib, Seaborn, Power BI, Tableau, Plotly",                   "category": "AI / Data Science",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0040"},
    {"id": 15, "name": "Machine Learning",             "description": "Supervised/unsupervised models, evaluation metrics, scikit-learn",  "category": "AI / Data Science",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0038"},
    {"id": 16, "name": "Deep Learning",                "description": "Neural networks, CNNs, RNNs, PyTorch/TensorFlow",                  "category": "AI / Data Science",      "parent_id": 15,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0043"},
    {"id": 17, "name": "Natural Language Processing",  "description": "Text preprocessing, embeddings, transformers, Hugging Face",       "category": "AI / Data Science",      "parent_id": 16,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0045"},
    {"id": 18, "name": "Computer Vision",              "description": "Image processing, object detection, CNNs, OpenCV",                 "category": "AI / Data Science",      "parent_id": 16,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0063"},
    {"id": 19, "name": "Reinforcement Learning",       "description": "MDPs, Q-learning, policy gradients, OpenAI Gym",                   "category": "AI / Data Science",      "parent_id": 15,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0065"},
    {"id": 20, "name": "Big Data Analytics",           "description": "Hadoop, Spark, distributed processing, data lakes",                "category": "AI / Data Science",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0047"},
    {"id": 21, "name": "Predictive Modeling",          "description": "Regression, forecasting, feature engineering, model deployment",   "category": "AI / Data Science",      "parent_id": 15,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0049"},
    {"id": 22, "name": "Neural Networks",              "description": "Perceptrons, backprop, activation functions, architectures",        "category": "AI / Data Science",      "parent_id": 16,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0059"},
    {"id": 23, "name": "TensorFlow / PyTorch",         "description": "Deep learning frameworks: training, deployment, TFX/Lightning",    "category": "AI / Data Science",      "parent_id": 16,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0067"},
    {"id": 24, "name": "Generative AI",                "description": "LLMs, diffusion models, prompt engineering, RAG, fine-tuning",     "category": "AI / Data Science",      "parent_id": 16,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0069"},
    {"id": 25, "name": "MLOps",                        "description": "ML pipelines, model versioning, monitoring, MLflow, Kubeflow",     "category": "AI / Data Science",      "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0072"},
    # Electronics / Embedded / IoT
    {"id": 26, "name": "Digital Electronics",          "description": "Logic gates, flip-flops, FSMs, combinational/sequential circuits", "category": "Electronics",            "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0073"},
    {"id": 27, "name": "Analog Electronics",           "description": "Op-amps, transistor circuits, filters, ADC/DAC",                  "category": "Electronics",            "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0075"},
    {"id": 28, "name": "Embedded Systems",             "description": "Firmware, bare-metal programming, peripherals, RTOS basics",       "category": "Embedded / IoT",         "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0076"},
    {"id": 29, "name": "VLSI Design",                  "description": "RTL design, Verilog/VHDL, FPGA, ASIC flows",                      "category": "Electronics",            "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0078"},
    {"id": 30, "name": "Microcontrollers",             "description": "ARM Cortex-M, Arduino, STM32, peripheral drivers",                 "category": "Embedded / IoT",         "parent_id": 28,   "taxonomy_source": "Skillora", "taxonomy_id": "SKL0079"},
    {"id": 31, "name": "PCB Design",                   "description": "Schematic capture, layout, DRC, KiCad/Altium/EasyEDA",            "category": "Electronics",            "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0081"},
    {"id": 32, "name": "Communication Systems",        "description": "UART, SPI, I2C, CAN, BLE, LoRa, wireless protocols",              "category": "Embedded / IoT",         "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0083"},
    {"id": 33, "name": "IoT",                          "description": "Sensor interfacing, MQTT/CoAP, edge computing, cloud ingestion",  "category": "Embedded / IoT",         "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0085"},
    {"id": 34, "name": "MATLAB / Simulink",            "description": "Numerical computation, signal processing, Simulink modelling",    "category": "Electronics",            "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0087"},
    {"id": 35, "name": "Signal Processing",            "description": "Fourier transforms, filters, DSP, spectral analysis",             "category": "Embedded / IoT",         "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0088"},
    # Electrical Engineering
    {"id": 36, "name": "Electrical Machines",          "description": "Transformers, induction motors, synchronous machines, drives",    "category": "Electrical Engineering", "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0090"},
    {"id": 37, "name": "Power Systems",                "description": "Generation, transmission, distribution, load flow, protection",   "category": "Electrical Engineering", "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0091"},
    {"id": 38, "name": "Power Electronics",            "description": "DC-DC converters, inverters, rectifiers, MOSFET/IGBT drives",    "category": "Electrical Engineering", "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0092"},
    {"id": 39, "name": "Control Systems",              "description": "Transfer functions, Bode plots, PID control, state-space",        "category": "Electrical Engineering", "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0094"},
    {"id": 40, "name": "Electrical Measurements",      "description": "Instruments, measurement techniques, calibration, transducers",   "category": "Electrical Engineering", "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0096"},
    {"id": 41, "name": "PLC & SCADA",                  "description": "Programmable logic controllers, ladder logic, SCADA systems",    "category": "Electrical Engineering", "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0100"},
    {"id": 42, "name": "Renewable Energy",             "description": "Solar PV, wind energy, grid integration, energy storage",         "category": "Electrical Engineering", "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0101"},
    {"id": 43, "name": "Electric Vehicles",            "description": "EV powertrain, BMS, charging infrastructure, motor control",     "category": "Electrical Engineering", "parent_id": None, "taxonomy_source": "Skillora", "taxonomy_id": "SKL0102"},
    # Cross-cutting
    {"id": 44, "name": "Version Control (Git)",        "description": "Git branching, merging, pull requests, GitHub/GitLab workflow",   "category": "Software Development",   "parent_id": None, "taxonomy_source": "NSQF",     "taxonomy_id": None},
    {"id": 45, "name": "System Design",                "description": "Scalability, load balancing, caching, microservices architecture","category": "Software Development",   "parent_id": None, "taxonomy_source": "NSQF",     "taxonomy_id": None},
    {"id": 46, "name": "DevOps & CI/CD",               "description": "Docker, GitHub Actions, deployment pipelines, monitoring",        "category": "Software Development",   "parent_id": None, "taxonomy_source": "NSQF",     "taxonomy_id": None},
    {"id": 47, "name": "Object-Oriented Design",       "description": "SOLID principles, design patterns, clean code",                  "category": "Software Development",   "parent_id": None, "taxonomy_source": "NSQF",     "taxonomy_id": None},
    {"id": 48, "name": "REST API Design",              "description": "HTTP verbs, status codes, OpenAPI, authentication patterns",      "category": "Software Development",   "parent_id": None, "taxonomy_source": "NSQF",     "taxonomy_id": None},
    {"id": 49, "name": "Linux & Command Line",         "description": "Shell scripting, file system, process management, bash",          "category": "Software Development",   "parent_id": None, "taxonomy_source": "NSQF",     "taxonomy_id": None},
    {"id": 50, "name": "Feature Engineering",          "description": "Encoding, scaling, selection, dimensionality reduction",          "category": "AI / Data Science",      "parent_id": 15,   "taxonomy_source": "NSQF",     "taxonomy_id": None},
]

# ============================================================
# SKILL → COMPETENCY ID mapping (for cross-referencing)
# ============================================================
SKILL_TO_COMPETENCY_ID: dict[str, int] = {
    "C Programming": 1, "Java": 2, "Python": 3, "Data Structures & Algorithms": 4,
    "DBMS & SQL": 5, "SQL": 6, "Web Development": 7, "Operating Systems": 8,
    "Computer Networks": 9, "Cloud Computing": 10, "Cybersecurity": 11,
    "Statistics": 12, "Data Analysis": 13, "Data Visualization": 14,
    "Machine Learning": 15, "Deep Learning": 16, "Natural Language Processing": 17,
    "Computer Vision": 18, "Reinforcement Learning": 19, "Big Data Analytics": 20,
    "Predictive Modeling": 21, "Neural Networks": 22, "TensorFlow/PyTorch": 23,
    "Generative AI": 24, "MLOps": 25, "Digital Electronics": 26,
    "Analog Electronics": 27, "Embedded Systems": 28, "VLSI Design": 29,
    "Microcontrollers": 30, "PCB Design": 31, "Communication Systems": 32,
    "IoT": 33, "MATLAB/Simulink": 34, "Signal Processing": 35,
    "Electrical Machines": 36, "Power Systems": 37, "Power Electronics": 38,
    "Control Systems": 39, "Electrical Measurements": 40, "PLC & SCADA": 41,
    "Renewable Energy": 42, "Electric Vehicles": 43,
}

# ============================================================
# NORMALIZATION MAP  (304 entries, variant → competency_id)
# ============================================================
SKILL_NORMALIZATION_MAP: dict[str, int] = {
    "python": 3, "python programming": 3, "python3": 3, "python scripting": 3,
    "python development": 3, "python fundamentals": 3, "python basics": 3,
    "pandas": 3, "numpy": 3, "flask": 3, "django": 3, "fastapi": 3,
    "scipy": 3, "matplotlib": 3,
    "c programming": 1, "c language": 1, "embedded c": 1, "c++": 1, "cpp": 1, "c/c++": 1,
    "java": 2, "java programming": 2, "core java": 2, "java development": 2,
    "spring": 2, "spring boot": 2,
    "data structures": 4, "algorithms": 4, "dsa": 4,
    "data structures and algorithms": 4, "data structures & algorithms": 4, "leetcode": 4,
    "sql": 6, "structured query language": 6, "mysql": 6, "postgresql": 6,
    "postgres": 6, "sqlite": 6, "dbms": 5, "database management": 5,
    "database": 5, "sqlalchemy": 5, "orm": 5,
    "web development": 7, "web dev": 7, "html": 7, "css": 7, "javascript": 7,
    "js": 7, "react": 7, "reactjs": 7, "nextjs": 7, "next.js": 7,
    "nodejs": 7, "node.js": 7, "typescript": 7, "vue": 7, "angular": 7,
    "operating systems": 8, "os": 8, "linux": 8, "unix": 8, "ubuntu": 8,
    "computer networks": 9, "networking": 9, "tcp/ip": 9, "network protocols": 9,
    "cloud computing": 10, "aws": 10, "azure": 10, "gcp": 10, "google cloud": 10,
    "cloud": 10, "ec2": 10, "s3": 10, "lambda": 10,
    "cybersecurity": 11, "cyber security": 11, "network security": 11,
    "information security": 11, "ethical hacking": 11, "penetration testing": 11,
    "statistics": 12, "probability": 12, "hypothesis testing": 12,
    "statistical analysis": 12, "stats": 12,
    "data analysis": 13, "data analytics": 13, "eda": 13,
    "exploratory data analysis": 13, "business intelligence": 13,
    "data visualization": 14, "data visualisation": 14, "tableau": 14,
    "power bi": 14, "powerbi": 14, "seaborn": 14, "plotly": 14,
    "machine learning": 15, "ml": 15, "scikit-learn": 15, "sklearn": 15,
    "scikit learn": 15, "supervised learning": 15, "unsupervised learning": 15,
    "random forest": 15, "xgboost": 15, "classification": 15,
    "deep learning": 16, "dl": 16,
    "neural network": 22, "neural networks": 22,
    "natural language processing": 17, "nlp": 17, "text mining": 17,
    "sentiment analysis": 17, "hugging face": 17, "bert": 17, "gpt": 17,
    "computer vision": 18, "opencv": 18, "image processing": 18,
    "object detection": 18, "yolo": 18,
    "reinforcement learning": 19, "rl": 19, "q-learning": 19,
    "big data": 20, "big data analytics": 20, "apache spark": 20,
    "spark": 20, "hadoop": 20, "hive": 20, "kafka": 20,
    "predictive modeling": 21, "predictive modelling": 21, "forecasting": 21,
    "time series": 21, "regression": 21,
    "tensorflow": 23, "pytorch": 23, "keras": 23, "tensorflow/pytorch": 23, "torch": 23,
    "generative ai": 24, "genai": 24, "llm": 24, "large language model": 24,
    "chatgpt": 24, "prompt engineering": 24, "diffusion": 24,
    "mlops": 25, "ml ops": 25, "mlflow": 25, "kubeflow": 25, "model deployment": 25,
    "digital electronics": 26, "logic design": 26, "verilog": 26,
    "vhdl": 26, "fpga": 26, "digital circuits": 26,
    "analog electronics": 27, "analogue electronics": 27, "op-amp": 27,
    "operational amplifier": 27, "adc": 27, "dac": 27,
    "embedded systems": 28, "embedded": 28, "rtos": 28, "freertos": 28,
    "firmware": 28, "arm": 28, "arm cortex": 28, "bare metal": 28,
    "vlsi": 29, "vlsi design": 29, "asic": 29, "synthesis": 29, "rtl design": 29,
    "microcontrollers": 30, "microcontroller": 30, "arduino": 30,
    "stm32": 30, "avr": 30, "pic": 30, "raspberry pi": 30,
    "pcb design": 31, "pcb": 31, "kicad": 31, "altium": 31, "eagle": 31, "schematic": 31,
    "communication systems": 32, "uart": 32, "spi": 32, "i2c": 32,
    "can bus": 32, "ble": 32, "bluetooth": 32, "lora": 32,
    "wireless communication": 32, "rf": 32,
    "iot": 33, "internet of things": 33, "mqtt": 33, "coap": 33,
    "edge computing": 33, "smart devices": 33,
    "matlab": 34, "simulink": 34, "matlab/simulink": 34,
    "signal processing": 35, "dsp": 35, "digital signal processing": 35,
    "fourier transform": 35, "fft": 35, "filter design": 35,
    "electrical machines": 36, "transformers": 36, "induction motor": 36,
    "synchronous machine": 36, "motor drives": 36,
    "power systems": 37, "power system analysis": 37, "load flow": 37,
    "electrical grid": 37, "transmission lines": 37,
    "power electronics": 38, "dc-dc converter": 38, "inverter": 38,
    "rectifier": 38, "mosfet": 38, "igbt": 38,
    "control systems": 39, "pid": 39, "pid control": 39,
    "bode plot": 39, "transfer function": 39, "state space": 39,
    "electrical measurements": 40, "instrumentation": 40,
    "measurement": 40, "calibration": 40,
    "plc": 41, "scada": 41, "plc & scada": 41, "ladder logic": 41,
    "industrial automation": 41, "automation": 41,
    "renewable energy": 42, "solar": 42, "solar pv": 42, "wind energy": 42,
    "green energy": 42,
    "electric vehicles": 43, "ev": 43, "electric vehicle": 43,
    "battery management": 43, "bms": 43, "ev charging": 43,
    "git": 44, "github": 44, "gitlab": 44, "version control": 44, "git/github": 44,
    "system design": 45, "microservices": 45, "distributed systems": 45,
    "scalability": 45, "high availability": 45, "load balancing": 45,
    "devops": 46, "docker": 46, "ci/cd": 46, "kubernetes": 46,
    "k8s": 46, "github actions": 46, "jenkins": 46,
    "oop": 47, "object oriented programming": 47, "object-oriented programming": 47,
    "design patterns": 47, "solid principles": 47,
    "rest api": 48, "restful api": 48, "api development": 48,
    "api design": 48, "openapi": 48, "swagger": 48, "graphql": 48,
    "linux & command line": 49, "shell scripting": 49, "bash": 49,
    "command line": 49, "terminal": 49,
    "feature engineering": 50, "feature selection": 50, "data preprocessing": 50,
}

# ============================================================
# RELATED SKILLS MAP (for classification engine)
# ============================================================
RELATED_SKILLS: dict[int, list[int]] = {
    3:  [1, 2, 47, 48, 15, 13, 14, 50],
    1:  [28, 30, 4, 47],
    2:  [47, 45, 48],
    4:  [15, 45, 3],
    6:  [5, 13],
    5:  [6, 45],
    15: [16, 21, 12, 22, 23],
    16: [15, 22, 23, 17, 18],
    28: [30, 1, 33, 32],
    30: [28, 1, 26, 33],
    33: [28, 30, 10, 32],
    38: [37, 39, 36],
    39: [28, 34, 38],
    13: [3, 12, 14, 21],
    12: [15, 21, 13],
    44: [46],
    10: [46, 48],
    7:  [48, 45, 47],
    24: [17, 15, 16],
    25: [46, 10, 15],
    35: [28, 34],
    29: [26, 28],
    27: [31, 28],
    32: [33, 28],
    42: [37, 38],
    43: [38, 28, 39],
}


# ============================================================
# SECTION B: ROLES
# ============================================================
ROLES: list[dict[str, Any]] = [
    {"id": 1, "name": "Software Development Engineer", "description": "Builds and maintains backend services, APIs, system components. Works with Java, Python, C++ and Git, Docker, cloud platforms.", "sector": "Technology / Engineering"},
    {"id": 2, "name": "Data Analyst",                  "description": "Analyses structured datasets, builds dashboards, reports insights using Python/SQL, statistical methods, and visualization tools.", "sector": "Technology / Engineering"},
    {"id": 3, "name": "Data Scientist",                "description": "Develops predictive models, runs experiments, applies ML/DL. Requires strong statistics, Python, and domain knowledge.", "sector": "Technology / Engineering"},
    {"id": 4, "name": "ML Engineer",                   "description": "Productionises ML models, builds training pipelines, manages MLOps infrastructure. Bridges data science and software engineering.", "sector": "Technology / Engineering"},
    {"id": 5, "name": "Embedded Systems Engineer",     "description": "Designs and programs firmware for microcontrollers and real-time systems. Works with C, ARM, RTOS, and hardware interfaces.", "sector": "Technology / Engineering"},
    {"id": 6, "name": "IoT Solutions Engineer",        "description": "Designs end-to-end IoT systems: firmware, connectivity protocols, cloud ingestion, and dashboards.", "sector": "Technology / Engineering"},
    {"id": 7, "name": "Electrical Design Engineer",    "description": "Designs power systems, electrical schematics, control systems, and PCBs. Works on EV, renewable energy, and industrial automation.", "sector": "Technology / Engineering"},
    {"id": 8, "name": "Statistical Officer (MoSPI)",   "description": "Collects, analyses and publishes official government statistics. Supports survey design, data quality, and statistical reporting.", "sector": "Government / Statistics"},
]

ROLE_COMPETENCIES: list[dict[str, Any]] = [
    # SDE (role 1)
    {"role_id": 1, "competency_id": 1,  "required_level": 3, "importance": 0.9},
    {"role_id": 1, "competency_id": 2,  "required_level": 3, "importance": 0.9},
    {"role_id": 1, "competency_id": 3,  "required_level": 3, "importance": 0.9},
    {"role_id": 1, "competency_id": 4,  "required_level": 4, "importance": 1.0},
    {"role_id": 1, "competency_id": 5,  "required_level": 3, "importance": 0.8},
    {"role_id": 1, "competency_id": 7,  "required_level": 3, "importance": 0.8},
    {"role_id": 1, "competency_id": 8,  "required_level": 2, "importance": 0.7},
    {"role_id": 1, "competency_id": 9,  "required_level": 2, "importance": 0.6},
    {"role_id": 1, "competency_id": 10, "required_level": 2, "importance": 0.6},
    {"role_id": 1, "competency_id": 11, "required_level": 2, "importance": 0.5},
    {"role_id": 1, "competency_id": 44, "required_level": 3, "importance": 0.8},
    {"role_id": 1, "competency_id": 45, "required_level": 3, "importance": 0.8},
    {"role_id": 1, "competency_id": 46, "required_level": 2, "importance": 0.6},
    {"role_id": 1, "competency_id": 47, "required_level": 3, "importance": 0.8},
    {"role_id": 1, "competency_id": 48, "required_level": 3, "importance": 0.8},
    {"role_id": 1, "competency_id": 49, "required_level": 2, "importance": 0.6},
    {"role_id": 1, "competency_id": 24, "required_level": 2, "importance": 0.5},
    # Data Analyst (role 2)
    {"role_id": 2, "competency_id": 3,  "required_level": 3, "importance": 0.9},
    {"role_id": 2, "competency_id": 6,  "required_level": 3, "importance": 1.0},
    {"role_id": 2, "competency_id": 12, "required_level": 3, "importance": 1.0},
    {"role_id": 2, "competency_id": 13, "required_level": 4, "importance": 1.0},
    {"role_id": 2, "competency_id": 14, "required_level": 3, "importance": 0.9},
    {"role_id": 2, "competency_id": 21, "required_level": 2, "importance": 0.7},
    {"role_id": 2, "competency_id": 5,  "required_level": 2, "importance": 0.7},
    # Data Scientist (role 3)
    {"role_id": 3, "competency_id": 3,  "required_level": 4, "importance": 0.9},
    {"role_id": 3, "competency_id": 12, "required_level": 4, "importance": 1.0},
    {"role_id": 3, "competency_id": 13, "required_level": 3, "importance": 0.8},
    {"role_id": 3, "competency_id": 14, "required_level": 3, "importance": 0.8},
    {"role_id": 3, "competency_id": 15, "required_level": 4, "importance": 1.0},
    {"role_id": 3, "competency_id": 16, "required_level": 3, "importance": 0.8},
    {"role_id": 3, "competency_id": 17, "required_level": 3, "importance": 0.7},
    {"role_id": 3, "competency_id": 18, "required_level": 2, "importance": 0.6},
    {"role_id": 3, "competency_id": 19, "required_level": 2, "importance": 0.5},
    {"role_id": 3, "competency_id": 20, "required_level": 2, "importance": 0.6},
    {"role_id": 3, "competency_id": 21, "required_level": 3, "importance": 0.8},
    {"role_id": 3, "competency_id": 22, "required_level": 3, "importance": 0.7},
    {"role_id": 3, "competency_id": 23, "required_level": 3, "importance": 0.8},
    {"role_id": 3, "competency_id": 24, "required_level": 2, "importance": 0.6},
    {"role_id": 3, "competency_id": 6,  "required_level": 3, "importance": 0.8},
    {"role_id": 3, "competency_id": 50, "required_level": 3, "importance": 0.7},
    # ML Engineer (role 4)
    {"role_id": 4, "competency_id": 3,  "required_level": 4, "importance": 0.9},
    {"role_id": 4, "competency_id": 4,  "required_level": 3, "importance": 0.7},
    {"role_id": 4, "competency_id": 15, "required_level": 4, "importance": 1.0},
    {"role_id": 4, "competency_id": 16, "required_level": 3, "importance": 0.8},
    {"role_id": 4, "competency_id": 17, "required_level": 3, "importance": 0.7},
    {"role_id": 4, "competency_id": 18, "required_level": 2, "importance": 0.6},
    {"role_id": 4, "competency_id": 19, "required_level": 2, "importance": 0.5},
    {"role_id": 4, "competency_id": 20, "required_level": 3, "importance": 0.7},
    {"role_id": 4, "competency_id": 22, "required_level": 3, "importance": 0.7},
    {"role_id": 4, "competency_id": 23, "required_level": 4, "importance": 0.9},
    {"role_id": 4, "competency_id": 24, "required_level": 2, "importance": 0.6},
    {"role_id": 4, "competency_id": 25, "required_level": 3, "importance": 0.9},
    {"role_id": 4, "competency_id": 10, "required_level": 3, "importance": 0.8},
    {"role_id": 4, "competency_id": 46, "required_level": 3, "importance": 0.8},
    {"role_id": 4, "competency_id": 48, "required_level": 2, "importance": 0.6},
    {"role_id": 4, "competency_id": 50, "required_level": 4, "importance": 0.9},
    # Embedded Systems Engineer (role 5)
    {"role_id": 5, "competency_id": 1,  "required_level": 4, "importance": 1.0},
    {"role_id": 5, "competency_id": 8,  "required_level": 3, "importance": 0.8},
    {"role_id": 5, "competency_id": 26, "required_level": 3, "importance": 0.9},
    {"role_id": 5, "competency_id": 27, "required_level": 2, "importance": 0.7},
    {"role_id": 5, "competency_id": 28, "required_level": 4, "importance": 1.0},
    {"role_id": 5, "competency_id": 29, "required_level": 2, "importance": 0.5},
    {"role_id": 5, "competency_id": 30, "required_level": 4, "importance": 1.0},
    {"role_id": 5, "competency_id": 31, "required_level": 2, "importance": 0.6},
    {"role_id": 5, "competency_id": 32, "required_level": 3, "importance": 0.8},
    {"role_id": 5, "competency_id": 34, "required_level": 2, "importance": 0.5},
    {"role_id": 5, "competency_id": 35, "required_level": 2, "importance": 0.5},
    {"role_id": 5, "competency_id": 38, "required_level": 2, "importance": 0.5},
    {"role_id": 5, "competency_id": 39, "required_level": 3, "importance": 0.7},
    {"role_id": 5, "competency_id": 43, "required_level": 2, "importance": 0.5},
    {"role_id": 5, "competency_id": 44, "required_level": 2, "importance": 0.5},
    # IoT Solutions Engineer (role 6)
    {"role_id": 6, "competency_id": 1,  "required_level": 3, "importance": 0.9},
    {"role_id": 6, "competency_id": 3,  "required_level": 2, "importance": 0.7},
    {"role_id": 6, "competency_id": 9,  "required_level": 2, "importance": 0.6},
    {"role_id": 6, "competency_id": 10, "required_level": 3, "importance": 0.8},
    {"role_id": 6, "competency_id": 11, "required_level": 2, "importance": 0.5},
    {"role_id": 6, "competency_id": 26, "required_level": 2, "importance": 0.7},
    {"role_id": 6, "competency_id": 28, "required_level": 3, "importance": 0.9},
    {"role_id": 6, "competency_id": 30, "required_level": 3, "importance": 1.0},
    {"role_id": 6, "competency_id": 32, "required_level": 3, "importance": 0.9},
    {"role_id": 6, "competency_id": 33, "required_level": 4, "importance": 1.0},
    {"role_id": 6, "competency_id": 35, "required_level": 2, "importance": 0.6},
    {"role_id": 6, "competency_id": 48, "required_level": 2, "importance": 0.5},
    # Electrical Design Engineer (role 7)
    {"role_id": 7, "competency_id": 31, "required_level": 3, "importance": 0.8},
    {"role_id": 7, "competency_id": 34, "required_level": 3, "importance": 0.8},
    {"role_id": 7, "competency_id": 36, "required_level": 3, "importance": 0.9},
    {"role_id": 7, "competency_id": 37, "required_level": 4, "importance": 1.0},
    {"role_id": 7, "competency_id": 38, "required_level": 3, "importance": 0.9},
    {"role_id": 7, "competency_id": 39, "required_level": 3, "importance": 0.9},
    {"role_id": 7, "competency_id": 40, "required_level": 3, "importance": 0.7},
    {"role_id": 7, "competency_id": 41, "required_level": 3, "importance": 0.8},
    {"role_id": 7, "competency_id": 42, "required_level": 2, "importance": 0.6},
    {"role_id": 7, "competency_id": 43, "required_level": 2, "importance": 0.5},
    {"role_id": 7, "competency_id": 28, "required_level": 2, "importance": 0.5},
    # Statistical Officer MoSPI (role 8)
    {"role_id": 8, "competency_id": 12, "required_level": 4, "importance": 1.0},
    {"role_id": 8, "competency_id": 13, "required_level": 4, "importance": 1.0},
    {"role_id": 8, "competency_id": 14, "required_level": 3, "importance": 0.8},
    {"role_id": 8, "competency_id": 3,  "required_level": 2, "importance": 0.6},
    {"role_id": 8, "competency_id": 6,  "required_level": 2, "importance": 0.6},
    {"role_id": 8, "competency_id": 21, "required_level": 3, "importance": 0.8},
]

# ============================================================
# SECTION C: USERS (demo cross-domain profiles)
# ============================================================
USERS: list[dict[str, Any]] = [
    {"id": 1, "name": "Arjun Verma",    "education": "B.Tech EEE",       "department": "Electrical Engineering",     "experience": 2},
    {"id": 2, "name": "Priya Nair",     "education": "B.Tech Mechanical", "department": "Mechanical Engineering",     "experience": 1},
    {"id": 3, "name": "Rahul Das",      "education": "B.Tech ECE",        "department": "Electronics & Communication","experience": 2},
    {"id": 4, "name": "Sneha Kulkarni", "education": "B.Sc Statistics",   "department": "Statistics",                 "experience": 0},
    {"id": 5, "name": "Vikram Singh",   "education": "B.Tech CSE",        "department": "Computer Science",           "experience": 3},
]

USER_COMPETENCIES: list[dict[str, Any]] = [
    # Arjun EEE → SDE
    {"user_id": 1, "competency_id": 37, "current_level": 4, "evidence_source": "B.Tech EEE coursework"},
    {"user_id": 1, "competency_id": 38, "current_level": 3, "evidence_source": "B.Tech EEE coursework"},
    {"user_id": 1, "competency_id": 39, "current_level": 3, "evidence_source": "B.Tech EEE coursework"},
    {"user_id": 1, "competency_id": 36, "current_level": 3, "evidence_source": "B.Tech EEE coursework"},
    {"user_id": 1, "competency_id": 34, "current_level": 2, "evidence_source": "MATLAB lab sessions"},
    {"user_id": 1, "competency_id": 3,  "current_level": 2, "evidence_source": "Online Python course"},
    {"user_id": 1, "competency_id": 1,  "current_level": 2, "evidence_source": "Self-taught C programming"},
    {"user_id": 1, "competency_id": 4,  "current_level": 1, "evidence_source": "Brief DSA exposure"},
    {"user_id": 1, "competency_id": 44, "current_level": 1, "evidence_source": "Basic Git usage"},
    {"user_id": 1, "competency_id": 6,  "current_level": 1, "evidence_source": "Basic SQL course"},
    # Priya Mechanical → Data Analyst
    {"user_id": 2, "competency_id": 12, "current_level": 2, "evidence_source": "Engineering mathematics"},
    {"user_id": 2, "competency_id": 13, "current_level": 1, "evidence_source": "Excel data work"},
    {"user_id": 2, "competency_id": 14, "current_level": 1, "evidence_source": "Excel charts"},
    {"user_id": 2, "competency_id": 3,  "current_level": 1, "evidence_source": "None"},
    # Rahul ECE → Embedded
    {"user_id": 3, "competency_id": 26, "current_level": 4, "evidence_source": "B.Tech ECE coursework"},
    {"user_id": 3, "competency_id": 30, "current_level": 3, "evidence_source": "Arduino lab projects"},
    {"user_id": 3, "competency_id": 1,  "current_level": 3, "evidence_source": "C programming coursework"},
    {"user_id": 3, "competency_id": 35, "current_level": 3, "evidence_source": "DSP course"},
    {"user_id": 3, "competency_id": 31, "current_level": 2, "evidence_source": "PCB design lab"},
    {"user_id": 3, "competency_id": 28, "current_level": 2, "evidence_source": "Embedded systems coursework"},
    {"user_id": 3, "competency_id": 44, "current_level": 2, "evidence_source": "Git for assignments"},
    # Sneha Stats → Data Scientist
    {"user_id": 4, "competency_id": 12, "current_level": 4, "evidence_source": "B.Sc Statistics degree"},
    {"user_id": 4, "competency_id": 13, "current_level": 3, "evidence_source": "Research project"},
    {"user_id": 4, "competency_id": 21, "current_level": 3, "evidence_source": "Statistical modelling coursework"},
    {"user_id": 4, "competency_id": 3,  "current_level": 2, "evidence_source": "Python for Statistics NPTEL"},
    {"user_id": 4, "competency_id": 14, "current_level": 2, "evidence_source": "R ggplot experience"},
    {"user_id": 4, "competency_id": 15, "current_level": 1, "evidence_source": "Intro ML MOOC"},
    {"user_id": 4, "competency_id": 50, "current_level": 1, "evidence_source": "None"},
    # Vikram CSE → Data Analyst
    {"user_id": 5, "competency_id": 3,  "current_level": 4, "evidence_source": "B.Tech CSE + projects"},
    {"user_id": 5, "competency_id": 4,  "current_level": 4, "evidence_source": "Competitive programming"},
    {"user_id": 5, "competency_id": 47, "current_level": 3, "evidence_source": "B.Tech CSE OOP coursework"},
    {"user_id": 5, "competency_id": 44, "current_level": 3, "evidence_source": "GitHub projects"},
    {"user_id": 5, "competency_id": 6,  "current_level": 3, "evidence_source": "DBMS coursework"},
    {"user_id": 5, "competency_id": 5,  "current_level": 3, "evidence_source": "DBMS coursework"},
    {"user_id": 5, "competency_id": 12, "current_level": 2, "evidence_source": "Probability & Stats course"},
    {"user_id": 5, "competency_id": 13, "current_level": 2, "evidence_source": "Data science workshop"},
    {"user_id": 5, "competency_id": 14, "current_level": 2, "evidence_source": "Data science workshop"},
]


# ============================================================
# SECTION D: SKILL CAREER DATASET — all 105 rows from Excel
# Fields: skill_id, skill_name, skill_category, suitable_job_role,
#         primary_required_skill, recommended_supporting_skills,
#         experience_level, experience_range,
#         salary_min_lpa, salary_max_lpa,
#         learning_duration, working_duration, work_mode,
#         job_demand, career_growth,
#         education_background, suitable_industry,
#         suggested_portfolio_project
# competency_id resolved via SKILL_TO_COMPETENCY_ID
# ============================================================

_SUPP = "Communication, Problem Solving, Teamwork, Domain Knowledge"
_EXP  = "Entry Level: 0–2 years"
_EXPR = "0–2 years"
_SAL_B = "Indicative annual CTC range; varies by company, location and experience"
_LRND = "3–6 months for fundamentals; 6–12 months for job readiness"
_WORK = "Full-time: typically 40–48 hrs/week"
_MODE = "Onsite / Hybrid / Remote depending on employer"
_DEMAND = "Medium to High"
_GROWTH = "High with advanced skills and experience"
_EDU = "Relevant degree, diploma, certification or demonstrable project portfolio"
_IND = "Technology / Engineering / Services"
_NOTES = "Designed for Skillora job matching, skill analysis and salary guidance"

def _r(sid, sname, scat, role, pmin, pmax, cid_key=None):
    """Helper to build a skill career record dict."""
    cid = SKILL_TO_COMPETENCY_ID.get(cid_key or sname)
    return {
        "skill_id": sid, "skill_name": sname, "skill_category": scat,
        "suitable_job_role": role,
        "role_description": f"Uses {sname} and related technical knowledge to perform responsibilities associated with the {role} role.",
        "primary_required_skill": sname,
        "recommended_supporting_skills": _SUPP,
        "experience_level": _EXP, "experience_range": _EXPR,
        "salary_min_lpa": pmin, "salary_max_lpa": pmax, "salary_basis": _SAL_B,
        "learning_duration": _LRND, "working_duration": _WORK, "work_mode": _MODE,
        "job_demand": _DEMAND, "career_growth": _GROWTH,
        "education_background": _EDU, "suitable_industry": _IND,
        "suggested_portfolio_project": f"Build a practical project demonstrating {sname}",
        "skill_match_logic": f"High match when {sname} is present in the user profile; increase score with supporting skills",
        "missing_skill_recommendation": "Show missing role-specific skills and recommended learning path",
        "dataset_notes": _NOTES,
        "competency_id": cid,
    }

SKILL_CAREER_RECORDS: list[dict[str, Any]] = [
    # C Programming
    _r("SKL0001","C Programming","Software Development","Software Development Engineer",5,14),
    _r("SKL0002","C Programming","Software Development","Embedded Systems Engineer",4,11),
    _r("SKL0003","C Programming","Software Development","IoT Solutions Engineer",4,12),
    # Java
    _r("SKL0004","Java","Software Development","Software Development Engineer",5,14),
    # Python (multiple roles)
    _r("SKL0005","Python","Software Development","Software Development Engineer",5,14),
    _r("SKL0006","Python","Software Development","Data Analyst",4,10),
    _r("SKL0007","Python","Software Development","Data Scientist",7,18),
    _r("SKL0008","Python","Software Development","ML Engineer",7,20),
    _r("SKL0009","Python","Software Development","IoT Solutions Engineer",4,12),
    # DSA
    _r("SKL0010","Data Structures & Algorithms","AI / Data Science","Software Development Engineer",5,14),
    _r("SKL0011","Data Structures & Algorithms","AI / Data Science","ML Engineer",7,20),
    # DBMS & SQL
    _r("SKL0012","DBMS & SQL","Software Development","Software Development Engineer",5,14),
    _r("SKL0013","DBMS & SQL","Software Development","Data Analyst",4,10),
    _r("SKL0014","DBMS & SQL","Software Development","Data Scientist",7,18),
    # Web Development
    _r("SKL0015","Web Development","Professional / Technical","Software Development Engineer",5,14),
    # Operating Systems
    _r("SKL0016","Operating Systems","Professional / Technical","Software Development Engineer",5,14),
    _r("SKL0017","Operating Systems","Professional / Technical","Embedded Systems Engineer",4,11),
    # Computer Networks
    _r("SKL0018","Computer Networks","IT Infrastructure","Software Development Engineer",5,14),
    _r("SKL0019","Computer Networks","IT Infrastructure","IoT Solutions Engineer",4,12),
    # Cloud Computing
    _r("SKL0020","Cloud Computing","IT Infrastructure","Software Development Engineer",5,14),
    _r("SKL0021","Cloud Computing","IT Infrastructure","ML Engineer",7,20),
    _r("SKL0022","Cloud Computing","IT Infrastructure","IoT Solutions Engineer",4,12),
    # Cybersecurity
    _r("SKL0023","Cybersecurity","IT Infrastructure","Software Development Engineer",5,14),
    _r("SKL0024","Cybersecurity","IT Infrastructure","IoT Solutions Engineer",4,12),
    # Python duplicates (dataset has these as separate rows)
    _r("SKL0025","Python","Software Development","Data Analyst",4,10),
    _r("SKL0026","Python","Software Development","Data Scientist",7,18),
    _r("SKL0027","Python","Software Development","ML Engineer",7,20),
    _r("SKL0028","Python","Software Development","Software Development Engineer",5,14),
    # Statistics
    _r("SKL0029","Statistics","Professional / Technical","Data Analyst",4,10),
    _r("SKL0030","Statistics","Professional / Technical","Data Scientist",7,18),
    _r("SKL0031","Statistics","Professional / Technical","Statistical Officer (MoSPI)",4,11),
    # Data Analysis
    _r("SKL0032","Data Analysis","AI / Data Science","Data Analyst",4,10),
    _r("SKL0033","Data Analysis","AI / Data Science","Data Scientist",7,18),
    _r("SKL0034","Data Analysis","AI / Data Science","Statistical Officer (MoSPI)",4,11),
    # SQL
    _r("SKL0035","SQL","Software Development","Data Analyst",4,10),
    _r("SKL0036","SQL","Software Development","Data Scientist",7,18),
    _r("SKL0037","SQL","Software Development","Software Development Engineer",5,14),
    # Machine Learning
    _r("SKL0038","Machine Learning","AI / Data Science","Data Scientist",7,18),
    _r("SKL0039","Machine Learning","AI / Data Science","ML Engineer",7,20),
    # Data Visualization
    _r("SKL0040","Data Visualization","AI / Data Science","Data Analyst",4,10),
    _r("SKL0041","Data Visualization","AI / Data Science","Data Scientist",7,18),
    _r("SKL0042","Data Visualization","AI / Data Science","Statistical Officer (MoSPI)",4,11),
    # Deep Learning
    _r("SKL0043","Deep Learning","AI / Data Science","Data Scientist",7,18),
    _r("SKL0044","Deep Learning","AI / Data Science","ML Engineer",7,20),
    # NLP
    _r("SKL0045","Natural Language Processing","Professional / Technical","Data Scientist",7,18),
    _r("SKL0046","Natural Language Processing","Professional / Technical","ML Engineer",7,20),
    # Big Data Analytics
    _r("SKL0047","Big Data Analytics","AI / Data Science","Data Scientist",7,18),
    _r("SKL0048","Big Data Analytics","AI / Data Science","ML Engineer",7,20),
    # Predictive Modeling
    _r("SKL0049","Predictive Modeling","Professional / Technical","Data Analyst",4,10),
    _r("SKL0050","Predictive Modeling","Professional / Technical","Data Scientist",7,18),
    # Python more duplicates
    _r("SKL0051","Python","Software Development","ML Engineer",7,20),
    _r("SKL0052","Python","Software Development","Data Scientist",7,18),
    _r("SKL0053","Python","Software Development","Data Analyst",4,10),
    _r("SKL0054","Python","Software Development","Software Development Engineer",5,14),
    # Machine Learning duplicates
    _r("SKL0055","Machine Learning","AI / Data Science","ML Engineer",7,20),
    _r("SKL0056","Machine Learning","AI / Data Science","Data Scientist",7,18),
    # Deep Learning duplicates
    _r("SKL0057","Deep Learning","AI / Data Science","ML Engineer",7,20),
    _r("SKL0058","Deep Learning","AI / Data Science","Data Scientist",7,18),
    # Neural Networks
    _r("SKL0059","Neural Networks","IT Infrastructure","ML Engineer",7,20),
    _r("SKL0060","Neural Networks","IT Infrastructure","Data Scientist",7,18),
    # NLP duplicates
    _r("SKL0061","Natural Language Processing","Professional / Technical","ML Engineer",7,20),
    _r("SKL0062","Natural Language Processing","Professional / Technical","Data Scientist",7,18),
    # Computer Vision
    _r("SKL0063","Computer Vision","AI / Data Science","ML Engineer",7,20),
    _r("SKL0064","Computer Vision","AI / Data Science","Data Scientist",7,18),
    # Reinforcement Learning
    _r("SKL0065","Reinforcement Learning","Professional / Technical","ML Engineer",7,20),
    _r("SKL0066","Reinforcement Learning","Professional / Technical","Data Scientist",7,18),
    # TensorFlow/PyTorch
    _r("SKL0067","TensorFlow/PyTorch","Professional / Technical","ML Engineer",7,20,"TensorFlow/PyTorch"),
    _r("SKL0068","TensorFlow/PyTorch","Professional / Technical","Data Scientist",7,18,"TensorFlow/PyTorch"),
    # Generative AI
    _r("SKL0069","Generative AI","AI / Data Science","ML Engineer",7,20),
    _r("SKL0070","Generative AI","AI / Data Science","Data Scientist",7,18),
    _r("SKL0071","Generative AI","AI / Data Science","Software Development Engineer",5,14),
    # MLOps
    _r("SKL0072","MLOps","Professional / Technical","ML Engineer",7,20),
    # Digital Electronics
    _r("SKL0073","Digital Electronics","Electrical / Electronics","Embedded Systems Engineer",4,11),
    _r("SKL0074","Digital Electronics","Electrical / Electronics","IoT Solutions Engineer",4,12),
    # Analog Electronics
    _r("SKL0075","Analog Electronics","Electrical / Electronics","Embedded Systems Engineer",4,11),
    # Embedded Systems
    _r("SKL0076","Embedded Systems","Embedded / IoT / Robotics","Embedded Systems Engineer",4,11),
    _r("SKL0077","Embedded Systems","Embedded / IoT / Robotics","IoT Solutions Engineer",4,12),
    # VLSI Design
    _r("SKL0078","VLSI Design","Engineering Design","Embedded Systems Engineer",4,11),
    # Microcontrollers
    _r("SKL0079","Microcontrollers","Embedded / IoT / Robotics","Embedded Systems Engineer",4,11),
    _r("SKL0080","Microcontrollers","Embedded / IoT / Robotics","IoT Solutions Engineer",4,12),
    # PCB Design
    _r("SKL0081","PCB Design","Engineering Design","Embedded Systems Engineer",4,11),
    _r("SKL0082","PCB Design","Engineering Design","Electrical Design Engineer",3.5,9),
    # Communication Systems
    _r("SKL0083","Communication Systems","Professional / Technical","Embedded Systems Engineer",4,11),
    _r("SKL0084","Communication Systems","Professional / Technical","IoT Solutions Engineer",4,12),
    # IoT
    _r("SKL0085","IoT","Embedded / IoT / Robotics","IoT Solutions Engineer",4,12),
    _r("SKL0086","IoT","Embedded / IoT / Robotics","Embedded Systems Engineer",4,11),
    # MATLAB/Simulink
    _r("SKL0087","MATLAB/Simulink","Electrical / Electronics","Embedded Systems Engineer",4,11,"MATLAB/Simulink"),
    # Signal Processing
    _r("SKL0088","Signal Processing","Professional / Technical","Embedded Systems Engineer",4,11),
    _r("SKL0089","Signal Processing","Professional / Technical","IoT Solutions Engineer",4,12),
    # Electrical Machines
    _r("SKL0090","Electrical Machines","Electrical / Electronics","Electrical Design Engineer",3.5,9),
    # Power Systems
    _r("SKL0091","Power Systems","Electrical / Electronics","Electrical Design Engineer",3.5,9),
    # Power Electronics
    _r("SKL0092","Power Electronics","Electrical / Electronics","Electrical Design Engineer",3.5,9),
    _r("SKL0093","Power Electronics","Electrical / Electronics","Embedded Systems Engineer",4,11),
    # Control Systems
    _r("SKL0094","Control Systems","Professional / Technical","Electrical Design Engineer",3.5,9),
    _r("SKL0095","Control Systems","Professional / Technical","Embedded Systems Engineer",4,11),
    # Electrical Measurements
    _r("SKL0096","Electrical Measurements","Electrical / Electronics","Electrical Design Engineer",3.5,9),
    # Embedded Systems more
    _r("SKL0097","Embedded Systems","Embedded / IoT / Robotics","Electrical Design Engineer",3.5,9),
    _r("SKL0098","Embedded Systems","Embedded / IoT / Robotics","Embedded Systems Engineer",4,11),
    _r("SKL0099","Embedded Systems","Embedded / IoT / Robotics","IoT Solutions Engineer",4,12),
    # PLC & SCADA
    _r("SKL0100","PLC & SCADA","Engineering Design","Electrical Design Engineer",3.5,9),
    # Renewable Energy
    _r("SKL0101","Renewable Energy","Professional / Technical","Electrical Design Engineer",3.5,9),
    # Electric Vehicles
    _r("SKL0102","Electric Vehicles","Professional / Technical","Electrical Design Engineer",3.5,9),
    _r("SKL0103","Electric Vehicles","Professional / Technical","Embedded Systems Engineer",4,11),
    # MATLAB/Simulink more
    _r("SKL0104","MATLAB/Simulink","Electrical / Electronics","Electrical Design Engineer",3.5,9,"MATLAB/Simulink"),
    _r("SKL0105","MATLAB/Simulink","Electrical / Electronics","Embedded Systems Engineer",4,11,"MATLAB/Simulink"),
]


# ============================================================
# SECTION E: SKILLORA LEARNING RESOURCES
# All 4 paid + 4 free resources per skill — URLs from dataset.
# is_free: False = paid, True = free
# slot_number: 1-4 within each group
# ============================================================

def _res(sname, roles_str, platform, title, url, is_free, slot):
    cid = SKILL_TO_COMPETENCY_ID.get(sname)
    return {
        "skill_name": sname, "roles": roles_str,
        "platform": platform, "course_title": title,
        "course_url": url, "is_free": is_free,
        "slot_number": slot, "competency_id": cid,
    }

_R_CPP = "Software Development Engineer; Embedded Systems Engineer; IoT Solutions Engineer"
_R_JAVA = "Software Development Engineer"
_R_PY = "Software Development Engineer; Data Analyst; Data Scientist; ML Engineer; IoT Solutions Engineer"
_R_DSA = "Software Development Engineer; ML Engineer"
_R_DBMS = "Software Development Engineer; Data Analyst; Data Scientist"
_R_WEB = "Software Development Engineer"
_R_OS = "Software Development Engineer; Embedded Systems Engineer"
_R_NET = "Software Development Engineer; IoT Solutions Engineer"
_R_CLD = "Software Development Engineer; ML Engineer; IoT Solutions Engineer"
_R_SEC = "Software Development Engineer; IoT Solutions Engineer"
_R_STAT = "Data Analyst; Data Scientist; Statistical Officer (MoSPI)"
_R_DA = "Data Analyst; Data Scientist; Statistical Officer (MoSPI)"
_R_SQL = "Data Analyst; Data Scientist; Software Development Engineer"
_R_ML = "Data Scientist; ML Engineer"
_R_VIZ = "Data Analyst; Data Scientist; Statistical Officer (MoSPI)"
_R_DL = "Data Scientist; ML Engineer"
_R_NLP = "Data Scientist; ML Engineer"
_R_BIG = "Data Scientist; ML Engineer"
_R_PRED = "Data Analyst; Data Scientist"
_R_PY2 = "ML Engineer; Data Scientist; Data Analyst; Software Development Engineer"
_R_ML2 = "ML Engineer; Data Scientist"
_R_DL2 = "ML Engineer; Data Scientist"
_R_NN = "ML Engineer; Data Scientist"
_R_NLP2 = "ML Engineer; Data Scientist"
_R_CV = "ML Engineer; Data Scientist"
_R_RL = "ML Engineer; Data Scientist"
_R_TF = "ML Engineer; Data Scientist"
_R_GEN = "ML Engineer; Data Scientist; Software Development Engineer"
_R_MOP = "ML Engineer"
_R_DE = "Embedded Systems Engineer; IoT Solutions Engineer"
_R_AE = "Embedded Systems Engineer"
_R_EMB = "Embedded Systems Engineer; IoT Solutions Engineer"
_R_VLS = "Embedded Systems Engineer"
_R_MCU = "Embedded Systems Engineer; IoT Solutions Engineer"
_R_PCB = "Embedded Systems Engineer; Electrical Design Engineer"
_R_COM = "Embedded Systems Engineer; IoT Solutions Engineer"
_R_IOT = "IoT Solutions Engineer; Embedded Systems Engineer"
_R_MAT = "Embedded Systems Engineer"
_R_SIG = "Embedded Systems Engineer; IoT Solutions Engineer"
_R_ELM = "Electrical Design Engineer"
_R_PWS = "Electrical Design Engineer"
_R_PWE = "Electrical Design Engineer; Embedded Systems Engineer"
_R_CTL = "Electrical Design Engineer; Embedded Systems Engineer"
_R_EMS = "Electrical Design Engineer"
_R_EMB2 = "Electrical Design Engineer; Embedded Systems Engineer; IoT Solutions Engineer"
_R_PLC = "Electrical Design Engineer"
_R_REN = "Electrical Design Engineer"
_R_EV = "Electrical Design Engineer; Embedded Systems Engineer"
_R_MAT2 = "Electrical Design Engineer; Embedded Systems Engineer"

SKILLORA_RESOURCES: list[dict[str, Any]] = [
    # ── C Programming ───────────────────────────────────────────────────────
    _res("C Programming",_R_CPP,"Udemy","C Programming Bootcamp - The Complete C Language Course","https://www.udemy.com/course/c-programming-bootcamp-for-beginners/",False,1),
    _res("C Programming",_R_CPP,"Coursera","C Programming: Getting Started (Duke University)","https://www.coursera.org/learn/c-programming-getting-started",False,2),
    _res("C Programming",_R_CPP,"LinkedIn Learning","Complete Guide to C Programming Foundations","https://www.linkedin.com/learning/complete-guide-to-c-programming-foundations",False,3),
    _res("C Programming",_R_CPP,"edX","C Programming: Getting Started (Dartmouth)","https://www.edx.org/learn/c-programming/dartmouth-c-programming-getting-started",False,4),
    _res("C Programming",_R_CPP,"NPTEL","Programming in C","https://www.nptel.ac.in/courses/106105171",True,1),
    _res("C Programming",_R_CPP,"MIT OpenCourseWare","Practical Programming in C","https://ocw.mit.edu/courses/6-087-practical-programming-in-c-january-iap-2010/",True,2),
    _res("C Programming",_R_CPP,"edX","C Programming: Getting Started (audit option)","https://www.edx.org/learn/c-programming/dartmouth-c-programming-getting-started",True,3),
    _res("C Programming",_R_CPP,"Harvard CS50","CS50x Introduction to Computer Science","https://cs50.harvard.edu/x/2026/",True,4),
    # ── Java ────────────────────────────────────────────────────────────────
    _res("Java",_R_JAVA,"Udemy","Java Programming Masterclass for Software Developers","https://www.udemy.com/course/java-the-complete-java-developer-course/",False,1),
    _res("Java",_R_JAVA,"Coursera","Object Oriented Programming in Java","https://www.coursera.org/learn/object-oriented-java",False,2),
    _res("Java",_R_JAVA,"LinkedIn Learning","Java Essential Training","https://www.linkedin.com/learning/paths/getting-started-as-a-java-developer",False,3),
    _res("Java",_R_JAVA,"edX","Introduction to Java Programming","https://www.edx.org/learn/java",False,4),
    _res("Java",_R_JAVA,"MOOC.fi","Java Programming I & II","https://java-programming.mooc.fi/",True,1),
    _res("Java",_R_JAVA,"Codecademy","Learn Java","https://www.codecademy.com/learn/learn-java",True,2),
    _res("Java",_R_JAVA,"freeCodeCamp","Java Programming Tutorial","https://www.freecodecamp.org/news/java-programming-for-beginners/",True,3),
    _res("Java",_R_JAVA,"edX","Java programming courses — audit option","https://www.edx.org/learn/java",True,4),
    # ── Python ──────────────────────────────────────────────────────────────
    _res("Python",_R_PY,"Udemy","The Complete Python Bootcamp From Zero to Hero in Python","https://www.udemy.com/course/complete-python-bootcamp/",False,1),
    _res("Python",_R_PY,"Coursera","Python for Everybody","https://www.coursera.org/specializations/python",False,2),
    _res("Python",_R_PY,"LinkedIn Learning","Python Essential Training","https://www.linkedin.com/learning/python-essential-training",False,3),
    _res("Python",_R_PY,"DataCamp","Introduction to Python","https://www.datacamp.com/courses/intro-to-python-for-data-science",False,4),
    _res("Python",_R_PY,"Kaggle Learn","Python","https://www.kaggle.com/learn/python",True,1),
    _res("Python",_R_PY,"freeCodeCamp","Scientific Computing with Python","https://www.freecodecamp.org/learn/scientific-computing-with-python/",True,2),
    _res("Python",_R_PY,"MIT OpenCourseWare","Introduction to Computer Science and Programming in Python","https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/",True,3),
    _res("Python",_R_PY,"Codecademy","Learn Python 3","https://www.codecademy.com/learn/learn-python-3",True,4),
    # ── Data Structures & Algorithms ────────────────────────────────────────
    _res("Data Structures & Algorithms",_R_DSA,"Udemy","Data Structures and Algorithms - Python","https://www.udemy.com/course/algorithms-and-data-structures-in-python/",False,1),
    _res("Data Structures & Algorithms",_R_DSA,"Coursera","Data Structures","https://www.coursera.org/learn/data-structures",False,2),
    _res("Data Structures & Algorithms",_R_DSA,"LinkedIn Learning","Become a Data Structures & Algorithms Developer","https://www.linkedin.com/learning/paths/become-a-data-structures-and-algorithms-developer",False,3),
    _res("Data Structures & Algorithms",_R_DSA,"edX","Data Structures and Algorithms","https://www.edx.org/learn/data-structures",False,4),
    _res("Data Structures & Algorithms",_R_DSA,"MIT OpenCourseWare","Introduction to Algorithms","https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/",True,1),
    _res("Data Structures & Algorithms",_R_DSA,"freeCodeCamp","Data Structures & Algorithms JavaScript","https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/",True,2),
    _res("Data Structures & Algorithms",_R_DSA,"Coursera","Data Structures (audit option)","https://www.coursera.org/learn/data-structures",True,3),
    _res("Data Structures & Algorithms",_R_DSA,"edX","Data Structures and Algorithms (audit option)","https://www.edx.org/learn/data-structures",True,4),
    # ── DBMS & SQL ──────────────────────────────────────────────────────────
    _res("DBMS & SQL",_R_DBMS,"Coursera","Databases and SQL for Data Science with Python","https://www.coursera.org/learn/sql-data-science",False,1),
    _res("DBMS & SQL",_R_DBMS,"Udemy","The Complete SQL Bootcamp","https://www.udemy.com/course/the-complete-sql-bootcamp/",False,2),
    _res("DBMS & SQL",_R_DBMS,"LinkedIn Learning","SQL Essential Training","https://www.linkedin.com/learning/sql-essential-training-3",False,3),
    _res("DBMS & SQL",_R_DBMS,"DataCamp","Introduction to SQL","https://www.datacamp.com/courses/introduction-to-sql",False,4),
    _res("DBMS & SQL",_R_DBMS,"Kaggle Learn","Intro to SQL","https://www.kaggle.com/learn/intro-to-sql",True,1),
    _res("DBMS & SQL",_R_DBMS,"Khan Academy","Intro to SQL","https://www.khanacademy.org/computing/computer-programming/sql",True,2),
    _res("DBMS & SQL",_R_DBMS,"freeCodeCamp","Relational Database / SQL curriculum","https://www.freecodecamp.org/learn/relational-database/",True,3),
    _res("DBMS & SQL",_R_DBMS,"Coursera","SQL for Data Science (audit option)","https://www.coursera.org/learn/sql-for-data-science",True,4),
    # ── Web Development ─────────────────────────────────────────────────────
    _res("Web Development",_R_WEB,"Udemy","The Web Developer Bootcamp","https://www.udemy.com/course/the-web-developer-bootcamp/",False,1),
    _res("Web Development",_R_WEB,"Coursera","Introduction to Front-End Development","https://www.coursera.org/learn/introduction-to-front-end-development",False,2),
    _res("Web Development",_R_WEB,"LinkedIn Learning","Become a Web Developer","https://www.linkedin.com/learning/paths/become-a-web-developer",False,3),
    _res("Web Development",_R_WEB,"edX","Web Development with JavaScript","https://www.edx.org/learn/javascript",False,4),
    _res("Web Development",_R_WEB,"MDN Web Docs","Learn Web Development","https://developer.mozilla.org/en-US/docs/Learn_web_development",True,1),
    _res("Web Development",_R_WEB,"freeCodeCamp","Responsive Web Design","https://www.freecodecamp.org/learn/2022/responsive-web-design/",True,2),
    _res("Web Development",_R_WEB,"The Odin Project","Foundations","https://www.theodinproject.com/paths/foundations/courses/foundations",True,3),
    _res("Web Development",_R_WEB,"University of Helsinki","Full Stack Open","https://fullstackopen.com/en/",True,4),
    # ── Operating Systems ───────────────────────────────────────────────────
    _res("Operating Systems",_R_OS,"Coursera","Operating Systems and You: Becoming a Power User","https://www.coursera.org/learn/os-power-user",False,1),
    _res("Operating Systems",_R_OS,"Udemy","Operating Systems from Scratch","https://www.udemy.com/course/operating-systems-from-scratch/",False,2),
    _res("Operating Systems",_R_OS,"LinkedIn Learning","Linux Essentials","https://www.linkedin.com/learning/linux-essential-training",False,3),
    _res("Operating Systems",_R_OS,"edX","Introduction to Operating Systems","https://www.edx.org/learn/operating-systems",False,4),
    _res("Operating Systems",_R_OS,"NPTEL","Introduction to Operating Systems","https://www.nptel.ac.in/courses/106106144",True,1),
    _res("Operating Systems",_R_OS,"MIT OpenCourseWare","Operating System Engineering","https://pdos.csail.mit.edu/6.1810/",True,2),
    _res("Operating Systems",_R_OS,"MIT OpenCourseWare","Computer System Engineering","https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/",True,3),
    _res("Operating Systems",_R_OS,"edX","Operating Systems (audit option)","https://www.edx.org/learn/operating-systems",True,4),
    # ── Computer Networks ───────────────────────────────────────────────────
    _res("Computer Networks",_R_NET,"Coursera","The Bits and Bytes of Computer Networking","https://www.coursera.org/learn/computer-networking",False,1),
    _res("Computer Networks",_R_NET,"Udemy","The Complete Networking Fundamentals Course","https://www.udemy.com/course/complete-networking-fundamentals-course-ccna/",False,2),
    _res("Computer Networks",_R_NET,"LinkedIn Learning","Networking Foundations: Networking Basics","https://www.linkedin.com/learning/networking-foundations-networking-basics",False,3),
    _res("Computer Networks",_R_NET,"edX","Computer Networking","https://www.edx.org/learn/computer-networking",False,4),
    _res("Computer Networks",_R_NET,"NPTEL","Computer Networks","https://onlinecourses.nptel.ac.in/e-learning/preview/noc26_cs99",True,1),
    _res("Computer Networks",_R_NET,"Cisco Networking Academy","Networking Basics","https://www.netacad.com/courses/networking-basics",True,2),
    _res("Computer Networks",_R_NET,"MIT OpenCourseWare","Computer Networks","https://ocw.mit.edu/courses/6-829-computer-networks-fall-2002/",True,3),
    _res("Computer Networks",_R_NET,"Coursera","The Bits and Bytes of Computer Networking (audit option)","https://www.coursera.org/learn/computer-networking",True,4),
    # ── Cloud Computing ─────────────────────────────────────────────────────
    _res("Cloud Computing",_R_CLD,"Coursera","Cloud Computing Basics (Cloud 101)","https://www.coursera.org/learn/cloud-computing-basics",False,1),
    _res("Cloud Computing",_R_CLD,"Udemy","AWS Certified Cloud Practitioner - Full Course","https://www.udemy.com/course/aws-certified-cloud-practitioner-new/",False,2),
    _res("Cloud Computing",_R_CLD,"LinkedIn Learning","Learning Cloud Computing: Core Concepts","https://www.linkedin.com/learning/learning-cloud-computing-core-concepts",False,3),
    _res("Cloud Computing",_R_CLD,"edX","Cloud Computing","https://www.edx.org/learn/cloud-computing",False,4),
    _res("Cloud Computing",_R_CLD,"AWS Skill Builder","AWS Cloud Practitioner Essentials","https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials",True,1),
    _res("Cloud Computing",_R_CLD,"Google Cloud Skills Boost","Cloud Digital Leader learning path","https://www.cloudskillsboost.google/paths/9",True,2),
    _res("Cloud Computing",_R_CLD,"Microsoft Learn","Azure Fundamentals learning path","https://learn.microsoft.com/training/paths/azure-fundamentals-describe-cloud-concepts/",True,3),
    _res("Cloud Computing",_R_CLD,"IBM SkillsBuild","Cloud Computing fundamentals","https://skillsbuild.org/",True,4),
    # ── Cybersecurity ───────────────────────────────────────────────────────
    _res("Cybersecurity",_R_SEC,"Coursera","Google Cybersecurity Professional Certificate","https://www.coursera.org/professional-certificates/google-cybersecurity",False,1),
    _res("Cybersecurity",_R_SEC,"Udemy","The Complete Cyber Security Course","https://www.udemy.com/course/the-complete-internet-security-privacy-course-vol-1/",False,2),
    _res("Cybersecurity",_R_SEC,"LinkedIn Learning","Cybersecurity Foundations","https://www.linkedin.com/learning/cybersecurity-foundations",False,3),
    _res("Cybersecurity",_R_SEC,"edX","Cybersecurity Fundamentals","https://www.edx.org/learn/cybersecurity",False,4),
    _res("Cybersecurity",_R_SEC,"Cisco Networking Academy","Introduction to Cybersecurity","https://www.netacad.com/courses/introduction-to-cybersecurity",True,1),
    _res("Cybersecurity",_R_SEC,"Google","Cybersecurity learning resources","https://www.google.com/about/careers/applications/students/",True,2),
    _res("Cybersecurity",_R_SEC,"MIT OpenCourseWare","Computer Systems Security","https://ocw.mit.edu/courses/6-858-computer-systems-security-fall-2014/",True,3),
    _res("Cybersecurity",_R_SEC,"Coursera","Foundations of Cybersecurity (audit option)","https://www.coursera.org/learn/foundations-of-cybersecurity",True,4),
    # ── Statistics ──────────────────────────────────────────────────────────
    _res("Statistics",_R_STAT,"Coursera","Statistics with Python","https://www.coursera.org/specializations/statistics-with-python",False,1),
    _res("Statistics",_R_STAT,"Udemy","Statistics for Data Science and Business Analysis","https://www.udemy.com/course/statistics-for-data-science/",False,2),
    _res("Statistics",_R_STAT,"LinkedIn Learning","Statistics Foundations","https://www.linkedin.com/learning/statistics-foundations-1",False,3),
    _res("Statistics",_R_STAT,"DataCamp","Statistics Fundamentals","https://www.datacamp.com/courses/statistics-fundamentals",False,4),
    _res("Statistics",_R_STAT,"Khan Academy","Statistics & Probability","https://www.khanacademy.org/math/statistics-probability",True,1),
    _res("Statistics",_R_STAT,"OpenStax","Introductory Statistics 2e","https://openstax.org/details/books/introductory-statistics-2e",True,2),
    _res("Statistics",_R_STAT,"MIT OpenCourseWare","Introduction to Probability","https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2014/",True,3),
    _res("Statistics",_R_STAT,"Coursera","Statistics with Python (audit option)","https://www.coursera.org/specializations/statistics-with-python",True,4),
    # ── Data Analysis ───────────────────────────────────────────────────────
    _res("Data Analysis",_R_DA,"Coursera","Data Analysis with Python","https://www.coursera.org/learn/data-analysis-with-python",False,1),
    _res("Data Analysis",_R_DA,"Udemy","Data Analysis with Pandas and Python","https://www.udemy.com/course/data-analysis-with-pandas/",False,2),
    _res("Data Analysis",_R_DA,"LinkedIn Learning","Learning Data Analytics","https://www.linkedin.com/learning/paths/become-a-data-analyst",False,3),
    _res("Data Analysis",_R_DA,"DataCamp","Data Analyst with Python","https://www.datacamp.com/tracks/data-analyst-with-python",False,4),
    _res("Data Analysis",_R_DA,"Kaggle Learn","Pandas","https://www.kaggle.com/learn/pandas",True,1),
    _res("Data Analysis",_R_DA,"freeCodeCamp","Data Analysis with Python","https://www.freecodecamp.org/learn/data-analysis-with-python/",True,2),
    _res("Data Analysis",_R_DA,"IBM SkillsBuild","Data Analytics fundamentals","https://skillsbuild.org/",True,3),
    _res("Data Analysis",_R_DA,"Coursera","Data Analysis with Python (audit option)","https://www.coursera.org/learn/data-analysis-with-python",True,4),
    # ── SQL ─────────────────────────────────────────────────────────────────
    _res("SQL",_R_SQL,"Coursera","SQL for Data Science","https://www.coursera.org/learn/sql-for-data-science",False,1),
    _res("SQL",_R_SQL,"Udemy","The Complete SQL Bootcamp","https://www.udemy.com/course/the-complete-sql-bootcamp/",False,2),
    _res("SQL",_R_SQL,"LinkedIn Learning","SQL Essential Training","https://www.linkedin.com/learning/sql-essential-training-3",False,3),
    _res("SQL",_R_SQL,"DataCamp","Introduction to SQL","https://www.datacamp.com/courses/introduction-to-sql",False,4),
    _res("SQL",_R_SQL,"Kaggle Learn","Intro to SQL","https://www.kaggle.com/learn/intro-to-sql",True,1),
    _res("SQL",_R_SQL,"Khan Academy","Intro to SQL","https://www.khanacademy.org/computing/computer-programming/sql",True,2),
    _res("SQL",_R_SQL,"freeCodeCamp","Relational Database","https://www.freecodecamp.org/learn/relational-database/",True,3),
    _res("SQL",_R_SQL,"Coursera","SQL for Data Science (audit option)","https://www.coursera.org/learn/sql-for-data-science",True,4),
    # ── Machine Learning ────────────────────────────────────────────────────
    _res("Machine Learning",_R_ML,"Coursera","Machine Learning Specialization","https://www.coursera.org/specializations/machine-learning-introduction",False,1),
    _res("Machine Learning",_R_ML,"Udemy","Machine Learning A-Z","https://www.udemy.com/course/machinelearning/",False,2),
    _res("Machine Learning",_R_ML,"DataCamp","Machine Learning Scientist with Python","https://www.datacamp.com/tracks/machine-learning-scientist-with-python",False,3),
    _res("Machine Learning",_R_ML,"LinkedIn Learning","Machine Learning Foundations","https://www.linkedin.com/learning/paths/become-a-machine-learning-engineer",False,4),
    _res("Machine Learning",_R_ML,"Google","Machine Learning Crash Course","https://developers.google.com/machine-learning/crash-course",True,1),
    _res("Machine Learning",_R_ML,"Kaggle Learn","Intro to Machine Learning","https://www.kaggle.com/learn/intro-to-machine-learning",True,2),
    _res("Machine Learning",_R_ML,"fast.ai","Practical Deep Learning for Coders","https://course.fast.ai/",True,3),
    _res("Machine Learning",_R_ML,"MIT OpenCourseWare","Introduction to Machine Learning","https://ocw.mit.edu/courses/6-390-introduction-to-machine-learning-fall-2023/",True,4),
    # ── Data Visualization ──────────────────────────────────────────────────
    _res("Data Visualization",_R_VIZ,"Coursera","Data Visualization","https://www.coursera.org/learn/datavisualization",False,1),
    _res("Data Visualization",_R_VIZ,"Udemy","Data Visualization Mastery","https://www.udemy.com/course/data-visualization-with-tableau/",False,2),
    _res("Data Visualization",_R_VIZ,"DataCamp","Data Visualization with Python","https://www.datacamp.com/courses/introduction-to-data-visualization-with-python",False,3),
    _res("Data Visualization",_R_VIZ,"LinkedIn Learning","Data Visualization: Storytelling","https://www.linkedin.com/learning/data-visualization-storytelling",False,4),
    _res("Data Visualization",_R_VIZ,"Kaggle Learn","Data Visualization","https://www.kaggle.com/learn/data-visualization",True,1),
    _res("Data Visualization",_R_VIZ,"freeCodeCamp","Data Visualization","https://www.freecodecamp.org/learn/data-visualization/",True,2),
    _res("Data Visualization",_R_VIZ,"Tableau","Tableau Public training resources","https://www.tableau.com/learn/training",True,3),
    _res("Data Visualization",_R_VIZ,"Microsoft Learn","Power BI learning path","https://learn.microsoft.com/training/powerplatform/power-bi/",True,4),
    # ── Deep Learning ───────────────────────────────────────────────────────
    _res("Deep Learning",_R_DL,"Coursera","Neural Networks and Deep Learning","https://www.coursera.org/learn/neural-networks-deep-learning",False,1),
    _res("Deep Learning",_R_DL,"Udemy","Deep Learning A-Z","https://www.udemy.com/course/deeplearning/",False,2),
    _res("Deep Learning",_R_DL,"DataCamp","Deep Learning for Python","https://www.datacamp.com/courses/deep-learning-for-python",False,3),
    _res("Deep Learning",_R_DL,"LinkedIn Learning","Deep Learning Foundations","https://www.linkedin.com/learning/paths/become-a-deep-learning-engineer",False,4),
    _res("Deep Learning",_R_DL,"Kaggle Learn","Intro to Deep Learning","https://www.kaggle.com/learn/intro-to-deep-learning",True,1),
    _res("Deep Learning",_R_DL,"fast.ai","Practical Deep Learning for Coders","https://course.fast.ai/",True,2),
    _res("Deep Learning",_R_DL,"DeepLearning.AI","Short Courses — Deep Learning","https://www.deeplearning.ai/short-courses/",True,3),
    _res("Deep Learning",_R_DL,"MIT OpenCourseWare","Deep Learning","https://ocw.mit.edu/",True,4),
    # ── Natural Language Processing ─────────────────────────────────────────
    _res("Natural Language Processing",_R_NLP,"Coursera","Natural Language Processing","https://www.coursera.org/learn/natural-language-processing-nlp",False,1),
    _res("Natural Language Processing",_R_NLP,"Udemy","NLP - Natural Language Processing with Python","https://www.udemy.com/course/nlp-natural-language-processing-with-python/",False,2),
    _res("Natural Language Processing",_R_NLP,"DataCamp","Natural Language Processing in Python","https://www.datacamp.com/courses/advanced-natural-language-processing-with-spacy",False,3),
    _res("Natural Language Processing",_R_NLP,"LinkedIn Learning","NLP and Machine Learning","https://www.linkedin.com/learning/natural-language-processing",False,4),
    _res("Natural Language Processing",_R_NLP,"Kaggle Learn","Intro to Natural Language Processing","https://www.kaggle.com/learn/natural-language-processing",True,1),
    _res("Natural Language Processing",_R_NLP,"Hugging Face","NLP Course","https://huggingface.co/learn/nlp-course/chapter1/1",True,2),
    _res("Natural Language Processing",_R_NLP,"Stanford","CS224N Natural Language Processing","https://web.stanford.edu/class/cs224n/",True,3),
    _res("Natural Language Processing",_R_NLP,"Coursera","Natural Language Processing (audit option)","https://www.coursera.org/learn/natural-language-processing-nlp",True,4),
    # ── Big Data Analytics ──────────────────────────────────────────────────
    _res("Big Data Analytics",_R_BIG,"Coursera","Big Data Specialization","https://www.coursera.org/specializations/big-data",False,1),
    _res("Big Data Analytics",_R_BIG,"Udemy","Apache Spark with Python","https://www.udemy.com/course/spark-and-python-for-big-data-with-pyspark/",False,2),
    _res("Big Data Analytics",_R_BIG,"DataCamp","Big Data with PySpark","https://www.datacamp.com/courses/big-data-with-pyspark",False,3),
    _res("Big Data Analytics",_R_BIG,"LinkedIn Learning","Big Data Foundations","https://www.linkedin.com/learning/paths/become-a-big-data-engineer",False,4),
    _res("Big Data Analytics",_R_BIG,"Apache Spark","Quick Start / Spark Programming Guide","https://spark.apache.org/docs/latest/quick-start.html",True,1),
    _res("Big Data Analytics",_R_BIG,"Kaggle Learn","Intro to Big Data","https://www.kaggle.com/learn",True,2),
    _res("Big Data Analytics",_R_BIG,"freeCodeCamp","Big Data / Spark tutorials","https://www.freecodecamp.org/news/tag/apache-spark/",True,3),
    _res("Big Data Analytics",_R_BIG,"MIT OpenCourseWare","Data Systems","https://ocw.mit.edu/",True,4),
    # ── Predictive Modeling ─────────────────────────────────────────────────
    _res("Predictive Modeling",_R_PRED,"Coursera","Applied Data Science with Python","https://www.coursera.org/specializations/data-science-python",False,1),
    _res("Predictive Modeling",_R_PRED,"Udemy","Machine Learning Practical Course","https://www.udemy.com/course/machine-learning-with-python/",False,2),
    _res("Predictive Modeling",_R_PRED,"DataCamp","Supervised Learning with scikit-learn","https://www.datacamp.com/courses/supervised-learning-with-scikit-learn",False,3),
    _res("Predictive Modeling",_R_PRED,"LinkedIn Learning","Machine Learning Foundations","https://www.linkedin.com/learning/machine-learning-foundations-linear-regression",False,4),
    _res("Predictive Modeling",_R_PRED,"Kaggle Learn","Intermediate Machine Learning","https://www.kaggle.com/learn/intermediate-machine-learning",True,1),
    _res("Predictive Modeling",_R_PRED,"Google","Machine Learning Crash Course","https://developers.google.com/machine-learning/crash-course",True,2),
    _res("Predictive Modeling",_R_PRED,"scikit-learn","Model Selection and Evaluation tutorial","https://scikit-learn.org/stable/modules/cross_validation.html",True,3),
    _res("Predictive Modeling",_R_PRED,"Coursera","Applied Data Science with Python (audit option)","https://www.coursera.org/specializations/data-science-python",True,4),
    # ── Neural Networks ─────────────────────────────────────────────────────
    _res("Neural Networks",_R_NN,"Coursera","Neural Networks and Deep Learning","https://www.coursera.org/learn/neural-networks-deep-learning",False,1),
    _res("Neural Networks",_R_NN,"Udemy","Neural Networks from Scratch","https://www.udemy.com/course/neural-network-from-scratch/",False,2),
    _res("Neural Networks",_R_NN,"DataCamp","Introduction to Deep Learning with PyTorch","https://www.datacamp.com/courses/introduction-to-deep-learning-with-pytorch",False,3),
    _res("Neural Networks",_R_NN,"LinkedIn Learning","Neural Networks and Deep Learning Foundations","https://www.linkedin.com/learning/neural-networks-and-deep-learning",False,4),
    _res("Neural Networks",_R_NN,"Kaggle Learn","Intro to Deep Learning","https://www.kaggle.com/learn/intro-to-deep-learning",True,1),
    _res("Neural Networks",_R_NN,"DeepLearning.AI","Neural Networks resources","https://www.deeplearning.ai/",True,2),
    _res("Neural Networks",_R_NN,"MIT OpenCourseWare","Deep Learning","https://ocw.mit.edu/",True,3),
    _res("Neural Networks",_R_NN,"Google","Neural Networks / ML Crash Course","https://developers.google.com/machine-learning/crash-course",True,4),
    # ── Computer Vision ─────────────────────────────────────────────────────
    _res("Computer Vision",_R_CV,"Coursera","Computer Vision with Embedded Systems","https://www.coursera.org/learn/computer-vision-opencv-in-android",False,1),
    _res("Computer Vision",_R_CV,"Udemy","Computer Vision with OpenCV and Python","https://www.udemy.com/course/computer-vision-with-opencv-and-deep-learning/",False,2),
    _res("Computer Vision",_R_CV,"DataCamp","Image Processing with Python","https://www.datacamp.com/courses/image-processing-with-python",False,3),
    _res("Computer Vision",_R_CV,"LinkedIn Learning","Computer Vision: Object Detection","https://www.linkedin.com/learning/computer-vision-object-detection",False,4),
    _res("Computer Vision",_R_CV,"Kaggle Learn","Computer Vision","https://www.kaggle.com/learn/computer-vision",True,1),
    _res("Computer Vision",_R_CV,"Stanford","CS231n: Deep Learning for Computer Vision","https://cs231n.stanford.edu/",True,2),
    _res("Computer Vision",_R_CV,"OpenCV","OpenCV Python Tutorials","https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html",True,3),
    _res("Computer Vision",_R_CV,"fast.ai","Practical Deep Learning for Coders","https://course.fast.ai/",True,4),
    # ── Reinforcement Learning ──────────────────────────────────────────────
    _res("Reinforcement Learning",_R_RL,"Coursera","Reinforcement Learning Specialization","https://www.coursera.org/specializations/reinforcement-learning",False,1),
    _res("Reinforcement Learning",_R_RL,"Udemy","Reinforcement Learning A-Z","https://www.udemy.com/course/reinforcement-learning/",False,2),
    _res("Reinforcement Learning",_R_RL,"DataCamp","Reinforcement Learning resources","https://www.datacamp.com/",False,3),
    _res("Reinforcement Learning",_R_RL,"LinkedIn Learning","Reinforcement Learning Foundations","https://www.linkedin.com/learning/reinforcement-learning-foundations",False,4),
    _res("Reinforcement Learning",_R_RL,"DeepMind / UCL","Reinforcement Learning Course","https://www.davidsilver.uk/teaching/",True,1),
    _res("Reinforcement Learning",_R_RL,"OpenAI Spinning Up","Deep RL resources","https://spinningup.openai.com/en/latest/",True,2),
    _res("Reinforcement Learning",_R_RL,"Sutton & Barto","Reinforcement Learning book resources","http://incompleteideas.net/book/the-book-2nd.html",True,3),
    _res("Reinforcement Learning",_R_RL,"Coursera","RL Specialization (audit option)","https://www.coursera.org/specializations/reinforcement-learning",True,4),
    # ── TensorFlow/PyTorch ──────────────────────────────────────────────────
    _res("TensorFlow/PyTorch",_R_TF,"Coursera","DeepLearning.AI TensorFlow Developer","https://www.coursera.org/professional-certificates/tensorflow-in-practice",False,1),
    _res("TensorFlow/PyTorch",_R_TF,"Udemy","PyTorch for Deep Learning","https://www.udemy.com/course/pytorch-for-deep-learning/",False,2),
    _res("TensorFlow/PyTorch",_R_TF,"DataCamp","Introduction to Deep Learning with PyTorch","https://www.datacamp.com/courses/introduction-to-deep-learning-with-pytorch",False,3),
    _res("TensorFlow/PyTorch",_R_TF,"LinkedIn Learning","PyTorch Essential Training","https://www.linkedin.com/learning/pytorch-essential-training",False,4),
    _res("TensorFlow/PyTorch",_R_TF,"TensorFlow","TensorFlow Learn","https://www.tensorflow.org/learn",True,1),
    _res("TensorFlow/PyTorch",_R_TF,"PyTorch","PyTorch Tutorials","https://pytorch.org/tutorials/",True,2),
    _res("TensorFlow/PyTorch",_R_TF,"Kaggle Learn","TensorFlow","https://www.kaggle.com/learn",True,3),
    _res("TensorFlow/PyTorch",_R_TF,"fast.ai","Practical Deep Learning for Coders","https://course.fast.ai/",True,4),
    # ── Generative AI ───────────────────────────────────────────────────────
    _res("Generative AI",_R_GEN,"Coursera","Generative AI for Everyone","https://www.coursera.org/learn/generative-ai-for-everyone",False,1),
    _res("Generative AI",_R_GEN,"Udemy","Generative AI: LLMs and AI Agents","https://www.udemy.com/course/generative-ai-for-beginners/",False,2),
    _res("Generative AI",_R_GEN,"DataCamp","Generative AI Concepts","https://www.datacamp.com/courses/understanding-artificial-intelligence",False,3),
    _res("Generative AI",_R_GEN,"LinkedIn Learning","Generative AI Skills for Leaders","https://www.linkedin.com/learning/paths/generative-ai",False,4),
    _res("Generative AI",_R_GEN,"Kaggle","Generative AI","https://www.kaggle.com/learn",True,1),
    _res("Generative AI",_R_GEN,"Hugging Face","LLM Course","https://huggingface.co/learn/llm-course/chapter1/1",True,2),
    _res("Generative AI",_R_GEN,"Google","Generative AI learning path","https://www.cloudskillsboost.google/paths/118",True,3),
    _res("Generative AI",_R_GEN,"Microsoft Learn","Generative AI for beginners","https://learn.microsoft.com/training/paths/get-started-with-generative-ai/",True,4),
    # ── MLOps ───────────────────────────────────────────────────────────────
    _res("MLOps",_R_MOP,"Coursera","Machine Learning Engineering for Production (MLOps)","https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",False,1),
    _res("MLOps",_R_MOP,"Udemy","MLOps Bootcamp","https://www.udemy.com/course/mlops/",False,2),
    _res("MLOps",_R_MOP,"DataCamp","MLOps Concepts","https://www.datacamp.com/",False,3),
    _res("MLOps",_R_MOP,"LinkedIn Learning","MLOps Foundations","https://www.linkedin.com/learning/machine-learning-operations-mlops-foundations",False,4),
    _res("MLOps",_R_MOP,"MLflow","MLflow Documentation / Tutorials","https://mlflow.org/docs/latest/ml/",True,1),
    _res("MLOps",_R_MOP,"Google Cloud","MLOps architecture resources","https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning",True,2),
    _res("MLOps",_R_MOP,"Kubeflow","Kubeflow training/docs","https://www.kubeflow.org/docs/",True,3),
    _res("MLOps",_R_MOP,"TensorFlow","TFX tutorials","https://www.tensorflow.org/tfx/tutorials",True,4),
    # ── Digital Electronics ─────────────────────────────────────────────────
    _res("Digital Electronics",_R_DE,"Coursera","Digital Systems: From Logic Gates to Processors","https://www.coursera.org/learn/digital-systems",False,1),
    _res("Digital Electronics",_R_DE,"Udemy","Digital Electronics: Complete Course","https://www.udemy.com/course/digital-electronics-complete-course/",False,2),
    _res("Digital Electronics",_R_DE,"LinkedIn Learning","Digital Electronics Foundations","https://www.linkedin.com/learning/digital-electronics-foundations",False,3),
    _res("Digital Electronics",_R_DE,"edX","Circuits and Electronics","https://www.edx.org/learn/electronics",False,4),
    _res("Digital Electronics",_R_DE,"NPTEL","Digital Electronics","https://www.nptel.ac.in/courses/117106086",True,1),
    _res("Digital Electronics",_R_DE,"MIT OpenCourseWare","Circuits and Electronics","https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/",True,2),
    _res("Digital Electronics",_R_DE,"All About Circuits","Digital Electronics Textbook","https://www.allaboutcircuits.com/textbook/digital/",True,3),
    _res("Digital Electronics",_R_DE,"edX","Circuits and Electronics (audit option)","https://www.edx.org/learn/electronics",True,4),
    # ── Analog Electronics ──────────────────────────────────────────────────
    _res("Analog Electronics",_R_AE,"Udemy","Complete Analog Electronics","https://www.udemy.com/course/analog-electronics/",False,1),
    _res("Analog Electronics",_R_AE,"Coursera","Analog Circuit Design","https://www.coursera.org/learn/analog-circuit-design",False,2),
    _res("Analog Electronics",_R_AE,"LinkedIn Learning","Analog Electronics Foundations","https://www.linkedin.com/learning/analog-electronics-foundations",False,3),
    _res("Analog Electronics",_R_AE,"edX","Circuits and Electronics","https://www.edx.org/learn/electronics",False,4),
    _res("Analog Electronics",_R_AE,"NPTEL","Analog Electronic Circuits","https://www.nptel.ac.in/courses/108102112",True,1),
    _res("Analog Electronics",_R_AE,"MIT OpenCourseWare","Circuits and Electronics","https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/",True,2),
    _res("Analog Electronics",_R_AE,"All About Circuits","Analog Circuits Textbook","https://www.allaboutcircuits.com/textbook/experiments/",True,3),
    _res("Analog Electronics",_R_AE,"edX","Circuits and Electronics (audit option)","https://www.edx.org/learn/electronics",True,4),
    # ── Embedded Systems ────────────────────────────────────────────────────
    _res("Embedded Systems",_R_EMB,"Coursera","Introduction to Embedded Systems Software and Development Environments","https://www.coursera.org/learn/introduction-embedded-systems",False,1),
    _res("Embedded Systems",_R_EMB,"Udemy","Embedded Systems Programming on ARM Cortex-M3/M4 Processor","https://www.udemy.com/course/embedded-systems-programming-on-arm-cortex-m3m4/",False,2),
    _res("Embedded Systems",_R_EMB,"LinkedIn Learning","Embedded Systems Foundations","https://www.linkedin.com/learning/embedded-systems-foundations",False,3),
    _res("Embedded Systems",_R_EMB,"edX","Embedded Systems Essentials with Arm: Getting Started","https://www.edx.org/learn/embedded-systems/arm-education-embedded-systems-essentials-with-arm-getting-started",False,4),
    _res("Embedded Systems",_R_EMB,"NPTEL","Embedded Systems","https://www.nptel.ac.in/courses/108102045",True,1),
    _res("Embedded Systems",_R_EMB,"Coursera","Introduction to the Internet of Things and Embedded Systems (audit option)","https://www.coursera.org/learn/iot",True,2),
    _res("Embedded Systems",_R_EMB,"MIT OpenCourseWare","Introduction to Electrical Engineering and Computer Science","https://ocw.mit.edu/",True,3),
    _res("Embedded Systems",_R_EMB,"Arm Education","Arm Embedded Systems learning resources","https://www.arm.com/resources/education",True,4),
    # ── VLSI Design ─────────────────────────────────────────────────────────
    _res("VLSI Design",_R_VLS,"Udemy","VLSI Design","https://www.udemy.com/course/vlsi-design-mask/",False,1),
    _res("VLSI Design",_R_VLS,"Coursera","VLSI CAD Part I","https://www.coursera.org/learn/vlsi-cad-part-i",False,2),
    _res("VLSI Design",_R_VLS,"LinkedIn Learning","VLSI Design Foundations","https://www.linkedin.com/learning/vlsi-design-foundations",False,3),
    _res("VLSI Design",_R_VLS,"edX","Semiconductor Devices","https://www.edx.org/learn/semiconductors",False,4),
    _res("VLSI Design",_R_VLS,"NPTEL","VLSI Design Flow: RTL to GDS","https://www.nptel.ac.in/courses/108106191",True,1),
    _res("VLSI Design",_R_VLS,"MIT OpenCourseWare","Microelectronic Devices and Circuits","https://ocw.mit.edu/",True,2),
    _res("VLSI Design",_R_VLS,"IIT / NPTEL","Advanced VLSI Design","https://www.nptel.ac.in/courses/117101004",True,3),
    _res("VLSI Design",_R_VLS,"edX","Semiconductor Devices (audit option)","https://www.edx.org/learn/semiconductors",True,4),
    # ── Microcontrollers ────────────────────────────────────────────────────
    _res("Microcontrollers",_R_MCU,"Coursera","Microcontrollers: Basic Architecture and Design","https://www.coursera.org/learn/microcontrollers-basic-architecture-and-design",False,1),
    _res("Microcontrollers",_R_MCU,"Udemy","Embedded Systems Programming on ARM Cortex-M3/M4","https://www.udemy.com/course/embedded-systems-programming-on-arm-cortex-m3m4/",False,2),
    _res("Microcontrollers",_R_MCU,"LinkedIn Learning","Microcontrollers: Introduction","https://www.linkedin.com/learning/microcontrollers",False,3),
    _res("Microcontrollers",_R_MCU,"edX","Embedded Systems Essentials with Arm","https://www.edx.org/learn/embedded-systems/arm-education-embedded-systems-essentials-with-arm-getting-started",False,4),
    _res("Microcontrollers",_R_MCU,"NPTEL","Introduction to Microcontrollers & Microprocessors","https://www.nptel.ac.in/courses/117104072",True,1),
    _res("Microcontrollers",_R_MCU,"Arduino","Arduino Education / Tutorials","https://docs.arduino.cc/learn/",True,2),
    _res("Microcontrollers",_R_MCU,"Arm Education","Arm Cortex-M learning resources","https://developer.arm.com/learn",True,3),
    _res("Microcontrollers",_R_MCU,"edX","Embedded Systems Essentials with Arm (audit option)","https://www.edx.org/learn/embedded-systems/arm-education-embedded-systems-essentials-with-arm-getting-started",True,4),
    # ── PCB Design ──────────────────────────────────────────────────────────
    _res("PCB Design",_R_PCB,"Udemy","Complete PCB Design: From Schematic to Manufacturing","https://www.udemy.com/course/learning-complete-pcb-design-from-an-idea-to-a-product/",False,1),
    _res("PCB Design",_R_PCB,"Coursera","PCB Design with Altium Designer: Hands-on","https://www.coursera.org/learn/pcb-design-with-altium-designer-hands-on",False,2),
    _res("PCB Design",_R_PCB,"LinkedIn Learning","PCB Design with Eagle","https://www.linkedin.com/learning/learning-pcb-design-with-eagle",False,3),
    _res("PCB Design",_R_PCB,"edX","Electronics / PCB Design resources","https://www.edx.org/learn/electronics",False,4),
    _res("PCB Design",_R_PCB,"KiCad","Getting Started with KiCad","https://www.kicad.org/help/learning-resources/",True,1),
    _res("PCB Design",_R_PCB,"Altium","Altium Academy / Learning Center","https://www.altium.com/education",True,2),
    _res("PCB Design",_R_PCB,"EasyEDA","Learning Center / Tutorials","https://easyeda.com/learning",True,3),
    _res("PCB Design",_R_PCB,"MIT OpenCourseWare","Circuits and Electronics","https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/",True,4),
    # ── Communication Systems ───────────────────────────────────────────────
    _res("Communication Systems",_R_COM,"Coursera","Digital Communications Specialization","https://www.coursera.org/specializations/digital-communication",False,1),
    _res("Communication Systems",_R_COM,"Udemy","Communication Systems for Electronics Engineers","https://www.udemy.com/course/communication-systems/",False,2),
    _res("Communication Systems",_R_COM,"LinkedIn Learning","Communication Systems Foundations","https://www.linkedin.com/learning/communication-systems-foundations",False,3),
    _res("Communication Systems",_R_COM,"edX","Signals and Systems","https://www.edx.org/learn/signals-and-systems",False,4),
    _res("Communication Systems",_R_COM,"NPTEL","Digital Communication","https://www.nptel.ac.in/courses",True,1),
    _res("Communication Systems",_R_COM,"MIT OpenCourseWare","Principles of Digital Communication","https://ocw.mit.edu/",True,2),
    _res("Communication Systems",_R_COM,"All About Circuits","Communications textbook","https://www.allaboutcircuits.com/textbook/",True,3),
    _res("Communication Systems",_R_COM,"edX","Communication Systems (audit option)","https://www.edx.org/learn/signals-and-systems",True,4),
    # ── IoT ─────────────────────────────────────────────────────────────────
    _res("IoT",_R_IOT,"Coursera","Introduction to the Internet of Things and Embedded Systems","https://www.coursera.org/learn/iot",False,1),
    _res("IoT",_R_IOT,"Udemy","IoT - Internet of Things for Beginners","https://www.udemy.com/course/iot-internet-of-things/",False,2),
    _res("IoT",_R_IOT,"LinkedIn Learning","IoT Foundations: Fundamentals","https://www.linkedin.com/learning/iot-foundations-fundamentals",False,3),
    _res("IoT",_R_IOT,"edX","IoT: Internet of Things","https://www.edx.org/learn/internet-of-things",False,4),
    _res("IoT",_R_IOT,"Arduino","Arduino IoT Cloud / Education resources","https://docs.arduino.cc/arduino-cloud/",True,1),
    _res("IoT",_R_IOT,"Cisco Networking Academy","IoT Fundamentals","https://www.netacad.com/courses/iot",True,2),
    _res("IoT",_R_IOT,"Coursera","Introduction to IoT (audit option)","https://www.coursera.org/learn/introduction-to-internet-of-things",True,3),
    _res("IoT",_R_IOT,"MIT OpenCourseWare","Networks and IoT resources","https://ocw.mit.edu/",True,4),
    # ── MATLAB/Simulink ─────────────────────────────────────────────────────
    _res("MATLAB/Simulink",_R_MAT,"Coursera","Introduction to Programming with MATLAB","https://www.coursera.org/learn/matlab",False,1),
    _res("MATLAB/Simulink",_R_MAT,"Udemy","MATLAB/SIMULINK for Beginners","https://www.udemy.com/course/matlab-simulink/",False,2),
    _res("MATLAB/Simulink",_R_MAT,"LinkedIn Learning","MATLAB Essential Training","https://www.linkedin.com/learning/matlab-essential-training",False,3),
    _res("MATLAB/Simulink",_R_MAT,"edX","MATLAB / numerical computing resources","https://www.edx.org/learn/matlab",False,4),
    _res("MATLAB/Simulink",_R_MAT,"MathWorks","MATLAB Onramp","https://matlabacademy.mathworks.com/details/matlab-onramp/gettingstarted",True,1),
    _res("MATLAB/Simulink",_R_MAT,"MathWorks","Simulink Onramp","https://matlabacademy.mathworks.com/details/simulink-onramp/simulink",True,2),
    _res("MATLAB/Simulink",_R_MAT,"MathWorks","Signal Processing Onramp","https://matlabacademy.mathworks.com/details/signal-processing-onramp/signalprocessing",True,3),
    _res("MATLAB/Simulink",_R_MAT,"Coursera","MATLAB course (audit option)","https://www.coursera.org/learn/matlab",True,4),
    # ── Signal Processing ───────────────────────────────────────────────────
    _res("Signal Processing",_R_SIG,"Coursera","Audio Signal Processing for Music Applications","https://www.coursera.org/learn/audio-signal-processing",False,1),
    _res("Signal Processing",_R_SIG,"Udemy","DSP - Digital Signal Processing from A to Z","https://www.udemy.com/course/digital-signal-processing/",False,2),
    _res("Signal Processing",_R_SIG,"LinkedIn Learning","Signal Processing Foundations","https://www.linkedin.com/learning/signal-processing-foundations",False,3),
    _res("Signal Processing",_R_SIG,"edX","Signals and Systems","https://www.edx.org/learn/signals-and-systems",False,4),
    _res("Signal Processing",_R_SIG,"NPTEL","Digital Signal Processing","https://www.nptel.ac.in/courses/117102060",True,1),
    _res("Signal Processing",_R_SIG,"MathWorks","Signal Processing Onramp","https://matlabacademy.mathworks.com/details/signal-processing-onramp/signalprocessing",True,2),
    _res("Signal Processing",_R_SIG,"MIT OpenCourseWare","Discrete Time Signal Processing","https://ocw.mit.edu/",True,3),
    _res("Signal Processing",_R_SIG,"Stanford","Digital Signal Processing resources","https://see.stanford.edu/",True,4),
    # ── Electrical Machines ─────────────────────────────────────────────────
    _res("Electrical Machines",_R_ELM,"Coursera","Electric Machines","https://www.coursera.org/learn/electric-machines",False,1),
    _res("Electrical Machines",_R_ELM,"Udemy","Electrical Machines","https://www.udemy.com/course/electrical-machines/",False,2),
    _res("Electrical Machines",_R_ELM,"LinkedIn Learning","Electrical Engineering Foundations: Machines","https://www.linkedin.com/learning/electrical-engineering-foundations-machines",False,3),
    _res("Electrical Machines",_R_ELM,"edX","Electrical Machines","https://www.edx.org/learn/electrical-engineering",False,4),
    _res("Electrical Machines",_R_ELM,"NPTEL","Electrical Machines - I","https://www.nptel.ac.in/courses/108105155",True,1),
    _res("Electrical Machines",_R_ELM,"MIT OpenCourseWare","Electric Machines","https://ocw.mit.edu/courses/6-685-electric-machines-fall-2013/",True,2),
    _res("Electrical Machines",_R_ELM,"NPTEL","Design of Electric Motor","https://www.nptel.ac.in/courses/108108191",True,3),
    _res("Electrical Machines",_R_ELM,"edX","Electrical Engineering (audit option)","https://www.edx.org/learn/electrical-engineering",True,4),
    # ── Power Systems ───────────────────────────────────────────────────────
    _res("Power Systems",_R_PWS,"Coursera","Electric Power Systems","https://www.coursera.org/learn/electric-power-systems",False,1),
    _res("Power Systems",_R_PWS,"Udemy","Power System Analysis","https://www.udemy.com/course/power-system-analysis/",False,2),
    _res("Power Systems",_R_PWS,"LinkedIn Learning","Power Systems Foundations","https://www.linkedin.com/learning/power-systems-foundations",False,3),
    _res("Power Systems",_R_PWS,"edX","Electric Power Systems","https://www.edx.org/learn/electrical-engineering",False,4),
    _res("Power Systems",_R_PWS,"NPTEL","Power System Analysis","https://www.nptel.ac.in/courses/117105140",True,1),
    _res("Power Systems",_R_PWS,"MIT OpenCourseWare","Electric Power Systems","https://ocw.mit.edu/courses/6-061-introduction-to-electric-power-systems-spring-2011/",True,2),
    _res("Power Systems",_R_PWS,"NPTEL","FACTS / Power System applications","https://www.nptel.ac.in/courses/117103488",True,3),
    _res("Power Systems",_R_PWS,"edX","Electricity / Power Systems (audit option)","https://www.edx.org/learn/electrical-engineering",True,4),
    # ── Power Electronics ───────────────────────────────────────────────────
    _res("Power Electronics",_R_PWE,"Coursera","Introduction to Power Electronics","https://www.coursera.org/learn/power-electronics",False,1),
    _res("Power Electronics",_R_PWE,"Udemy","Power Electronics A-Z","https://www.udemy.com/course/power-electronics/",False,2),
    _res("Power Electronics",_R_PWE,"LinkedIn Learning","Power Electronics Foundations","https://www.linkedin.com/learning/power-electronics-foundations",False,3),
    _res("Power Electronics",_R_PWE,"edX","Power Electronics","https://www.edx.org/learn/electrical-engineering",False,4),
    _res("Power Electronics",_R_PWE,"NPTEL","Power Electronics","https://www.nptel.ac.in/courses/108102145",True,1),
    _res("Power Electronics",_R_PWE,"NPTEL","Fundamentals of Power Electronics","https://www.nptel.ac.in/courses/108101038",True,2),
    _res("Power Electronics",_R_PWE,"MIT OpenCourseWare","Power Electronics","https://ocw.mit.edu/",True,3),
    _res("Power Electronics",_R_PWE,"Coursera","Introduction to Power Electronics (audit option)","https://www.coursera.org/learn/power-electronics",True,4),
    # ── Control Systems ─────────────────────────────────────────────────────
    _res("Control Systems",_R_CTL,"Coursera","Introduction to Control Systems","https://www.coursera.org/learn/introduction-to-control-systems",False,1),
    _res("Control Systems",_R_CTL,"Udemy","Control Systems: From Mathematical Modelling to PID Control","https://www.udemy.com/course/control-systems-pid/",False,2),
    _res("Control Systems",_R_CTL,"LinkedIn Learning","Control Systems Foundations","https://www.linkedin.com/learning/control-systems-foundations",False,3),
    _res("Control Systems",_R_CTL,"edX","Control Systems","https://www.edx.org/learn/control-systems",False,4),
    _res("Control Systems",_R_CTL,"NPTEL","Control Systems","https://www.nptel.ac.in/courses",True,1),
    _res("Control Systems",_R_CTL,"MIT OpenCourseWare","Feedback Systems","https://ocw.mit.edu/",True,2),
    _res("Control Systems",_R_CTL,"Khan Academy","Control systems / engineering math","https://www.khanacademy.org/science/engineering",True,3),
    _res("Control Systems",_R_CTL,"Coursera","Control Systems (audit option)","https://www.coursera.org/learn/control-systems",True,4),
    # ── Electrical Measurements ─────────────────────────────────────────────
    _res("Electrical Measurements",_R_EMS,"Coursera","Electrical Measurements and Instrumentation","https://www.coursera.org/learn/electrical-measurements",False,1),
    _res("Electrical Measurements",_R_EMS,"Udemy","Electrical Measurement and Instrumentation","https://www.udemy.com/course/electrical-measurement-instrumentation/",False,2),
    _res("Electrical Measurements",_R_EMS,"LinkedIn Learning","Electrical Engineering Foundations: Instrumentation","https://www.linkedin.com/learning/electrical-engineering-foundations-instrumentation",False,3),
    _res("Electrical Measurements",_R_EMS,"edX","Electrical Engineering Measurement","https://www.edx.org/learn/electrical-engineering",False,4),
    _res("Electrical Measurements",_R_EMS,"NPTEL","Electrical Measurement and Instrumentation","https://www.nptel.ac.in/courses",True,1),
    _res("Electrical Measurements",_R_EMS,"MIT OpenCourseWare","Measurement and Instrumentation resources","https://ocw.mit.edu/",True,2),
    _res("Electrical Measurements",_R_EMS,"All About Circuits","Electrical Measurement textbook","https://www.allaboutcircuits.com/textbook/",True,3),
    _res("Electrical Measurements",_R_EMS,"edX","Electrical Engineering (audit option)","https://www.edx.org/learn/electrical-engineering",True,4),
    # ── PLC & SCADA ─────────────────────────────────────────────────────────
    _res("PLC & SCADA",_R_PLC,"Udemy","PLC Programming from Scratch","https://www.udemy.com/course/plc-programming-from-scratch/",False,1),
    _res("PLC & SCADA",_R_PLC,"Coursera","Industrial Automation","https://www.coursera.org/learn/industrial-automation",False,2),
    _res("PLC & SCADA",_R_PLC,"LinkedIn Learning","PLC and Industrial Automation Foundations","https://www.linkedin.com/learning/plc-and-industrial-automation",False,3),
    _res("PLC & SCADA",_R_PLC,"edX","Industrial Automation","https://www.edx.org/learn/industrial-engineering",False,4),
    _res("PLC & SCADA",_R_PLC,"Siemens SITRAIN","Automation training resources","https://www.siemens.com/global/en/products/automation/topic-areas/industrial-automation/training.html",True,1),
    _res("PLC & SCADA",_R_PLC,"PLC Academy","Free PLC programming resources","https://www.plcacademy.com/",True,2),
    _res("PLC & SCADA",_R_PLC,"Schneider Electric","Automation training resources","https://www.se.com/ww/en/work/support/resources-and-tools/training/",True,3),
    _res("PLC & SCADA",_R_PLC,"edX","Industrial Automation (audit option)","https://www.edx.org/learn/industrial-engineering",True,4),
    # ── Renewable Energy ────────────────────────────────────────────────────
    _res("Renewable Energy",_R_REN,"Coursera","Introduction to Renewable Energy","https://www.coursera.org/learn/renewable-energy",False,1),
    _res("Renewable Energy",_R_REN,"Udemy","Renewable Energy Engineering","https://www.udemy.com/course/renewable-energy-engineering/",False,2),
    _res("Renewable Energy",_R_REN,"LinkedIn Learning","Renewable Energy Foundations","https://www.linkedin.com/learning/renewable-energy-foundations",False,3),
    _res("Renewable Energy",_R_REN,"edX","Renewable Energy","https://www.edx.org/learn/renewable-energy",False,4),
    _res("Renewable Energy",_R_REN,"NPTEL","Renewable Energy and related courses","https://www.nptel.ac.in/courses",True,1),
    _res("Renewable Energy",_R_REN,"MIT OpenCourseWare","Renewable Energy resources","https://ocw.mit.edu/",True,2),
    _res("Renewable Energy",_R_REN,"OpenLearn","Renewable Energy","https://www.open.edu/openlearn/science-maths-technology/engineering-and-technology/renewable-energy",True,3),
    _res("Renewable Energy",_R_REN,"edX","Renewable Energy (audit option)","https://www.edx.org/learn/renewable-energy",True,4),
    # ── Electric Vehicles ───────────────────────────────────────────────────
    _res("Electric Vehicles",_R_EV,"Coursera","Electric Vehicle Sensors and Systems","https://www.coursera.org/learn/electric-vehicle-sensors-systems",False,1),
    _res("Electric Vehicles",_R_EV,"Udemy","Introduction to Electric Vehicles","https://www.udemy.com/course/electric-vehicles/",False,2),
    _res("Electric Vehicles",_R_EV,"LinkedIn Learning","Electric Vehicle Foundations","https://www.linkedin.com/learning/electric-vehicle-foundations",False,3),
    _res("Electric Vehicles",_R_EV,"edX","Electric Vehicles","https://www.edx.org/learn/electric-vehicles",False,4),
    _res("Electric Vehicles",_R_EV,"NPTEL","Electric Vehicle","https://www.nptel.ac.in/courses/108102121",True,1),
    _res("Electric Vehicles",_R_EV,"NPTEL","Introduction to Electric Vehicles","https://www.nptel.ac.in/courses/108106182",True,2),
    _res("Electric Vehicles",_R_EV,"MIT OpenCourseWare","Electric Vehicles / Energy resources","https://ocw.mit.edu/",True,3),
    _res("Electric Vehicles",_R_EV,"Coursera","EV course (audit option)","https://www.coursera.org/learn/introduction-to-electric-vehicles",True,4),
]


# ============================================================
# SECTION F: COMPANY JOB REFERENCES — all 35 rows from Excel
# 20 Software + 15 Hardware companies
# ============================================================

COMPANY_JOB_REFS: list[dict[str, Any]] = [
    # Software (20)
    {"category":"Software","serial_number":1, "company_name":"Google",      "about_role":"Software Development Engineer (SDE)",                "required_skills":"Data Structures, Algorithms, System Design, Java/C++/Python",            "working_duration":"Full-time (40 hrs/wk) / 10–12 wk Intern","application_link":"https://www.google.com/about/careers/applications/jobs/results/104556982945358534-systems-development-engineer"},
    {"category":"Software","serial_number":2, "company_name":"Microsoft",   "about_role":"Software Engineer",                                  "required_skills":"C#, .NET, Cloud Computing (Azure), OOP, Problem Solving",                 "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://apply.careers.microsoft.com/careers?query=sde&start=0&pid=1970393556958336&sort_by=relevance"},
    {"category":"Software","serial_number":3, "company_name":"Amazon",      "about_role":"Software Development Engineer (SDE I/II)",           "required_skills":"Distributed Systems, Java/C++, AWS, Scalability",                        "working_duration":"Full-time (40 hrs/wk) / 10–12 wk Intern","application_link":"https://www.amazon.jobs/en/jobs/10495532/sde"},
    {"category":"Software","serial_number":4, "company_name":"Meta",        "about_role":"Software Engineer",                                  "required_skills":"React, Python, C++, System Design, GraphQL",                             "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.metacareers.com/"},
    {"category":"Software","serial_number":5, "company_name":"Apple",       "about_role":"Software Engineer (OS / Apps)",                      "required_skills":"Swift, Objective-C, C++, System Architecture, macOS/iOS",                "working_duration":"Full-time (40 hrs/wk) / 12–16 wk Intern","application_link":"https://www.apple.com/careers/"},
    {"category":"Software","serial_number":6, "company_name":"Netflix",     "about_role":"Senior Software Engineer",                           "required_skills":"Java, Spring Boot, Microservices, Cloud Infra, Node.js",                  "working_duration":"Full-time (40 hrs/wk)",                  "application_link":"https://jobs.netflix.com/"},
    {"category":"Software","serial_number":7, "company_name":"Adobe",       "about_role":"Software Engineer",                                  "required_skills":"C++, JavaScript, WebGL, Image Processing, Java",                         "working_duration":"Full-time (40 hrs/wk) / 10–12 wk Intern","application_link":"https://www.adobe.com/careers.html"},
    {"category":"Software","serial_number":8, "company_name":"Salesforce",  "about_role":"Software Engineer",                                  "required_skills":"Java, Apex, Salesforce Platform, API Integration, JS",                   "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.salesforce.com/company/careers/"},
    {"category":"Software","serial_number":9, "company_name":"Oracle",      "about_role":"Software Developer",                                 "required_skills":"Java, SQL/Database Systems, Cloud Infrastructure, C++",                   "working_duration":"Full-time (40 hrs/wk) / 10–12 wk Intern","application_link":"https://www.oracle.com/corporate/careers/"},
    {"category":"Software","serial_number":10,"company_name":"SAP",         "about_role":"Software Engineer",                                  "required_skills":"ABAP, Java, SAP HANA, Cloud Platform, Microservices",                     "working_duration":"Full-time (40 hrs/wk) / 6–12 mo Co-op", "application_link":"https://www.sap.com/careers.html"},
    {"category":"Software","serial_number":11,"company_name":"IBM",         "about_role":"Software Engineer",                                  "required_skills":"Python, Docker, Kubernetes, AI/ML Infrastructure, Java",                  "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://careers.ibm.com/en_US/careers/JobDetail?jobId=128898&source=WEB_Sweng_INDIA"},
    {"category":"Software","serial_number":12,"company_name":"Uber",        "about_role":"Software Engineer",                                  "required_skills":"Go, Java, Python, Distributed Systems, Microservices",                    "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.uber.com/us/en/careers/"},
    {"category":"Software","serial_number":13,"company_name":"Airbnb",      "about_role":"Software Engineer",                                  "required_skills":"Kotlin, Swift, React, Java, System Architecture",                        "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://careers.airbnb.com/"},
    {"category":"Software","serial_number":14,"company_name":"Snowflake",   "about_role":"Software Engineer - Data Engineering",               "required_skills":"C++, Java, Cloud Data Warehousing, SQL, Distributed Systems",            "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.snowflake.com/careers/"},
    {"category":"Software","serial_number":15,"company_name":"Atlassian",   "about_role":"Software Engineer",                                  "required_skills":"Java, React, TypeScript, Microservices, Cloud Security",                  "working_duration":"Full-time (40 hrs/wk) / 10–12 wk Intern","application_link":"https://www.atlassian.com/company/careers"},
    {"category":"Software","serial_number":16,"company_name":"Databricks",  "about_role":"Software Engineer",                                  "required_skills":"Apache Spark, Scala, Python, Cloud Storage, Distributed Systems",        "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.databricks.com/company/careers"},
    {"category":"Software","serial_number":17,"company_name":"Palantir",    "about_role":"Software Engineer",                                  "required_skills":"Java, TypeScript, Python, Data Analytics, C++",                          "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.palantir.com/careers/"},
    {"category":"Software","serial_number":18,"company_name":"Stripe",      "about_role":"Software Engineer",                                  "required_skills":"Ruby, Go, Java, API Design, Payment Infrastructure",                     "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://boards.greenhouse.io/stripe/jobs/8174965"},
    {"category":"Software","serial_number":19,"company_name":"Workday",     "about_role":"Software Engineer",                                  "required_skills":"Java, Scala, Cloud Architecture, Object-Oriented Design",                "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.workday.com/en-us/company/careers.html"},
    {"category":"Software","serial_number":20,"company_name":"ServiceNow",  "about_role":"Software Engineer",                                  "required_skills":"JavaScript, React, Java, SaaS Architecture, REST APIs",                  "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.servicenow.com/careers.html"},
    # Hardware (15)
    {"category":"Hardware","serial_number":1, "company_name":"NVIDIA",              "about_role":"Hardware / Silicon Design Engineer",               "required_skills":"Verilog, SystemVerilog, ASIC/FPGA, GPU Architecture, Computer Architecture",      "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.nvidia.com/en-us/about-nvidia/careers/"},
    {"category":"Hardware","serial_number":2, "company_name":"Intel",               "about_role":"Hardware Design Engineer",                         "required_skills":"RTL Design, VLSI, Verilog/VHDL, Silicon Validation, C++",                        "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.intel.com/content/www/us/en/jobs/jobs-at-intel.html"},
    {"category":"Hardware","serial_number":3, "company_name":"AMD",                 "about_role":"Silicon Design & Verification Engineer",           "required_skills":"SystemVerilog, UVM, RTL, Semiconductor Physics, C/C++",                         "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.amd.com/en/corporate/careers.html"},
    {"category":"Hardware","serial_number":4, "company_name":"Qualcomm",            "about_role":"Hardware Engineer (RF / ASIC)",                    "required_skills":"RF Circuit Design, SystemVerilog, Embedded C, Wireless Protocols (5G)",          "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.qualcomm.com/company/careers"},
    {"category":"Hardware","serial_number":5, "company_name":"Apple",               "about_role":"Hardware Systems Engineer",                        "required_skills":"PCB Design, Signal Integrity, CAD, Embedded Systems, Circuit Analysis",           "working_duration":"Full-time (40 hrs/wk) / 12–16 wk Intern","application_link":"https://www.apple.com/careers/"},
    {"category":"Hardware","serial_number":6, "company_name":"Broadcom",            "about_role":"IC Design Engineer",                               "required_skills":"Analog/Digital IC Design, Cadence Tools, CMOS, SystemVerilog",                    "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.broadcom.com/company/careers"},
    {"category":"Hardware","serial_number":7, "company_name":"Texas Instruments",   "about_role":"Applications / Embedded Hardware Engineer",        "required_skills":"Analog Circuit Design, Power Electronics, Microcontrollers, PCB Design",         "working_duration":"Full-time (40 hrs/wk) / 10–12 wk Intern","application_link":"https://careers.ti.com/"},
    {"category":"Hardware","serial_number":8, "company_name":"Cisco",               "about_role":"Hardware Engineer",                                "required_skills":"Board Design, High-Speed Digital Design, Networking Hardware, FPGA",              "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.cisco.com/c/en/us/about/careers.html"},
    {"category":"Hardware","serial_number":9, "company_name":"ASML",                "about_role":"Hardware / Mechatronics Engineer",                 "required_skills":"Precision Engineering, Optics, Mechatronics, MATLAB, Controls",                   "working_duration":"Full-time (40 hrs/wk) / 6–12 mo Intern", "application_link":"https://www.asml.com/en/careers"},
    {"category":"Hardware","serial_number":10,"company_name":"TSMC",                "about_role":"Semiconductor Process Engineer",                   "required_skills":"Semiconductor Fabrication, Cleanroom Operations, Materials Science, Physics",      "working_duration":"Full-time (40 hrs/wk)",                  "application_link":"https://www.tsmc.com/english/careers"},
    {"category":"Hardware","serial_number":11,"company_name":"Samsung Electronics", "about_role":"Hardware Engineer",                                "required_skills":"SoC Design, DRAM/NAND Memory Architecture, VLSI, Circuit Simulation",            "working_duration":"Full-time (40 hrs/wk) / 10–12 wk Intern","application_link":"https://sec.wd3.myworkdayjobs.com/en-US/Samsung_Careers/details/Electrical-Engineer_R119411-1?q=Hardware%20Engineer"},
    {"category":"Hardware","serial_number":12,"company_name":"Western Digital",     "about_role":"Firmware / Hardware Engineer",                     "required_skills":"Embedded C/C++, PCIe, NVMe, Storage Controllers, PCB Layout",                    "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://careers.westerndigital.com/"},
    {"category":"Hardware","serial_number":13,"company_name":"Micron Technology",   "about_role":"Memory Design Engineer",                           "required_skills":"DRAM/NAND Design, Verilog, SPICE, CMOS Technology",                             "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://www.micron.com/careers"},
    {"category":"Hardware","serial_number":14,"company_name":"Arm",                 "about_role":"IP Design Engineer",                               "required_skills":"RISC Architecture, Verilog, Computer Architecture, Assembly, C/C++",              "working_duration":"Full-time (40 hrs/wk) / 12 wk Intern",  "application_link":"https://careers.arm.com/"},
    {"category":"Hardware","serial_number":15,"company_name":"Applied Materials",   "about_role":"Process / Mechanical Hardware Engineer",           "required_skills":"Precision CAD, Vacuum Systems, Semiconductor Equipment Design, Thermodynamics",   "working_duration":"Full-time (40 hrs/wk) / 10–12 wk Intern","application_link":"https://www.appliedmaterials.com/us/en/careers.html"},
]

# ============================================================
# SECTION G: GAP ENGINE COURSES (used for recommendations)
# These back the gap engine's course ↔ competency coverage.
# ============================================================
COURSES: list[dict[str, Any]] = [
    {"id":1,  "title":"C Programming Bootcamp - The Complete C Language Course",    "description":"Comprehensive C programming course",           "provider":"Udemy",            "duration":"6–12 months","level":"beginner",    "source":"Udemy",            "source_url":"https://www.udemy.com/course/c-programming-bootcamp-for-beginners/"},
    {"id":2,  "title":"Programming in C",                                           "description":"NPTEL C programming fundamentals",             "provider":"NPTEL",            "duration":"12 weeks",   "level":"beginner",    "source":"NPTEL",            "source_url":"https://www.nptel.ac.in/courses/106105171"},
    {"id":3,  "title":"CS50x Introduction to Computer Science",                    "description":"Harvard CS50: C, Python, SQL and web",         "provider":"Harvard CS50",     "duration":"12 weeks",   "level":"beginner",    "source":"Harvard CS50",     "source_url":"https://cs50.harvard.edu/x/2026/"},
    {"id":4,  "title":"Java Programming Masterclass for Software Developers",       "description":"Complete Java with OOP and collections",       "provider":"Udemy",            "duration":"6–12 months","level":"beginner",    "source":"Udemy",            "source_url":"https://www.udemy.com/course/java-the-complete-java-developer-course/"},
    {"id":5,  "title":"Java Programming I & II",                                   "description":"Helsinki MOOC free Java course",               "provider":"MOOC.fi",          "duration":"8 weeks each","level":"beginner",   "source":"MOOC.fi",          "source_url":"https://java-programming.mooc.fi/"},
    {"id":6,  "title":"The Complete Python Bootcamp From Zero to Hero",             "description":"Python fundamentals to advanced OOP",          "provider":"Udemy",            "duration":"6–12 months","level":"beginner",    "source":"Udemy",            "source_url":"https://www.udemy.com/course/complete-python-bootcamp/"},
    {"id":7,  "title":"Python for Everybody Specialization",                        "description":"Coursera Python specialisation by U Michigan",  "provider":"Coursera",         "duration":"8 months",   "level":"beginner",    "source":"Coursera",         "source_url":"https://www.coursera.org/specializations/python"},
    {"id":8,  "title":"Scientific Computing with Python",                          "description":"freeCodeCamp Python certification",             "provider":"freeCodeCamp",     "duration":"300 hours",  "level":"intermediate","source":"freeCodeCamp",     "source_url":"https://www.freecodecamp.org/learn/scientific-computing-with-python/"},
    {"id":9,  "title":"Introduction to Computer Science and Programming in Python", "description":"MIT OCW Python and computational thinking",     "provider":"MIT OpenCourseWare","duration":"Self-paced","level":"intermediate","source":"MIT OpenCourseWare","source_url":"https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/"},
    {"id":10, "title":"Data Structures and Algorithms — Python",                    "description":"Arrays, trees, graphs, DP with Python",        "provider":"Udemy",            "duration":"6–12 months","level":"intermediate","source":"Udemy",            "source_url":"https://www.udemy.com/course/algorithms-and-data-structures-in-python/"},
    {"id":11, "title":"Introduction to Algorithms",                                "description":"MIT OCW flagship algorithms course",            "provider":"MIT OpenCourseWare","duration":"Self-paced","level":"advanced",    "source":"MIT OpenCourseWare","source_url":"https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/"},
    {"id":12, "title":"Databases and SQL for Data Science with Python",             "description":"IBM/Coursera SQL with Python integration",      "provider":"Coursera",         "duration":"6 weeks",    "level":"beginner",    "source":"Coursera",         "source_url":"https://www.coursera.org/learn/sql-data-science"},
    {"id":13, "title":"The Complete SQL Bootcamp",                                  "description":"Udemy SQL fundamentals to advanced queries",    "provider":"Udemy",            "duration":"6–12 months","level":"beginner",    "source":"Udemy",            "source_url":"https://www.udemy.com/course/the-complete-sql-bootcamp/"},
    {"id":14, "title":"Intro to SQL",                                               "description":"Kaggle free SQL hands-on course",               "provider":"Kaggle",           "duration":"3 hours",    "level":"beginner",    "source":"Kaggle",           "source_url":"https://www.kaggle.com/learn/intro-to-sql"},
    {"id":15, "title":"The Web Developer Bootcamp",                                 "description":"Full-stack: HTML, CSS, JS, Node, MongoDB",      "provider":"Udemy",            "duration":"12 months",  "level":"beginner",    "source":"Udemy",            "source_url":"https://www.udemy.com/course/the-web-developer-bootcamp/"},
    {"id":16, "title":"Full Stack Open",                                            "description":"U Helsinki: React, Node, GraphQL, TypeScript",  "provider":"University of Helsinki","duration":"Self-paced","level":"intermediate","source":"University of Helsinki","source_url":"https://fullstackopen.com/en/"},
    {"id":17, "title":"Statistics for Data Science and Business Analysis",          "description":"Udemy stats: descriptive, probability, regression","provider":"Udemy",         "duration":"6–12 months","level":"beginner",    "source":"Udemy",            "source_url":"https://www.udemy.com/course/statistics-for-data-science/"},
    {"id":18, "title":"Statistics & Probability",                                   "description":"Khan Academy free statistics course",           "provider":"Khan Academy",     "duration":"Self-paced", "level":"beginner",    "source":"Khan Academy",     "source_url":"https://www.khanacademy.org/math/statistics-probability"},
    {"id":19, "title":"Data Analysis with Python",                                  "description":"Coursera data analysis with NumPy/Pandas",      "provider":"Coursera",         "duration":"6 weeks",    "level":"intermediate","source":"Coursera",         "source_url":"https://www.coursera.org/learn/data-analysis-with-python"},
    {"id":20, "title":"Pandas",                                                     "description":"Kaggle free Pandas course",                     "provider":"Kaggle",           "duration":"4 hours",    "level":"beginner",    "source":"Kaggle",           "source_url":"https://www.kaggle.com/learn/pandas"},
    {"id":21, "title":"Data Visualization with Python",                             "description":"DataCamp Matplotlib, Seaborn, Plotly",          "provider":"DataCamp",         "duration":"4 hours",    "level":"beginner",    "source":"DataCamp",         "source_url":"https://www.datacamp.com/courses/introduction-to-data-visualization-with-python"},
    {"id":22, "title":"Data Visualization",                                         "description":"Kaggle free data visualization course",         "provider":"Kaggle",           "duration":"4 hours",    "level":"beginner",    "source":"Kaggle",           "source_url":"https://www.kaggle.com/learn/data-visualization"},
    {"id":23, "title":"Machine Learning Specialization",                            "description":"Andrew Ng Coursera ML — industry standard",     "provider":"Coursera",         "duration":"4 months",   "level":"intermediate","source":"Coursera",         "source_url":"https://www.coursera.org/specializations/machine-learning-introduction"},
    {"id":24, "title":"Machine Learning Crash Course",                              "description":"Google free ML course with TensorFlow",         "provider":"Google",           "duration":"15 hours",   "level":"intermediate","source":"Google",            "source_url":"https://developers.google.com/machine-learning/crash-course"},
    {"id":25, "title":"Intro to Machine Learning",                                  "description":"Kaggle free ML hands-on course",                "provider":"Kaggle",           "duration":"3 hours",    "level":"beginner",    "source":"Kaggle",           "source_url":"https://www.kaggle.com/learn/intro-to-machine-learning"},
    {"id":26, "title":"Neural Networks and Deep Learning",                          "description":"DeepLearning.AI Deep Learning Specialization 1","provider":"Coursera",         "duration":"4 weeks",    "level":"intermediate","source":"Coursera",         "source_url":"https://www.coursera.org/learn/neural-networks-deep-learning"},
    {"id":27, "title":"Deep Learning A-Z",                                          "description":"Udemy end-to-end DL with PyTorch/TensorFlow",   "provider":"Udemy",            "duration":"6–12 months","level":"intermediate","source":"Udemy",            "source_url":"https://www.udemy.com/course/deeplearning/"},
    {"id":28, "title":"Practical Deep Learning for Coders",                         "description":"fast.ai free practical DL course",              "provider":"fast.ai",          "duration":"Self-paced", "level":"intermediate","source":"fast.ai",           "source_url":"https://course.fast.ai/"},
    {"id":29, "title":"NLP Course",                                                 "description":"Hugging Face free NLP and transformers",        "provider":"Hugging Face",     "duration":"Self-paced", "level":"intermediate","source":"Hugging Face",      "source_url":"https://huggingface.co/learn/nlp-course/chapter1/1"},
    {"id":30, "title":"CS224N Natural Language Processing",                         "description":"Stanford free NLP course",                      "provider":"Stanford",         "duration":"Self-paced", "level":"advanced",    "source":"Stanford",         "source_url":"https://web.stanford.edu/class/cs224n/"},
    {"id":31, "title":"DeepLearning.AI TensorFlow Developer",                       "description":"Coursera TF professional certificate",          "provider":"Coursera",         "duration":"4 months",   "level":"intermediate","source":"Coursera",         "source_url":"https://www.coursera.org/professional-certificates/tensorflow-in-practice"},
    {"id":32, "title":"PyTorch Tutorials",                                          "description":"Official PyTorch tutorials — free",             "provider":"PyTorch",          "duration":"Self-paced", "level":"intermediate","source":"PyTorch",           "source_url":"https://pytorch.org/tutorials/"},
    {"id":33, "title":"Generative AI for Everyone",                                 "description":"Andrew Ng Coursera GenAI course",               "provider":"Coursera",         "duration":"3 weeks",    "level":"beginner",    "source":"Coursera",         "source_url":"https://www.coursera.org/learn/generative-ai-for-everyone"},
    {"id":34, "title":"LLM Course",                                                 "description":"Hugging Face free LLM course — RAG, agents",   "provider":"Hugging Face",     "duration":"Self-paced", "level":"intermediate","source":"Hugging Face",      "source_url":"https://huggingface.co/learn/llm-course/chapter1/1"},
    {"id":35, "title":"Machine Learning Engineering for Production (MLOps)",        "description":"Coursera MLOps specialization",                 "provider":"Coursera",         "duration":"4 months",   "level":"advanced",    "source":"Coursera",         "source_url":"https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops"},
    {"id":36, "title":"AWS Cloud Practitioner Essentials",                          "description":"AWS Skill Builder free cloud fundamentals",     "provider":"AWS Skill Builder","duration":"6 hours",    "level":"beginner",    "source":"AWS",              "source_url":"https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials"},
    {"id":37, "title":"Docker & CI/CD Fundamentals",                                "description":"Containerisation, Docker Compose, GitHub Actions","provider":"Coursera",       "duration":"4 weeks",    "level":"intermediate","source":"Coursera",         "source_url":"https://www.coursera.org/"},
    {"id":38, "title":"Supervised Learning with scikit-learn",                      "description":"DataCamp supervised ML course",                 "provider":"DataCamp",         "duration":"4 hours",    "level":"intermediate","source":"DataCamp",         "source_url":"https://www.datacamp.com/courses/supervised-learning-with-scikit-learn"},
    {"id":39, "title":"Intermediate Machine Learning",                              "description":"Kaggle intermediate ML — pipelines, CV",        "provider":"Kaggle",           "duration":"4 hours",    "level":"intermediate","source":"Kaggle",           "source_url":"https://www.kaggle.com/learn/intermediate-machine-learning"},
    {"id":40, "title":"Digital Systems: From Logic Gates to Processors",            "description":"Coursera digital electronics course",           "provider":"Coursera",         "duration":"8 weeks",    "level":"beginner",    "source":"Coursera",         "source_url":"https://www.coursera.org/learn/digital-systems"},
    {"id":41, "title":"Digital Electronics",                                        "description":"NPTEL digital electronics free course",         "provider":"NPTEL",            "duration":"12 weeks",   "level":"beginner",    "source":"NPTEL",            "source_url":"https://www.nptel.ac.in/courses/117106086"},
    {"id":42, "title":"Embedded Systems Programming on ARM Cortex-M3/M4",          "description":"Udemy embedded ARM bare-metal course",          "provider":"Udemy",            "duration":"6–12 months","level":"intermediate","source":"Udemy",            "source_url":"https://www.udemy.com/course/embedded-systems-programming-on-arm-cortex-m3m4/"},
    {"id":43, "title":"Introduction to Embedded Systems Software",                  "description":"Coursera embedded systems by U Colorado Boulder","provider":"Coursera",         "duration":"4 weeks",    "level":"beginner",    "source":"Coursera",         "source_url":"https://www.coursera.org/learn/introduction-embedded-systems"},
    {"id":44, "title":"Embedded Systems",                                           "description":"NPTEL embedded systems free course",            "provider":"NPTEL",            "duration":"12 weeks",   "level":"intermediate","source":"NPTEL",            "source_url":"https://www.nptel.ac.in/courses/108102045"},
    {"id":45, "title":"Introduction to the Internet of Things and Embedded Systems","description":"Coursera IoT fundamentals",                     "provider":"Coursera",         "duration":"4 weeks",    "level":"beginner",    "source":"Coursera",         "source_url":"https://www.coursera.org/learn/iot"},
    {"id":46, "title":"IoT Fundamentals",                                           "description":"Cisco Networking Academy IoT free course",      "provider":"Cisco Networking Academy","duration":"Self-paced","level":"beginner","source":"Cisco",           "source_url":"https://www.netacad.com/courses/iot"},
    {"id":47, "title":"MATLAB Onramp",                                              "description":"MathWorks official free MATLAB intro",          "provider":"MathWorks",        "duration":"2 hours",    "level":"beginner",    "source":"MathWorks",        "source_url":"https://matlabacademy.mathworks.com/details/matlab-onramp/gettingstarted"},
    {"id":48, "title":"Introduction to Programming with MATLAB",                    "description":"Coursera MATLAB by Vanderbilt University",      "provider":"Coursera",         "duration":"8 weeks",    "level":"beginner",    "source":"Coursera",         "source_url":"https://www.coursera.org/learn/matlab"},
    {"id":49, "title":"Power Systems Analysis",                                     "description":"NPTEL power systems free course",               "provider":"NPTEL",            "duration":"12 weeks",   "level":"advanced",    "source":"NPTEL",            "source_url":"https://www.nptel.ac.in/courses/117105140"},
    {"id":50, "title":"Introduction to Power Electronics",                          "description":"Coursera power electronics by U Colorado",      "provider":"Coursera",         "duration":"16 weeks",   "level":"intermediate","source":"Coursera",         "source_url":"https://www.coursera.org/learn/power-electronics"},
    {"id":51, "title":"Control Systems Engineering",                                "description":"NPTEL control systems free course",             "provider":"NPTEL",            "duration":"12 weeks",   "level":"intermediate","source":"NPTEL",            "source_url":"https://www.nptel.ac.in/courses"},
    {"id":52, "title":"MATLAB and Simulink for Engineers",                          "description":"Control and signal processing toolboxes",        "provider":"MathWorks",        "duration":"6 weeks",    "level":"intermediate","source":"Coursera",         "source_url":"https://www.coursera.org/learn/matlab"},
    {"id":53, "title":"Introduction to Renewable Energy",                           "description":"Coursera renewable energy course",              "provider":"Coursera",         "duration":"8 weeks",    "level":"beginner",    "source":"Coursera",         "source_url":"https://www.coursera.org/learn/renewable-energy"},
    {"id":54, "title":"Electric Vehicle Sensors and Systems",                       "description":"Coursera EV — battery, powertrain, charging",  "provider":"Coursera",         "duration":"6 weeks",    "level":"intermediate","source":"Coursera",         "source_url":"https://www.coursera.org/learn/electric-vehicle-sensors-systems"},
    {"id":55, "title":"PLC Programming from Scratch",                               "description":"Udemy PLC and SCADA industrial automation",     "provider":"Udemy",            "duration":"6–12 months","level":"beginner",    "source":"Udemy",            "source_url":"https://www.udemy.com/course/plc-programming-from-scratch/"},
    {"id":56, "title":"Electrical Machines & Transformers",                          "description":"NPTEL complete course on Electrical Machines & Drives", "provider":"NPTEL",            "duration":"12 weeks",   "level":"intermediate","source":"NPTEL",            "source_url":"https://www.nptel.ac.in/courses/108108191"},
    {"id":57, "title":"Electrical Measurements & Instrumentation",                  "description":"Coursera/NPTEL electrical measurement & transducers","provider":"NPTEL",            "duration":"12 weeks",   "level":"intermediate","source":"NPTEL",            "source_url":"https://www.nptel.ac.in/courses"},
]

COURSE_COMPETENCIES: list[dict[str, Any]] = [
    {"course_id":1,  "competency_id":1,  "coverage_level":5},
    {"course_id":1,  "competency_id":28, "coverage_level":2},
    {"course_id":2,  "competency_id":1,  "coverage_level":5},
    {"course_id":3,  "competency_id":1,  "coverage_level":3},
    {"course_id":3,  "competency_id":3,  "coverage_level":3},
    {"course_id":3,  "competency_id":6,  "coverage_level":2},
    {"course_id":3,  "competency_id":7,  "coverage_level":2},
    {"course_id":4,  "competency_id":2,  "coverage_level":5},
    {"course_id":4,  "competency_id":47, "coverage_level":3},
    {"course_id":5,  "competency_id":2,  "coverage_level":5},
    {"course_id":5,  "competency_id":47, "coverage_level":3},
    {"course_id":6,  "competency_id":3,  "coverage_level":5},
    {"course_id":6,  "competency_id":47, "coverage_level":2},
    {"course_id":7,  "competency_id":3,  "coverage_level":4},
    {"course_id":7,  "competency_id":6,  "coverage_level":2},
    {"course_id":8,  "competency_id":3,  "coverage_level":4},
    {"course_id":8,  "competency_id":13, "coverage_level":3},
    {"course_id":8,  "competency_id":12, "coverage_level":2},
    {"course_id":9,  "competency_id":3,  "coverage_level":4},
    {"course_id":9,  "competency_id":4,  "coverage_level":2},
    {"course_id":10, "competency_id":4,  "coverage_level":5},
    {"course_id":10, "competency_id":3,  "coverage_level":2},
    {"course_id":11, "competency_id":4,  "coverage_level":5},
    {"course_id":11, "competency_id":45, "coverage_level":2},
    {"course_id":12, "competency_id":6,  "coverage_level":5},
    {"course_id":12, "competency_id":5,  "coverage_level":3},
    {"course_id":12, "competency_id":3,  "coverage_level":2},
    {"course_id":13, "competency_id":6,  "coverage_level":5},
    {"course_id":13, "competency_id":5,  "coverage_level":3},
    {"course_id":14, "competency_id":6,  "coverage_level":3},
    {"course_id":15, "competency_id":7,  "coverage_level":5},
    {"course_id":15, "competency_id":48, "coverage_level":3},
    {"course_id":15, "competency_id":47, "coverage_level":2},
    {"course_id":16, "competency_id":7,  "coverage_level":5},
    {"course_id":16, "competency_id":48, "coverage_level":4},
    {"course_id":16, "competency_id":47, "coverage_level":2},
    {"course_id":17, "competency_id":12, "coverage_level":5},
    {"course_id":17, "competency_id":21, "coverage_level":2},
    {"course_id":18, "competency_id":12, "coverage_level":4},
    {"course_id":19, "competency_id":13, "coverage_level":5},
    {"course_id":19, "competency_id":3,  "coverage_level":2},
    {"course_id":19, "competency_id":12, "coverage_level":2},
    {"course_id":20, "competency_id":13, "coverage_level":4},
    {"course_id":20, "competency_id":3,  "coverage_level":2},
    {"course_id":21, "competency_id":14, "coverage_level":5},
    {"course_id":21, "competency_id":3,  "coverage_level":2},
    {"course_id":22, "competency_id":14, "coverage_level":4},
    {"course_id":23, "competency_id":15, "coverage_level":5},
    {"course_id":23, "competency_id":21, "coverage_level":3},
    {"course_id":23, "competency_id":50, "coverage_level":3},
    {"course_id":23, "competency_id":12, "coverage_level":2},
    {"course_id":24, "competency_id":15, "coverage_level":4},
    {"course_id":24, "competency_id":23, "coverage_level":2},
    {"course_id":25, "competency_id":15, "coverage_level":3},
    {"course_id":25, "competency_id":21, "coverage_level":2},
    {"course_id":26, "competency_id":16, "coverage_level":5},
    {"course_id":26, "competency_id":22, "coverage_level":5},
    {"course_id":26, "competency_id":15, "coverage_level":3},
    {"course_id":27, "competency_id":16, "coverage_level":5},
    {"course_id":27, "competency_id":22, "coverage_level":4},
    {"course_id":27, "competency_id":23, "coverage_level":3},
    {"course_id":28, "competency_id":16, "coverage_level":5},
    {"course_id":28, "competency_id":23, "coverage_level":4},
    {"course_id":28, "competency_id":18, "coverage_level":3},
    {"course_id":28, "competency_id":17, "coverage_level":2},
    {"course_id":29, "competency_id":17, "coverage_level":5},
    {"course_id":29, "competency_id":24, "coverage_level":3},
    {"course_id":29, "competency_id":23, "coverage_level":2},
    {"course_id":30, "competency_id":17, "coverage_level":5},
    {"course_id":30, "competency_id":16, "coverage_level":3},
    {"course_id":31, "competency_id":23, "coverage_level":5},
    {"course_id":31, "competency_id":16, "coverage_level":4},
    {"course_id":31, "competency_id":17, "coverage_level":3},
    {"course_id":32, "competency_id":23, "coverage_level":5},
    {"course_id":32, "competency_id":16, "coverage_level":3},
    {"course_id":33, "competency_id":24, "coverage_level":5},
    {"course_id":33, "competency_id":17, "coverage_level":2},
    {"course_id":34, "competency_id":24, "coverage_level":5},
    {"course_id":34, "competency_id":17, "coverage_level":3},
    {"course_id":34, "competency_id":25, "coverage_level":2},
    {"course_id":35, "competency_id":25, "coverage_level":5},
    {"course_id":35, "competency_id":46, "coverage_level":3},
    {"course_id":35, "competency_id":10, "coverage_level":2},
    {"course_id":35, "competency_id":15, "coverage_level":2},
    {"course_id":36, "competency_id":10, "coverage_level":4},
    {"course_id":36, "competency_id":46, "coverage_level":2},
    {"course_id":37, "competency_id":46, "coverage_level":5},
    {"course_id":37, "competency_id":10, "coverage_level":2},
    {"course_id":38, "competency_id":50, "coverage_level":5},
    {"course_id":38, "competency_id":15, "coverage_level":3},
    {"course_id":38, "competency_id":21, "coverage_level":3},
    {"course_id":39, "competency_id":50, "coverage_level":4},
    {"course_id":39, "competency_id":15, "coverage_level":3},
    {"course_id":40, "competency_id":26, "coverage_level":5},
    {"course_id":41, "competency_id":26, "coverage_level":5},
    {"course_id":41, "competency_id":29, "coverage_level":2},
    {"course_id":42, "competency_id":28, "coverage_level":5},
    {"course_id":42, "competency_id":30, "coverage_level":4},
    {"course_id":42, "competency_id":1,  "coverage_level":3},
    {"course_id":43, "competency_id":28, "coverage_level":4},
    {"course_id":43, "competency_id":30, "coverage_level":3},
    {"course_id":44, "competency_id":28, "coverage_level":5},
    {"course_id":44, "competency_id":30, "coverage_level":3},
    {"course_id":44, "competency_id":32, "coverage_level":2},
    {"course_id":45, "competency_id":33, "coverage_level":5},
    {"course_id":45, "competency_id":28, "coverage_level":2},
    {"course_id":46, "competency_id":33, "coverage_level":4},
    {"course_id":46, "competency_id":9,  "coverage_level":2},
    {"course_id":47, "competency_id":34, "coverage_level":3},
    {"course_id":48, "competency_id":34, "coverage_level":5},
    {"course_id":48, "competency_id":35, "coverage_level":2},
    {"course_id":49, "competency_id":37, "coverage_level":5},
    {"course_id":49, "competency_id":36, "coverage_level":2},
    {"course_id":50, "competency_id":38, "coverage_level":5},
    {"course_id":50, "competency_id":37, "coverage_level":2},
    {"course_id":51, "competency_id":39, "coverage_level":5},
    {"course_id":51, "competency_id":34, "coverage_level":2},
    {"course_id":52, "competency_id":34, "coverage_level":5},
    {"course_id":52, "competency_id":39, "coverage_level":3},
    {"course_id":52, "competency_id":35, "coverage_level":2},
    {"course_id":53, "competency_id":42, "coverage_level":5},
    {"course_id":53, "competency_id":37, "coverage_level":2},
    {"course_id":54, "competency_id":43, "coverage_level":5},
    {"course_id":54, "competency_id":38, "coverage_level":3},
    {"course_id":55, "competency_id":41, "coverage_level":5},
    {"course_id":56, "competency_id":36, "coverage_level":5},
    {"course_id":56, "competency_id":37, "coverage_level":2},
    {"course_id":57, "competency_id":40, "coverage_level":5},
    {"course_id":57, "competency_id":39, "coverage_level":2},
]

