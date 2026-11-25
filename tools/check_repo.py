"""Validate module metadata and local Markdown links from repository root."""
from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
errors=[]
for n in range(13):
 prefix=f'm{n:02d}-';matches=list((root/'modules').glob(prefix+'*'))
 if len(matches)!=1:errors.append(f'{prefix}: expected one module');continue
 path=matches[0];readme=path/'README.md';meta=path/'module.json'
 if not readme.is_file() or not meta.is_file():errors.append(f'{path.name}: missing README or metadata');continue
 try:
  data=json.loads(meta.read_text())
  if data['id']!=f'M{n:02d}' or data['status'] not in ('proposed','draft','verified','deprecated'):
   errors.append(f'{path.name}: invalid metadata')
  for field in ('title','prerequisites','estimated_hours','offline_path','project','last_verified','maintainer'):
   if field not in data:errors.append(f'{path.name}: missing {field}')
  prerequisites=data.get('prerequisites')
  if not isinstance(prerequisites,list) or any(
      not isinstance(prereq,str) or not re.fullmatch(r'M\d\d',prereq)
      or int(prereq[1:])>=n for prereq in prerequisites):
   errors.append(f'{path.name}: invalid or forward prerequisite')
 except (ValueError,KeyError) as exc:errors.append(f'{path.name}: {exc}')
for md in root.rglob('*.md'):
 if '.git' in md.parts:continue
 body=md.read_text(encoding='utf-8')
 for target in re.findall(r'(?<!!)\[[^]]+\]\(([^)]+)\)',body):
  target=target.split('#')[0]
  if target and not re.match(r'^[a-z]+:',target) and not (md.parent/target).exists():
   errors.append(f'{md.relative_to(root)}: broken link {target}')
if errors:
 print('\n'.join(errors));sys.exit(1)
print('module metadata and local links: OK')
