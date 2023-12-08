import random

from openai import OpenAI


def get_api_key():
    return "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"


def get_content_text():
    with open('Prompt/content_text.txt', 'r', encoding='utf-8') as file:
        content_text = file.read()
    return content_text


def generate_titles_prompt_from_abstract(abstract):
    # titles_prompt_text.txt要收集一些公众号中的好标题
    with open('Prompt/titles_prompt_text.txt', 'r', encoding='utf-8') as file:
        titles_prompt_text = file.read()
    titles_prompt = f"{titles_prompt_text}\n" \
                    f"参考上面的好标题示例，结合文章内容，生成100个多种多样的标题，善用各种标点符号，尤其是感叹号，双引号等等。" \
                    f"文章内容参考后面的摘要:{abstract}"
    with open('Prompt_Output/titles_prompt.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(titles_prompt)
    return titles_prompt


def generate_selection_prompt_from_titles(abstract, titles):
    # selection_prompt_text.txt要说明好标题的标准
    with open('Prompt/selection_prompt_text.txt', 'r', encoding='utf-8') as file:
        selection_prompt_text = file.read()
    selection_prompt = f"{selection_prompt_text}。" \
                       f"参考上面的好标题标准，结合文章内容，选出10个和文章最相关的标题。" \
                       f"\n100个标题如下\n{titles}\n文章内容参考后面的摘要:{abstract}"
    with open('Prompt_Output/selection_prompt.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(selection_prompt)
    return selection_prompt


def generate_article_titles(api_key, text):
    client = OpenAI(api_key=api_key)

    # 生成摘要
    abstract_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"为下面的文章写个摘要：{text}"}]
    )
    abstract = abstract_response.choices[0].message.content

    # 生成100个标题
    titles_prompt = generate_titles_prompt_from_abstract(abstract)
    titles_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": titles_prompt}]
    )
    titles = titles_response.choices[0].message.content.split('\n')
    titles_str = '\n'.join(titles)  # 将列表转换为字符串
    with open('titles/100 titles.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(titles_str)

    # 选择最相关的十个标题
    selection_prompt = generate_selection_prompt_from_titles(abstract, titles)
    selection_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": selection_prompt}]
    )
    top_titles = selection_response.choices[0].message.content.split('\n')
    top_titles_str = '\n'.join(top_titles)  # 将列表转换为字符串
    with open('titles/top 10 titles.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(top_titles_str)

    # 将结果保存到字典中
    results = {
        "abstract": abstract,
        "top_titles": top_titles
    }
    return results


def find_highest_scoring_title(titles, score_title):
    highest_score = float('-inf')
    highest_scoring_title = None

    for title in titles:
        score = score_title(title)
        if score > highest_score:
            highest_score = score
            highest_scoring_title = title

    return highest_scoring_title, highest_score


def score_title(title):
    return random.randint(1, 100)


# 文本输入通过content_text.txt
content_text = get_content_text()
api_key = get_api_key()
result = generate_article_titles(api_key, content_text)
print(result)
# top_titles 是之前生成的10个标题列表
top_titles = result['top_titles']

# 找出分数最高的标题
highest_scoring_title, highest_score = find_highest_scoring_title(top_titles, score_title)

print(f"Highest Scoring Title: {highest_scoring_title}")
print(f"Score: {highest_score}")