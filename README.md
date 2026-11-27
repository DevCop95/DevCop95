<div align="center">
<img src="assets/img/dev101x_banner.png" alt="DEV101X banner" width="100%" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=20&pause=1200&color=EF4444&center=true&vCenter=true&width=720&lines=Detection+Engineering+%26+Applied+AI+Security;LOLBAS+%C2%B7+Atomic+Red+Team+%C2%B7+Microsoft+Sentinel+%C2%B7+LOLRMM+%C2%B7+Maigret;Penetration+Tester+%40+Henkel+%C2%B7+M.Sc.+AI+(UB)" alt="Typing SVG"/>

[![Portfolio](https://img.shields.io/badge/Portfolio-dev101x.online-ef4444?style=flat-square&logo=googlechrome&logoColor=white)](https://dev101x.online/)
[![Research Deep Dives](https://img.shields.io/badge/Research-Deep_Dives-00e87a?style=flat-square&logo=gitbook&logoColor=black)](https://dev101x.online/research/)
[![LOLBAS Contributor](https://img.shields.io/badge/LOLBAS-3_PRs_Merged-00c466?style=flat-square&logo=github&logoColor=white)](https://github.com/LOLBAS-Project/LOLBAS/pulls?q=is%3Apr+author%3ADevCop95+is%3Amerged)
[![Atomic Red Team Contributor](https://img.shields.io/badge/Atomic_Red_Team-2_PRs_Merged-d00000?style=flat-square&logo=github&logoColor=white)](https://github.com/redcanaryco/atomic-red-team/pulls?q=is%3Apr+author%3ADevCop95+is%3Amerged)
[![Microsoft Sentinel Contributor](https://img.shields.io/badge/Microsoft_Sentinel-PR_%2315693_Merged-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)](https://github.com/Azure/Azure-Sentinel/pull/15693)
[![LOLRMM Contributor](https://img.shields.io/badge/LOLRMM-PR_%23253-0ea5e9?style=flat-square&logo=github&logoColor=white)](https://github.com/magicsword-io/LOLRMM/pull/253)
[![Maigret Contributor](https://img.shields.io/badge/Maigret-7_PRs_Merged-8957e5?style=flat-square&logo=github&logoColor=white)](https://github.com/soxoj/maigret/pulls?q=is%3Apr+author%3ADevCop95+is%3Amerged)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-yared--dev-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yared-dev)
[![X](https://img.shields.io/badge/@Devcop101-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/Devcop101)
[![Email](https://img.shields.io/badge/Email-yared.henriquezb-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:yared.henriquezb@gmail.com)
[![Profile views](https://komarev.com/ghpvc/?username=DevCop95&style=flat-square&color=ef4444&label=views&v=1795716000)](https://github.com/DevCop95)

</div>

---

```bash
dev101x@kali:~$ whoami
```

**Yared Henriquez (`DevCop95` / `Dev101x`)** — Security Researcher specializing in **Detection Engineering (Offense-to-Defense)** and **Applied AI Security**, based in **Cartagena, Colombia** 🇨🇴. Currently a Penetration Tester at **Henkel** (Switzerland · Remote) and M.Sc. in Artificial Intelligence candidate at **Universitat de Barcelona**.

```bash
dev101x@kali:~$ cat focus.txt
```

- 🛡️ **Detection Engineering & Threat Emulation:** Full *Offense → Emulation → Detection* lifecycle across Windows LOLBins and RMM tooling (**LOLBAS**, **LOLRMM**, **Red Canary Atomic Red Team**, **SigmaHQ**, **Elastic Security**, **Microsoft Sentinel**) and endpoint kernel-handle correlation (**[`BDB-Guardian`](https://github.com/DevCop95/BDB-Guardian)**, cited by **CUHK ITSC**).
- 🤖 **Applied AI Security:** Multi-layer security review skills for coding agents (**[`cyhber-deploy`](https://github.com/DevCop95/cyhber-deploy)**, Grade A on SkillsDirectory), LLM guardrail robustness evaluation (**[`promt`](https://github.com/DevCop95/promt)**), and upstream AI red-teaming tooling (**`NVIDIA/garak`**).
- 🎯 **Offensive Security & Automation:** Authorized corporate penetration testing, **HackerOne** private programs, and scope-enforced recon/post-exploitation auditing (**[`bugbounty-lab101`](https://github.com/DevCop95/bugbounty-lab101)**, **[`pullgoscript`](https://github.com/DevCop95/pullgoscript)**, **[`shodan_reconsx`](https://github.com/DevCop95/shodan_reconsx)**).
- 🤝 Open to **Detection Engineering**, **Threat Research**, and **Applied AI Security** collaborations — 📫 [yared.henriquezb@gmail.com](mailto:yared.henriquezb@gmail.com).

> ⚠️ **Authorized use only.** Every offensive/security tool linked below is built for use in scoped engagements, CTFs, bug bounty programs and environments the operator owns or is authorized to test. None of it is intended for use against systems without explicit permission.

---

## 🔬 Featured Research (Deep Dives)

1. **[Abusing Windows OpenSSH (`KnownHostsCommand` & `PermitLocalCommand`) and Closing First-Match-Wins Detection Bypasses in KQL & Sigma](https://dev101x.online/research/windows-openssh-indirect-execution/)**  
   `LOLBAS #539/#532` (Merged) → `Azure/Azure-Sentinel #15693` (Merged) → `SigmaHQ #6585` · Covers pre-auth vs. post-auth `ssh.exe` vectors, `-F`/`.ssh/config` child-process lineage, pure-RE2 automaton closing OpenSSH first-match-wins evasion, and 21-case Azure Data Explorer validation (`12/12` TP, `0/9` FP).
2. **[From Disk-Exhaustion DoS against Windows Defender (`fsutil.exe` / BigDiskBuster) to Multi-SIEM & Kernel-Handle Detection](https://dev101x.online/research/bigdiskbuster-fsutil-defense-evasion/)**  
   `BDB-Guardian` (CUHK ITSC cited) → `LOLBAS #525` (Merged) → `Atomic Red Team #3439` (Merged, `T1685`) → `SigmaHQ #6310` (Approved) → `Elastic #6946` (Approved ×2) · Covers native NT vs. LOLBin disk exhaustion, fixing `0xC0000374` (`RM_PROCESS_INFO`) and pipe deadlocks in Win32 handle correlation, safe emulation, and multi-SIEM detection.

---

## 🛡️ Upstream Contributions & Recognition

<div align="center">
  <a href="https://github.com/LOLBAS-Project/LOLBAS/pulls?q=is%3Apr+author%3ADevCop95+is%3Amerged">
    <img src="./assets/img/lolbas_devcop95_banner.jpg" alt="LOLBAS Contribution Banner" width="100%" />
  </a>
</div>

| Upstream Project | Technique & Emulation Scope | Pull Requests | MITRE ATT&CK / Domain |
|---|---|---|---|
| 🛡️ [**LOLBAS Project · LOLBAS**](https://github.com/LOLBAS-Project/LOLBAS) | `Fsutil.exe` (`file createnew` Defender disk exhaustion) & `Ssh.exe` (`KnownHostsCommand` pre-auth / `PermitLocalCommand` post-auth execution) | [![3 PRs Merged](https://img.shields.io/badge/3_PRs-MERGED-8957e5?style=flat-square&logo=github&logoColor=white)](https://github.com/LOLBAS-Project/LOLBAS/pulls?q=is%3Apr+author%3ADevCop95+is%3Amerged) | [T1685](https://attack.mitre.org/techniques/T1685/) · [T1202](https://attack.mitre.org/techniques/T1202/) |
| ☁️ [**Microsoft · Azure-Sentinel**](https://github.com/Azure/Azure-Sentinel) | `SshIndirectCommandExecution.yaml` M365 Defender KQL hunting query for Windows OpenSSH (`KnownHostsCommand`, `PermitLocalCommand`/`LocalCommand`, `ProxyCommand`, `-F`/`.ssh/config` child lineage & pure-RE2 first-match-wins defense; 21-case ADX `12/12` TP, `0/9` FP) | [![PR #15693 Merged](https://img.shields.io/badge/PR_%2315693-MERGED-8957e5?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/Azure-Sentinel/pull/15693) | [T1202](https://attack.mitre.org/techniques/T1202/) · [T1059](https://attack.mitre.org/techniques/T1059/) |
| 🔴 [**Red Canary · Atomic Red Team**](https://github.com/redcanaryco/atomic-red-team) | Multi-platform KeePass credential discovery/staging (`KeePass.config.xml`) & Windows Defender `%TEMP%` disk-exhaustion emulation | [![2 PRs Merged](https://img.shields.io/badge/2_PRs-MERGED-8957e5?style=flat-square&logo=github&logoColor=white)](https://github.com/redcanaryco/atomic-red-team/pulls?q=is%3Apr+author%3ADevCop95+is%3Amerged) | [T1555.005](https://attack.mitre.org/techniques/T1555/005/) · [T1685](https://attack.mitre.org/techniques/T1685/) |
| 🗡️ [**magicsword-io · LOLRMM**](https://github.com/magicsword-io/LOLRMM) | AnyDesk custom per-org client coverage (`ad_*`), service normalization, EventLog 7045 telemetry & Sigma detection rules | [![PR #253 Merged](https://img.shields.io/badge/PR_%23253-MERGED-8957e5?style=flat-square&logo=github&logoColor=white)](https://github.com/magicsword-io/LOLRMM/pull/253) | [T1219](https://attack.mitre.org/techniques/T1219/) |
| 🕵️ [**soxoj · maigret**](https://github.com/soxoj/maigret) | OSINT false-positive elimination (`Freelance.habr`, `Rlocman`, `Starsonice`/`Terminatorium`, `sanatorii`/`RussianFI`, `Dota2`), Imunify360/Stile HTTP-200 bot-challenge detection & `soupsieve ^4.0` security upgrade | [![7 PRs Merged](https://img.shields.io/badge/7_PRs-MERGED-8957e5?style=flat-square&logo=github&logoColor=white)](https://github.com/soxoj/maigret/pulls?q=is%3Apr+author%3ADevCop95+is%3Amerged) | OSINT · Signal Integrity |

**Active Upstream Review Pipeline:** [`elastic/detection-rules #6946`](https://github.com/elastic/detection-rules/pull/6946) (`APPROVED` ×2) · [`SigmaHQ/sigma #6310`](https://github.com/SigmaHQ/sigma/pull/6310) & [`#6323`](https://github.com/SigmaHQ/sigma/pull/6323) (`APPROVED`, awaiting 2nd review) + [`#6585`](https://github.com/SigmaHQ/sigma/pull/6585) · [`NVIDIA/garak #2357`](https://github.com/NVIDIA/garak/pull/2357) (`22/22` CI).

---

## 🚀 Security & AI Engineering Arsenal

<div align="center">

[![bugbounty-lab101](./assets/stats/pin-bugbounty-lab101.svg)](https://github.com/DevCop95/bugbounty-lab101)
<br>
[![bugbounty-lab101 Stars](https://img.shields.io/github/stars/DevCop95/bugbounty-lab101?style=for-the-badge&logo=github&label=Stars&labelColor=0d1117&color=ef4444&v=1795716000)](https://github.com/DevCop95/bugbounty-lab101/stargazers)
[![bugbounty-lab101 Forks](https://img.shields.io/github/forks/DevCop95/bugbounty-lab101?style=for-the-badge&logo=github&label=Forks&labelColor=0d1117&color=494649&v=1795716000)](https://github.com/DevCop95/bugbounty-lab101/network/members)

<br>

[![shodan_reconsx](./assets/stats/pin-shodan_reconsx.svg)](https://github.com/DevCop95/shodan_reconsx)
<br>
[![shodan_reconsx Stars](https://img.shields.io/github/stars/DevCop95/shodan_reconsx?style=for-the-badge&logo=github&label=Stars&labelColor=0d1117&color=ef4444&v=1795716000)](https://github.com/DevCop95/shodan_reconsx/stargazers)
[![shodan_reconsx Forks](https://img.shields.io/github/forks/DevCop95/shodan_reconsx?style=for-the-badge&logo=github&label=Forks&labelColor=0d1117&color=494649&v=1795716000)](https://github.com/DevCop95/shodan_reconsx/network/members)

</div>

| Project | Stack | Description |
|---|---|---|
| 🏹 [**bugbounty-lab101**](https://github.com/DevCop95/bugbounty-lab101) | `Shell` · `Recon` | Scope-enforced bug bounty workspace: automated recon/vuln pipeline, report templates, CVE/CWE watchlists |
| 🛡️ [**BDB-Guardian**](https://github.com/DevCop95/BDB-Guardian) | `PowerShell` · `Win32/C#` | Windows Defender DoS defensive monitor correlating `MRT.exe` + volume handles (cited by CUHK ITSC, LOLBAS #525 & Atomic #3439) |
| 🔒 [**pullgoscript**](https://github.com/DevCop95/pullgoscript) | `Go` · `Assembly` | Windows credential-exposure audit toolkit & hardened `127.0.0.1` console with fuzzing & `gosec` (`T1003`/`T1555`/`T1547`/`T1055`) |
| 🤖 [**cyhber-deploy**](https://github.com/DevCop95/cyhber-deploy) | `Python` · `AI Sec` | Multi-layer security review skill for AI coding agents (`Grade A` on SkillsDirectory; packaged in `agents.nix`) |
| 🔍 [**shodan_reconsx**](https://github.com/DevCop95/shodan_reconsx) | `Python` · `OSINT` | Zero-dependency passive hostname reconnaissance via `ctl.shodan.io` (`unittest` + CI) |
| 🧪 [**dev101x-pentest-lab**](https://github.com/DevCop95/dev101x-pentest-lab) | `Docker` · `Python` | Self-contained Pro Lab box: blind SQLi → internal network pivot → SUID privesc, with live flag engine |

---

## 🛠️ Tech Stack

<div align="center">

**Detection & Threat Engineering**

![MITRE ATT&CK](https://img.shields.io/badge/MITRE_ATT%26CK-C8102E?style=for-the-badge)
![Sigma](https://img.shields.io/badge/Sigma_Rules-00A8E8?style=for-the-badge)
![KQL](https://img.shields.io/badge/KQL_Sentinel_%2F_MDE-0078D4?style=for-the-badge)
![Elastic EQL](https://img.shields.io/badge/Elastic_EQL-005571?style=for-the-badge&logo=elastic&logoColor=white)
![PowerShell](https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge)

**Systems, Offensive & Applied AI**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![Assembly](https://img.shields.io/badge/Assembly-6E4C13?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

</div>

---

## 💼 Experience

| Period | Role | Company |
|---|---|---|
| 2026 — present | 🛡️ Penetration Tester | Henkel · Switzerland (Remote · Part-time) |
| 2022 — 2025 | 🏢 Chief Technology Officer | EXIA S.A.S — Cartagena, CO |
| 2021 — 2024 | 💻 Associate Software Developer (QA & Testing) | Google (Affiliate / Extended Workforce) |
| 2020 — present | 🚀 Freelance · Offensive Security & AI | Independent |

## 🎓 Education

| Period | Degree | Institution |
|---|---|---|
| 2024 — present | 🤖 Master's in Artificial Intelligence | Universitat de Barcelona |
| 2017 — 2021 | 🎓 Systems & Computer Engineering | Universidad Tecnológica de Bolívar |
| 2013 — 2017 | 💡 Systems & Computer Technology | Universidad Tecnológica de Bolívar |

---

## 📊 GitHub Stats

<div align="center">

<img height="170" src="./assets/stats/github-stats.svg" alt="DevCop95's GitHub stats" />
&nbsp;
<img height="170" src="./assets/stats/top-langs.svg" alt="DevCop95's most used languages" />

</div>

---

## 🎯 HackTheBox

<div align="center">

<a href="https://profile.hackthebox.com/profile/019f8d0f-a8d2-73bb-8f12-d863b7261aa3">
  <img src="assets/img/htb_stats.png" alt="dev101x on HackTheBox — Pro Hacker, Top 2 Colombia" width="640" />
</a>

<br>

[![HTB Rank](https://img.shields.io/badge/Rank-Pro_Hacker-9FEF00?style=for-the-badge&logo=hackthebox&logoColor=black&labelColor=0d1117)](https://profile.hackthebox.com/profile/019f8d0f-a8d2-73bb-8f12-d863b7261aa3)
[![HTB Country Ranking](https://img.shields.io/badge/Colombia-Top_2-ef4444?style=for-the-badge&labelColor=0d1117)](https://profile.hackthebox.com/profile/019f8d0f-a8d2-73bb-8f12-d863b7261aa3)
[![HTB Profile](https://img.shields.io/badge/View_live_profile-dev101x-494649?style=for-the-badge&logo=hackthebox&logoColor=9FEF00&labelColor=0d1117)](https://profile.hackthebox.com/profile/019f8d0f-a8d2-73bb-8f12-d863b7261aa3)

<sub>Snapshot from November 2026 · click the card for live stats</sub>

</div>

---

<div align="center">

<i>"Security is not a product, but a process. Code is poetry. Ship it."</i>

<sub>⭐️ From <a href="https://github.com/DevCop95">DevCop95</a> · Detection Engineering &amp; Applied AI Security · Cartagena, Colombia 🇨🇴</sub>

</div>
