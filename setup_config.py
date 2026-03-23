#!/usr/bin/env python3
"""First-time setup wizard for viewserver-python-example.

Run once after cloning to generate a config.json tailored to your machine.
"""

import json
import os
import platform
import socket
import sys

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULTS = {
    "service_name": platform.node(),
    "service_hostname": socket.gethostbyname(socket.gethostname()),
    "grpc_port": 19000,
    "http_port": 19001,
    "log_level": "Info",
}

ENVIRONMENTS = [
    {"name": "EXP",   "hostname": "192.168.171.174", "grpc_port": 6080, "http_port": 6081},
    {"name": "UAT",   "hostname": "192.168.4.104",   "grpc_port": 6080, "http_port": 6081},
    {"name": "STAGE", "hostname": "192.168.4.131",   "grpc_port": 6080, "http_port": 6081},
]
DEFAULT_ENV = 0  # EXP


def prompt(label: str, default):
    """Prompt user for a value, showing the default."""
    suffix = f" [{default}]: "
    try:
        value = input(f"  {label}{suffix}").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(1)
    return type(default)(value) if value else default


def main():
    print()
    print("=" * 60)
    print("  ViewServer Python Node - First-Time Setup")
    print("=" * 60)
    print()

    # --- Service config ---
    print("Service Configuration")
    print("-" * 40)
    service_name = prompt("Node name", DEFAULTS["service_name"])
    service_hostname = prompt("Hostname / IP", DEFAULTS["service_hostname"])
    grpc_port = prompt("gRPC port", DEFAULTS["grpc_port"])
    http_port = prompt("HTTP port", DEFAULTS["http_port"])
    print()

    # --- Report engine environment ---
    print("Report Engine Environment")
    print("-" * 40)
    for i, env in enumerate(ENVIRONMENTS):
        default_marker = " (default)" if i == DEFAULT_ENV else ""
        print(f"  {i + 1}) {env['name']:6s}  {env['hostname']}:{env['grpc_port']}{default_marker}")
    print()
    choice = prompt("Select environment", DEFAULT_ENV + 1)
    try:
        env_index = int(choice) - 1
        if not 0 <= env_index < len(ENVIRONMENTS):
            raise ValueError
    except (ValueError, TypeError):
        print(f"  Invalid choice, using default ({ENVIRONMENTS[DEFAULT_ENV]['name']})")
        env_index = DEFAULT_ENV
    selected_env = ENVIRONMENTS[env_index]
    re_hostname = selected_env["hostname"]
    re_grpc_port = selected_env["grpc_port"]
    re_http_port = selected_env["http_port"]
    print(f"  -> {selected_env['name']} ({re_hostname}:{re_grpc_port})")
    print()

    # --- Misc ---
    print("General")
    print("-" * 40)
    log_level = prompt("Log level (Trace/Debug/Info/Warn/Error)", DEFAULTS["log_level"])
    print()

    config = {
        "serviceConfig": {
            "name": service_name,
            "hostName": service_hostname,
            "grpcPort": grpc_port,
            "httpPort": http_port,
            "httpContentRoot": "",
            "isSecure": False,
            "expressionUsername": "",
            "expressionPassword": "",
        },
        "reportEngineConfig": {
            "name": "ReportingEngine",
            "hostName": re_hostname,
            "grpcPort": re_grpc_port,
            "httpPort": re_http_port,
            "httpContentRoot": None,
            "isSecure": False,
            "expressionUsername": "",
            "expressionPassword": "",
        },
        "sqlServerPersistenceConfigs": [],
        "parquetPersistenceConfigs": [],
        "jsonPersistenceConfigs": [],
        "gitHubPersistenceConfigs": [],
        "persistenceStrategyAliases": {},
        "expressionReleaseTag": "",
        "isReportEngine": False,
        "logLevel": log_level,
        "fakeData": False,
    }

    # --- Summary ---
    print("=" * 60)
    print("  Configuration Summary")
    print("=" * 60)
    print(f"  Node name:              {service_name}")
    print(f"  Hostname:               {service_hostname}")
    print(f"  gRPC port:              {grpc_port}")
    print(f"  HTTP port:              {http_port}")
    print(f"  Report engine:          {selected_env['name']} ({re_hostname}:{re_grpc_port})")
    print(f"  Log level:              {log_level}")
    print()

    confirm = input(f"  Write to {CONFIG_PATH}? [Y/n]: ").strip().lower()
    if confirm and confirm != "y":
        print("  Aborted.")
        sys.exit(0)

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    print(f"  Config written to {CONFIG_PATH}")
    print()


if __name__ == "__main__":
    main()
