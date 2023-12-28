# Local Contexts Hub DB Backup

---

How it works
- A Docker image is built using the instructions within the Dockerfile
  - The image is pushed to a Docker registry
- A scheduled job runs and does the following:
  - Pulls the image from the Docker registry
  - Builds a Docker container using the prebuilt image
  - Executes the entrypoint of the container which runs the db backup logic
  
---
