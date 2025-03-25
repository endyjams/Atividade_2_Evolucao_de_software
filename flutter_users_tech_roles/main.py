import pandas as pd
from github_api import get_releases, get_contributors_between_releases, get_user_info
from role_inference import infer_role
from visualization import plot_roles_distribution

OWNER = "flutter"
REPO = "flutter"

def main():
    releases = get_releases(OWNER, REPO, num_releases=10)
    all_contributors = set()

    for i in range(1, len(releases)):
        prev_tag = releases[i-1]["tag_name"]
        curr_tag = releases[i]["tag_name"]
        contributors = get_contributors_between_releases(OWNER, REPO, prev_tag, curr_tag)
        all_contributors.update(contributors)

    print(f"Total de contribuidores únicos: {len(all_contributors)}")

    data = []
    for username in all_contributors:
        print(f"Processando {username}...")
        user_info = get_user_info(username)
        role = infer_role(user_info)
        data.append({"username": username, "role": role})

    df = pd.DataFrame(data)
    print(df.head())

    plot_roles_distribution(df['role'])

if __name__ == "__main__":
    main()
