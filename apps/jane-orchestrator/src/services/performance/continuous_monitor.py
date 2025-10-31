"""
Continuous Performance Monitoring - T137
Constitutional threshold alerting and real-time monitoring
"""

import asyncio
import json
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import httpx


@dataclass
class PerformanceAlert:
    """Performance alert data structure"""
    id: str
    domain: str
    metric_type: str
    threshold: float
    actual_value: float
    severity: str  # 'critical', 'warning', 'info'
    message: str
    timestamp: float
    resolved: bool = False


@dataclass
class MonitoringConfig:
    """Performance monitoring configuration"""
    enabled: bool = True
    check_interval_seconds: int = 30
    alert_threshold_multiplier: float = 1.0
    max_alerts_per_domain: int = 10
    alert_cooldown_seconds: int = 300  # 5 minutes


class ConstitutionalPerformanceMonitor:
    """
    Continuous performance monitoring with constitutional compliance

    Monitors:
    - Domain-specific response times (Security <1s, Productivity <2s, etc.)
    - UI response times (<200ms for executive function support)
    - Error rates and availability
    - Constitutional threshold violations
    """

    # Constitutional thresholds
    DOMAIN_THRESHOLDS = {
        'security': 1000,       # <1s - threat analysis criticality
        'productivity': 2000,   # <2s - task management workflows
        'mtg': 3000,           # <3s - game analysis complexity
        'infrastructure': 5000  # <5s - system operations tolerance
    }

    UI_THRESHOLD_MS = 200  # <200ms for ADHD/autism accommodations
    ERROR_RATE_THRESHOLD = 0.05  # 5% max error rate

    def __init__(self, config: Optional[MonitoringConfig] = None,
                 base_url: str = "http://localhost:8000"):
        self.config = config or MonitoringConfig()
        self.base_url = base_url
        self.active_alerts: Dict[str, PerformanceAlert] = {}
        self.alert_history: List[PerformanceAlert] = []
        self.monitoring_data: Dict[str, List[float]] = {}
        self.last_check_time = time.time()

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("PerformanceMonitor")

        # Create monitoring data directory
        self.data_dir = Path("monitoring_data")
        self.data_dir.mkdir(exist_ok=True)

    async def start_monitoring(self):
        """Start continuous performance monitoring"""
        self.logger.info("🎯 Starting constitutional performance monitoring")
        self.logger.info(
            f"Check interval: {self.config.check_interval_seconds}s")

        while self.config.enabled:
            try:
                await self._perform_monitoring_cycle()
                await asyncio.sleep(self.config.check_interval_seconds)
            except KeyboardInterrupt:
                self.logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(self.config.check_interval_seconds)

    async def _perform_monitoring_cycle(self):
        """Perform one monitoring cycle"""
        cycle_start = time.time()

        # Test domain endpoints
        domain_results = await self._check_domain_performance()

        # Test UI endpoints
        ui_results = await self._check_ui_performance()

        # Process results and generate alerts
        await self._process_results(domain_results, ui_results)

        # Clean up old alerts
        self._cleanup_old_alerts()

        # Save monitoring data
        await self._save_monitoring_data()

        cycle_duration = time.time() - cycle_start
        self.logger.info(
            f"Monitoring cycle completed in {cycle_duration:.2f}s")

    async def _check_domain_performance(self) -> Dict[str, Dict]:
        """Check domain-specific performance"""
        results = {}

        # Define domain endpoints to monitor
        domain_endpoints = {
            'security': '/api/security/health',
            'productivity': '/api/productivity/health',
            'mtg': '/api/mtg/health',
            'infrastructure': '/api/infrastructure/health'
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            for domain, endpoint in domain_endpoints.items():
                try:
                    start_time = time.time()
                    response = await client.get(f"{self.base_url}{endpoint}")
                    response_time_ms = (time.time() - start_time) * 1000

                    results[domain] = {
                        'response_time_ms': response_time_ms,
                        'status_code': response.status_code,
                        'success': response.status_code == 200,
                        'threshold': self.DOMAIN_THRESHOLDS[domain]
                    }

                    # Store monitoring data
                    if domain not in self.monitoring_data:
                        self.monitoring_data[domain] = []
                    self.monitoring_data[domain].append(response_time_ms)

                    # Keep only recent data (last 100 measurements)
                    if len(self.monitoring_data[domain]) > 100:
                        self.monitoring_data[domain] = self.monitoring_data[domain][-100:]

                except Exception as e:
                    self.logger.warning(f"Failed to check {domain}: {e}")
                    results[domain] = {
                        'response_time_ms': float('inf'),
                        'status_code': 0,
                        'success': False,
                        'threshold': self.DOMAIN_THRESHOLDS[domain],
                        'error': str(e)
                    }

        return results

    async def _check_ui_performance(self) -> Dict[str, Dict]:
        """Check UI performance for executive function support"""
        results = {}

        ui_endpoints = ['/', '/api/health']

        async with httpx.AsyncClient(timeout=5.0) as client:
            for endpoint in ui_endpoints:
                try:
                    start_time = time.time()
                    response = await client.get(f"{self.base_url}{endpoint}")
                    response_time_ms = (time.time() - start_time) * 1000

                    results[endpoint] = {
                        'response_time_ms': response_time_ms,
                        'status_code': response.status_code,
                        'success': response.status_code == 200,
                        'threshold': self.UI_THRESHOLD_MS
                    }

                except Exception as e:
                    self.logger.warning(f"Failed to check UI {endpoint}: {e}")
                    results[endpoint] = {
                        'response_time_ms': float('inf'),
                        'status_code': 0,
                        'success': False,
                        'threshold': self.UI_THRESHOLD_MS,
                        'error': str(e)
                    }

        return results

    async def _process_results(self, domain_results: Dict, ui_results: Dict):
        """Process monitoring results and generate alerts"""
        current_time = time.time()

        # Process domain results
        for domain, result in domain_results.items():
            await self._check_domain_threshold(domain, result, current_time)

        # Process UI results
        for endpoint, result in ui_results.items():
            await self._check_ui_threshold(endpoint, result, current_time)

    async def _check_domain_threshold(self, domain: str, result: Dict,
                                      timestamp: float):
        """Check domain performance against constitutional thresholds"""
        response_time = result['response_time_ms']
        threshold = result['threshold']
        success = result['success']

        alert_id = f"domain_{domain}_{int(timestamp)}"

        # Critical: Response time exceeds threshold or service is down
        if not success or response_time > threshold:
            severity = 'critical' if not success else 'critical'
            message = (f"{domain.title()} domain performance critical: "
                       f"{response_time:.1f}ms > {threshold}ms threshold")

            if not success:
                message = f"{domain.title()} domain is unavailable"

            await self._create_alert(
                alert_id, domain, 'response_time', threshold,
                response_time, severity, message, timestamp
            )

        # Warning: Response time approaching threshold (80%)
        elif response_time > threshold * 0.8:
            severity = 'warning'
            message = (f"{domain.title()} domain performance warning: "
                       f"{response_time:.1f}ms approaching {threshold}ms threshold")

            await self._create_alert(
                alert_id, domain, 'response_time', threshold * 0.8,
                response_time, severity, message, timestamp
            )

        else:
            # Performance is good, resolve any existing alerts
            await self._resolve_domain_alerts(domain)

    async def _check_ui_threshold(self, endpoint: str, result: Dict,
                                  timestamp: float):
        """Check UI performance for executive function support"""
        response_time = result['response_time_ms']
        threshold = result['threshold']
        success = result['success']

        alert_id = f"ui_{endpoint.replace('/', '_')}_{int(timestamp)}"

        # Critical: UI response time exceeds 200ms (affects executive function)
        if not success or response_time > threshold:
            severity = 'critical'
            message = (f"UI executive function support critical: "
                       f"{endpoint} responded in {response_time:.1f}ms > "
                       f"{threshold}ms (ADHD/autism accommodation threshold)")

            if not success:
                message = f"UI endpoint {endpoint} is unavailable"

            await self._create_alert(
                alert_id, 'ui', 'response_time', threshold,
                response_time, severity, message, timestamp
            )

        # Warning: UI response time approaching threshold (80% of 200ms = 160ms)
        elif response_time > threshold * 0.8:
            severity = 'warning'
            message = (f"UI executive function support warning: "
                       f"{endpoint} responded in {response_time:.1f}ms "
                       f"approaching {threshold}ms threshold")

            await self._create_alert(
                alert_id, 'ui', 'response_time', threshold * 0.8,
                response_time, severity, message, timestamp
            )

    async def _create_alert(self, alert_id: str, domain: str, metric_type: str,
                            threshold: float, actual_value: float, severity: str,
                            message: str, timestamp: float):
        """Create or update performance alert"""

        # Check if we're in cooldown period for this domain
        recent_alerts = [a for a in self.alert_history
                         if a.domain == domain and
                         timestamp - a.timestamp < self.config.alert_cooldown_seconds]

        if len(recent_alerts) >= self.config.max_alerts_per_domain:
            return  # Skip alert due to cooldown

        alert = PerformanceAlert(
            id=alert_id,
            domain=domain,
            metric_type=metric_type,
            threshold=threshold,
            actual_value=actual_value,
            severity=severity,
            message=message,
            timestamp=timestamp
        )

        self.active_alerts[alert_id] = alert
        self.alert_history.append(alert)

        # Log alert
        log_level = logging.CRITICAL if severity == 'critical' else logging.WARNING
        self.logger.log(log_level, f"🚨 ALERT: {message}")

        # In a real implementation, this would:
        # - Send notifications (email, Slack, etc.)
        # - Update dashboard in real-time
        # - Trigger automated responses

    async def _resolve_domain_alerts(self, domain: str):
        """Resolve alerts for a domain that's now performing well"""
        resolved_count = 0

        for alert_id, alert in list(self.active_alerts.items()):
            if alert.domain == domain and not alert.resolved:
                alert.resolved = True
                resolved_count += 1
                self.logger.info(f"✅ Resolved alert: {alert.message}")

        if resolved_count > 0:
            # Remove resolved alerts from active list
            self.active_alerts = {
                aid: alert for aid, alert in self.active_alerts.items()
                if not alert.resolved
            }

    def _cleanup_old_alerts(self):
        """Clean up old alerts from history"""
        cutoff_time = time.time() - (24 * 3600)  # 24 hours
        self.alert_history = [
            alert for alert in self.alert_history
            if alert.timestamp > cutoff_time
        ]

    async def _save_monitoring_data(self):
        """Save monitoring data to disk"""
        timestamp = datetime.now().isoformat()

        # Save current monitoring snapshot
        snapshot = {
            'timestamp': timestamp,
            'active_alerts': [asdict(alert) for alert in self.active_alerts.values()],
            'monitoring_data': {
                domain: {
                    # Last 10 measurements
                    'recent_response_times': times[-10:],
                    'avg_response_time': sum(times) / len(times) if times else 0,
                    'threshold': self.DOMAIN_THRESHOLDS.get(domain, 0)
                }
                for domain, times in self.monitoring_data.items()
            },
            'constitutional_compliance': {
                'security_compliant': all(
                    t < self.DOMAIN_THRESHOLDS['security']
                    for t in self.monitoring_data.get('security', [])[-5:]
                ),
                'productivity_compliant': all(
                    t < self.DOMAIN_THRESHOLDS['productivity']
                    for t in self.monitoring_data.get('productivity', [])[-5:]
                ),
                'mtg_compliant': all(
                    t < self.DOMAIN_THRESHOLDS['mtg']
                    for t in self.monitoring_data.get('mtg', [])[-5:]
                ),
                'infrastructure_compliant': all(
                    t < self.DOMAIN_THRESHOLDS['infrastructure']
                    for t in self.monitoring_data.get('infrastructure', [])[-5:]
                )
            }
        }

        # Save to file
        snapshot_file = self.data_dir / \
            f"monitoring_snapshot_{int(time.time())}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)

        # Keep only recent snapshots (last 100)
        snapshot_files = sorted(
            self.data_dir.glob("monitoring_snapshot_*.json"))
        if len(snapshot_files) > 100:
            for old_file in snapshot_files[:-100]:
                old_file.unlink()

    def get_current_status(self) -> Dict:
        """Get current monitoring status"""
        return {
            'active_alerts_count': len(self.active_alerts),
            'critical_alerts': len([a for a in self.active_alerts.values()
                                    if a.severity == 'critical']),
            'warning_alerts': len([a for a in self.active_alerts.values()
                                   if a.severity == 'warning']),
            'domains_monitored': list(self.DOMAIN_THRESHOLDS.keys()),
            'ui_threshold_ms': self.UI_THRESHOLD_MS,
            'last_check': datetime.fromtimestamp(self.last_check_time).isoformat(),
            'monitoring_enabled': self.config.enabled
        }


async def main():
    """Main monitoring function"""
    print("🎯 Constitutional Performance Monitoring")
    print("Starting continuous monitoring with threshold alerting...")

    # Configure monitoring
    config = MonitoringConfig(
        enabled=True,
        check_interval_seconds=30,  # Check every 30 seconds
        alert_threshold_multiplier=1.0,
        max_alerts_per_domain=5,
        alert_cooldown_seconds=300  # 5 minute cooldown
    )

    # Start monitor
    monitor = ConstitutionalPerformanceMonitor(config)

    try:
        await monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")
        status = monitor.get_current_status()
        print(f"Final status: {status}")


if __name__ == "__main__":
    asyncio.run(main())
