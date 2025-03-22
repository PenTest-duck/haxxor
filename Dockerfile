FROM kalilinux/kali-rolling

# Update
RUN apt -y update && DEBIAN_FRONTEND=noninteractive apt -y dist-upgrade && apt -y autoremove && apt clean

# Install common and useful tools
RUN apt install -y --no-install-recommends \
    openvpn iputils-ping \
    curl ca-certificates wget net-tools whois netcat-traditional

# Install useful languages
RUN apt -y install python3-pip

# Set up uv
RUN curl -LsSf https://astral.sh/uv/0.6.9/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Install Python dependencies
ADD pyproject.toml /pyproject.toml
ADD uv.lock /uv.lock
RUN uv sync --frozen && rm /pyproject.toml /uv.lock

# Install Kali Linux "Top 10" metapackage and a few cybersecurity useful tools
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends \
    kali-tools-top10 exploitdb man-db dirb nikto wpscan uniscan lsof apktool dex2jar ltrace strace binwalk \
    wordlists \
    wapiti gobuster dirbuster sqlninja \
    smbclient enum4linux smbmap nbtscan crackmapexec evil-winrm

# kali-linux-headless

WORKDIR /app
