from collections import Counter

def infer_role(user_info):
    bio_lower = user_info['bio'].lower()
    languages = [repo['language'] for repo in user_info['repos'] if repo['language']]
    lang_counts = Counter([lang.lower() for lang in languages]).most_common(3)
    top_languages = [lang for lang, _ in lang_counts]

    topics_all = []
    for proj in user_info['repos']:
        topics_all.extend(proj.get('topics', []))
        if proj.get('description'):
            topics_all.extend(proj['description'].lower().split())
    topics_text = " ".join(topics_all).lower()

    scores = {role: 0 for role in ["Frontend", "Backend", "Mobile", "DevOps", "Data Science", "Full-stack"]}

    front_keywords = ["frontend", "front-end", "ui", "react", "angular", "javascript", "web"]
    back_keywords = ["backend", "back-end", "server", "api", "database", "node.js", "django", "spring"]
    mobile_keywords = ["mobile", "android", "ios", "flutter", "react-native"]
    devops_keywords = ["devops", "ci/cd", "docker", "kubernetes", "terraform", "cloud"]
    data_keywords = ["data", "machine-learning", "deep-learning", "ai", "analysis"]
    fullstack_keywords = ["fullstack", "full-stack"]

    role_keywords = {
        "Frontend": front_keywords,
        "Backend": back_keywords,
        "Mobile": mobile_keywords,
        "DevOps": devops_keywords,
        "Data Science": data_keywords,
        "Full-stack": fullstack_keywords
    }

    language_roles = {
        "javascript": ["Frontend"],
        "typescript": ["Frontend"],
        "html": ["Frontend"],
        "css": ["Frontend"],
        "java": ["Backend", "Mobile"],
        "c#": ["Backend", "Mobile"],
        "dart": ["Mobile"],
        "kotlin": ["Mobile"],
        "swift": ["Mobile"],
        "python": ["Data Science", "Backend"],
        "shell": ["DevOps"]
    }

    for lang in top_languages:
        roles = language_roles.get(lang, [])
        for role in roles:
            scores[role] += 1

    for role, keywords in role_keywords.items():
        for kw in keywords:
            if kw in bio_lower or kw in topics_text:
                scores[role] += 1

    role = max(scores, key=scores.get)
    top_two = sorted(scores.values(), reverse=True)[:2]
    if abs(top_two[0] - top_two[1]) <= 1 and "Frontend" in scores and "Backend" in scores:
        role = "Full-stack"

    return role
