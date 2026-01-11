# Multi-Source Market Analytics



## Overview

This repository contains an end-to-end **financial data analytics platform** designed to ingest, process, and analyze market data from multiple heterogeneous sources.
The system combines **real-time streaming data** with **historical, fundamental, and macroeconomic datasets** to generate analytical insights that are not available from any single source in isolation.

The platform is built around modern **Big Data and data engineering technologies**, with a strong focus on scalability, fault tolerance, and analytical flexibility.


## Project Goals

The main objectives of this project are to:

* Build a hybrid data processing architecture capable of handling both **streaming** and **batch** workloads
* Integrate **real-time market trades** with slowly changing reference data
* Generate **enriched analytical datasets** for quantitative analysis, monitoring, and decision support
* Demonstrate practical analytical use cases such as **real-time indicators**, **anomaly detection**, and **macroeconomic impact analysis**



## Data Sources

The platform integrates multiple external data providers:

### Real-Time Streaming Data

* Live trades and price updates for equities and cryptocurrencies via WebSocket APIs

### Batch Data Sources

* Historical OHLCV price data
* Company fundamental data (financial statements, valuation metrics)
* Macroeconomic indicators (GDP, CPI, interest rates, commodities)

Each data source differs in update frequency, structure, and latency, making **data normalization and enrichment** a core challenge of the system.



## Architecture Overview

The system follows a **layered architecture**:

### 1. Data Ingestion

* Real-time data is ingested via WebSocket connections and published to **Apache Kafka**
* Batch data is fetched periodically using scheduled workflows

### 2. Storage Layer

* **Data Lake (HDFS)** for raw and historical datasets
* **Apache Hive** for structured analytical access using SQL
* **NoSQL storage** for low-latency access to the most recent data

### 3. Processing and Analytics

**Apache Spark** is used for:

* Batch analytics
* Stream enrichment
* Aggregations, joins, and anomaly detection
* Creation of analytical tables ready for BI tools or downstream models



## Example Analytical Use Cases

The platform enables several advanced analytical scenarios, including:

### Real-Time Valuation Metrics

Continuous recalculation of indicators such as **P/E** or **P/B ratios** using live trade prices combined with fundamental data.

### Crypto Volume Anomaly Detection

Detection of abnormal trading activity by comparing real-time volume aggregates with historical baselines.

### Macroeconomic Event Impact Analysis

Measuring the effect of macroeconomic data releases on asset prices and trading volume across different asset classes.



## Technologies Used

* Apache Kafka
* Apache NiFi
* Apache Hadoop (HDFS)
* Apache Hive
* Apache Spark (SQL / PySpark)
* HBase
* Python



## Intended Use

This project can serve as:

* A foundation for **market analytics platforms**
* A backend for **real-time dashboards**
* A data source for **quantitative models and research**
* A reference architecture for **hybrid stream–batch data processing systems**


