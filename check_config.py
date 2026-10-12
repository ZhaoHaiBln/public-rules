"""Check the public Tower/Stash INI without reading subscription credentials."""
from pathlib import Path
import argparse
import ipaddress
import re
import urllib.request
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('--config', default=str(Path(__file__).with_name('custom_full.ini')))
parser.add_argument('--online', action='store_true', help='Also fetch public rule sources')
args = parser.parse_args()
text = Path(args.config).read_text(encoding='utf-8-sig')
groups = {}
rules = []
for raw in text.splitlines():
    line = raw.strip()
    if line.startswith('custom_proxy_group='):
        fields = line.split('=', 1)[1].split('`')
        name, kind = fields[:2]
        assert name not in groups, f'Duplicate group: {name}'
        assert kind in {'select', 'url-test'}, (name, kind)
        groups[name] = fields[2:]
        for field in fields[2:]:
            if not field.startswith(('[]', 'http://', 'https://')) and not re.fullmatch(r'\d+,,\d+', field):
                re.compile(field)
        if kind == 'url-test':
            assert fields[-2] == 'https://www.gstatic.com/generate_204', name
            assert fields[-1] == '900,,100', name
            assert '[]REJECT' in fields[2:-2], f'Empty group could become DIRECT: {name}'
    elif line.startswith('ruleset='):
        rules.append(line.split('=', 1)[1].split(',', 1))
builtins = {'DIRECT', 'REJECT'}
for name, members in groups.items():
    for field in members:
        if field.startswith('[]'):
            assert field[2:] in groups or field[2:] in builtins, (name, field)
def walk(name, visiting):
    assert name not in visiting, f'Group cycle: {name}'
    for field in groups[name]:
        if field.startswith('[]') and field[2:] in groups:
            walk(field[2:], visiting | {name})
for name in groups:
    walk(name, set())
for alias in ['▶️ YouTube', '🛍️ Google Play']:
    assert groups[alias] == ['[]🌐 Google服务'], alias
assert groups['🌐 Google服务'][0] == '[]🇺🇸 美国-IEPL'
assert groups['✈️ Telegram'][0] == '[]🇭🇰 香港-IEPL'
assert groups['🤖 AI平台'][0] == '[]🇺🇸 美国-IEPL'
assert groups['🎬 Emby'][0] == '[]🇭🇰 香港-IEPL'
assert groups['🛑 广告拦截'][0] == '[]DIRECT'
urls = []
for policy, resource in rules:
    assert policy in groups or policy in builtins, policy
    if resource.startswith('[]'):
        parts = resource[2:].split(',')
        assert parts[0] in {'DOMAIN', 'DOMAIN-SUFFIX', 'IP-CIDR', 'IP-CIDR6', 'GEOIP', 'FINAL'}, resource
        if parts[0] in {'IP-CIDR', 'IP-CIDR6'}:
            ipaddress.ip_network(parts[1])
            assert parts[-1] == 'no-resolve', resource
            assert not parts[1].startswith('198.18.'), resource
    else:
        url = urllib.parse.urlparse(resource)
        assert url.scheme == 'https' and url.netloc == 'raw.githubusercontent.com', resource
        assert url.path.startswith(('/ACL4SSR/ACL4SSR/', '/blackmatrix7/ios_rule_script/')), resource
        urls.append(resource)
assert len(urls) == len(set(urls)), 'Duplicate remote source'
assert rules[-2] == ['🐟 国内漏网', '[]GEOIP,CN']
assert rules[-1] == ['🐟 国外漏网', '[]FINAL']
assert '[General]' in text and 'ipv6=false' in text
assert 'encrypted-dns-server=https://dns.alidns.com/dns-query,https://doh.pub/dns-query' in text
assert not any(old in text for old in ['main/ai.list', 'main/foreign.list', 'main/media.list', 'main/domestic.list', 'main/reject.list'])
if args.online:
    for url in urls:
        with urllib.request.urlopen(url, timeout=20) as response:
            body = response.read(2_000_001)
            assert response.status == 200 and 0 < len(body) <= 2_000_000, url
            content = body.decode('utf-8-sig')
            assert '<html' not in content.lower(), url
            assert any(re.match(r'^(DOMAIN|IP-|PROCESS|GEOIP)', line.strip()) for line in content.splitlines()), url
print(f'PASS: {len(groups)} groups, {len(rules)} rule entries, {len(urls)} public sources')
