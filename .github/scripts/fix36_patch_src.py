import os

os.chdir(os.environ.get('GITHUB_WORKSPACE', '.'))
MARK_L = 'K414LPMBYPASS'
MARK_M = 'K414MALIWARN'

# --- 1) ip_regulator.c: LPM3 enable 失败按成功处理 ---
p = 'drivers/regulator/ip_regulator.c'
s = open(p, encoding='utf-8', errors='surrogateescape').read()
old = 'ret = ip_regulator_cmd_send(dev, REGULATOR_ENABLE);'
assert s.count(old) == 1, 'expected exactly one ENABLE cmd_send, got %d' % s.count(old)
new = ('/* ' + MARK_L + ': EMUI9.1 LPM3 firmware rejects this mailbox IPC (EINVAL); '
       'treat the rail as powered for this probe build */\n'
       '\tret = 0; /* disabled: ' + old + ' */')
s = s.replace(old, new)
open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
print('patched', p)

# --- 2) mali: BUG_ON(1) -> 仅告警 ---
q = ('drivers/gpu/arm/bifrost-r18p0-01rel0/platform/hisilicon/'
     'mali_kbase_config_hisilicon.c')
t = open(q, encoding='utf-8', errors='surrogateescape').read()
oldb = 'BUG_ON(1);'
assert t.count(oldb) == 1, 'expected exactly one BUG_ON(1), got %d' % t.count(oldb)
newb = ('dev_err(kbdev->dev, "' + MARK_M + ': regulator enable failed, '
        'continuing (probe build, GPU unpowered)\\n");')
t = t.replace(oldb, newb)
open(q, 'w', encoding='utf-8', errors='surrogateescape').write(t)
print('patched', q)
