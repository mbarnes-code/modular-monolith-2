# Performance Benchmark Analysis Report
Generated from 9561 test files

## 📊 Executive Summary

### Performance Test Coverage
- **Files with Performance Data**: 641
- **Performance Test Functions**: 686
- **Languages with Performance Tests**: {'Shell': 2, 'JSON': 92, 'Unknown': 310, 'TypeScript': 170, 'Python': 57, 'YAML': 10}

## 🎯 Performance Metrics Discovery

### Timeout Values
- **Total Occurrences**: 3891
- **Range**: 0.01 - 999999.0
- **Median**: 15000.0
- **95th Percentile**: 60000.0
- **Sample Values**: [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

### Response Time Expectations
- **Total Occurrences**: 479
- **Range**: 0.1 - 1234567890.0
- **Median**: 99.0
- **95th Percentile**: 9941.0
- **Sample Values**: [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.2, 0.2]

### Load Test Indicators
- **Total Occurrences**: 888
- **Range**: 1.0 - 10010231.0
- **Median**: 7.0
- **95th Percentile**: 829.0
- **Sample Values**: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

### Database Performance
- **Total Occurrences**: 74
- **Range**: 1.0 - 123456789.0
- **Median**: 5.0
- **95th Percentile**: 300000.0
- **Sample Values**: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

### Memory Limits
- **Total Occurrences**: 33
- **Range**: 1.0 - 768.0
- **Median**: 11.0
- **95th Percentile**: 768.0
- **Sample Values**: [1.0, 1.0, 1.0, 1.0, 10.0, 10.0, 11.0, 11.0, 11.0, 11.0]

### Cache Ttl Values
- **Total Occurrences**: 245
- **Range**: 1.0 - 1234567890.0
- **Median**: 10.0
- **95th Percentile**: 4763.0
- **Sample Values**: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

### Benchmark Thresholds
- **Total Occurrences**: 6
- **Range**: 1.0 - 9.0
- **Median**: 8.0
- **95th Percentile**: 9.0
- **Sample Values**: [1.0, 1.0, 4.0, 8.0, 9.0, 9.0]

## 🏆 Specification Benchmark Comparison

### Response Times
- **Specification Requirement**: 500ms
- **Actual Median Performance**: 99.0ms  
- **Actual 95th Percentile**: 9941.0ms
- **Attainability Assessment**: EASILY_ATTAINABLE

### Database Performance
- **Specification Requirement**: N/Ams
- **Actual Median Performance**: 5.0ms  
- **Actual 95th Percentile**: 300000.0ms
- **Attainability Assessment**: EASILY_ATTAINABLE

### Productivity Domain
- **Specification Requirement**: 2000ms
- **Actual Median Performance**: 979.0ms  
- **Actual 95th Percentile**: 18924.0ms
- **Attainability Assessment**: EASILY_ATTAINABLE

### Infrastructure Domain
- **Specification Requirement**: 5000ms
- **Actual Median Performance**: 7.0ms  
- **Actual 95th Percentile**: 2270.0ms
- **Attainability Assessment**: EASILY_ATTAINABLE

## 🏗️ Domain Performance Analysis

### Security Domain
- **Load Test Indicators**: 197 tests, median 6.0ms
- **Timeout Values**: 8 tests, median 3.0ms

### Productivity Domain
- **Timeout Values**: 1227 tests, median 1001.0ms
- **Load Test Indicators**: 450 tests, median 5.0ms
- **Cache Performance**: 143 tests, median 60.0ms
- **Response Time Expectations**: 273 tests, median 979.0ms
- **Memory Indicators**: 19 tests, median 11.0ms
- **Performance Assertions**: 37 tests, median 1.0ms
- **Database Performance**: 63 tests, median 2.0ms
- **Benchmark Indicators**: 2 tests, median 1.0ms

### Infrastructure Domain
- **Benchmark Indicators**: 4 tests, median 9.0ms
- **Timeout Values**: 2644 tests, median 60000.0ms
- **Load Test Indicators**: 239 tests, median 498.0ms
- **Cache Performance**: 101 tests, median 4.0ms
- **Response Time Expectations**: 206 tests, median 7.0ms
- **Performance Assertions**: 21 tests, median 1.0ms
- **Database Performance**: 11 tests, median 9.0ms
- **Memory Indicators**: 14 tests, median 11.0ms

### General Domain
- **Timeout Values**: 12 tests, median 1000.0ms
- **Cache Performance**: 1 tests, median 3600.0ms
- **Load Test Indicators**: 2 tests, median 86.0ms

## 🔬 Analysis Methodology

This analysis examined all test files for:
- Timeout values and performance assertions
- Response time expectations and benchmarks  
- Load testing indicators and concurrent user limits
- Database performance thresholds
- Memory and cache performance indicators
- Explicit benchmark and timing measurements

Pattern matching identified numeric values associated with performance keywords across Python, JavaScript, TypeScript, and other test files.

## 📈 Recommendations

Based on the performance data discovered in existing tests:

1. **Benchmark Validation**: Most specification benchmarks appear attainable based on existing test expectations
2. **Domain Optimization**: Focus optimization efforts on domains showing higher actual performance requirements
3. **Test Coverage**: Consider adding explicit performance tests where gaps exist
4. **Monitoring**: Implement runtime performance monitoring matching test expectations
