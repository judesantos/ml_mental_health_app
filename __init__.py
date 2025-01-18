"""
This script creates the directories and certificates needed
the first time the project is cloned into a development environment.
This script also checks if the target table exists in the database and
creates it if it does not exist using the CSV file in the 'data' directory.

The script creates the following directories:
    - certs: Contains the private key and certificate for the application.
    - data: Contains the cd dataset csv file used for the inference model.
"""

import os
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv


def create_directories_and_certificates():
    """
    Create the directories and certificates for the application
    if certs directory is created for the first time.

    The function creates the following directories:
        - certs: Contains the private key and certificate for the application.
        - data: Contains the cd dataset csv file used for the inference model.
    """
    # Define the directories
    directories = ["certs", "data"]
    create_certs = False

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
            if directory == "certs":
                create_certs = True
        else:
            print(f"Directory already exists: {directory}")

    if create_certs:
        # Generate self-signed certificates
        generate_self_signed_cert()

def generate_self_signed_cert():
    """
    Generate a self-signed certificate for the application.

    The certificate is generated with the predefined attributes
    and used for development purposes only.

    Files created:
        - app_private_key.pem: The private key for the application.
        - app_certificate.pem: The self-signed certificate for the application.

    Cautions:
        This certificate is for development purposes only.
    """
    print("Generating self-signed certificate...")
    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Write the private key to a file
    private_key_path = os.path.join("certs", "app_private_key.pem")
    with open(private_key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )
    print(f"Private key saved to {private_key_path}")

    # Generate a public certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Irvine"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "yourtechy.com LLC"),
        x509.NameAttribute(NameOID.COMMON_NAME, "yourtechy.com"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName("yourtechy.com")]),
        critical=False,
    ).sign(private_key, SHA256(), default_backend())

    # Write the certificate to a file
    cert_path = os.path.join("certs", "app_certificate.pem")
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    print(f"Certificate saved to {cert_path}")

def check_and_create_table():
    # Load environment variables
    load_dotenv()
    db_url = os.getenv("DB_URL")  # Database connection string
    table_name = os.getenv("TABLE_NAME")  # Target table name
    csv_file_name = os.getenv("CSV_FILE_NAME")  # CSV file name in the 'data' directory

    if not db_url or not table_name or not csv_file_name:
        print("Environment variables DB_URL, TABLE_NAME, or CSV_FILE_NAME not found.")
        return

    # Connect to the database
    engine = sqlalchemy.create_engine(db_url)
    connection = engine.connect()

    try:
        # Check if the table exists
        if engine.dialect.has_table(connection, table_name):
            print(f"Table '{table_name}' exists in the database.")
        else:
            print(f"Table '{table_name}' does not exist. Creating from CSV...")
            create_table_from_csv(engine, table_name, csv_file_name)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        connection.close()

def create_table_from_csv(engine, table_name, csv_file_name):
    # Load CSV into a Pandas DataFrame
    csv_path = os.path.join("data", csv_file_name)
    if not os.path.exists(csv_path):
        print(f"CSV file '{csv_path}' not found.")
        return

    df = pd.read_csv(csv_path)
    print(f"Loaded CSV file with columns: {df.columns.tolist()}")

    # Generate a SQL CREATE TABLE statement (automatically handled by Pandas + SQLAlchemy)
    try:
        # Write DataFrame to SQL table
        df.to_sql(table_name, engine, if_exists="fail", index=False)
        print(f"Table '{table_name}' created successfully.")
    except ValueError as e:
        print(f"Table creation failed: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")


# Call the function when the script is executed
if __name__ == "__main__":
    create_directories_and_certificates()
    check_and_create_table()
