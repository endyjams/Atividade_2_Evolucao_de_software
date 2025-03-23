"""
change_management.py

Este módulo contém funções para analisar evidências de gerência de mudanças:
- Extração de informações dos labels das issues.
- Análise de palavras-chave específicas relacionadas aos processos de mudança.
- Integração dos dados das issues com a estratégia de releases.
"""

def extract_change_management_evidence(issues):
    """
    Para cada issue, extrai evidências de gerência de mudança:
    - Labels que podem indicar planejamento, análise, documentação, etc.
    - Conta palavras-chave que estejam relacionadas a processos de mudança.
    
    Retorna uma lista de dicionários com informações resumidas da issue.
    """
    evidence_list = []
    # Defina palavras-chave relevantes (pode ser ampliado conforme necessário)
    keywords = {
        "planejamento": ["planejamento", "plan"],
        "classificacao": ["classificação", "classificar"],
        "impacto": ["impacto", "impact"],
        "implementacao": ["implementação", "implementar"],
        "propagacao": ["propagação", "propagar"],
        "documentacao": ["documentação", "documentar"]
    }
    
    for issue in issues:
        labels = issue.get("labels", [])
        label_names = [label.get("name", "").lower() for label in labels]
        # Verifica palavras-chave no título e corpo
        title = (issue.get("title") or "").lower()
        body = (issue.get("body") or "").lower()
        text = title + " " + body
        
        evidence = {key: 0 for key in keywords}
        for key, kw_list in keywords.items():
            for kw in kw_list:
                if kw in text or any(kw in label for label in label_names):
                    evidence[key] += 1
        evidence_list.append({
            "issue_number": issue.get("number"),
            "labels": label_names,
            "evidence": evidence
        })
    return evidence_list