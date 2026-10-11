WireGuard Ansible Role
=========================

An Ansible role to install WireGuard and configure one or more WireGuard interfaces. Works on Debian-based distributions.

Requirements
------------

* `apt` based host

Role Variables
--------------

Interfaces are declared as a dict in `wireguard_interfaces`, keyed by interface name. Each entry is merged over the shared defaults (`wireguard_interface_defaults`).

```yaml
# All interfaces to configure, keyed by interface name
wireguard_interfaces: {}

# Defaults applied to every interface (override per-interface)
wireguard_interface_defaults:
  private_key: ""           # if empty, a key is generated once on the server and reused
  private_key_path: /etc/wireguard/{{ wireguard_interface.name }}.key
  ip_address:
  listen_port: 51820
  dns:                      # optional, omitted if empty
  mtu:                      # optional, omitted if empty
  preup:                    # optional single command or list, rendered as multiple PreUp lines
  postup:
  predown:
  postdown:
  peers: []
```

Each interface supports the following keys (they replace the `name` / `private_key` / ... entries in `wireguard_interface_defaults`):

```yaml
wireguard_interfaces:
  wg0:                                              # the dict key becomes the interface name
    ip_address: 10.0.0.1/24
    listen_port: 51820
    private_key: <private_key>                      # optional; generated on first run if empty
    dns: 1.1.1.1                                    # optional
    mtu: 1420                                       # optional
    preup: "iptables -A FORWARD -i wg0 -j ACCEPT"   # optional, string or list
    postdown:
      - "iptables -D FORWARD -i wg0 -j ACCEPT"
      - "ip route del ..."
    peers:
      - name: laptop                                # optional, shown as a # comment
        public_key: <peer public key>
        allowed_ips: 10.0.0.2/32                    # string or list of addresses
        endpoint: example.com:51820                 # optional, domain names allowed
        keepalive: 25                               # optional, keep NAT mappings alive
        psk: <preshared_key>                        # optional
      - public_key: <peer public key>
        allowed_ips: [10.0.0.3/32, fd00::44/128]
```

Notes
-----

* **Private keys**: if `private_key` is empty, a key is generated on the first run, persisted to
  `private_key_path` (mode `0600`) and reused on subsequent runs. If a `private_key` is provided,
  it is written as-is. The corresponding **public key is printed** at the end of each interface run.
* **Multiple interfaces**: declare several entries in `wireguard_interfaces`; each becomes its own
  `wg-quick@<name>` service with its own `/etc/wireguard/<name>.conf`.
* **Reload**: the interface service is reloaded only when its `.conf` file changed.

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- hosts: servers
  become: true
  roles:
    - role: wireguard
```

With host variables:

```yaml
---
wireguard_interfaces:
  wg0:
    ip_address: 10.0.0.1/16
    listen_port: 51820
    private_key: <private_key>
    peers:
      - name: laptop
        public_key: <public_key>
        allowed_ips: 10.0.0.2/32
        endpoint: example.com:51820
      - public_key: <public_key>
        allowed_ips: [10.0.0.3/32, fd00::44/128]
```

License
-------

MIT
