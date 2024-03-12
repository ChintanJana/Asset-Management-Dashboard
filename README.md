# Asset Performance Analytics Dashboard - Backend

This FastAPI application serves as the backend for an Asset Performance Analytics Dashboard. It interacts with a MongoDB database to analyze and collate data related to various assets' performance metrics.

## Setup
1. **Creating a Virtual Environment:**
    Open the backend directory in terminal. We use `pipenv` to activate the virtual environment.
    ```bash
    pipenv shell
    ```
    We can use `pip` to install `pipenv`
    ```bash
    pip install pipenv
    ```

2. **Install Dependencies:**
    ```bash
    pipenv install -r requirements.txt
    ```
    The above command is used to install the depencied in the virtual environment.

3. **Start MongoDB Server:**
   Ensure that your MongoDB server is running. You can start it using the following command:
   ```bash
   sudo service mongod start
   ```
   We can also do this using the MongoDB Compass.
   
   We also may create a database `asset_performance` containg 2 collections `assests` and `performance_metrics`
   
4. **Run the Application:**
    ```bash
    uvicorn main:app
    ```
    
## Usage

### Authentication
- Some endpoints require authentication using HTTP Basic Authentication. 
- **username = "admin"** and **password = "password"** is used to authenticate and access protected endpoints.

### Endpoint Details 

#### CRUD Operations
    
We can use the provided CRUD endpoints to perform Create, Read, Update, and Delete operations on assets and performance

##### `asset_router.py`
Here are the details for the endpoints defined in `asset_router.py`:

1. **`/assets/`**
   - **HTTP Method:** POST
   - **Request Body:** JSON object representing the new asset
   - **Response Body:** JSON object representing the created asset
   - **Response Model:** Asset

2. **`/assets`**
   - **HTTP Method:** GET
   - **Response Body:** List of JSON objects representing all assets
   - **Response Model:** List of Asset objects

3. **`/assets/{asset_id}`**
   - **HTTP Method:** GET
   - **Path Parameters:** `asset_id` - ID of the asset to retrieve
   - **Response Body:** JSON object representing the asset with the specified ID
   - **Response Model:** Asset

4. **`/assets/{asset_id}`**
   - **HTTP Method:** PUT
   - **Path Parameters:** `asset_id` - ID of the asset to update
   - **Request Body:** JSON object representing the updated asset
   - **Response Body:** JSON object representing the updated asset
   - **Response Model:** Asset

5. **`/assets/{asset_id}`**
   - **HTTP Method:** DELETE
   - **Path Parameters:** `asset_id` - ID of the asset to delete
   - **Response Body:** JSON object with a success message
   - **Response Status:** 200 OK if successful, 404 Not Found if the asset does not exist

These endpoints allow you to perform CRUD (Create, Read, Update, Delete) operations on assets in your system.

##### `metric_router.py`

Here are the details for the endpoints defined in `metric_router.py`:

1. **`/metrics/`**
   - **HTTP Method:** POST
   - **Request Body:** JSON object representing the new performance metric
   - **Response Body:** JSON object representing the created performance metric
   - **Response Model:** PerformanceMetric

2. **`/metrics`**
   - **HTTP Method:** GET
   - **Response Body:** List of JSON objects representing all performance metrics
   - **Response Model:** List of PerformanceMetric objects

3. **`/metrics/{metric_id}`**
   - **HTTP Method:** GET
   - **Path Parameters:** `metric_id` - ID of the performance metric to retrieve
   - **Response Body:** JSON object representing the performance metric with the specified ID
   - **Response Model:** PerformanceMetric

4. **`/metrics/{metric_id}`**
   - **HTTP Method:** PUT
   - **Path Parameters:** `metric_id` - ID of the performance metric to update
   - **Request Body:** JSON object representing the updated performance metric
   - **Response Body:** JSON object representing the updated performance metric
   - **Response Model:** PerformanceMetric

5. **`/metrics/{metric_id}`**
   - **HTTP Method:** DELETE
   - **Path Parameters:** `metric_id` - ID of the performance metric to delete
   - **Response Body:** JSON object with a success message
   - **Response Status:** 200 OK if successful, 404 Not Found if the performance metric does not exist

These endpoints allow you to perform CRUD (Create, Read, Update, Delete) operations on performance metrics in your system.

#### Data Aggregation and Insights
Here are the details for the endpoints defined in `aggregation_router.py`:

1. **Calculate Average Downtime**
   - **HTTP Method:** GET
   - **URL:** `/average-downtime`
   - **Response Body:** JSON object containing the average downtime
   - **Response Model:** `{"average_downtime": float}`
   - This endpoint calculates the average downtime across all assets. It uses a data aggregation function `calculate_average_downtime`(in **database.py**) that retrieves the downtime metrics for all assets from the database and computes their average value.

2. **Calculate Total Maintenance Costs**
   - **HTTP Method:** GET
   - **URL:** `/total-maintenance-costs`
   - **Response Body:** JSON object containing the total maintenance costs
   - **Response Model:** `{"total_maintenance_costs": float}`
   -  This endpoint calculates the total maintenance costs across all assets. It uses a data aggregation function `calculate_total_maintenance_costs`(in **database.py**) that retrieves the maintenance cost metrics for all assets from the database and sums up their values.

3. **Identify Assets with High Failure Rates**
   - **HTTP Method:** GET
   - **URL:** `/assets/high-failure-rates/`
   - **Query Parameters:** `threshold` - Threshold value for failure rates (default: 0.01)
   - **Response Body:** List of JSON objects representing assets with high failure rates
   - **Response Status:** 200 OK if successful, 404 Not Found if no assets are found
   - **Response Model:** List of asset objects
   - This endpoint identifies assets with failure rates above a specified threshold. It uses a data aggregation function `identify_assets_with_high_failure_rates`(in **database.py**) that filters assets based on their failure rate metrics and returns those with rates exceeding the given `threshold` value.

These endpoints provide valuable insights into asset performance and help in identifying areas that require attention or improvement.

### Example API Requests:
- Create a new asset:
  ```bash
    curl -X 'POST' \
      'http://127.0.0.1:8000/assets/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
          "asset_id": "4",
          "asset_name": "Machine D",
          "asset_type": "Machine",
          "location": "Factory 1",
          "purchase_date": "2023-01-10",
          "initial_cost": 25000.0,
          "operational_status": "operational"
    }'
  ```

- Retrieve a specified assets:
  ```bash
    curl -X 'GET' \
        'http://127.0.0.1:8000/assets/4' \
        -H 'accept: application/json'
  ```
  Retreiving asset with `"asset_id" = "4"`

- Delete an asset and its associated metrics:
  ```bash
    curl -X 'DELETE' \
      'http://127.0.0.1:8000/assets/4' \
      -H 'accept: application/json'
  ```
This README provides clear instructions for setting up the application, using its endpoints, and understanding its functionality. We can customize it further based on our specific application requirements and add any additional details as needed.

