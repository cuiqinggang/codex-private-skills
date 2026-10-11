# CODEX-008 ��������֤�ݾ���

��Polsiaִ��ҳ��POLSIA_CAPABILITY_REPLICATION_20261011��CODEX-008��

TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
NODE_ID=CODEX-008_MATURE_FULL_CAPABILITY_COVERAGE
CEO_DISPOSITION_ID=POLSIA-CEO-D007-COMPLETE-COVERAGE-20261012
ENGINE=28
MATRIX_STATUS=COMPLETE_NINE_CATEGORY_FACT_COVERAGE_WITH_SCOPE_LIMIT
FUNCTIONAL_RESULT=REAL_TOOL_EXECUTED_SYNTHETIC_RECONCILIATION_AND_GIT_FILE_RECOVERY
INDEPENDENT_REVIEW=PASS_ISOLATED_FUNCTION_ONLY;evidence/INDEPENDENT_SCENARIO_REVIEW.md
MOTHER_FINAL_VALID=NO
GENERATED_AT_UTC=2026-10-11 17:04:02 UTC

������̳� V001�CV007 ��������ʵ����ˢ�� Polsia �ٷ��������ϡ�����ȫ������������˵���������ʽ��ڡ��ϳ������ϵ���ʵ����ִ�к���ʵ����ҵ���ǲ�֤ͬ�ݲ㡣û��һ�б�ʾȫ��˾ PASS��V008 ����CSV����ִ�С��Ƿ����ܾ���Git���ļ��ָ�������ʵ��ִ�����ܽ׶�ԭ��ִ״̬ PASS_FUNCTIONAL_AWAIT_INDEPENDENT_REVIEW ������������Ķ������״̬�������ף�GitHub����ɽڵ�־û���ִ֤���������þ������߳��������

## ֤����״̬�ھ�

- PUBLIC_CLAIM��Polsia ��������ٷ�ҳ����������棻��֤���ɸ���ҵ��ɹ���
- MATURE_ENTRY���ֳ���ʽ��Ʒ/�ڽ�������ʵ����ڣ�����װ���汾������ HTTP ��ٷ��ĵ�������ҵ��ִ�С�
- LOCAL_EXECUTED_SYNTHETIC��������ȷΪ�ϳɣ�������� Agent ʵ�����в������������ռ�������������ð����ʵ�ͻ�/����/���롣
- LOCAL_DELIVERY��ʵ�����ɲ��������ҵ���ļ���δ���Ͳݸ塢�Ƽ�������ɫ��������ʵ�ظ����˹�������
- UNKNOWN/NOT_TESTED/UNAUTHORIZED���ֱ��ʾ֤�ݲ��㡢δ���С���ǰȱ��Ҫ��Ȩ�����úϲ�Ϊʧ�ܣ�Ҳ��������Ϊ����ɡ�
- HISTORICAL_ONLY������ɽڵ���ʵ�����̳У����ڵ㲻���ܾ�ý�塢��ʮ�ֻ���ļ���ͻ������

��ǰ�����Ͱ���ҳֱ����ֻ���� JavaScript ��ǣ����� UI UNKNOWN�������ɴ��жϲ�Ʒ���ߡ�deck ��ֱ�Ӷ������ģ�����ҳ/�Ӵ�����������Ϣֻ�����������棬������ȷ��ע����ԴԪ���ݡ����ʲ�𡢶�ժ¼���ٷ� URL �� [OFFICIAL_SOURCE_EVIDENCE.json](research/OFFICIAL_SOURCE_EVIDENCE.json)����ȥ����/��ֵ��������Ϊ�����������ݣ������������о����ʡ�

## ����̶�����

| ��� | Polsia �ٷ��������� | ���г�����������ò㼶 | ��ʷʵ�ʳɹ���ҵ��ɹ���Χ | V008 ��ʵ���� | ����������Ϸ���֤ |
|---|---|---|---|---|---|
| 1. ���̿����� BUG �޸� | [deck](https://polsia.com/deck)�й��̡�BUG���ʹ�������/�޸���[�Ӵ���������](https://polsia.com/subprocessors)������������ GitHub ���ɺ� Sentry ��ϡ����ڹ��������� | ��ǰ Codex ԭ������/����/�� Agent ����ʽ GitHub �������ɸ��ã����� PowerShell/Git �ǳ��� CLI��n8n [GitHub �ڽ��ڵ�](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.github)�ǹٷ����ܺ�ѡ���䱾��ƾ��/ҵ���� UNKNOWN�� | �ɽڵ�һ�����ļ�У��/�鵵�ű�ȷʵ���У���ʵ��ָ�� GitHub ��ִ�ɶ���V3ֻ���ع�֤ʵ�ض� CRLF/�����ϣ�������������������BUG��λ���޸����ع���ܿؽ�����ҵ���ͬδ�顣 | ��ҵ���ض�PowerShellУ����ʵ���У���ȫ�����ܾ���Git�ָ������ļ��ֽ�һ�£���[���ܻ�ִ](evidence/FIN008_FUNCTIONAL_RESULT.json)������ҵ���������ļ��ָ�����������BUG�ջ���UNKNOWN�� | ���ܰѹ��߳ɹ����ļ��ָ��������з���������һ�Ϸ���֤�����в��Բ�/Ӧ���е���ȷ BUG������ʧ�ܸ��ֺ�Ԥ�ڣ��ֳ� Codex/Git ִ���޸����������գ��������跶Χ��Ȩ�ޡ� |
| 2. �о���Ӫ�������ݷ��� | [deck](https://polsia.com/deck)���о���Meta������ý��[����ʽ����](https://help.polsia.com/add-funds-to-your-ads-balance)�������������ʽ�����ͣ�ͻָ��� | ���й����о����ߡ��ֳ�ý�� CLI/��������ʷ����ģ�壻���� n8n �ٷ���ý/�������������ѡ����֤�����������á��Ӵ����߻����� Late.dev ��ý�ӿڣ�δ���ӡ� | �����о�/��Դȥ�ء�NASA ������������/��Ӫ���� V004-F002 ����ʷ��ʵ��V005�CV007���þ����ݡ�ʵ���ϴ���Ͷ�š����ڡ����ڷ�������� UNKNOWN�� | RESEARCH_REFRESH�������ٷ�����/�ӿڱ߽���أ�NEW_MEDIA_EXECUTION=0�����������ơ�probe�������ý�壬���Դ˴��о�ð�䷢���ɹ��� | ��վ/����/����������ݣ��������˻����ӡ�����ֵ��������ǰ��ִ�С����������ü��йٷ�ƽ̨�� preview/draft/test ������֤δ�������ݣ���ʵ��������ȷ��Ȩ��������ִ�� |
| 3. �ͷ����˹����� | [deck](https://polsia.com/deck)�� Support��[�տ����](https://help.polsia.com/accept-payments-on-your-site)����������ȷ�˿���Ҫ��ϵ֧�֣���ʾ�˹�����Դ��ڡ� | V005 ���� FAQ/�ظ��ꡢ֤��Ŀ¼�������嵥����ǰ Codex��Hermes ��ʽ�����ʷ health �ɼ�����ʵ��ģ��/����ҵ��δ֤ʵ��n8n���й���/�ͷ���ڴ��ˡ� | V005 ʵ�ʽ���21�ļ���18��FAQ/���16��ϳ�˫��ݸ壬������ PASS_WITH_SCOPE_LIMIT��12��������ɫ���send=NOT_SENT��handoff=NOT_PERFORMED���˹�����/��ʵ�ر� UNKNOWN�� | ��[����Agent����](scenario/agent/FINANCE_ESCALATION.md)ʵ�������ظ������֡�������ˮ������/δ��/�������˹��˲齨�飻δ���͡�δ�ɵ���δ�˿ֻ֤����������׼�����������״̬�����ס� | ��ʵ�ͷ�������SLA�������رպ��˹�����û��֤�ݡ���һ�Ϸ���֤�Ȳ����ֳɹ���ϵͳ���в��Կռ�/ɳ�м�¼����ֻ��֤δ���Ͳݸ�ͽ�ɫ·�ɣ���ʽ��������������Ȩ�� |
| 4. ���ۻ�� | [deck](https://polsia.com/deck)�� Cold Outreach��[���԰���](https://help.polsia.com/polish-interface)������������ outreach ���������ԡ�û�й����ɸ����ɽ�/�ͻ��������ա� | V006�����ʸ�/����/�᰸ģ���뵱ǰ Codex������ n8n CRM/�ʼ��ٷ������Ǻ�ѡ����ǰ�˺�/�̶����� UNKNOWN�� | V006 19�ļ���12���ϳ������ʵ���ʸ�/˫��ݸ��Ѷ������ܣ����ݡ��������۸񡢺�ͬ�������˾� null��δ���͡�δ���ӡ�FIT_OFFLINEֻ�������߷�Χƥ�䡣 | NOT_TESTED_FOR_LEAD_ACQUISITION�����ڵ�����������䵱��ʵǱ�͡��������롢CRM��ͨ��ת���� | ��ɾ����������������Ǳ����Դ����ϵ�Ϸ��ԡ�CRM���Կռ䡢ȥ��/�����ֶκ��˹���׼ȱ�ڡ�����ʹ������ CRM ɳ��/���ص���Ԥ����ֻ��Ǳ���о���֤����ֹδ��Ȩʵ�������� |
| 5. ����֧������� | [deck](https://polsia.com/deck)�� Payments��[�ͻ��տ����](https://help.polsia.com/accept-payments-on-your-site)��������˵�� Stripe����/�����������˹��˿[����ʽ����](https://help.polsia.com/add-funds-to-your-ads-balance)���������ʽ������Metaʵ��Ͷ�ſɿ��ղ�ͬ�� | �����ֳ� PowerShell [Import-Csv](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/import-csv?view=powershell-7.5) + ��ǰ Codex ����������ˣ�n8n [Stripe�ڵ�](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.stripe)�ٷ���balance/charge�ӿڣ����ޱ�������֤����֤�ݡ� | V001�CV007�޸���˿��ʵ������������ͨ�����ҵ����ԣ����ౣ�� UNKNOWN�����������޿ͻ���ȡ���� | FUNCTIONAL_REAL_EXECUTED_AWAIT_REVIEW��[�˵����](scenario/output/ledger.csv)7�źϳ��˵���[��ˮȥ��](scenario/output/payment-routing.csv)9�У��Ѷ�ƽ2������/δ��/����/���ֺ˲�/�ظ��˲��1���ظ�2�С�����1�С�����1�и��롣����Agent��������ԭ���룬δ�����������[���߻�ִ](evidence/FIN008_FUNCTIONAL_RESULT.json)������ҵ��1��/����0�Σ�ֻ�ޱ��ع����������� | ��ǰ�ɹ������ߺϳɲ�����˼�������������ʵ�ʽ�/����/�˿�/���нӿڼ���UNKNOWN/UNAUTHORIZED����������������֧���ṩ����ʽ sandbox/test mode ��ֻ������������ȡ/����ƾ�ݣ�����ģ�⸶�����콻�ס� |
| 6. �� Agent�������������� | [deck](https://polsia.com/deck)�������ִ���ִ�У���������û�п��ز����������롢Exactly-once�Ϳ�Ự�������ա� | ��ǰ Codex �ٷ��ڽ�ί��ʵ�ʿɵ��ã��ֳ� n8n �̶��������Ȳ飬ԭ�� [Executions](https://docs.n8n.io/build/understand-workflows/understand-executions.md)���ṩ������ʷ��Windows��������/runner���̳У����½���������ϵͳ�� | �ɽڵ���ʵ��ͬAgent�ֱ��д�������飻V007�ݸ�/��ͨ����������顣�������в��п���Ȼ�ڵ���ʵ���������Ƴ��๫˾����/72Сʱ�ȶ��� | ��ǰ�о�ί����[�����������Agent](scenario/agent/AGENT_FINANCE_RECEIPT.json)����ʵ���أ�����SHA�󶨲�����δ�����߽ű�/������������������һ������ִ�У�״̬�����ס�n8n��ǰ401/Docker�ܾ���ִ��0�Ρ��������ܺ���Դ����δ�⡣ | ��Agent�������ǹ�˾ҵ��ɹ���ȡ��/��ʱ/��Դ��ռ/��Ự�ָ�/��������UNKNOWN���������ùٷ�ԭ����Agent���Ѻ˶��̶� n8n ���̣���ͬ�������Դ�߽��¼�¼���ء���ʱ���ָ���ҵ����������������/��/���С� |
| 7. ������Ӫ�������� | [deck](https://polsia.com/deck)����BUG���������ϣ��Ӵ����߻����� Sentry����ң�⡣û�е�ǰ�������ɱ����/ҵ��һ������֤�� | ���� Windows�ƻ�����/��־��[Get-ScheduledTaskInfo](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/get-scheduledtaskinfo?view=windowsserver2025-ps)�ɶ�������Ϣ��GitHub�ٷ�Contents+SHA/Blob��ִ��Codex���߻�ִ��n8n executions/��������Ϊ��ѡ�� | �ɽڵ��������˳������/manifest������������GitHub�ض���V3ֻ���ع���֤parser��LF/CRLF/����SHA���䷢���뵱ǰlive�����ֿ���60��״̬��ֻ֤��չʾ/��ѯ���������ܾ�Ӫ��ء� | �·Ƿ������ʵ�˳�1��д[guard�¼�](evidence/GUARD_INCIDENTS.jsonl)������������ļ���SHA���/�ָ���ִ���ڡ���ǰ[ֻ��probe](probes/MATURE_COMPONENT_PROBE.md)��¼�����ѯ�ܾ���Operational��־�رա�runtimeָ��3.0/liveͷ3.1���죻GitHub����Խڵ�־û���ִΪ׼�� | ����ֱ��¼����״̬��ҵ���������ϸ澯��֤�������ԡ�Exactly-once��ָ����ߣ��±������ϵ�/72Сʱ���ȳ���δͨ���������ȸ����ֳ�execution/log/�����ѯ��ֻ�ںϷ�������������֤�澯��ʵ��ҵ���ж������Խ���ط��� |
| 8. �쳣�ָ��������ж�����ָ� | [deck](https://polsia.com/deck)���ƻ�����ʩ������[���ָ�ϰ���](https://help.polsia.com/your-design-guide)������������������ȡʧ�ܽ���/�������ĵ�����Χ�����ĵ����ܡ� | safe-file-demo��ԭCLI��ͻ�ָ���ԭ�� [Git restore](https://git-scm.com/docs/git-restore)�ɻָ�ָ������·����n8n [Error Workflow](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully.md)/[Wait](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait)�ֳɻ��ƴ�����ڡ� | V001���ļ�Ŀ¼��ͻ��10��ֻ�޺ϳ��ļ��ָ���V002ԴURI/��ȡ�ָ���ʷPASS��V003������/ȱ�ڷ�����δע���¹��ϡ�V3 readonly�����ع鲻�������������ϵ�ָ��� | ��[���ܻ�ִ](evidence/FIN008_FUNCTIONAL_RESULT.json)��¼����ledger�����ضϺ��SHA�仯����֪commitԭ��git restore�ָ�����ͬSHA��ҵ��ִ��1��������0�Σ������ܾ��������������FUNCTIONAL_AWAIT_REVIEW��ֻ���ļ����ָ�����������/������ | ���̱�����д��ʱUNKNOWN�����ύ���ϵ��72Сʱδ��֤��WaitС��65�벻ת��DB�����ܾݶ̵ȴ���������ȫ����һ�Ϸ���֤��������ʽ��Ʒ�Ĳ���ִ�м�¼/�ָ��ӿںͰ�ȫ�жϣ����ܹػ������������ؽ��ָ������� |
| 9. ����ѧϰ�뼼�ܳ��� | [deck](https://polsia.com/deck)���ƿ繫˾��������к�ѧϰ��[���԰���](https://help.polsia.com/polish-interface)����˵���ĵ��汾/�������ã��������Ƴ�ѧϰЧ���� | �ֳ�Knowledge Brain����������/������ԭ�������Ͱ汾����Ŀ֤�ݿɸ��ã���ʽSkill����/manifest����ԭ���޸ġ� | ���а������������ж�����أ�KB health��ʷPASS��V005�CV007����Ϊ��Ŀ����/����֤�ݣ�δ������Skill����³����������ܿس�������/���������UNKNOWN�� | �����������ٷ���Դ���ʱ߽硢�����ּ��Ϸ���֤��ڣ��Ƿ����ܾ���ԭ��Git�ָ���n8n���Ȩ�޲����Ϊ�¿ɸ��龭�顣��������Ŀ��ʵ���������Զ�ѧϰ���������л���Skill�Ѳ��� | ��һ�Ϸ���֤�����ֳɰ汾�����򽫱���ʵ��ʧ����ڡ��ָ����ߺ�checklist����һ�ڵ����ã�����Skill����/�汾�����붨��֪ʶ������̡�ֻ��������ʵ�����в�����������֤�ݣ����ܳƸ�����Ч�������¼���ƽ̨�� |

## ���ܼ�ص������ж���

| �ж��� | ������ʽ���/Ӧ��ȡ��֤�� | ��������ȷ�ϵ���ʵ | ��ǰȱ������ʵ���� |
|---|---|---|---|
| ����״̬ | Windows����״̬���������ʱ��/��������̡�ԭ��Codex���߻�ִ | V007β���˳�0����ǰn8n health/readiness200�������ѯHRESULT 0x80041003�ܾ���Codexԭ��־����д�롣���в�ָ��3.0��live���3.1ͷ��ͬ | ���߽׶�ʵ����ֹ/�˳��Ѽ�¼������������/��ǰ״̬UNKNOWN��δ��ϵͳ��ѯȨ�� |
| ҵ���� | �������롢ʵ�������ҵ�����ͷ��������� | ��7�˵�/9��ˮ��ʵ���������Agentԭ���������ѷ��أ�ʵ�ʵ�����UNKNOWN | �������״̬�����ף�n8nҵ��ִ��0��/���UNKNOWN |
| ���ϸ澯 | ԭ��stderr/�˳���SHA���졢�ֳ�Executions/Error Trigger | �Ƿ�����˳�1��guard FAILURE_OPENED�¼����ļ���SHAȷʵ�����δ������Ϣ����/�¹�SLA | ����BAD/FIRST_DELTA��ԭ��TaskScheduler/Operational��ǰ�رգ�δ���� |
| ֤�������� | ����SHA�����manifest����ִ��ԭ�ֽں�BlobУ�� | ������SHA�����ܻ�ִ��������������󶨴��ڣ�Git�ָ�����֪SHA��ͬ | ����������оٻ�ִ��manifest��Freeze��GitHubԭ�ֽڽ���ɽڵ���Ӧ��ִ֤�����������߳������ |
| Exactly-once | �Ȳ�CURRENT/MOTHER/Freeze/ִ�л�ִ��DONE��������UNKNOWN�ȶ��� | V007 CONFIRMED_DONE_WITH_SCOPE_LIMIT������INFLIGHT����V008��������ҵ��1�Ρ�����0�Σ��ⲿδ���� | V008�ύǰ���Ȳ�ٷ�״̬�������ظ�Freeze/ָ�룻�ⲿ����Exactly-once UNKNOWN |
| �ָ����� | CONFIRMED_DONE/CONFIRMED_NOT_DONE/UNKNOWN��ԭ���ָ���ں͸��� | ���븱���𻵶�ԭGit commit���ڣ�ԭ��restore�ָ�SHA���������δ�������ǣ�δ����ҵ�� | �ļ������ָܻ�����ʵ��ִ����ָ�/�ϵ�/72h��UNKNOWN |

n8n����������ִ��id/url�����������ݣ������ڵ�ʧ��ʱ�ֶο��ܲ�ͬ���ʲ����Կ��ֶζ���δִ�У��ٷ�[������˵��](https://docs.n8n.io/build/flow-logic/handle-errors-gracefully.md)֧�ִ˱߽硣�ٷ�[Wait˵��](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait)ָ��С��65��ȴ���ת�����ݿ⣬�̵ȴ����Բ����Զ�֤���ϵ�/�����ָ���

## ����·�ߺͶ���ǰԼ��

���ڵ��һ��ѡ���� n8n �̶������Ѳ飺health/readiness HTTP200����/rest/workflows HTTP401��Docker�ܵ�Ȩ�޾ܾ�����ȷ�汾���������̵�ǰ�ڵ�/������UNKNOWN����ʷactive Reasonix webhook�뱾��ͬ������û�д����κ����̡�����GOOD/BAD/FIRST_DELTA��ԭ��ִ��[�������probe](probes/MATURE_COMPONENT_PROBE.md)������ִ��ǰȨ��ȱ����Ϊҵ��ʧ�ܡ���ѡ��ǰCodex + ԭ��PowerShell/Git + GitHub��ʵ��ִ·��������ʵ���ܻ�ִ���������״̬�����ס����2������·�ߣ�û��������̨�����ݿ⡢���ȡ��������Ի��ط���

����������ڵ�T_VALID=UNKNOWN_AT_MATRIX_CUTOFF�������ڵ�����ɸ��������ձ����������ʵ[���߼о߻�ִ](evidence/FIN008_FUNCTIONAL_RESULT.json)Ϊ5.0504�룬����guard����2.3792�롢�Ƿ����guard����2.2022�롢ԭ��git restore����0.0529�룻��Щ�ֶα߽粻ͬ��δ��ȫ�����䡢Agent����������ͷ�棬���������ڵ�T_VALID���о���ʱ����ý��ʱ��;ֲ����ʱ�䲻����������ܲ������ֶ�UNKNOWN��������ROI��ָ��û���ͣ�������Ž���

## ʣ��Ϸ���֤���

1. n8n����������Ȩֻ��ͨ���˵�ǰ�̶��������ݡ��ڵ�͸����ã��ٶ������ԭ���������ִ�У���ǰ401/�ܵ��ܾ�֤�ݱ�����������ƾ�ݻ��ƹ��ܾ���
2. ����/�ͷ�/����/�������Ȳ����ֳ���ʽ��Ʒ�����õ�sandbox��draft��preview��ֻ����������ʵ�˻�������/����˹��ռ��������͹�������������Ȩȱ�ڡ�
3. ���̣����в��Բ��е���ȷBUG����ʧ�ܸ��֡��ֳ��޸���ںͷ����߻ع���֤�ƽ�������Git�ļ��ָ�������������ͬ��
4. �ָ�/��أ�ԭ�ƻ�����native executions/log�����лָ����Ʒֱ�����С�ҵ�񡢸澯�������ԡ�Exactly-once����ߣ���ǰtask��ѯ�ܾ����¼�ͨ���رա�runtime����Ư�Ʋ��ڻ�ڵ��ȸġ��ϵ硢OS������72Сʱ�ȶ�����UNKNOWN��
5. ѧϰ�����˴���ʵʧ�����/�ָ�checklist���ֳɰ汾��������һ�������ã�����Skill��ԭ�ģ���������/����������ʵ��֤�ݡ�ĸ����FINAL_VALID����NO��

Knowledge Brain usage:
- INDEX checked: YES��C����ʽԴ�����ȡ��
- ROUTING_MAP checked: YES��
- Relevant indexes checked: skills-index.md�����ȡ��Top-KΪ����������CAPABILITY_MATRIX/REUSE_MAP��V003/V005/V006/V007��ʵ��V3���в��ִ��
- CodeGraph used where relevant: NOT_APPLICABLE����������ı�/������Դ֤�ݡ�
- OpenHuman reference used where relevant: NOT_APPLICABLE��δ��Ƽ���ܹ���
- Sync run before/after: NO_SYNC��δ��KB/Skill/������health�ɸ������ڵ���βͳһ��¼��
- If not used, reason: ��ʹ�ö���·�ɣ�ֻC�̣���H/K��ȡ/д�룬��ȫ��ɨ�衣

��Polsiaִ��ҳ��POLSIA_CAPABILITY_REPLICATION_20261011��CODEX-008��


