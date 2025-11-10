# Test Migration Analysis Report

**Generated**: Sun Oct 26 07:28:40 UTC 2025
**Purpose**: Analyze existing tool capabilities through test discovery

## Domain Statistics

### Security Domain
- **Tools**: 7
- **Test Directories**: 85
- **Test Files**: 101
- **Frameworks**: unittest, phpunit, cargo_test, pytest
- **Capabilities**: 10 discovered

### Productivity Domain
- **Tools**: 8
- **Test Directories**: 103
- **Test Files**: 729
- **Frameworks**: unittest, cargo_test, pytest, jest
- **Capabilities**: 224 discovered

### Mtg Domain
- **Tools**: 2
- **Test Directories**: 10
- **Test Files**: 79
- **Frameworks**: unittest
- **Capabilities**: 42 discovered

### Infrastructure Domain
- **Tools**: 5
- **Test Directories**: 373
- **Test Files**: 2886
- **Frameworks**: unittest, pytest, jest
- **Capabilities**: 309 discovered

## Tool Analysis

### CyberChef (security)
- **Test Files**: 5
- **Frameworks**: 
- **Performance Tests**: 0
- **Integration Tests**: 0

### Ghostwriter (security)
- **Test Files**: 42
- **Frameworks**: 
- **Performance Tests**: 0
- **Integration Tests**: 4
- **Capabilities**: table, list...

### KasmVNC (infrastructure)
- **Test Files**: 0
- **Frameworks**: 
- **Performance Tests**: 0
- **Integration Tests**: 0

### MISP (security)
- **Test Files**: 20
- **Frameworks**: phpunit, unittest
- **Performance Tests**: 0
- **Integration Tests**: 2
- **Capabilities**: ex$code);, $gpg = $this->in);, public function testIn): void...

### MalwareBazaar_MCP (infrastructure)
- **Test Files**: 1
- **Frameworks**: unittest
- **Performance Tests**: 0
- **Integration Tests**: 0
- **Capabilities**: async get_info_success...

### actual (productivity)
- **Test Files**: 35
- **Frameworks**: jest
- **Performance Tests**: 0
- **Integration Tests**: 3
- **Capabilities**: 'extracts card transaction date', , 'should return a normalized account object', , 'provides correct amount in pending transaction and removes payee prefix', , 'sorts transactions by bookingDate field from newest to oldest', , 'returns the remittanceInformationUnstructured as payeeName when the amount is negative', , 'returns the internalTransactionId as transactionId', , 'correctly extracts the payee and when not provided', , 'returns the expected remittanceInformationUnstructured from a bizum expense transfer', , 'extracts card merchant between the circuit prefix and operation suffix', , 'returns the expected payeeName from a transaction with a set creditorName', ...

### apiscout (security)
- **Test Files**: 6
- **Frameworks**: 
- **Performance Tests**: 0
- **Integration Tests**: 5

### blackarch (security)
- **Test Files**: 0
- **Frameworks**: 
- **Performance Tests**: 0
- **Integration Tests**: 0

### chroma-mcp (infrastructure)
- **Test Files**: 1
- **Frameworks**: unittest, pytest
- **Performance Tests**: 0
- **Integration Tests**: 0

### commander-spellbook-backend (mtg)
- **Test Files**: 79
- **Frameworks**: unittest
- **Performance Tests**: 0
- **Integration Tests**: 9
- **Capabilities**: method_count, template_fields, async by_results, empty_graph, website_properties_view, root_endpoint, with_command_zone, plain, escape_markdown, feature_fields...

### commander-spellbook-site (mtg)
- **Test Files**: 0
- **Frameworks**: 
- **Performance Tests**: 0
- **Integration Tests**: 0

### dispatch (productivity)
- **Test Files**: 96
- **Frameworks**: unittest, pytest, jest
- **Performance Tests**: 0
- **Integration Tests**: 8
- **Capabilities**: find_links__no_links, find_links, get_all_by_signal, get, create_cost_model_activity, get_by_case_id, get_default_or_raise__fail, create_custom_event, create_tactical_report, get_all...

### firecrawl (productivity)
- **Test Files**: 149
- **Frameworks**: unittest, jest, pytest
- **Performance Tests**: 0
- **Integration Tests**: 68
- **Capabilities**: , async async_crawl_start_and_status, "should handle invalid prompt gracefully", , "should return 2 for scrapethissite.com/pages/articles", , invalid_url, crawl_watcher, validate_empty_query, async async_map_minimal, validate_invalid_limself):, "should prepend http:// to URLs without a protocol", ...

### goose (productivity)
- **Test Files**: 71
- **Frameworks**: cargo_test, jest
- **Performance Tests**: 1
- **Integration Tests**: 9
- **Capabilities**: 'should extract variables with underscores', , 'should render default message when no conversationCompacted content found', , 'should extract simple template variables', , 'should render info alert with message', , 'renders without crashing', , 'should start with empty alerts array', ...

### inspector (productivity)
- **Test Files**: 23
- **Frameworks**: jest
- **Performance Tests**: 0
- **Integration Tests**: 0
- **Capabilities**: "should allow HTTPS URLs", , "should allow HTTP URLs", , "should handle empty strings", , "should allow URLs with ports", , "Returns successful: false and error when error is present", , "should escape Unicode characters in a string", , "should allow URLs with paths", , "should render 'No pending requests' when there are no pending requests", , test, "should preserve required fields even when undefined", ...

### it-tools (productivity)
- **Test Files**: 3
- **Frameworks**: 
- **Performance Tests**: 0
- **Integration Tests**: 0

### kong (productivity)
- **Test Files**: 11
- **Frameworks**: pytest
- **Performance Tests**: 0
- **Integration Tests**: 2

### mealie (productivity)
- **Test Files**: 341
- **Frameworks**: unittest, pytest
- **Performance Tests**: 0
- **Integration Tests**: 195
- **Capabilities**: no_claims, alchemy_exporter, duplicate_recipe_changes_household, no_expired_tokens, create_plan_with_title, create_group_resolve_similar_names, get_household_members, openapi_returns_json, login, alembic_revisions_are_in_order...

### n8n (infrastructure)
- **Test Files**: 2869
- **Frameworks**: unittest, jest, pytest
- **Performance Tests**: 11
- **Integration Tests**: 1101
- **Capabilities**: 'should process alert_create event correctly', async , 'should throw an error if the database type is not supported', , 'should return a message with method with tip', , 'should return true for strings with banned characters', , 'should return "error" when resultData.error exists', , const toLines = , 'should not modify requestOptions if title and dueDate are provided', async , 'should pick only selected properties', , 'should default to `error` level', , 'should set default base path when no path provided', ...

### n8n-mcp-server (infrastructure)
- **Test Files**: 15
- **Frameworks**: jest
- **Performance Tests**: 0
- **Integration Tests**: 6
- **Capabilities**: 'returns the correct emoji for known statuses', , 'should return the correct URI template', , 'does not append "s" for already plural resource types', , 'returns URI without id when none is provided', , 'appends "s" for singular resource types', , 'should return the correct tool definition', ...

### securityonion (security)
- **Test Files**: 0
- **Frameworks**: 
- **Performance Tests**: 0
- **Integration Tests**: 0

### yara-x (security)
- **Test Files**: 28
- **Frameworks**: cargo_test, pytest
- **Performance Tests**: 0
- **Integration Tests**: 0
- **Capabilities**: bad_variable_type, relaxed_re_syntax, env_logger::in);, fn e2e_test, syntax_error...

## Constitutional Compliance Assessment

- **Total Performance Tests**: 12
- **Total Integration Tests**: 1412
- **Performance Validation**: Requires analysis of discovered performance tests
- **Business Logic Preservation**: Requires comparison with original implementations

## Next Steps

1. **Performance Baseline**: Run existing performance tests to establish baselines
2. **Capability Mapping**: Map discovered capabilities to constitutional requirements
3. **Integration Strategy**: Use integration tests as migration validation
4. **Business Logic Analysis**: Compare test expectations with integrated implementations
