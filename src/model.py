from llama_cpp import Llama

# Load the model
llm = Llama.from_pretrained(
	repo_id="microsoft/Phi-3-mini-4k-instruct-gguf",
	filename="Phi-3-mini-4k-instruct-q4.gguf",
    local_dir="./models", n_ctx=4096, verbose=False
)

def generate_topics(brand_theme: str, num_days: int = 30):
    prompt = [
        {
            "role": "system",
            "content": "You are an expert social media content planner. Your task is to generate a list of "
                f"{num_days} unique and engaging social media topic ideas based on a given brand theme. "
                "From the theme, infer the target audience and adopt a tone, style, and vocabulary that "
                "is appropriate and appealing to that audience. "
                "Each topic idea should be very short, between 5 and 7 words. "
                "List the topic ideas numerically, one per line, and do not include any extra commentary, "
                "introductory sentences, or concluding remarks. Just provide the numbered list."
        },
        {
            "role": "user",
            "content": f"Generate {num_days} concise topic ideas for the theme: '{brand_theme}'"
    	}
    ]

    output = llm.create_chat_completion(messages=prompt)
    generated_text = output["choices"][0]["message"]["content"]

    topics = [
        line.strip()[line.strip().find(' ') + 1:]
        for line in generated_text.split('\n')
        if line.strip() and line.strip()[0].isdigit()
    ]

    if len(topics) < num_days:
        print(f"[WARNING] Expected {num_days} topics, but got {len(topics)}.")
    return topics


def generate_caption(topic: str):
    prompt = [
        {
            "role": "system",
            "content": "You are a creative social media content writer. Your task is to generate a single, captivating "
                "caption for a social media post based on a given topic "
                "The caption must be concise, no more than two sentences. "
                "The tone and style should be appropriate for the target audience of the brand theme. "
                "Do not include any extra commentary, just the caption text."
        },
        {
            "role": "user",
            "content": f"Generate an engaging caption for the topic: '{topic}' "
            "with appropriate tone and style for the intended audience. Make it concise, no more than two sentences."
        }
    ]

    output = llm.create_chat_completion(messages=prompt, max_tokens=1024)
    return output["choices"][0]["message"]["content"].strip()


def generate_hashtags(topic: str):
    prompt = [
        {
            "role": "system",
            "content": "You are an expert social media content creator. Your task is to generate at most 5 "
                "relevant hashtags for a social media post based on a given topic and brand theme. "
                "The hashtags must be popular, concise, and suitable for the target audience. "
                "Return the hashtags one per line, without any numbers or extra text."
        },
        {
            "role": "user",
            "content": f"Generate 5 hashtags for the topic: '{topic}'"
        }
    ]

    output = llm.create_chat_completion(messages=prompt, max_tokens=128)
    hashtags = output["choices"][0]["message"]["content"].strip().split('\n')
    return [
        line.strip()[line.strip().find(' ') + 1:]
        for line in hashtags
        if line.strip() and line.strip()[0].isdigit()
    ]


if __name__ == "__main__":
    brand_theme = input("Enter the brand theme: ")
    num_days = int(input("Enter number of days: "))

    topics = generate_topics(brand_theme, num_days)
    print(f"Generated Topics: {topics}\n")

    for topic in topics:
        caption = generate_caption(topic)
        hashtags = generate_hashtags(topic)
        print(f"Topic: {topic}\nCaption: {caption}\nHashtags: {hashtags}\n")