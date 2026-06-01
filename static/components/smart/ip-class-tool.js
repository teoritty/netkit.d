// Smart component: IPv4/IPv6 address classification.

import { byId, setLoading } from '../../utils/dom.js';
import { isValidIPv4, isValidIPv6 } from '../../utils/ip-validation.js';
import { renderIpClass } from '../dumb/result-views.js';
import { t } from '../../i18n/i18n.js';

export function mountIpClassTool({ calculationService, notify }) {
  bind({
    formId: 'ip-check-form',
    inputId: 'ipv4CheckInput',
    resultId: 'ipv4ClassResult',
    validator: isValidIPv4,
    invalidMessage: 'Enter a valid IPv4 address',
    classify: calculationService.classifyIpv4,
    notify,
  });
  bind({
    formId: 'ip-checkv6-form',
    inputId: 'ipv6CheckInput',
    resultId: 'ipv6ClassResult',
    validator: isValidIPv6,
    invalidMessage: 'Enter a valid IPv6 address',
    classify: calculationService.classifyIpv6,
    notify,
  });
}

function bind({ formId, inputId, resultId, validator, invalidMessage, classify, notify }) {
  const form = byId(formId);
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const input = byId(inputId);
    if (!validator(input.value)) {
      notify(t(invalidMessage), 'error');
      input.classList.add('invalid');
      return;
    }
    const button = form.querySelector('[data-submit-btn]');
    setLoading(button, true);
    try {
      const data = await classify(input.value.trim());
      renderIpClass(resultId, data.address_class);
    } catch (error) {
      notify(error.message, 'error');
    } finally {
      setLoading(button, false);
    }
  });
}
