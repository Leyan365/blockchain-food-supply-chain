# Farm-to-Chain Fresh: A Blockchain-based Food Supply Chain

## 📖 Project Overview

**Farm-to-Chain Fresh** is a web application that leverages blockchain technology and data science to create a transparent and traceable food supply chain. Built with Python's **Flask** framework, this project demonstrates how every step of a food product's journey—from the farm to the retailer—can be recorded on an immutable ledger. The application provides stakeholders with real-time analytics to ensure quality, prevent fraud, and build consumer trust.

## ✨ Key Features

* **Stakeholder Dashboards:** Role-based dashboards for **Farmers**, **Distributors**, and **Retailers** to manage their specific operations.
* **End-to-End Traceability:** A public-facing explorer to view the entire history of any product on the blockchain, from origin to final destination.
* **Data Analytics:** Integrates data science quality control, anomaly detection, and supply chain performance analysis.

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.8+ installed.

### Installation

1.  Clone the repository:
  

2.  Create and activate a virtual environment:
   

3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  Run the application:
    ```bash
    python run.py
    ```

5.  Open your web browser and navigate to `http://127.0.0.1:5000`.

## 🔒 User Credentials

The application uses hardcoded credentials for demonstration purposes.

| Role | Email | Password |
| :--- | :--- | :--- |
| **Farmer** | `farmer1@example.com` | `pass123` |
| **Distributor** | `dist1@example.com` | `pass123` |
| **Retailer** | `retail1@example.com` | `pass123` |

---

## 📸 Application Walkthrough

### 1. Landing Page & Login

The application's landing page provides a clean, user-friendly introduction to the platform and its purpose. It clearly explains the benefits of blockchain-based traceability.

!<img width="1920" height="1044" alt="landing page 1" src="https://github.com/user-attachments/assets/0771bd81-bd60-4f3d-b193-eae23b482ac0" />
!<img width="1891" height="1034" alt="landing page 2" src="https://github.com/user-attachments/assets/163fac7e-472f-4d05-924f-f4153f52ae8b" />


The login page ensures secure, role-based access for each stakeholder, directing them to their unique dashboard.

!<img width="1696" height="867" alt="login" src="https://github.com/user-attachments/assets/3925075f-f22e-49bb-b68d-ae8b80926c39" />


### 2. Stakeholder Dashboards

#### Farmer Dashboard

This dashboard allows a farmer to register a new product, logging its initial details, location, and environmental conditions. This action creates the first immutable transaction on the blockchain.

!<img width="1780" height="996" alt="farmer dashboard" src="https://github.com/user-attachments/assets/c9ef49e7-42dd-4c14-878b-8baa6338f1e5" />
!<img width="1732" height="972" alt="farmer dashboard 2" src="https://github.com/user-attachments/assets/b28e1f22-fce4-4430-bd23-04ee856233c4" />


#### Distributor Dashboard

The distributor's dashboard allows them to receive products from farmers, update their status, and transfer them to retailers. Every step is logged on the blockchain, ensuring a continuous chain of custody.

!<img width="1751" height="991" alt="dist dashboard" src="https://github.com/user-attachments/assets/b3f5d38b-2557-4dea-9c69-28d6c4020e4c" />
!<img width="1643" height="737" alt="dist shipments" src="https://github.com/user-attachments/assets/db158c0f-6427-4586-9802-b3554ad24edc" />


#### Retailer Dashboard

The retailer manages incoming deliveries and updates the inventory's status. They can also record the final sale to a consumer, completing the product's journey on the blockchain.

!<img width="1702" height="870" alt="retailer dash" src="https://github.com/user-attachments/assets/565c3b49-6573-4af0-91a6-cab832a35915" />
!<img width="1676" height="713" alt="inven" src="https://github.com/user-attachments/assets/61a231d5-8a85-41ab-9b26-f750ce839b5a" />


### 3. Blockchain Explorer

This page provides a public, transparent view of the entire blockchain. Any user can inspect each block to see its hash, timestamp, and the transactions it contains, proving the immutability of the data.

!<img width="1708" height="962" alt="logged blockchain" src="https://github.com/user-attachments/assets/46302e1a-dbca-4dbe-88c8-54daa0239969" />
!<img width="1695" height="1001" alt="loggeed in block data" src="https://github.com/user-attachments/assets/55c63a65-0cc9-4812-a384-dd67bc17b05d" />
!<img width="1241" height="1006" alt="chain visualization" src="https://github.com/user-attachments/assets/e4e3a379-aa06-4839-bd39-20e11d30193b" />


### 4. Analytics Dashboard

This dashboard transforms raw blockchain data into actionable insights using data science. Visualizations help monitor performance, detect anomalies (like temperature spikes), and ensure product quality throughout the journey.

!<img width="1740" height="1010" alt="ana" src="https://github.com/user-attachments/assets/0445ffff-b4ea-40dd-9fe0-e45fb798fbbc" />
!<img width="1660" height="775" alt="temp ano" src="https://github.com/user-attachments/assets/6e875526-d78c-457b-880e-5527ba7206a2" />
!<img width="1638" height="837" alt="time" src="https://github.com/user-attachments/assets/26350038-b8e1-4969-9ffe-d18b624803c8" />
!<img width="1752" height="927" alt="bar" src="https://github.com/user-attachments/assets/18557a8c-972f-4df1-a937-608738e378f6" />
!<img width="1692" height="746" alt="boxplot" src="https://github.com/user-attachments/assets/09c0f99b-91ac-4cc5-8068-84597891dbec" />
!<img width="1707" height="750" alt="transsactions" src="https://github.com/user-attachments/assets/d28ae5bc-6e02-43b9-ae02-215119e42f91" />
!<img width="1731" height="761" alt="scatter" src="https://github.com/user-attachments/assets/a6075202-bdd8-40d7-95c4-56c756a77720" />



---

## 🛠️ Technology Stack

* **Backend:** Python-Flask
* **Blockchain:** Custom implementation for a private, permissioned network.
* **Data Science:** Pandas, Matplotlib, Plotly for data analysis and visualization.
* **Frontend:** HTML, CSS.
* **Data Persistence:** JSON files for simple data storage.
* **Version Control:** Git, GitHub.
