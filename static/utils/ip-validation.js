// Client-side UX format validation. The server is always the source of truth —
// this only highlights fields for the user's convenience.

export function isValidIPv4(ip) {
  const parts = ip.trim().split('.');
  if (parts.length !== 4) return false;
  return parts.every((part) => {
    const number = Number(part);
    return /^\d+$/.test(part) && number >= 0 && number <= 255;
  });
}

export function isValidIPv6(ip) {
  const value = ip.trim();
  return value.length > 0 && (value.includes(':') || value === '::');
}

export function attachIPValidation(input, validator) {
  if (!input) return;
  const errorElement = input.closest('.form-group')?.querySelector('.form-error');
  input.addEventListener('blur', () => {
    const value = input.value.trim();
    if (!value) {
      input.classList.remove('invalid');
      errorElement?.classList.remove('visible');
      return;
    }
    const valid = validator(value);
    input.classList.toggle('invalid', !valid);
    errorElement?.classList.toggle('visible', !valid);
  });
  input.addEventListener('input', () => {
    input.classList.remove('invalid');
    errorElement?.classList.remove('visible');
  });
}
