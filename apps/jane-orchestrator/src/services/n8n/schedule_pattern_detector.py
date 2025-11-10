"""Scheduling Pattern Recognition for n8n Workflow Automation.

This module identifies temporal patterns in user workflows to enable
automated scheduling through n8n Cron triggers, Schedule nodes, and
time-based workflow automation.
"""

import calendar
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class ScheduleType(Enum):
    """Types of scheduling patterns that can be detected."""
    FIXED_INTERVAL = "fixed_interval"  # Every N minutes/hours/days
    DAILY_RECURRING = "daily_recurring"  # Same time each day
    WEEKLY_RECURRING = "weekly_recurring"  # Same day(s) each week
    MONTHLY_RECURRING = "monthly_recurring"  # Same date(s) each month
    BUSINESS_HOURS = "business_hours"  # During work hours only
    EVENT_TRIGGERED = "event_triggered"  # Based on external events
    CONDITIONAL_SCHEDULE = "conditional_schedule"  # Schedule with conditions
    BATCH_PROCESSING = "batch_processing"  # Process accumulated data
    DEADLINE_DRIVEN = "deadline_driven"  # Before specific deadlines
    SEASONAL_PATTERN = "seasonal_pattern"  # Seasonal/quarterly patterns


class TimeGranularity(Enum):
    """Time granularity for scheduling patterns."""
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class ScheduleTrigger(Enum):
    """Types of triggers that can initiate scheduled workflows."""
    CRON_EXPRESSION = "cron_expression"
    INTERVAL_TIMER = "interval_timer"
    WEBHOOK_EVENT = "webhook_event"
    FILE_SYSTEM_WATCH = "file_system_watch"
    DATABASE_CHANGE = "database_change"
    EMAIL_ARRIVAL = "email_arrival"
    API_POLL = "api_poll"
    TIME_WINDOW = "time_window"


@dataclass
class SchedulePattern:
    """Represents a detected scheduling pattern."""
    pattern_id: str
    pattern_name: str
    schedule_type: ScheduleType
    granularity: TimeGranularity
    frequency: int  # How often this pattern occurs
    cron_expression: str  # Generated cron expression
    time_windows: List[Tuple[time, time]]  # Active time windows
    days_of_week: Set[int]  # 0=Monday, 6=Sunday
    days_of_month: Set[int]  # 1-31
    excluded_dates: Set[datetime]  # Holidays, exceptions
    trigger_type: ScheduleTrigger
    confidence: float  # Confidence in pattern detection
    automation_potential: float  # Suitability for automation


@dataclass
class ScheduledAction:
    """Represents an action that follows a schedule pattern."""
    action_id: str
    user_id: str
    action_description: str
    tools_involved: Set[str]
    average_duration_minutes: float
    success_rate: float
    data_volume_pattern: Dict[str, Any]  # Volume patterns over time
    dependencies: List[str]  # Other scheduled actions this depends on
    resource_requirements: Dict[str, Any]  # CPU, memory, network needs


@dataclass
class TemporalWorkflow:
    """Represents a complete temporal workflow pattern."""
    workflow_id: str
    workflow_name: str
    schedule_pattern: SchedulePattern
    scheduled_actions: List[ScheduledAction]
    workflow_description: str
    estimated_runtime_minutes: float
    resource_conflicts: List[str]  # Potential scheduling conflicts
    optimization_opportunities: List[Dict[str, Any]]
    historical_performance: Dict[str, Any]


@dataclass
class UserActivity:
    """Represents a user activity with timing information."""
    activity_id: str
    user_id: str
    timestamp: datetime
    action_type: str
    tool_used: str
    duration_minutes: float
    data_processed: int  # Volume of data
    success: bool
    context_tags: List[str]
    session_id: Optional[str]  # Groups related activities


class SchedulePatternDetector:
    """Detects temporal patterns in user activities for automation."""

    def __init__(self):
        self.activity_history = []
        self.business_hours = (time(9, 0), time(17, 0))  # 9 AM - 5 PM
        self.business_days = {0, 1, 2, 3, 4}  # Monday-Friday
        self.holiday_dates = set()  # Can be populated with known holidays
        self.min_pattern_occurrences = 3  # Minimum for pattern detection

    def record_activity(
        self,
        user_id: str,
        action_type: str,
        tool_used: str,
        duration_minutes: float = 1.0,
        data_processed: int = 1,
        success: bool = True,
        context_tags: Optional[List[str]] = None,
        session_id: Optional[str] = None
    ) -> UserActivity:
        """Record a user activity for schedule analysis."""

        activity = UserActivity(
            activity_id=f"{user_id}_{datetime.utcnow().isoformat()}",
            user_id=user_id,
            timestamp=datetime.utcnow(),
            action_type=action_type,
            tool_used=tool_used,
            duration_minutes=duration_minutes,
            data_processed=data_processed,
            success=success,
            context_tags=context_tags or [],
            session_id=session_id
        )

        self.activity_history.append(activity)
        return activity

    def analyze_temporal_patterns(
        self, user_id: str, time_window: timedelta = timedelta(days=30)
    ) -> List[SchedulePattern]:
        """Analyze user activities to identify scheduling patterns."""

        # Filter activities for user and time window
        cutoff_time = datetime.utcnow() - time_window
        user_activities = [
            activity for activity in self.activity_history
            if (activity.user_id == user_id and
                activity.timestamp >= cutoff_time)
        ]

        if len(user_activities) < self.min_pattern_occurrences:
            return []

        # Sort by timestamp
        user_activities.sort(key=lambda x: x.timestamp)

        patterns = []

        # Detect different types of patterns
        patterns.extend(self._detect_fixed_interval_patterns(user_activities))
        patterns.extend(self._detect_daily_recurring_patterns(user_activities))
        patterns.extend(
            self._detect_weekly_recurring_patterns(user_activities))
        patterns.extend(
            self._detect_monthly_recurring_patterns(user_activities))
        patterns.extend(self._detect_business_hour_patterns(user_activities))
        patterns.extend(
            self._detect_batch_processing_patterns(user_activities))

        # Sort by confidence and automation potential
        patterns.sort(
            key=lambda p: (p.confidence, p.automation_potential),
            reverse=True
        )

        return patterns

    def detect_scheduled_workflows(
        self, patterns: List[SchedulePattern], user_id: str
    ) -> List[TemporalWorkflow]:
        """Detect complete scheduled workflows from patterns."""

        workflows = []

        # Group patterns by similarity and timing
        pattern_groups = self._group_related_patterns(patterns)

        for group in pattern_groups:
            workflow = self._create_temporal_workflow(group, user_id)
            if workflow and self._is_viable_workflow(workflow):
                workflows.append(workflow)

        return workflows

    def analyze_activity_distribution(
        self, user_id: str, time_window: timedelta = timedelta(days=30)
    ) -> Dict[str, Any]:
        """Analyze how user activities are distributed over time."""

        cutoff_time = datetime.utcnow() - time_window
        user_activities = [
            activity for activity in self.activity_history
            if (activity.user_id == user_id and
                activity.timestamp >= cutoff_time)
        ]

        if not user_activities:
            return {}

        # Analyze time-based distributions
        hourly_distribution = self._analyze_hourly_distribution(
            user_activities)
        daily_distribution = self._analyze_daily_distribution(user_activities)
        weekly_distribution = self._analyze_weekly_distribution(
            user_activities)

        # Analyze activity patterns
        peak_hours = self._identify_peak_activity_hours(user_activities)
        quiet_periods = self._identify_quiet_periods(user_activities)

        # Analyze tool usage patterns
        tool_timing_patterns = self._analyze_tool_timing_patterns(
            user_activities)

        return {
            'total_activities': len(user_activities),
            'time_span_days': (user_activities[-1].timestamp -
                               user_activities[0].timestamp).days,
            'hourly_distribution': hourly_distribution,
            'daily_distribution': daily_distribution,
            'weekly_distribution': weekly_distribution,
            'peak_activity_hours': peak_hours,
            'quiet_periods': quiet_periods,
            'tool_timing_patterns': tool_timing_patterns,
            'business_hours_ratio': self._calculate_business_hours_ratio(
                user_activities
            )
        }

    def generate_cron_expressions(
        self, pattern: SchedulePattern
    ) -> List[str]:
        """Generate cron expressions for a schedule pattern."""

        expressions = []

        if pattern.schedule_type == ScheduleType.FIXED_INTERVAL:
            expressions.extend(self._generate_interval_cron(pattern))
        elif pattern.schedule_type == ScheduleType.DAILY_RECURRING:
            expressions.extend(self._generate_daily_cron(pattern))
        elif pattern.schedule_type == ScheduleType.WEEKLY_RECURRING:
            expressions.extend(self._generate_weekly_cron(pattern))
        elif pattern.schedule_type == ScheduleType.MONTHLY_RECURRING:
            expressions.extend(self._generate_monthly_cron(pattern))
        elif pattern.schedule_type == ScheduleType.BUSINESS_HOURS:
            expressions.extend(self._generate_business_hours_cron(pattern))
        elif pattern.schedule_type == ScheduleType.BATCH_PROCESSING:
            expressions.extend(self._generate_batch_cron(pattern))

        return expressions

    def suggest_schedule_optimizations(
        self, workflows: List[TemporalWorkflow]
    ) -> List[Dict[str, Any]]:
        """Suggest optimizations for scheduled workflows."""

        optimizations = []

        # Detect resource conflicts
        conflicts = self._detect_scheduling_conflicts(workflows)
        if conflicts:
            optimizations.extend(conflicts)

        # Suggest load balancing
        load_balancing = self._suggest_load_balancing(workflows)
        if load_balancing:
            optimizations.extend(load_balancing)

        # Suggest batch consolidation
        batch_opportunities = self._identify_batch_opportunities(workflows)
        if batch_opportunities:
            optimizations.extend(batch_opportunities)

        # Suggest off-peak scheduling
        off_peak_opportunities = self._suggest_off_peak_scheduling(workflows)
        if off_peak_opportunities:
            optimizations.extend(off_peak_opportunities)

        return optimizations

    def generate_n8n_schedule_nodes(
        self, workflow: TemporalWorkflow
    ) -> List[Dict[str, Any]]:
        """Generate n8n scheduling nodes for a temporal workflow."""

        nodes = []
        pattern = workflow.schedule_pattern

        # Create trigger node based on schedule type
        if pattern.trigger_type == ScheduleTrigger.CRON_EXPRESSION:
            trigger_node = self._create_cron_trigger_node(pattern)
        elif pattern.trigger_type == ScheduleTrigger.INTERVAL_TIMER:
            trigger_node = self._create_interval_trigger_node(pattern)
        elif pattern.trigger_type == ScheduleTrigger.WEBHOOK_EVENT:
            trigger_node = self._create_webhook_trigger_node(pattern)
        else:
            trigger_node = self._create_manual_trigger_node(pattern)

        if trigger_node:
            nodes.append(trigger_node)

        # Create condition nodes for time windows
        if pattern.time_windows:
            condition_node = self._create_time_window_condition_node(pattern)
            if condition_node:
                nodes.append(condition_node)

        return nodes

    # Private helper methods for pattern detection

    def _detect_fixed_interval_patterns(
        self, activities: List[UserActivity]
    ) -> List[SchedulePattern]:
        """Detect fixed interval patterns (every N minutes/hours/days)."""

        patterns = []

        # Group activities by action type and tool
        activity_groups = defaultdict(list)
        for activity in activities:
            key = f"{activity.action_type}_{activity.tool_used}"
            activity_groups[key].append(activity)

        for group_key, group_activities in activity_groups.items():
            if len(group_activities) < self.min_pattern_occurrences:
                continue

            # Calculate intervals between activities
            intervals = []
            for i in range(1, len(group_activities)):
                interval = (group_activities[i].timestamp -
                            group_activities[i-1].timestamp)
                intervals.append(interval.total_seconds())

            if not intervals:
                continue

            # Check for consistent intervals
            avg_interval = sum(intervals) / len(intervals)
            interval_variance = sum(
                (interval - avg_interval) ** 2 for interval in intervals
            ) / len(intervals)

            # If variance is low, we have a fixed interval pattern
            if interval_variance < (avg_interval * 0.2) ** 2:  # 20% tolerance
                granularity = self._determine_interval_granularity(
                    avg_interval)
                cron_expr = self._generate_interval_cron_expression(
                    avg_interval, granularity
                )

                pattern = SchedulePattern(
                    pattern_id=f"interval_{group_key}_{int(avg_interval)}",
                    pattern_name=f"Fixed interval: {group_key} every {self._format_interval(avg_interval)}",
                    schedule_type=ScheduleType.FIXED_INTERVAL,
                    granularity=granularity,
                    frequency=len(group_activities),
                    cron_expression=cron_expr,
                    time_windows=[],
                    days_of_week=set(),
                    days_of_month=set(),
                    excluded_dates=set(),
                    trigger_type=ScheduleTrigger.CRON_EXPRESSION,
                    confidence=self._calculate_interval_confidence(
                        intervals, avg_interval
                    ),
                    automation_potential=self._assess_interval_automation_potential(
                        group_activities
                    )
                )
                patterns.append(pattern)

        return patterns

    def _detect_daily_recurring_patterns(
        self, activities: List[UserActivity]
    ) -> List[SchedulePattern]:
        """Detect daily recurring patterns (same time each day)."""

        patterns = []

        # Group activities by action type and tool
        activity_groups = defaultdict(list)
        for activity in activities:
            key = f"{activity.action_type}_{activity.tool_used}"
            activity_groups[key].append(activity)

        for group_key, group_activities in activity_groups.items():
            if len(group_activities) < self.min_pattern_occurrences:
                continue

            # Group by time of day (within 30-minute windows)
            time_groups = defaultdict(list)
            for activity in group_activities:
                # Round to nearest 30-minute window
                minute_window = (activity.timestamp.hour * 60 +
                                 activity.timestamp.minute) // 30 * 30
                hour = minute_window // 60
                minute = minute_window % 60
                time_key = f"{hour:02d}:{minute:02d}"
                time_groups[time_key].append(activity)

            # Find time windows with sufficient frequency
            for time_key, time_activities in time_groups.items():
                if len(time_activities) >= self.min_pattern_occurrences:
                    # Check if activities span multiple days
                    dates = set(activity.timestamp.date()
                                for activity in time_activities)

                    if len(dates) >= self.min_pattern_occurrences:
                        hour, minute = map(int, time_key.split(':'))
                        cron_expr = f"{minute} {hour} * * *"

                        pattern = SchedulePattern(
                            pattern_id=f"daily_{group_key}_{time_key}",
                            pattern_name=f"Daily: {group_key} at {time_key}",
                            schedule_type=ScheduleType.DAILY_RECURRING,
                            granularity=TimeGranularity.DAY,
                            frequency=len(time_activities),
                            cron_expression=cron_expr,
                            time_windows=[(time(hour, minute),
                                           time(hour, minute + 30))],
                            days_of_week=set(),
                            days_of_month=set(),
                            excluded_dates=set(),
                            trigger_type=ScheduleTrigger.CRON_EXPRESSION,
                            confidence=self._calculate_daily_confidence(
                                time_activities, dates
                            ),
                            automation_potential=self._assess_daily_automation_potential(
                                time_activities
                            )
                        )
                        patterns.append(pattern)

        return patterns

    def _detect_weekly_recurring_patterns(
        self, activities: List[UserActivity]
    ) -> List[SchedulePattern]:
        """Detect weekly recurring patterns (same day(s) each week)."""

        patterns = []

        activity_groups = defaultdict(list)
        for activity in activities:
            key = f"{activity.action_type}_{activity.tool_used}"
            activity_groups[key].append(activity)

        for group_key, group_activities in activity_groups.items():
            if len(group_activities) < self.min_pattern_occurrences:
                continue

            # Group by day of week and time
            day_time_groups = defaultdict(list)
            for activity in group_activities:
                day_of_week = activity.timestamp.weekday()  # 0=Monday
                hour = activity.timestamp.hour
                minute = activity.timestamp.minute // 30 * 30  # 30-min windows
                key = f"{day_of_week}_{hour:02d}:{minute:02d}"
                day_time_groups[key].append(activity)

            # Find patterns with sufficient frequency
            for key, day_time_activities in day_time_groups.items():
                if len(day_time_activities) >= self.min_pattern_occurrences:
                    # Check if activities span multiple weeks
                    weeks = set(
                        activity.timestamp.isocalendar()[1]  # Week number
                        for activity in day_time_activities
                    )

                    if len(weeks) >= 2:  # At least 2 weeks
                        day_str, time_str = key.split('_')
                        day_of_week = int(day_str)
                        hour, minute = map(int, time_str.split(':'))

                        # Convert to cron day format (0=Sunday)
                        cron_day = (day_of_week + 1) % 7
                        cron_expr = f"{minute} {hour} * * {cron_day}"

                        pattern = SchedulePattern(
                            pattern_id=f"weekly_{group_key}_{key}",
                            pattern_name=f"Weekly: {group_key} on {calendar.day_name[day_of_week]} at {time_str}",
                            schedule_type=ScheduleType.WEEKLY_RECURRING,
                            granularity=TimeGranularity.WEEK,
                            frequency=len(day_time_activities),
                            cron_expression=cron_expr,
                            time_windows=[(time(hour, minute),
                                           time(hour, minute + 30))],
                            days_of_week={day_of_week},
                            days_of_month=set(),
                            excluded_dates=set(),
                            trigger_type=ScheduleTrigger.CRON_EXPRESSION,
                            confidence=self._calculate_weekly_confidence(
                                day_time_activities, weeks
                            ),
                            automation_potential=self._assess_weekly_automation_potential(
                                day_time_activities
                            )
                        )
                        patterns.append(pattern)

        return patterns

    def _detect_monthly_recurring_patterns(
        self, activities: List[UserActivity]
    ) -> List[SchedulePattern]:
        """Detect monthly recurring patterns."""

        patterns = []

        activity_groups = defaultdict(list)
        for activity in activities:
            key = f"{activity.action_type}_{activity.tool_used}"
            activity_groups[key].append(activity)

        for group_key, group_activities in activity_groups.items():
            if len(group_activities) < self.min_pattern_occurrences:
                continue

            # Group by day of month and time
            day_time_groups = defaultdict(list)
            for activity in group_activities:
                day_of_month = activity.timestamp.day
                hour = activity.timestamp.hour
                minute = activity.timestamp.minute // 30 * 30
                key = f"{day_of_month}_{hour:02d}:{minute:02d}"
                day_time_groups[key].append(activity)

            # Find patterns with sufficient frequency
            for key, day_time_activities in day_time_groups.items():
                if len(day_time_activities) >= self.min_pattern_occurrences:
                    # Check if activities span multiple months
                    months = set(
                        (activity.timestamp.year, activity.timestamp.month)
                        for activity in day_time_activities
                    )

                    if len(months) >= 2:  # At least 2 months
                        day_str, time_str = key.split('_')
                        day_of_month = int(day_str)
                        hour, minute = map(int, time_str.split(':'))

                        cron_expr = f"{minute} {hour} {day_of_month} * *"

                        pattern = SchedulePattern(
                            pattern_id=f"monthly_{group_key}_{key}",
                            pattern_name=f"Monthly: {group_key} on day {day_of_month} at {time_str}",
                            schedule_type=ScheduleType.MONTHLY_RECURRING,
                            granularity=TimeGranularity.MONTH,
                            frequency=len(day_time_activities),
                            cron_expression=cron_expr,
                            time_windows=[(time(hour, minute),
                                           time(hour, minute + 30))],
                            days_of_week=set(),
                            days_of_month={day_of_month},
                            excluded_dates=set(),
                            trigger_type=ScheduleTrigger.CRON_EXPRESSION,
                            confidence=self._calculate_monthly_confidence(
                                day_time_activities, months
                            ),
                            automation_potential=self._assess_monthly_automation_potential(
                                day_time_activities
                            )
                        )
                        patterns.append(pattern)

        return patterns

    def _detect_business_hour_patterns(
        self, activities: List[UserActivity]
    ) -> List[SchedulePattern]:
        """Detect patterns that occur during business hours."""

        patterns = []

        # Filter activities to business hours and days
        business_activities = []
        for activity in activities:
            is_business_day = activity.timestamp.weekday() in self.business_days
            is_business_hour = (
                self.business_hours[0] <= activity.timestamp.time() <=
                self.business_hours[1]
            )

            if is_business_day and is_business_hour:
                business_activities.append(activity)

        if len(business_activities) < self.min_pattern_occurrences:
            return patterns

        # Calculate business hours ratio
        total_activities = len(activities)
        business_ratio = len(business_activities) / total_activities

        # If most activities happen during business hours, create pattern
        if business_ratio >= 0.8:  # 80% during business hours
            activity_groups = defaultdict(list)
            for activity in business_activities:
                key = f"{activity.action_type}_{activity.tool_used}"
                activity_groups[key].append(activity)

            for group_key, group_activities in activity_groups.items():
                if len(group_activities) >= self.min_pattern_occurrences:
                    start_hour = self.business_hours[0].hour
                    end_hour = self.business_hours[1].hour

                    # Create hourly triggers during business hours
                    cron_expr = f"0 {start_hour}-{end_hour} * * 1-5"

                    pattern = SchedulePattern(
                        pattern_id=f"business_{group_key}",
                        pattern_name=f"Business hours: {group_key}",
                        schedule_type=ScheduleType.BUSINESS_HOURS,
                        granularity=TimeGranularity.HOUR,
                        frequency=len(group_activities),
                        cron_expression=cron_expr,
                        time_windows=[(self.business_hours[0],
                                       self.business_hours[1])],
                        days_of_week=self.business_days,
                        days_of_month=set(),
                        excluded_dates=self.holiday_dates.copy(),
                        trigger_type=ScheduleTrigger.CRON_EXPRESSION,
                        confidence=business_ratio,
                        automation_potential=self._assess_business_hours_automation_potential(
                            group_activities
                        )
                    )
                    patterns.append(pattern)

        return patterns

    def _detect_batch_processing_patterns(
        self, activities: List[UserActivity]
    ) -> List[SchedulePattern]:
        """Detect batch processing patterns (accumulate then process)."""

        patterns = []

        # Look for activities that process large amounts of data
        batch_activities = [
            activity for activity in activities
            if activity.data_processed > 10  # Threshold for batch processing
        ]

        if len(batch_activities) < self.min_pattern_occurrences:
            return patterns

        activity_groups = defaultdict(list)
        for activity in batch_activities:
            key = f"{activity.action_type}_{activity.tool_used}"
            activity_groups[key].append(activity)

        for group_key, group_activities in activity_groups.items():
            if len(group_activities) < self.min_pattern_occurrences:
                continue

            # Analyze data volume patterns
            avg_data_volume = sum(
                a.data_processed for a in group_activities
            ) / len(group_activities)

            # Check if activities happen at low-traffic times
            off_peak_activities = [
                activity for activity in group_activities
                if self._is_off_peak_time(activity.timestamp)
            ]

            off_peak_ratio = len(off_peak_activities) / len(group_activities)

            # If significant batch processing happens off-peak
            if off_peak_ratio >= 0.6 and avg_data_volume >= 20:
                # Suggest scheduling during off-peak hours
                cron_expr = "0 2 * * *"  # 2 AM daily

                pattern = SchedulePattern(
                    pattern_id=f"batch_{group_key}",
                    pattern_name=f"Batch processing: {group_key}",
                    schedule_type=ScheduleType.BATCH_PROCESSING,
                    granularity=TimeGranularity.DAY,
                    frequency=len(group_activities),
                    cron_expression=cron_expr,
                    time_windows=[(time(2, 0), time(4, 0))],  # 2-4 AM window
                    days_of_week=set(),
                    days_of_month=set(),
                    excluded_dates=set(),
                    trigger_type=ScheduleTrigger.CRON_EXPRESSION,
                    confidence=off_peak_ratio,
                    automation_potential=self._assess_batch_automation_potential(
                        group_activities, avg_data_volume
                    )
                )
                patterns.append(pattern)

        return patterns

    # Helper methods for time analysis

    def _determine_interval_granularity(self, seconds: float) -> TimeGranularity:
        """Determine appropriate granularity for an interval."""
        if seconds < 3600:  # Less than 1 hour
            return TimeGranularity.MINUTE
        elif seconds < 86400:  # Less than 1 day
            return TimeGranularity.HOUR
        elif seconds < 604800:  # Less than 1 week
            return TimeGranularity.DAY
        elif seconds < 2592000:  # Less than 1 month
            return TimeGranularity.WEEK
        else:
            return TimeGranularity.MONTH

    def _generate_interval_cron_expression(
        self, seconds: float, granularity: TimeGranularity
    ) -> str:
        """Generate cron expression for fixed intervals."""
        if granularity == TimeGranularity.MINUTE:
            minutes = max(1, int(seconds / 60))
            return f"*/{minutes} * * * *"
        elif granularity == TimeGranularity.HOUR:
            hours = max(1, int(seconds / 3600))
            return f"0 */{hours} * * *"
        elif granularity == TimeGranularity.DAY:
            days = max(1, int(seconds / 86400))
            return f"0 0 */{days} * *"
        else:
            return "0 0 * * *"  # Daily fallback

    def _format_interval(self, seconds: float) -> str:
        """Format interval duration for human readability."""
        if seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''}"

    def _is_off_peak_time(self, timestamp: datetime) -> bool:
        """Check if timestamp is during off-peak hours."""
        hour = timestamp.hour
        # Off-peak: 10 PM to 6 AM
        return hour >= 22 or hour <= 6

    # Confidence calculation methods

    def _calculate_interval_confidence(
        self, intervals: List[float], avg_interval: float
    ) -> float:
        """Calculate confidence for interval patterns."""
        if not intervals:
            return 0.0

        # Calculate coefficient of variation
        variance = sum((i - avg_interval) **
                       2 for i in intervals) / len(intervals)
        std_dev = variance ** 0.5
        cv = std_dev / avg_interval if avg_interval > 0 else 0

        # Lower CV = higher confidence
        confidence = max(0.0, 1.0 - cv)
        return min(confidence, 1.0)

    def _calculate_daily_confidence(
        self, activities: List[UserActivity], dates: Set
    ) -> float:
        """Calculate confidence for daily patterns."""
        # Confidence based on consistency across days
        total_possible_days = (max(dates) - min(dates)).days + 1
        actual_days = len(dates)
        consistency = actual_days / total_possible_days

        # Boost confidence if pattern spans reasonable time period
        if total_possible_days >= 7:  # At least a week
            consistency = min(consistency + 0.2, 1.0)

        return consistency

    def _calculate_weekly_confidence(
        self, activities: List[UserActivity], weeks: Set
    ) -> float:
        """Calculate confidence for weekly patterns."""
        # Similar to daily, but for weeks
        week_span = max(weeks) - min(weeks) + 1
        actual_weeks = len(weeks)
        consistency = actual_weeks / week_span

        if week_span >= 4:  # At least a month
            consistency = min(consistency + 0.2, 1.0)

        return consistency

    def _calculate_monthly_confidence(
        self, activities: List[UserActivity], months: Set
    ) -> float:
        """Calculate confidence for monthly patterns."""
        month_span = len(months)
        if month_span >= 3:  # At least 3 months
            return 0.8  # High confidence for monthly patterns
        elif month_span >= 2:
            return 0.6
        else:
            return 0.4

    # Automation potential assessment methods

    def _assess_interval_automation_potential(
        self, activities: List[UserActivity]
    ) -> float:
        """Assess automation potential for interval patterns."""
        factors = []

        # Success rate factor
        success_rate = sum(
            1 for a in activities if a.success) / len(activities)
        factors.append(success_rate)

        # Frequency factor
        frequency_factor = min(len(activities) / 20.0,
                               1.0)  # Max at 20 occurrences
        factors.append(frequency_factor)

        # Duration consistency factor
        durations = [a.duration_minutes for a in activities]
        avg_duration = sum(durations) / len(durations)
        duration_variance = sum((d - avg_duration) **
                                2 for d in durations) / len(durations)
        consistency_factor = max(
            0.0, 1.0 - (duration_variance / avg_duration ** 2))
        factors.append(consistency_factor)

        return sum(factors) / len(factors)

    def _assess_daily_automation_potential(
        self, activities: List[UserActivity]
    ) -> float:
        """Assess automation potential for daily patterns."""
        # Similar to interval, but consider day-to-day consistency
        return self._assess_interval_automation_potential(activities)

    def _assess_weekly_automation_potential(
        self, activities: List[UserActivity]
    ) -> float:
        """Assess automation potential for weekly patterns."""
        return self._assess_interval_automation_potential(activities)

    def _assess_monthly_automation_potential(
        self, activities: List[UserActivity]
    ) -> float:
        """Assess automation potential for monthly patterns."""
        # Monthly patterns have high automation potential if consistent
        base_potential = self._assess_interval_automation_potential(activities)
        # Boost for monthly patterns due to their regular nature
        return min(base_potential + 0.2, 1.0)

    def _assess_business_hours_automation_potential(
        self, activities: List[UserActivity]
    ) -> float:
        """Assess automation potential for business hours patterns."""
        return self._assess_interval_automation_potential(activities)

    def _assess_batch_automation_potential(
        self, activities: List[UserActivity], avg_data_volume: float
    ) -> float:
        """Assess automation potential for batch patterns."""
        base_potential = self._assess_interval_automation_potential(activities)

        # Higher data volume = higher automation potential
        volume_factor = min(avg_data_volume / 100.0, 1.0)

        return (base_potential + volume_factor) / 2.0

    # Analysis methods for activity distribution

    def _analyze_hourly_distribution(
        self, activities: List[UserActivity]
    ) -> Dict[int, int]:
        """Analyze activity distribution by hour of day."""
        hourly_counts = defaultdict(int)
        for activity in activities:
            hourly_counts[activity.timestamp.hour] += 1
        return dict(hourly_counts)

    def _analyze_daily_distribution(
        self, activities: List[UserActivity]
    ) -> Dict[int, int]:
        """Analyze activity distribution by day of week."""
        daily_counts = defaultdict(int)
        for activity in activities:
            daily_counts[activity.timestamp.weekday()] += 1
        return dict(daily_counts)

    def _analyze_weekly_distribution(
        self, activities: List[UserActivity]
    ) -> Dict[int, int]:
        """Analyze activity distribution by week of year."""
        weekly_counts = defaultdict(int)
        for activity in activities:
            week = activity.timestamp.isocalendar()[1]
            weekly_counts[week] += 1
        return dict(weekly_counts)

    def _identify_peak_activity_hours(
        self, activities: List[UserActivity]
    ) -> List[int]:
        """Identify peak activity hours."""
        hourly_dist = self._analyze_hourly_distribution(activities)
        if not hourly_dist:
            return []

        avg_activity = sum(hourly_dist.values()) / len(hourly_dist)
        peak_threshold = avg_activity * 1.5  # 50% above average

        peak_hours = [
            hour for hour, count in hourly_dist.items()
            if count >= peak_threshold
        ]

        return sorted(peak_hours)

    def _identify_quiet_periods(
        self, activities: List[UserActivity]
    ) -> List[Tuple[int, int]]:
        """Identify quiet periods (consecutive low-activity hours)."""
        hourly_dist = self._analyze_hourly_distribution(activities)
        if not hourly_dist:
            return []

        avg_activity = sum(hourly_dist.values()) / len(hourly_dist)
        quiet_threshold = avg_activity * 0.3  # 30% of average

        quiet_hours = [
            hour for hour in range(24)
            if hourly_dist.get(hour, 0) <= quiet_threshold
        ]

        # Group consecutive quiet hours
        quiet_periods = []
        start_hour = None

        for hour in quiet_hours:
            if start_hour is None:
                start_hour = hour
            elif hour != quiet_hours[quiet_hours.index(hour) - 1] + 1:
                # Non-consecutive, close previous period
                quiet_periods.append(
                    (start_hour, quiet_hours[quiet_hours.index(hour) - 1]))
                start_hour = hour

        # Close final period
        if start_hour is not None:
            quiet_periods.append((start_hour, quiet_hours[-1]))

        return quiet_periods

    def _analyze_tool_timing_patterns(
        self, activities: List[UserActivity]
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze timing patterns for each tool."""
        tool_patterns = defaultdict(lambda: defaultdict(list))

        for activity in activities:
            tool = activity.tool_used
            hour = activity.timestamp.hour
            day = activity.timestamp.weekday()

            tool_patterns[tool]['hours'].append(hour)
            tool_patterns[tool]['days'].append(day)
            tool_patterns[tool]['activities'].append(activity)

        # Calculate patterns for each tool
        result = {}
        for tool, data in tool_patterns.items():
            hours = data['hours']
            days = data['days']
            activities = data['activities']

            result[tool] = {
                'most_active_hours': list(Counter(hours).most_common(3)),
                'most_active_days': list(Counter(days).most_common(3)),
                'total_activities': len(activities),
                'avg_duration': sum(a.duration_minutes for a in activities) / len(activities),
                'success_rate': sum(1 for a in activities if a.success) / len(activities)
            }

        return result

    def _calculate_business_hours_ratio(
        self, activities: List[UserActivity]
    ) -> float:
        """Calculate ratio of activities during business hours."""
        business_activities = 0

        for activity in activities:
            is_business_day = activity.timestamp.weekday() in self.business_days
            is_business_hour = (
                self.business_hours[0] <= activity.timestamp.time() <=
                self.business_hours[1]
            )

            if is_business_day and is_business_hour:
                business_activities += 1

        return business_activities / len(activities) if activities else 0.0

    # Workflow creation and optimization methods

    def _group_related_patterns(
        self, patterns: List[SchedulePattern]
    ) -> List[List[SchedulePattern]]:
        """Group related schedule patterns into workflows."""
        # For now, return each pattern as its own workflow
        # In practice, this could analyze pattern relationships
        return [[pattern] for pattern in patterns]

    def _create_temporal_workflow(
        self, pattern_group: List[SchedulePattern], user_id: str
    ) -> Optional[TemporalWorkflow]:
        """Create a temporal workflow from a group of patterns."""
        if not pattern_group:
            return None

        primary_pattern = pattern_group[0]

        # Create scheduled actions (simplified)
        scheduled_actions = []
        for pattern in pattern_group:
            action = ScheduledAction(
                action_id=f"action_{pattern.pattern_id}",
                user_id=user_id,
                action_description=pattern.pattern_name,
                tools_involved={'n8n'},  # Simplified
                average_duration_minutes=5.0,  # Default estimate
                success_rate=0.9,  # Default estimate
                data_volume_pattern={},
                dependencies=[],
                resource_requirements={}
            )
            scheduled_actions.append(action)

        workflow = TemporalWorkflow(
            workflow_id=f"workflow_{primary_pattern.pattern_id}",
            workflow_name=f"Automated workflow: {primary_pattern.pattern_name}",
            schedule_pattern=primary_pattern,
            scheduled_actions=scheduled_actions,
            workflow_description=f"Temporal workflow based on {primary_pattern.schedule_type.value}",
            estimated_runtime_minutes=sum(
                a.average_duration_minutes for a in scheduled_actions),
            resource_conflicts=[],
            optimization_opportunities=[],
            historical_performance={}
        )

        return workflow

    def _is_viable_workflow(self, workflow: TemporalWorkflow) -> bool:
        """Determine if a workflow is viable for automation."""
        pattern = workflow.schedule_pattern

        # Must have reasonable confidence and automation potential
        if pattern.confidence < 0.6 or pattern.automation_potential < 0.6:
            return False

        # Must have sufficient frequency
        if pattern.frequency < 3:
            return False

        return True

    # Optimization methods (placeholder implementations)

    def _detect_scheduling_conflicts(
        self, workflows: List[TemporalWorkflow]
    ) -> List[Dict[str, Any]]:
        """Detect conflicts between scheduled workflows."""
        # Placeholder - would analyze overlapping time windows
        return []

    def _suggest_load_balancing(
        self, workflows: List[TemporalWorkflow]
    ) -> List[Dict[str, Any]]:
        """Suggest load balancing optimizations."""
        # Placeholder - would analyze resource usage patterns
        return []

    def _identify_batch_opportunities(
        self, workflows: List[TemporalWorkflow]
    ) -> List[Dict[str, Any]]:
        """Identify opportunities to batch similar workflows."""
        # Placeholder - would find workflows that could be combined
        return []

    def _suggest_off_peak_scheduling(
        self, workflows: List[TemporalWorkflow]
    ) -> List[Dict[str, Any]]:
        """Suggest moving workflows to off-peak hours."""
        # Placeholder - would identify workflows suitable for off-peak execution
        return []

    # n8n node generation methods (placeholder implementations)

    def _create_cron_trigger_node(self, pattern: SchedulePattern) -> Dict[str, Any]:
        """Create n8n cron trigger node."""
        return {
            'id': f'cron_trigger_{pattern.pattern_id}',
            'type': 'n8n-nodes-base.cron',
            'name': f'Schedule: {pattern.pattern_name}',
            'parameters': {
                'cronExpression': pattern.cron_expression
            },
            'position': [100, 200],
            'typeVersion': 1
        }

    def _create_interval_trigger_node(self, pattern: SchedulePattern) -> Dict[str, Any]:
        """Create n8n interval trigger node."""
        return {
            'id': f'interval_trigger_{pattern.pattern_id}',
            'type': 'n8n-nodes-base.interval',
            'name': f'Interval: {pattern.pattern_name}',
            'parameters': {
                'interval': 3600  # Default 1 hour
            },
            'position': [100, 200],
            'typeVersion': 1
        }

    def _create_webhook_trigger_node(self, pattern: SchedulePattern) -> Dict[str, Any]:
        """Create n8n webhook trigger node."""
        return {
            'id': f'webhook_trigger_{pattern.pattern_id}',
            'type': 'n8n-nodes-base.webhook',
            'name': f'Webhook: {pattern.pattern_name}',
            'parameters': {
                'path': f'schedule/{pattern.pattern_id}'
            },
            'position': [100, 200],
            'typeVersion': 1
        }

    def _create_manual_trigger_node(self, pattern: SchedulePattern) -> Dict[str, Any]:
        """Create n8n manual trigger node."""
        return {
            'id': f'manual_trigger_{pattern.pattern_id}',
            'type': 'n8n-nodes-base.manualTrigger',
            'name': f'Manual: {pattern.pattern_name}',
            'parameters': {},
            'position': [100, 200],
            'typeVersion': 1
        }

    def _create_time_window_condition_node(
        self, pattern: SchedulePattern
    ) -> Optional[Dict[str, Any]]:
        """Create time window condition node."""
        if not pattern.time_windows:
            return None

        time_window = pattern.time_windows[0]

        return {
            'id': f'time_condition_{pattern.pattern_id}',
            'type': 'n8n-nodes-base.if',
            'name': f'Time Window Check',
            'parameters': {
                'conditions': {
                    'options': {
                        'leftValue': '={{ new Date().getHours() }}',
                        'operation': 'between',
                        'rightValue': f'{time_window[0].hour}-{time_window[1].hour}'
                    }
                }
            },
            'position': [300, 200],
            'typeVersion': 1
        }

    # Cron generation helper methods

    def _generate_interval_cron(self, pattern: SchedulePattern) -> List[str]:
        """Generate cron expressions for interval patterns."""
        return [pattern.cron_expression]

    def _generate_daily_cron(self, pattern: SchedulePattern) -> List[str]:
        """Generate cron expressions for daily patterns."""
        return [pattern.cron_expression]

    def _generate_weekly_cron(self, pattern: SchedulePattern) -> List[str]:
        """Generate cron expressions for weekly patterns."""
        return [pattern.cron_expression]

    def _generate_monthly_cron(self, pattern: SchedulePattern) -> List[str]:
        """Generate cron expressions for monthly patterns."""
        return [pattern.cron_expression]

    def _generate_business_hours_cron(self, pattern: SchedulePattern) -> List[str]:
        """Generate cron expressions for business hours patterns."""
        return [pattern.cron_expression]

    def _generate_batch_cron(self, pattern: SchedulePattern) -> List[str]:
        """Generate cron expressions for batch patterns."""
        return [pattern.cron_expression]


# Utility functions

def analyze_user_schedule_patterns(
    user_id: str,
    activity_history: List[Dict[str, Any]],
    time_window: timedelta = timedelta(days=45)
) -> Dict[str, Any]:
    """High-level function to analyze scheduling patterns for a user."""

    detector = SchedulePatternDetector()

    # Record activities
    for record in activity_history:
        detector.record_activity(
            user_id=user_id,
            action_type=record['action_type'],
            tool_used=record['tool_used'],
            duration_minutes=record.get('duration_minutes', 1.0),
            data_processed=record.get('data_processed', 1),
            success=record.get('success', True),
            context_tags=record.get('context_tags', []),
            session_id=record.get('session_id')
        )

    # Analyze patterns and workflows
    patterns = detector.analyze_temporal_patterns(user_id, time_window)
    workflows = detector.detect_scheduled_workflows(patterns, user_id)
    distribution = detector.analyze_activity_distribution(user_id, time_window)
    optimizations = detector.suggest_schedule_optimizations(workflows)

    return {
        'patterns_detected': len(patterns),
        'workflows_identified': len(workflows),
        'activity_distribution': distribution,
        'top_patterns': patterns[:5],  # Top 5 patterns
        'recommended_workflows': workflows[:3],  # Top 3 workflows
        'optimization_suggestions': optimizations,
        'summary': {
            'most_common_schedule_types': list(Counter([
                p.schedule_type.value for p in patterns
            ]).most_common(3)),
            'peak_activity_hours': distribution.get('peak_activity_hours', []),
            'business_hours_ratio': distribution.get('business_hours_ratio', 0),
            'high_automation_potential': len([
                p for p in patterns if p.automation_potential > 0.7
            ])
        }
    }
