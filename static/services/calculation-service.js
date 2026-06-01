// Calculation endpoints client. Injected into smart components.

export function createCalculationService(api) {
  return {
    calculateSubnet: (ipAddress, subnetMask) =>
      api.postJson('/calculate_network_info/', {
        ip_address: ipAddress,
        subnet_mask: subnetMask,
      }),

    groupNetworks: (pairs) => api.postJson('/find_same_network/', { pairs }),

    classifyIpv4: (ipAddress) =>
      api.postJson('/check_ip_class/', { ip_address: ipAddress }),

    classifyIpv6: (ipAddress) =>
      api.postJson('/check_ipv6_class/', { ip_address: ipAddress }),

    lookupPort: (port) => api.get(`/port_info?port=${encodeURIComponent(port)}`),

    convertIpv6: (address) => api.postJson('/convert_ipv6/', { address }),

    splitVlsm: (network, requirements) =>
      api.postJson('/vlsm/', { network, requirements }),

    summarizeSupernet: (networks) => api.postJson('/supernet/', { networks }),

    rangeToCidr: (startIp, endIp) =>
      api.postJson('/ip_range_to_cidr/', { start_ip: startIp, end_ip: endIp }),
  };
}
