# Exotic Testing Patterns Analysis
==================================================

## 📊 Exotic Pattern Statistics
- **Total Exotic Pattern Instances**: 1,970
- **Unique Pattern Types**: 10
- **Highly Complex Files**: 101 (3+ exotic patterns)

## 🚀 Most Complex Testing Scenarios
1. **infrastructure/n8n/testing/playwright/tests/ui/building-blocks/01-workflow-entry-points.spec.ts**
   - Complexity Score: 13
   - Patterns: performance_testing, ui_testing, event_driven_testing, state_machine_testing, async_testing
2. **infrastructure/n8n/tests/ui/building-blocks/01-workflow-entry-points.spec.ts**
   - Complexity Score: 13
   - Patterns: performance_testing, ui_testing, event_driven_testing, state_machine_testing, async_testing
3. **infrastructure/n8n/test/nodes/TriggerHelpers.ts**
   - Complexity Score: 13
   - Patterns: security_testing, monkey_patching, event_driven_testing, state_machine_testing, async_testing
4. **infrastructure/n8n/testing/playwright/composables/CanvasComposer.ts**
   - Complexity Score: 12
   - Patterns: performance_testing, security_testing, ui_testing, state_machine_testing, async_testing
5. **infrastructure/n8n/testing/playwright/tests/ui/16-webhook-node.spec.ts**
   - Complexity Score: 11
   - Patterns: security_testing, state_machine_testing, async_testing, event_driven_testing
6. **infrastructure/n8n/testing/playwright/pages/CanvasPage.ts**
   - Complexity Score: 11
   - Patterns: ui_testing, state_machine_testing, async_testing, event_driven_testing
7. **infrastructure/n8n/testing/playwright/pages/NodeDetailsViewPage.ts**
   - Complexity Score: 11
   - Patterns: ui_testing, state_machine_testing, async_testing, event_driven_testing
8. **infrastructure/n8n/nodes-testing/node-test-harness.ts**
   - Complexity Score: 11
   - Patterns: monkey_patching, state_machine_testing, async_testing, event_driven_testing
9. **infrastructure/n8n/tests/ui/16-webhook-node.spec.ts**
   - Complexity Score: 11
   - Patterns: security_testing, state_machine_testing, async_testing, event_driven_testing
10. **infrastructure/n8n/test-runner/test-runner.service.ee.ts**
   - Complexity Score: 10
   - Patterns: performance_testing, security_testing, state_machine_testing, async_testing

## 🔬 Exotic Pattern Deep Dive

### Integration Testing
**Occurrences**: 558
**Example Files**:
- `mtg/commander-spellbook-backend/tests/testing.py`
- `mtg/commander-spellbook-backend/tests/test_card_list_from_url.py`
- `mtg/commander-spellbook-backend/tests/test_find_my_combos.py`
**Example Code**:
```python
# From: mtg/commander-spellbook-backend/tests/test_card_list_from_url.py (line 9)
with self.assertRaises(BadRequestException):
            async with self.anonymous_api_client as api_client:
                api_instance = CardListFromUrlApi(api_client)
```

### State Machine Testing
**Occurrences**: 443
**Example Files**:
- `productivity/dispatch/tests/factories.py`
- `productivity/dispatch/tests/conftest.py`
- `productivity/dispatch/dispatch_test/workflow.py`
**Example Code**:
```python
# From: productivity/dispatch/dispatch_test/workflow.py (line 1)
from dispatch.plugins.bases import WorkflowPlugin
```

### Async Testing
**Occurrences**: 273
**Example Files**:
- `mtg/commander-spellbook-backend/tests/test_card_list_from_url.py`
- `mtg/commander-spellbook-backend/tests/test_find_my_combos.py`
- `mtg/commander-spellbook-backend/tests/test_variant_search.py`
**Example Code**:
```python
# From: mtg/commander-spellbook-backend/tests/test_variant_search.py (line 5)
class TestVariantSearch(SpellbookClientTest):
    async def test_without_parameters(self):
        variants = await self.get_variants()
```

### Parametrized Testing
**Occurrences**: 199
**Example Files**:
- `productivity/mealie/repository_tests/test_recipe_repository.py`
- `productivity/mealie/repository_tests/test_search.py`
- `productivity/mealie/repository_tests/test_pagination.py`
**Example Code**:
```python
# From: productivity/mealie/repository_tests/test_recipe_repository.py (line 633)
@pytest.mark.parametrize(
    "search, expected_names",
```

### Ui Testing
**Occurrences**: 137
**Example Files**:
- `security/apiscout/tests/testScout.py`
- `productivity/dispatch/tests/static/e2e/report-case.spec.ts`
- `productivity/dispatch/tests/static/e2e/report-submission.spec.ts`
**Example Code**:
```python
# From: security/apiscout/tests/testScout.py (line 103)
def testRender(self):
        scout = ApiScout()
```

### Security Testing
**Occurrences**: 114
**Example Files**:
- `mtg/commander-spellbook-backend/test_views/test_variant_suggestions_views.py`
- `security/MISP/tests/testlive_security.py`
- `mtg/commander-spellbook-backend/test_views/test_variant_update_suggestions_views.py`
**Example Code**:
```python
# From: mtg/commander-spellbook-backend/test_views/test_variant_update_suggestions_views.py (line 4)
import logging
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
```

### Event Driven Testing
**Occurrences**: 106
**Example Files**:
- `productivity/mealie/integration_tests/test_repository_factory.py`
- `productivity/dispatch/dispatch_test/document.py`
- `security/Ghostwriter/tests/test_models.py`
**Example Code**:
```python
# From: security/Ghostwriter/tests/test_models.py (line 129)
def test_sanitized_webhook_property(self):
        entry = self.SlackConfiguration.get_solo()
```

### Performance Testing
**Occurrences**: 66
**Example Files**:
- `security/MISP/tests/testlive_security.py`
- `productivity/mealie/integration_tests/test_repository_factory.py`
- `security/apiscout/tests/testImportTableLoader.py`
**Example Code**:
```python
# From: security/MISP/tests/testlive_security.py (line 527)
}):
            expiration = int((datetime.datetime.now() + datetime.timedelta(days=300)).timestamp())
            auth_key = self.__create_advanced_authkey(self.test_usr.id, {"expiration": expiration})
```

### Monkey Patching
**Occurrences**: 64
**Example Files**:
- `productivity/dispatch/tests/signal/test_signal_flow.py`
- `productivity/dispatch/tests/plugins/dispatch_slack/case/test_interactive.py`
**Example Code**:
```python
# From: productivity/dispatch/tests/signal/test_signal_flow.py (line 477)
with mock.patch.object(service_flows, "resolve_oncall") as mock_resolve_oncall, \
        mock.patch.object(case_service, "create") as mock_case_create, \
```

### Database Testing
**Occurrences**: 10
**Example Files**:
- `productivity/mealie/public_explorer_tests/test_public_recipes.py`
- `productivity/dispatch/tests/conftest.py`
- `productivity/mealie/integration_tests/public_explorer_tests/test_public_recipes.py`
**Example Code**:
```python
# From: productivity/dispatch/tests/conftest.py (line 142)
yield session
    session.rollback()
```

==================================================
# Business Logic Complexity Analysis
## 🧠 Complex Business Logic Patterns

### Concurrency Control
**Occurrences**: 2
**Example Functions**:
- `test_concurrent_access` in `productivity/mealie/unit_tests/core/security/auth_cache/test_auth_cache.py`
- `test_concurrent_access` in `productivity/mealie/tests/unit_tests/core/security/auth_cache/test_auth_cache.py`

### Complex Algorithms
**Occurrences**: 1
**Example Functions**:
- `test_search_filter_sort_paginate_basic` in `productivity/dispatch/tests/database/test_service.py`
