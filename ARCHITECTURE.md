# Architecture Overview

## High-level Summary
This service is a small, event-driven Todo Backend built to demonstrate a practical architecture that combines an HTTP API, JWT authentication, event streaming via Kafka (Redpanda), and optional runtime abstraction through Dapr.

Client → FastAPI (Auth) → Business Logic → Kafka (publish events)

Key components:
- FastAPI app: Exposes REST endpoints for todos and authentication
- Auth layer: JWT-based, stateless tokens protect todo endpoints
- Kafka (Redpanda): Durable event streaming for created/updated/deleted todos
- Dapr (optional): Pub/sub abstraction to decouple producers and consumers across runtimes
- Simple in-memory store (demo): `todos_db` used for demonstration; replace with a real DB in production

## ASCII Diagram

Client (browser/CLI)
  |
  | HTTP (Bearer JWT)
  v
FastAPI (app/main.py)
  ├─ Auth (`/auth/login`) — issues JWT
  ├─ API (`/todos`) — CRUD handlers
  └─ KafkaService -> Kafka Topic `todos`
          |
          v
      Kafka (Redpanda)
          |
          +--> Consumer A (analytics / event-processor)
          +--> Consumer B (email/notifications)
          +--> Dapr subscribers (if Dapr configured)

## Request Flow (Create todo)
1. Client calls `POST /auth/login?username&password` → receives JWT
2. Client calls `POST /todos` with `Authorization: Bearer <token>`
3. FastAPI `create_todo` endpoint validates token and creates a Todo in memory (or DB)
4. `KafkaService.publish_message()` queues a JSON event to topic `todos` (event: `todo_created`)
5. One or more consumers process that event asynchronously (analytics, other microservices)

## Role of Dapr
- Dapr provides a portable pub/sub layer: if enabled, you can configure Dapr components (e.g., Kafka) and subscribe to topics without tightly coupling services.
- With Dapr, consumers can subscribe to topics using Dapr runtime endpoints, and the application code can remain unchanged (Dapr handles delivery).
- This project includes a sample `dapr` component configuration; running with `dapr run` enables the sidecar for local development.

## Why event-driven here?
- Decouples producers (API) from consumers (analytics, notifications)
- Improves resilience: temporary consumer downtime does not block the API
- Enables horizontal scaling of consumers independently from the API

## Scalability & Reliability Notes
- API: run multiple Uvicorn workers or behind an ASGI server/load balancer
- Kafka: scale partitions and consumers to increase throughput
- Use a real database (Postgres, etc.) for persistence and partitioning/sharding strategies if needed
- Add retries, DLQ (dead-letter queue), and backoff logic for consumers
- Use health checks and monitoring (Prometheus/Grafana). Add tracing (OpenTelemetry) for end-to-end observability

## Deployment Considerations
- Containerize the app and run via Docker Compose or Kubernetes
- Use managed Kafka for production (Confluent Cloud, Amazon MSK, or Redpanda managed)
- Secure secrets (JWT secret) with environment variables or a secrets store
- Use TLS for Kafka and HTTPS for API endpoints

## Extending the Design
- Replace in-memory store with PostgreSQL and add migrations
- Implement user management + password reset flows
- Add event versioning and schema registry for Kafka messages
- Add retries and idempotency when processing events

---

This document provides a concise view of how data and control flow through the system and why the chosen patterns (JWT, event-driven, Dapr) were selected.