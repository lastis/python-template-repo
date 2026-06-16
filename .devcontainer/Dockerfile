# Use a devcontainer image which comes with some pre-installed tools like git.
FROM mcr.microsoft.com/devcontainers/base:bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Switch to vscode user and install system tools in their environment
USER vscode
RUN uv tool install go-task-bin
