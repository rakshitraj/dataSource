# DataSource Project Documentation

## Overview
The `dataSource` project is a Python-based data ingestion framework designed to fetch data from various sources, process it, and store it in an S3 bucket. It includes modular components for configuration management, logging, and data source abstraction.

---

## Project Structure
```
dataSource/
├── .gitignore
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── src/
│   ├── audit_logger.py
│   ├── config.py
│   ├── data_source.py
│   ├── main.py
│   ├── models/
│   │   └── pipeline_configuration_orm.py
│   ├── s3_writer.py
│   ├── sources/
│   │   ├── example_api.py
│   │   └── s3_source.py
│   ├── utils.py
```

---

## Key Components

### 1. **Main Entry Point**
- **File:** `src/main.py`
- **Purpose:** Orchestrates the ingestion process by:
    - Parsing command-line arguments.
    - Initializing the appropriate data source client.
    - Running the ingestion pipeline.

### 2. **Data Sources**
- **Abstract Base Class:** `src/data_source.py`
    - Defines the interface for data sources (`fetch_data`, `data_filter`, `format_data`).
- **Implementations:**
    - **Example API Client:** `src/sources/example_api.py`
        - Fetches data from an external API.
    - **S3 File Fetcher:** `src/sources/s3_source.py`
        - Fetches files from an S3 bucket.

### 3. **Configuration Management**
- **File:** `src/config.py`
- **Purpose:** Manages pipeline configurations stored in an RDS database.
- **Key Class:** `RDSConfigurationProvider`
    - Fetches configuration values for a specific pipeline.

### 4. **Audit Logging**
- **File:** `src/audit_logger.py`
- **Purpose:** Logs audit information such as job status, duration, and errors.

### 5. **S3 Writer**
- **File:** `src/s3_writer.py`
- **Purpose:** Writes processed data to an S3 bucket.

### 6. **Utilities**
- **File:** `src/utils.py`
- **Purpose:** Provides helper functions, such as argument parsing.

### 7. **ORM Models**
- **File:** `src/models/pipeline_configuration_orm.py`
- **Purpose:** Defines the SQLAlchemy ORM model for the `pipeline_configuration` table.

---

## Installation

1. Clone the repository:
     ```bash
     git clone <repository-url>
     cd dataSource
     ```

2. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. Set up environment variables for AWS credentials and database connection.

---

## Usage

### Command-Line Arguments
The ingestion process is configured via command-line arguments:
- `--pipeline_id`: Unique pipeline identifier.
- `--job_id`: Job identifier.
- `--source`: Data source type (`example_api` or `s3`).
- `--conn_conf`: Path to encrypted connection configuration.
- `--private_key`: Decryption key for the configuration.

### Running the Ingestion
```bash
python src/main.py --pipeline_id <pipeline_id> --job_id <job_id> --source <source> --conn_conf <path_to_config> --private_key <decryption_key>
```

---

## Docker Support
Build and run the project using Docker:
1. Build the Docker image:
     ```bash
     docker build -t data-source .
     ```

2. Run the container:
     ```bash
     docker run data-source
     ```

---

## License
This project is licensed under the [Apache License 2.0](LICENSE).

---

## Contributing
Contributions are welcome! Please follow the standard GitHub workflow:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

---

## Contact
For questions or support, please contact the project maintainer.
