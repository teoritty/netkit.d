// Frontend entry point (composition root): creates services and mounts
// components, passing dependencies as parameters. The ES module runs
// after the DOM is parsed, so a separate DOMContentLoaded is not needed.

import { createApiClient } from '../services/api-client.js';
import { createCalculationService } from '../services/calculation-service.js';
import { createDiagnosticsService } from '../services/diagnostics-service.js';
import { createThemeStore } from '../store/theme-store.js';
import { createLanguageStore } from '../store/language-store.js';
import { mountToasts, showToast } from '../components/dumb/toast.js';
import { initCopyDelegation } from '../components/dumb/copy-button.js';
import { initRowRemoval } from '../components/dumb/dynamic-rows.js';
import { attachIPValidation, isValidIPv4 } from '../utils/ip-validation.js';
import { byId } from '../utils/dom.js';

import { mountNavigation } from '../components/smart/navigation.js';
import { mountSubnetTool } from '../components/smart/subnet-tool.js';
import { mountGrouperTool } from '../components/smart/grouper-tool.js';
import { mountIpClassTool } from '../components/smart/ip-class-tool.js';
import { mountPortInfoTool } from '../components/smart/port-info-tool.js';
import { mountIpv6ConvertTool } from '../components/smart/ipv6-convert-tool.js';
import { mountVlsmTool } from '../components/smart/vlsm-tool.js';
import { mountSupernetTool } from '../components/smart/supernet-tool.js';
import { mountRangeCidrTool } from '../components/smart/range-cidr-tool.js';
import { mountPingTool } from '../components/smart/ping-tool.js';
import { mountTracerouteTool } from '../components/smart/traceroute-tool.js';
import { mountDnsTool } from '../components/smart/dns-tool.js';
import { mountWhoisTool } from '../components/smart/whois-tool.js';
import { mountPortScanTool } from '../components/smart/port-scan-tool.js';
import { mountBaseConverterTool } from '../components/smart/base-converter-tool.js';
import { mountMtuTool } from '../components/smart/mtu-tool.js';
import { mountConfigGenTool } from '../components/smart/config-gen-tool.js';
import { mountBase64Tool } from '../components/smart/base64-tool.js';

function bootstrap() {
  const api = createApiClient();
  const calculationService = createCalculationService(api);
  const diagnosticsService = createDiagnosticsService(api);
  const calc = { calculationService, notify: showToast };
  const diag = { diagnosticsService, notify: showToast };

  // Global UI infrastructure.
  mountToasts(byId('toastContainer'));
  initCopyDelegation(document.body);
  initRowRemoval(document.body, '.ip-row, .req-row, .network-entry-row');

  // Theme + navigation.
  const themeStore = createThemeStore();
  themeStore.applyCurrent();
  document.querySelectorAll('.theme-btn[data-theme]').forEach((button) => {
    button.addEventListener('click', () => themeStore.setTheme(button.dataset.theme));
  });
  mountNavigation();

  // Language (default English). Translates the static DOM on switch.
  const languageStore = createLanguageStore();
  languageStore.applyCurrent();
  document.querySelectorAll('.lang-btn').forEach((button) => {
    button.addEventListener('click', () => languageStore.setLang(button.dataset.lang));
  });

  // UX validation for the main subnet field.
  attachIPValidation(byId('subnetIpInput'), isValidIPv4);

  // Calculation tools.
  mountSubnetTool(calc);
  mountGrouperTool(calc);
  mountIpClassTool(calc);
  mountPortInfoTool(calc);
  mountIpv6ConvertTool(calc);
  mountVlsmTool(calc);
  mountSupernetTool(calc);
  mountRangeCidrTool(calc);

  // Diagnostics.
  mountPingTool(diag);
  mountTracerouteTool(diag);
  mountDnsTool(diag);
  mountWhoisTool(diag);
  mountPortScanTool(diag);

  // Client-side tools (no backend).
  mountBaseConverterTool({ notify: showToast });
  mountMtuTool();
  mountConfigGenTool({ notify: showToast });
  mountBase64Tool({ notify: showToast });
}

bootstrap();
