import json
import pandas as pd
import numpy as np
import torch
import matplotlib.pyplot as plt
from datetime import datetime
from transformers import pipeline

print("\n=== VERIFICAÇÃO DO AMBIENTE ===")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA Disponível: {torch.cuda.is_available()}")
print(f"NumPy: {np.__version__}")


# =============================
# Carregamento dos dados
# =============================
with open("flutter_issues.json", "r", encoding="utf-8") as f:
    issues_data = json.load(f)
with open("flutter_commits.json", "r", encoding="utf-8") as f:
    commits_data = json.load(f)
with open("flutter_comments.json", "r", encoding="utf-8") as f:
    comments_data = json.load(f)


# =============================
# Processamento
# =============================
def remove_bot_names(login):
    if pd.isna(login): return None
    lower = login.lower()
    if "[bot]" in lower or lower.endswith("-bot"):
        return None
    return login


def parse_datetime(dt):
    return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")


# Processa df_comments
df_comments = pd.DataFrame(comments_data)
df_comments.dropna(subset=["comment_user"], inplace=True)
df_comments["comment_created_at"] = pd.to_datetime(df_comments["comment_created_at"])
df_comments["comment_user"] = df_comments["comment_user"].apply(remove_bot_names)
df_comments.dropna(subset=["comment_user"], inplace=True)
df_comments["year_month"] = df_comments["comment_created_at"].dt.to_period("M").astype(str)

# =============================
# Análise de Sentimentos
# =============================
device = 0 if torch.cuda.is_available() else -1
print(f"Rodando em: {'GPU' if device == 0 else 'CPU'}")
sentiment_pipeline = pipeline(
    task="sentiment-analysis",
    model="finiteautomata/bertweet-base-sentiment-analysis",
    device=device,
    torch_dtype=torch.float16 if device == 0 else torch.float32,
    batch_size=12,
    truncation=True
)

print("Analisando sentimentos dos comentários...")
sentiments = []
batch_size = 16
for i in range(0, len(df_comments), batch_size):
    batch_texts = df_comments["comment_body"].iloc[i:i + batch_size].tolist()
    result = sentiment_pipeline(batch_texts)
    sentiments.extend(result)

df_comments["sentiment_label"] = [r["label"] for r in sentiments]
df_comments["sentiment_score"] = [float(r["score"]) for r in sentiments]

# =============================
# Exportar para JSON
# =============================
def json_serial(obj):
    if isinstance(obj, (datetime, pd.Timestamp)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

output_json = df_comments.to_dict(orient="records")
with open("flutter_comments_with_sentiment.json", "w", encoding="utf-8") as f:
    json.dump(output_json, f, ensure_ascii=False, indent=4, default=json_serial)

print("✅ Sentimentos salvos em flutter_comments_with_sentiment.json")

# =============================
# Análise e Gráfico
# =============================
print("Gerando gráfico de sentimentos...")
sentiment_counts = df_comments["sentiment_label"].value_counts()

plt.figure(figsize=(8, 6))
plt.bar(sentiment_counts.index, sentiment_counts.values, color=["gray", "red", "green"])
plt.xlabel("Sentimento")
plt.ylabel("Quantidade de Comentários")
plt.title("Distribuição dos Sentimentos nos Comentários")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()

print("✅ Gráfico gerado com sucesso!")
