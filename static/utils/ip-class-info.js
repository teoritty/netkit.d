// IP address class descriptions for the UI (reference text).

const DESCRIPTIONS = {
  Private: 'Private address, used on local networks (not routed on the internet)',
  Loopback: 'Loopback address, used for local testing',
  Multicast: 'Multicast address for group delivery',
  Reserved: 'IANA-reserved address',
  Global: 'Global public address, routed on the internet',
  'Link-Local': 'Link-local address, valid only within the network segment',
  Unspecified: 'Unspecified address (0.0.0.0 / ::)',
};

export function ipClassInfo(addressClass) {
  return DESCRIPTIONS[addressClass] || 'Unknown type';
}

export function badgeClass(addressClass) {
  return `badge-${addressClass.toLowerCase().replace('-', '')}`;
}
