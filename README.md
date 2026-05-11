# Farm-to-Chain Fresh: Blockchain Food Supply Chain

Farm-to-Chain Fresh is a Flask web application that demonstrates how blockchain-style records can improve food supply-chain traceability. Farmers, distributors, and retailers can record product movements, storage conditions, and custody changes, while consumers can verify a product's journey through a public tracking page or QR code.

## Key Features

- Role dashboards for farmers, distributors, retailers, and consumers.
- Blockchain-backed product history with block hashes, proof values, and chain validation.
- Public product tracking by product ID.
- QR codes for product tracking links.
- Analytics dashboard with filters, KPIs, insights, anomaly reports, and charts.
- Role-based access control for protected stakeholder dashboards.
- JSON-backed demo persistence for blockchain and sample product data.
- Automated tests for blockchain behavior, route access, tracking, QR generation, and analytics.

## Technology Stack

- Backend: Python, Flask
- Blockchain: Custom proof-of-work blockchain implementation
- Analytics: Pandas, Plotly, NumPy, scikit-learn
- Frontend: HTML, Bootstrap, CSS
- Persistence: JSON files
- Testing: Python unittest

## Setup

### 1. Clone The Repository

```bash
git clone https://github.com/Leyan365/blockchain-food-supply-chain.git
cd blockchain-food-supply-chain
```

### 2. Create And Activate A Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Conda:

```powershell
conda create -n dsenv python=3.13
conda activate dsenv
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run The Application

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## Demo Credentials

| Role | Email | Password |
| :--- | :--- | :--- |
| Farmer | `farmer1@example.com` | `pass123` |
| Distributor | `dist1@example.com` | `pass123` |
| Retailer | `retail1@example.com` | `pass123` |
| Consumer | `consumer1@example.com` | `pass123` |

## Useful URLs

| Page | URL |
| :--- | :--- |
| Home | `http://127.0.0.1:5000/` |
| Login | `http://127.0.0.1:5000/auth/login` |
| Farmer Dashboard | `http://127.0.0.1:5000/farmer/dashboard` |
| Distributor Dashboard | `http://127.0.0.1:5000/distributor/dashboard` |
| Retailer Dashboard | `http://127.0.0.1:5000/retailer/dashboard` |
| Consumer Tracking | `http://127.0.0.1:5000/consumer/dashboard` |
| Analytics | `http://127.0.0.1:5000/analytics/overview` |
| Blockchain Explorer | `http://127.0.0.1:5000/blockchain-data` |
| Blockchain Status API | `http://127.0.0.1:5000/api/blockchain/status` |
| Products API | `http://127.0.0.1:5000/api/products` |

Product-specific tracking URLs use this format:

```text
http://127.0.0.1:5000/consumer/track/<product_id>
```

QR images use this format:

```text
http://127.0.0.1:5000/consumer/qr/<product_id>
```

## JSON API

The project includes read-only JSON endpoints for integrations, mobile clients, and testing:

```text
GET /api/blockchain/status
GET /api/products
GET /api/products/<product_id>
GET /api/products/<product_id>/history
```

These endpoints expose chain health, product summaries, latest product state, and full product history without requiring the HTML dashboards.

## Demo Flow

1. Log in as the farmer and register a new product.
2. Open the farmer dashboard and use the product's Track button or QR code.
3. Log in as the distributor and update shipment conditions.
4. Log in as the retailer and update inventory or sale status.
5. Open the consumer tracking page to verify the full product journey.
6. Open the analytics dashboard to filter by product, status, stakeholder, date range, anomalies, or "My activity".
7. Open the blockchain explorer and confirm the chain integrity status is valid.

## Analytics Dashboard

The analytics dashboard starts with all supply-chain data. Logged-in stakeholder users can switch the Data Scope filter to "My activity" to focus only on transactions where they are the sender or recipient.

Current analytics include:

- Total products and transactions
- In-transit and sold/stocked counts
- Average temperature
- Temperature anomaly count and anomaly rate
- Average journey duration
- Chain validity status
- Temperature trend chart
- Status distribution chart
- Product condition chart
- Stakeholder activity chart
- Journey duration chart
- Anomalies by product chart

## Access Control

The application protects role-specific dashboards:

- Farmers can access farmer routes.
- Distributors can access distributor routes.
- Retailers can access retailer routes.
- Wrong-role users are redirected back to their own dashboard.
- Consumer tracking remains public for product verification.
- Analytics and blockchain explorer require login.

## Running Tests

```bash
python -m unittest discover -s tests -v
```

The current test suite covers:

- Blockchain mining and validity
- Transaction expiry date persistence
- Consumer tracking routes
- Product and blockchain status APIs
- QR PNG generation
- Role-based route protection
- Analytics filters and page rendering

## Application Walkthrough

### Landing Page And Login

The landing page introduces the platform and the value of blockchain-based traceability.

<img width="1920" height="1044" alt="landing page 1" src="https://github.com/user-attachments/assets/0771bd81-bd60-4f3d-b193-eae23b482ac0" />
<img width="1891" height="1034" alt="landing page 2" src="https://github.com/user-attachments/assets/163fac7e-472f-4d05-924f-f4153f52ae8b" />

The login page sends each stakeholder to the correct dashboard.

<img width="1696" height="867" alt="login" src="https://github.com/user-attachments/assets/3925075f-f22e-49bb-b68d-ae8b80926c39" />

### Stakeholder Dashboards

#### Farmer Dashboard

Farmers register products, capture origin details, and create the first immutable transaction in the product journey.

<img width="1780" height="996" alt="farmer dashboard" src="https://github.com/user-attachments/assets/c9ef49e7-42dd-4c14-878b-8baa6338f1e5" />
<img width="1732" height="972" alt="farmer dashboard 2" src="https://github.com/user-attachments/assets/b28e1f22-fce4-4430-bd23-04ee856233c4" />

#### Distributor Dashboard

Distributors receive products, update shipment conditions, and forward products to retailers.

<img width="1751" height="991" alt="distributor dashboard" src="https://github.com/user-attachments/assets/b3f5d38b-2557-4dea-9c69-28d6c4020e4c" />
<img width="1643" height="737" alt="distributor shipments" src="https://github.com/user-attachments/assets/db158c0f-6427-4586-9802-b3554ad24edc" />

#### Retailer Dashboard

Retailers manage incoming deliveries, storage conditions, inventory status, and final sale records.

<img width="1702" height="870" alt="retailer dashboard" src="https://github.com/user-attachments/assets/565c3b49-6573-4af0-91a6-cab832a35915" />
<img width="1676" height="713" alt="inventory" src="https://github.com/user-attachments/assets/61a231d5-8a85-41ab-9b26-f750ce839b5a" />

### Blockchain Explorer

The blockchain explorer shows blocks, transactions, hashes, proof values, pending transactions, and chain integrity.

<img width="1708" height="962" alt="logged blockchain" src="https://github.com/user-attachments/assets/46302e1a-dbca-4dbe-88c8-54daa0239969" />
<img width="1695" height="1001" alt="logged in block data" src="https://github.com/user-attachments/assets/55c63a65-0cc9-4812-a384-dd67bc17b05d" />
<img width="1241" height="1006" alt="chain visualization" src="https://github.com/user-attachments/assets/e4e3a379-aa06-4839-bd39-20e11d30193b" />

### Analytics Dashboard

The analytics dashboard transforms blockchain records into operational metrics, charts, and anomaly insights.

<img width="1740" height="1010" alt="analytics" src="https://github.com/user-attachments/assets/0445ffff-b4ea-40dd-9fe0-e45fb798fbbc" />
<img width="1660" height="775" alt="temperature anomalies" src="https://github.com/user-attachments/assets/6e875526-d78c-457b-880e-5527ba7206a2" />
<img width="1638" height="837" alt="journey time" src="https://github.com/user-attachments/assets/26350038-b8e1-4969-9ffe-d18b624803c8" />
<img width="1752" height="927" alt="bar chart" src="https://github.com/user-attachments/assets/18557a8c-972f-4df1-a937-608738e378f6" />
<img width="1692" height="746" alt="box plot" src="https://github.com/user-attachments/assets/09c0f99b-91ac-4cc5-8068-84597891dbec" />
<img width="1707" height="750" alt="transactions" src="https://github.com/user-attachments/assets/d28ae5bc-6e02-43b9-ae02-215119e42f91" />
<img width="1731" height="761" alt="scatter chart" src="https://github.com/user-attachments/assets/a6075202-bdd8-40d7-95c4-56c756a77720" />

## Notes

This is a demonstration project. The current credentials and JSON persistence are intentionally simple for coursework and local demos. For production use, replace demo credentials with hashed passwords and use a database-backed persistence layer.
