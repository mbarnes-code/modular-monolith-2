"""
Health check and monitoring endpoints for HexStrike service.
"""
import time
from typing import Any, Dict

import psutil
from flask import jsonify


def get_health_info() -> Dict[str, Any]:
    """Get health information about the service."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime": time.time() - psutil.boot_time(),
        "version": "6.0.0",
        "service": "hexstrike-ai"
    }


def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "used": memory.used
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": (disk.used / disk.total) * 100
        },
        "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
    }


def health_endpoint():
    """Health check endpoint handler."""
    try:
        health_data = get_health_info()
        return jsonify(health_data), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }), 503


def metrics_endpoint():
    """Metrics endpoint handler."""
    try:
        health_data = get_health_info()
        system_data = get_system_info()

        return jsonify({
            **health_data,
            "system": system_data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }), 500
