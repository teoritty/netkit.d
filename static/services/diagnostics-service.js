// Diagnostics endpoints client. Injected into smart components.

export function createDiagnosticsService(api) {
  return {
    ping: (host, count) => api.postJson('/ping/', { host, count }),

    traceroute: (host, maxHops) =>
      api.postJson('/traceroute/', { host, max_hops: maxHops }),

    dnsLookup: (hostname, recordType) =>
      api.postJson('/dns_lookup/', { hostname, record_type: recordType }),

    whois: (ip) => api.postJson('/whois/', { ip }),

    portScan: (host, ports) => api.postJson('/port_scan/', { host, ports }),
  };
}
